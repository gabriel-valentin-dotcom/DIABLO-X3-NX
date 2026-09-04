#!/usr/bin/env python3
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String


class FollowManager(Node):

    def __init__(self):
        super().__init__('follow_manager_node')

        self.follow_enabled = False
        self.follow_requested = False
        self.follow_armed = False
        self.follow_state = 'FOLLOW_OFF'
        self.follow_arm_until = 0.0
        self.follow_on_pending_until = 0.0

        self.target_visible = False
        self.target_dir = 'UNKNOWN'
        self.target_source = 'UNKNOWN'
        self.vision_state = 'NO_DEPTH'
        self.track_image_width = 0
        self.last_target_time = 0.0
        self.target_timeout_s = 4.0

        self.cam_enabled = False
        self.track_enabled = False
        self.auto_enabled = False
        self.last_cam_time = 0.0
        self.last_track_time = 0.0
        self.cam_timeout_s = 15.0
        self.track_timeout_s = 15.0
        self.follow_arm_window_s = 4.0
        self.follow_on_reorder_grace_s = 0.5

        self.dependency_phase = 'IDLE'
        self.dependency_deadline = 0.0
        self.follow_owned_cam = False
        self.follow_owned_track = False

        self.sub = self.create_subscription(
            String,
            '/system_command',
            self.cb,
            10
        )
        self.create_subscription(String, '/vision_track/target', self.on_vision_target, 10)
        self.create_subscription(Bool, '/diablo/mode/cam_enabled', self.on_cam_enabled, 10)
        self.create_subscription(Bool, '/diablo/mode/track_enabled', self.on_track_enabled, 10)
        self.create_subscription(Bool, '/diablo/mode/auto_enabled', self.on_auto_enabled, 10)
        self.pub = self.create_publisher(Bool, '/diablo/mode/follow_enabled', 10)
        self.status_pub = self.create_publisher(String, '/diablo/follow/status', 10)
        self.cmd_pub = self.create_publisher(String, '/system_command', 10)

        self.timer = self.create_timer(0.2, self.tick)

        self.get_logger().info(
            'FOLLOW Manager dependency-gated aktiv: CAM/TRACK on-demand vor FOLLOW'
        )

    def fresh(self, stamp, timeout_s):
        return (time.time() - stamp) <= timeout_s

    def target_ready(self):
        return (
            self.fresh(self.last_target_time, self.target_timeout_s) and
            self.target_visible and
            self.target_dir in ['LEFT', 'RIGHT', 'FRONT']
        )

    def cam_ready(self):
        return (
            self.cam_enabled and
            self.fresh(self.last_cam_time, self.cam_timeout_s) and
            self.count_publishers('/camera/camera/color/image_raw') >= 1 and
            self.count_publishers('/camera/camera/depth/image_rect_raw') >= 1
        )

    def track_ready(self):
        return (
            self.track_enabled and
            self.fresh(self.last_track_time, self.track_timeout_s) and
            self.fresh(self.last_target_time, self.target_timeout_s) and
            self.track_image_width > 0 and
            self.target_source == 'YOLO_PERSON' and
            self.vision_state != 'NO_DEPTH'
        )

    def normalize_target_dir(self, value):
        value = (value or '').strip().upper()
        if value in ['LEFT', 'TARGET_LEFT', 'TARGET_DIR_LEFT']:
            return 'LEFT'
        if value in ['RIGHT', 'TARGET_RIGHT', 'TARGET_DIR_RIGHT']:
            return 'RIGHT'
        if value in ['FRONT', 'CENTER', 'CENTRE', 'FORWARD', 'TARGET_FRONT', 'TARGET_DIR_FRONT']:
            return 'FRONT'
        return 'UNKNOWN'

    def on_vision_target(self, msg):
        self.last_target_time = time.time()
        target_visible = False
        target_dir = 'UNKNOWN'
        for part in msg.data.split(','):
            part = part.strip()
            if '=' not in part:
                continue
            key, value = part.split('=', 1)
            key = key.strip().lower()
            value = value.strip().upper()
            if key == 'target_visible':
                target_visible = value == 'TRUE'
            elif key in ['target_dir', 'target_direction']:
                parsed_dir = self.normalize_target_dir(value)
                if parsed_dir != 'UNKNOWN':
                    target_dir = parsed_dir
            elif key == 'target_side':
                parsed_dir = self.normalize_target_dir(value)
                if target_dir == 'UNKNOWN' and parsed_dir != 'UNKNOWN':
                    target_dir = parsed_dir
            elif key == 'target_source':
                self.target_source = value
            elif key == 'vision_state':
                self.vision_state = value
            elif key == 'image_width':
                try:
                    self.track_image_width = int(value)
                except ValueError:
                    self.track_image_width = 0
        self.target_visible = target_visible
        self.target_dir = target_dir

    def on_cam_enabled(self, msg):
        self.cam_enabled = bool(msg.data)
        self.last_cam_time = time.time()

    def on_track_enabled(self, msg):
        self.track_enabled = bool(msg.data)
        self.last_track_time = time.time()

    def on_auto_enabled(self, msg):
        self.auto_enabled = bool(msg.data)

    def publish_state(self):
        self.pub.publish(Bool(data=self.follow_enabled))
        self.status_pub.publish(String(data=self.follow_state))

    def set_follow(self, enabled, state, log_text=None):
        changed = self.follow_enabled != enabled or self.follow_state != state
        self.follow_enabled = enabled
        self.follow_state = state
        self.publish_state()
        if log_text and changed:
            self.get_logger().info(log_text)

    def publish_command(self, cmd):
        self.cmd_pub.publish(String(data=cmd))

    def reset_dependency_state(self):
        self.dependency_phase = 'IDLE'
        self.dependency_deadline = 0.0

    def clear_follow_request(self):
        self.follow_requested = False
        self.follow_arm_until = 0.0
        self.follow_on_pending_until = 0.0
        self.reset_dependency_state()

    def cleanup_follow_dependencies(self, reason):
        ownership = (
            f'cam={"follow-owned" if self.follow_owned_cam else "manual"} '
            f'track={"follow-owned" if self.follow_owned_track else "manual"}'
        )
        self.get_logger().info(
            f'FOLLOW dependency cleanup reason={reason} ownership={ownership}'
        )

        send_track_off = self.follow_owned_track and not self.auto_enabled
        send_cam_off = self.follow_owned_cam and not self.auto_enabled

        self.follow_owned_track = False
        self.follow_owned_cam = False

        if send_track_off:
            self.publish_command('TRACK_OFF')
        if send_cam_off:
            self.publish_command('CAM_OFF')

    def handle_dependency_timeout(self, stage):
        self.get_logger().error(f'FOLLOW dependency timeout: {stage}')
        self.set_follow(False, f'FOLLOW_DEP_TIMEOUT_{stage} HOLD_NO_MOVE')
        self.follow_armed = False
        self.clear_follow_request()
        self.cleanup_follow_dependencies(f'timeout_{stage.lower()}')

    def request_cam_dependency(self):
        self.dependency_phase = 'WAIT_CAM'
        self.dependency_deadline = time.time() + self.cam_timeout_s
        self.set_follow(False, 'FOLLOW_ARMED WAIT_DEP_CAM HOLD_NO_MOVE')

        if self.cam_enabled:
            self.follow_owned_cam = False
            self.get_logger().info('FOLLOW dependency ownership: manual CAM')
            self.get_logger().info('FOLLOW dependency wait: CAM already active, waiting ready')
            return

        self.follow_owned_cam = True
        self.get_logger().info('FOLLOW dependency ownership: follow-owned CAM')
        self.get_logger().info('FOLLOW dependency request: CAM')
        self.publish_command('CAM_ON')

    def request_track_dependency(self):
        self.dependency_phase = 'WAIT_TRACK'
        self.dependency_deadline = time.time() + self.track_timeout_s
        self.set_follow(False, 'FOLLOW_ARMED WAIT_DEP_TRACK HOLD_NO_MOVE')

        if self.track_enabled:
            self.follow_owned_track = False
            self.get_logger().info('FOLLOW dependency ownership: manual TRACK')
            self.get_logger().info('FOLLOW dependency wait: TRACK already active, waiting ready')
            return

        self.follow_owned_track = True
        self.get_logger().info('FOLLOW dependency ownership: follow-owned TRACK')
        self.get_logger().info('FOLLOW dependency request: TRACK')
        self.publish_command('TRACK_ON')

    def begin_follow_arm(self):
        if self.follow_requested or self.follow_enabled or self.follow_armed or self.dependency_phase != 'IDLE':
            self.get_logger().info(
                f'FOLLOW_ARM idempotent ignore phase={self.dependency_phase} '
                f'follow_enabled={self.follow_enabled} follow_requested={self.follow_requested} '
                f'follow_armed={self.follow_armed}'
            )
            return

        self.follow_arm_until = time.time() + self.follow_arm_window_s
        self.follow_requested = True
        self.follow_armed = True
        self.follow_on_pending_until = 0.0
        self.follow_owned_cam = False
        self.follow_owned_track = False
        self.get_logger().info('FOLLOW_ARM accepted -> dependency preparation start')
        self.request_cam_dependency()

    def finalize_follow_ready(self):
        self.reset_dependency_state()
        self.follow_requested = False
        self.get_logger().info('FOLLOW arm ready')
        if self.target_ready():
            self.set_follow(
                False,
                'FOLLOW_ARMED_READY HOLD_NO_MOVE',
                'FOLLOW_ARMED_READY HOLD_NO_MOVE'
            )
        else:
            self.set_follow(
                False,
                'FOLLOW_ARMED_WAIT_TARGET HOLD_NO_MOVE',
                'FOLLOW armed, waiting for visible target before explicit start'
            )

    def begin_follow_start(self):
        if self.follow_enabled:
            self.get_logger().info('FOLLOW_ON idempotent ignore: already active')
            return

        if not self.follow_armed:
            self.get_logger().warn('FOLLOW_ON ignored: missing FOLLOW_ARM/ARMED state')
            return

        if self.follow_requested or self.dependency_phase != 'IDLE':
            self.set_follow(False, 'FOLLOW_ARMED WAIT_READY HOLD_NO_MOVE')
            self.get_logger().warn('FOLLOW_ON ignored: dependencies not ready yet')
            return

        if not self.cam_ready():
            self.set_follow(False, 'FOLLOW_ARMED WAIT_DEP_CAM HOLD_NO_MOVE')
            self.get_logger().warn('FOLLOW_ON ignored: CAM not ready')
            return

        if not self.track_ready():
            self.set_follow(False, 'FOLLOW_ARMED WAIT_DEP_TRACK HOLD_NO_MOVE')
            self.get_logger().warn('FOLLOW_ON ignored: TRACK not ready')
            return

        if self.target_ready():
            self.follow_arm_until = 0.0
            self.follow_on_pending_until = 0.0
            self.set_follow(True, 'FOLLOW_ACTIVE', 'FOLLOW_ACTIVE')
            return

        self.set_follow(False, 'FOLLOW_ARMED_WAIT_TARGET HOLD_NO_MOVE')
        self.get_logger().warn('FOLLOW_ON ignored: target not ready')

    def cancel_follow(self, reason, cleanup_dependencies):
        self.set_follow(False, 'FOLLOW_OFF', f'{reason} -> FOLLOW_OFF')
        self.follow_armed = False
        self.clear_follow_request()
        if cleanup_dependencies:
            self.cleanup_follow_dependencies(reason)
        else:
            self.follow_owned_track = False
            self.follow_owned_cam = False

    def tick(self):
        now = time.time()

        if self.follow_requested:
            if self.dependency_phase == 'WAIT_CAM':
                if self.cam_ready():
                    self.get_logger().info('FOLLOW dependency ready: CAM')
                    self.request_track_dependency()
                elif now > self.dependency_deadline:
                    self.handle_dependency_timeout('CAM')
                else:
                    self.publish_state()
                return

            if self.dependency_phase == 'WAIT_TRACK':
                if self.track_ready():
                    self.get_logger().info('FOLLOW dependency ready: TRACK')
                    self.finalize_follow_ready()
                elif now > self.dependency_deadline:
                    self.handle_dependency_timeout('TRACK')
                else:
                    self.publish_state()
            return

        if self.follow_armed and not self.follow_enabled:
            if not self.cam_ready():
                self.set_follow(False, 'FOLLOW_ARMED WAIT_DEP_CAM HOLD_NO_MOVE')
            elif not self.track_ready():
                self.set_follow(False, 'FOLLOW_ARMED WAIT_DEP_TRACK HOLD_NO_MOVE')
            elif self.target_ready():
                self.set_follow(False, 'FOLLOW_ARMED_READY HOLD_NO_MOVE')
            else:
                self.set_follow(False, 'FOLLOW_ARMED_WAIT_TARGET HOLD_NO_MOVE')
            return

        if self.follow_enabled and self.target_ready():
            self.set_follow(True, 'FOLLOW_ACTIVE')
        elif self.follow_enabled:
            self.set_follow(
                True,
                'FOLLOW_WAIT_TARGET TARGET_MISSING TARGET_DIR_UNKNOWN',
            )
        elif self.follow_on_pending_until > 0.0 and now > self.follow_on_pending_until:
            self.follow_on_pending_until = 0.0
            self.get_logger().warn('FOLLOW_ON ignored: missing fresh FOLLOW_ARM')
        else:
            self.publish_state()

    def cb(self, msg):
        cmd = msg.data.strip().upper()

        if cmd == 'FOLLOW_ARM':
            self.begin_follow_arm()
            return

        if cmd == 'FOLLOW_ON':
            self.begin_follow_start()
            return

        if cmd == 'FOLLOW_OFF':
            self.cancel_follow('FOLLOW_OFF', cleanup_dependencies=True)
            return

        if cmd == 'STOP':
            self.cancel_follow('STOP', cleanup_dependencies=True)
            return

        if cmd == 'AUTO_ON':
            self.cancel_follow('AUTO_ON', cleanup_dependencies=False)
            return

        if cmd == 'CAM_OFF':
            self.cancel_follow('CAM_OFF', cleanup_dependencies=False)
            return

        if cmd == 'TRACK_OFF':
            self.cancel_follow('TRACK_OFF', cleanup_dependencies=False)


def main():
    rclpy.init()
    node = FollowManager()

    try:
        rclpy.spin(node)

    finally:
        node.follow_requested = False
        node.follow_enabled = False
        node.follow_state = 'FOLLOW_OFF'
        node.publish_state()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
