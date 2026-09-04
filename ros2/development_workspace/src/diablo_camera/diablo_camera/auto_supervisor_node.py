#!/usr/bin/env python3
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String


class AutoSupervisor(Node):

    def __init__(self):
        super().__init__('auto_supervisor_node')

        self.auto_enabled = False
        self.track_enabled = False
        self.cam_enabled = False
        self.follow_enabled = False

        self.target_ok = False
        self.target_visible = False
        self.target_dir = 'UNKNOWN'
        self.last_visible_target_side = 'UNKNOWN'
        self.vision_state = 'UNKNOWN'
        self.floor_drop_stop = False
        self.last_vision_time = 0.0
        self.last_visible_target_time = 0.0
        self.vision_timeout_s = 1.0
        self.uwb_ready = False
        self.uwb_status = 'UNKNOWN'
        self.last_uwb_time = 0.0
        self.uwb_timeout_s = 1.5
        self.lidar_safe = False
        self.safety_ok = True
        self.estop = False
        self.stop_hold_until = 0.0

        self.create_subscription(Bool, '/diablo/mode/auto_enabled', self.on_auto, 10)
        self.create_subscription(Bool, '/diablo/mode/track_enabled', self.on_track, 10)
        self.create_subscription(Bool, '/diablo/mode/cam_enabled', self.on_cam, 10)
        self.create_subscription(Bool, '/diablo/mode/follow_enabled', self.on_follow, 10)
        self.create_subscription(String, '/system_command', self.on_system_command, 10)

        self.create_subscription(String, '/tracker_status', self.on_tracker_status, 10)
        self.create_subscription(String, '/vision_track/target', self.on_vision_target, 10)
        self.create_subscription(String, '/diablo/uwb/follow_status', self.on_uwb_follow_status, 10)
        self.create_subscription(Bool, '/diablo/safety/lidar_safe_filtered', self.on_lidar_safe, 10)
        self.create_subscription(Bool, '/diablo/safety/ok', self.on_safety_ok, 10)
        self.create_subscription(Bool, '/diablo/safety/estop', self.on_estop, 10)

        self.permission_pub = self.create_publisher(String, '/diablo/auto/permission', 10)
        self.state_pub = self.create_publisher(String, '/diablo/auto/state', 10)

        self.publish_count = 0
        self.timer = self.create_timer(0.2, self.evaluate)

        self.get_logger().info('AUTO Supervisor V1 aktiv: Safety/Permission only, keine Motoren')

    def on_auto(self, msg):
        self.auto_enabled = msg.data

    def on_track(self, msg):
        self.track_enabled = msg.data

    def on_cam(self, msg):
        self.cam_enabled = msg.data

    def on_follow(self, msg):
        self.follow_enabled = msg.data

    def on_system_command(self, msg):
        cmd = msg.data.strip().upper()
        if cmd == 'STOP':
            self.stop_hold_until = time.time() + 1.0
            self.auto_enabled = False
            self.track_enabled = False
            self.cam_enabled = False
            self.follow_enabled = False
            self.permission_pub.publish(String(data='HOLD'))
            self.state_pub.publish(String(data='permission=HOLD;reason=STOP;auto=False;track=False;cam=False;follow=False'))
            self.get_logger().warn('STOP_APPLIED auto_supervisor -> permission=HOLD')

    def on_tracker_status(self, msg):
        # Legacy tracker input. Vision target is the live follow signal today.
        text = msg.data.upper()
        if ('OK' in text) or ('CONNECTED' in text):
            self.target_ok = True

    def on_vision_target(self, msg):
        self.last_vision_time = time.time()
        state = 'UNKNOWN'
        target_visible = False
        target_dir = 'UNKNOWN'

        for part in msg.data.split(','):
            part = part.strip()
            if '=' not in part:
                continue
            key, value = part.split('=', 1)
            key = key.strip().lower()
            value = value.strip()
            if key == 'state':
                state = value.upper()
            elif key == 'target_visible':
                target_visible = value.lower() == 'true'
            elif key in ['target_dir', 'target_side', 'target_direction']:
                target_dir = value.upper()

        self.vision_state = state
        self.target_visible = target_visible
        self.target_dir = target_dir if target_dir in ['LEFT', 'RIGHT', 'FRONT'] else 'UNKNOWN'
        if self.target_visible and self.target_dir in ['LEFT', 'RIGHT', 'FRONT']:
            self.last_visible_target_side = self.target_dir
            self.last_visible_target_time = self.last_vision_time
        self.floor_drop_stop = 'floor_state=FLOOR_DROP_STOP' in msg.data
        vision_not_stopped = state not in [
            'DEPTH_FRONT_STOP',
            'VISION_HARD_STOP',
            'DEPTH_STAIR_STOP',
        ]
        self.target_ok = vision_not_stopped and self.target_visible and self.target_dir in ['LEFT', 'RIGHT', 'FRONT']

        if self.floor_drop_stop:
            self.target_ok = False

    def on_lidar_safe(self, msg):
        self.lidar_safe = msg.data

    def parse_key_value(self, text, key):
        prefix = f'{key}='
        for part in text.split(','):
            item = part.strip()
            if item.startswith(prefix):
                return item[len(prefix):].strip()
        return None

    def parse_float(self, value):
        try:
            parsed = float(value)
            if parsed != parsed:
                return None
            return parsed
        except Exception:
            return None

    def on_uwb_follow_status(self, msg):
        self.last_uwb_time = time.time()
        text = msg.data.strip()
        status = text.split(',', 1)[0].strip().upper()
        range_m = self.parse_float(self.parse_key_value(text, 'range_m'))
        last_age = self.parse_float(self.parse_key_value(text, 'last_age'))
        valid_status = status in [
            'UWB_TARGET_OK',
            'UWB_TARGET_FAR',
            'UWB_FAR_EDGE',
            'UWB_NEAR_EDGE',
            'UWB_TOO_CLOSE',
        ]
        valid_age = last_age is not None and 0.0 <= last_age <= 1.0
        valid_range = range_m is not None and 0.1 <= range_m <= 20.0
        self.uwb_status = status
        self.uwb_ready = valid_status and valid_age and valid_range

    def on_safety_ok(self, msg):
        self.safety_ok = msg.data

    def on_estop(self, msg):
        self.estop = msg.data

    def evaluate(self):
        try:
            self.publish_count += 1
            vision_fresh = (time.time() - self.last_vision_time) <= self.vision_timeout_s
            uwb_fresh = (time.time() - self.last_uwb_time) <= self.uwb_timeout_s
            uwb_ok = uwb_fresh and self.uwb_ready
            target_ok = vision_fresh and self.target_ok
            occlusion_recent = (
                vision_fresh and
                not self.target_visible and
                self.follow_enabled and
                self.cam_enabled and
                (time.time() - self.last_visible_target_time) <= 1.5
            )
            vision_hard_stop = vision_fresh and (
                self.vision_state in [
                    'DEPTH_FRONT_STOP',
                    'VISION_HARD_STOP',
                    'DEPTH_STAIR_STOP',
                ] or
                self.floor_drop_stop
            )

            if time.time() < self.stop_hold_until:
                permission = 'HOLD'
                reason = 'STOP_APPLIED'

            elif self.estop:
                permission = 'STOP_REQUIRED'
                reason = 'ESTOP_ACTIVE'

            elif not self.safety_ok:
                permission = 'STOP_REQUIRED'
                reason = 'SAFETY_NOT_OK'

            elif vision_hard_stop:
                permission = 'STOP_REQUIRED'
                reason = f'VISION_STOP_{self.vision_state}'

            elif not self.lidar_safe:
                if self.auto_enabled:
                    permission = 'AUTO_ESCAPE_ALLOWED'
                    reason = 'LIDAR_NOT_SAFE_ESCAPE'
                elif self.follow_enabled and self.cam_enabled and target_ok and uwb_ok:
                    permission = 'AUTO_ESCAPE_ALLOWED'
                    reason = 'FOLLOW_LIDAR_NOT_SAFE_ESCAPE'
                else:
                    permission = 'HOLD'
                    reason = 'LIDAR_NOT_SAFE'

            elif self.follow_enabled:
                if self.cam_enabled and target_ok and uwb_ok:
                    permission = 'FOLLOW_ALLOWED'
                    reason = 'FOLLOW_TARGET_OK'
                elif self.cam_enabled and occlusion_recent and uwb_ok:
                    permission = 'FOLLOW_REACQUIRE_ALLOWED'
                    reason = 'VISION_OCCLUDED_UWB_VALID'
                else:
                    permission = 'HOLD'
                    reason = 'FOLLOW_BLOCKED_NO_TARGET_OR_UWB'

            elif self.auto_enabled:
                permission = 'AUTO_ALLOWED'
                reason = 'AUTO_SAFETY_OK'

            else:
                permission = 'HOLD'
                reason = 'NO_ACTIVE_MODE'

            self.permission_pub.publish(String(data=permission))

            state = (
                f'permission={permission};'
                f'reason={reason};'
                f'auto={self.auto_enabled};'
                f'track={self.track_enabled};'
                f'cam={self.cam_enabled};'
                f'follow={self.follow_enabled};'
                f'target_ok={target_ok};'
                f'target_visible={self.target_visible};'
                f'target_dir={self.target_dir};'
                f'last_visible_target_side={self.last_visible_target_side};'
                f'vision_fresh={vision_fresh};'
                f'vision_state={self.vision_state};'
                f'vision_hard_stop={vision_hard_stop};'
                f'uwb_ok={uwb_ok};'
                f'uwb_status={self.uwb_status};'
                f'lidar_safe={self.lidar_safe};'
                f'safety_ok={self.safety_ok};'
                f'estop={self.estop}'
            )

            self.state_pub.publish(String(data=state))

            if self.publish_count % 10 == 0:
                self.get_logger().info(
                    f"AUTO_SUPERVISOR_ALIVE count={self.publish_count} "
                    f"auto={self.auto_enabled} "
                    f"cam={self.cam_enabled} "
                    f"lidar={self.lidar_safe}"
                )
        except Exception as exc:
            self.get_logger().error(f"AUTO_SUPERVISOR_ERROR: {exc}")

def main():
    rclpy.init()
    node = AutoSupervisor()

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
