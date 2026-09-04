#!/usr/bin/env python3
import os
import signal
import subprocess
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool


class CameraManager(Node):
    def __init__(self):
        super().__init__('camera_manager_node')

        self.proc = None
        self.manual_cam_enabled = False
        self.last_start_attempt = 0.0
        self.last_vision_time = 0.0
        self.vision_timeout_s = 2.0
        self.startup_grace_s = 30.0
        self.restart_backoff_s = 12.0
        self.follow_arm_until = 0.0

        self.sub = self.create_subscription(String, '/system_command', self.cb, 10)
        self.create_subscription(String, '/vision_track/target', self.on_vision_target, 10)
        self.pub = self.create_publisher(Bool, '/diablo/mode/cam_enabled', 10)
        self.status = self.create_publisher(String, '/camera/cmd', 10)
        self.timer = self.create_timer(0.5, self.publish_periodic_state)
        self.watchdog_timer = self.create_timer(5.0, self.camera_watchdog)

        self.publish_state(False, 'CAM_OFF: Boot idle, waiting for UI CAM')
        self.get_logger().info('Camera Manager aktiv: idle bis CAM_ON')

    def publish_state(self, enabled, text):
        self.manual_cam_enabled = bool(enabled)
        self.pub.publish(Bool(data=enabled))
        self.status.publish(String(data=text))
        self.get_logger().info(text)

    def on_vision_target(self, msg):
        self.last_vision_time = time.time()

    def camera_process_alive(self):
        return self.proc is not None and self.proc.poll() is None

    def vision_fresh(self):
        return (time.time() - self.last_vision_time) <= self.vision_timeout_s

    def publish_periodic_state(self):
        enabled = (
            self.manual_cam_enabled and
            (self.camera_process_alive() or self.vision_fresh())
        )
        self.pub.publish(Bool(data=enabled))

    def ros_env_prefix(self):
        parts = [
            'export ROS_DOMAIN_ID=5',
            'export ROS_LOCALHOST_ONLY=0',
            'export RMW_IMPLEMENTATION=rmw_fastrtps_cpp',
            'source /opt/ros/foxy/setup.bash',
            'source /home/diablo/diablo_ws/install/setup.bash',
        ]
        return ' && '.join(parts)

    def camera_watchdog(self):
        if not self.manual_cam_enabled:
            return

        now = time.time()
        if self.camera_process_alive():
            if now - self.last_start_attempt <= self.startup_grace_s:
                return
            if self.vision_fresh():
                return
            if now - self.last_start_attempt < self.restart_backoff_s:
                return
            self.get_logger().warn('CAM_WATCHDOG: RealSense laeuft ohne frische Vision-Updates, Neustart')
            self.cam_off(manual=False)
            self.cam_on()
            return

        if now - self.last_start_attempt >= self.restart_backoff_s:
            self.get_logger().warn('CAM_WATCHDOG: RealSense Prozess fehlt, CAM_ON Retry')
            self.cam_on()

    def cam_on(self):
        if self.proc and self.proc.poll() is None:
            self.publish_state(True, 'CAM already ON')
            return

        self.manual_cam_enabled = True
        self.last_start_attempt = time.time()
        self.last_vision_time = 0.0

        cmd = (
            "bash -lc '"
            f"{self.ros_env_prefix()} && "
            "ros2 launch realsense2_camera rs_launch.py rgb_camera.color_profile:=640x480x15 depth_module.depth_profile:=640x480x15 enable_depth:=true enable_infra1:=false enable_infra2:=false"
            "'"
        )

        self.proc = subprocess.Popen(
            cmd,
            shell=True,
            preexec_fn=os.setsid
        )

        self.publish_state(True, 'CAM_ON: RealSense gestartet')

    def cam_off(self, manual=True):
        if manual:
            self.manual_cam_enabled = False

        try:
            if self.proc and self.proc.poll() is None:
                os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        except Exception as e:
            self.get_logger().warn(f'CAM_OFF killpg Problem: {e}')

        subprocess.call("pkill -f realsense2_camera_node", shell=True)
        subprocess.call("pkill -f rs_launch.py", shell=True)
        subprocess.call("pkill -f 'ros2 launch realsense2_camera'", shell=True)

        self.proc = None
        self.publish_state(False, 'CAM_OFF: RealSense gestoppt')

    def cb(self, msg):
        cmd = msg.data.strip().upper()

        if cmd == 'FOLLOW_ARM':
            self.follow_arm_until = time.time() + 4.0
            return

        if cmd == 'CAM_ON':
            self.cam_on()
        elif cmd == 'FOLLOW_ON':
            if time.time() <= self.follow_arm_until:
                self.follow_arm_until = 0.0
                self.get_logger().info(
                    'FOLLOW_ON acknowledged in camera_manager, waiting for explicit CAM_ON dependency request'
                )
            else:
                self.get_logger().warn('FOLLOW_ON ignored for CAM: missing fresh FOLLOW_ARM')
        elif cmd in ['CAM_OFF', 'STOP']:
            self.follow_arm_until = 0.0
            self.cam_off()


def main():
    rclpy.init()
    node = CameraManager()

    try:
        rclpy.spin(node)
    finally:
        node.cam_off(manual=False)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
