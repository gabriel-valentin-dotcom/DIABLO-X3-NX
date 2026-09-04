#!/usr/bin/env python3

import os
import signal
import subprocess
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import Bool, String
from std_srvs.srv import Trigger
from motion_msgs.msg import RobotStatus


class VoiceRuntimeManagerNode(Node):
    """Start and stop the complete voice stack on demand."""

    LAUNCHER = '/home/diablo/start_safe_voice_pose.sh'
    READY_PERIOD_SEC = 0.5
    VOICE_ENABLED_HEARTBEAT_PERIOD_SEC = 0.5
    HEALTH_FRESHNESS_SEC = 1.5
    BODY_STATE_FRESHNESS_SEC = 1.5

    def __init__(self):
        super().__init__('voice_runtime_manager_node')
        self.voice_process = None
        self.voice_enabled = False
        self.voice_input_ready = False
        self.voice_input_ready_at = 0.0
        self.body_state_at = 0.0
        self.body_error = None
        self.body_warning = None
        self.armed_status = 'ARMED_OFF'
        self.armed_voice_rejection_logged = False
        self.motion_pub = self.create_publisher(
            String, '/diablo_motion_request', 10
        )
        self.voice_enabled_pub = self.create_publisher(
            Bool, '/diablo/mode/voice_enabled', 10
        )
        self.interact_ready_pub = self.create_publisher(
            Bool, '/diablo/interact/ready', 10
        )
        self.create_subscription(
            String, '/system_command', self.on_system_command, 10
        )
        armed_status_qos = QoSProfile(
            depth=1,
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )
        self.create_subscription(
            String, '/diablo/mode/armed_status', self.on_armed_status,
            armed_status_qos
        )
        self.create_subscription(
            Bool, '/diablo/interact/voice_input_ready',
            self.on_voice_input_ready, 10
        )
        self.create_subscription(
            RobotStatus, '/diablo/sensor/Body_state', self.on_body_state, 1
        )
        self.create_service(
            Trigger, '/diablo/voice_runtime/stop', self.on_stop_service
        )
        self.monitor_timer = self.create_timer(1.0, self.monitor_process)
        self.ready_timer = self.create_timer(
            self.READY_PERIOD_SEC, self.publish_interact_ready
        )
        self.voice_enabled_heartbeat_timer = self.create_timer(
            self.VOICE_ENABLED_HEARTBEAT_PERIOD_SEC,
            self.publish_voice_enabled_heartbeat,
        )
        self.publish_voice_enabled(False)
        self.publish_interact_ready()
        self.get_logger().info(
            'Voice Runtime Manager V1 active; voice stack is off at startup'
        )

    def voice_is_running(self):
        return (
            self.voice_process is not None
            and self.voice_process.poll() is None
        )

    def publish_voice_enabled(self, enabled):
        self.voice_enabled = bool(enabled)
        self.voice_enabled_pub.publish(Bool(data=self.voice_enabled))

    def publish_voice_enabled_heartbeat(self):
        self.voice_enabled_pub.publish(Bool(data=self.voice_enabled))

    def on_voice_input_ready(self, msg):
        self.voice_input_ready = bool(msg.data)
        self.voice_input_ready_at = time.monotonic()

    def on_body_state(self, msg):
        self.body_error = int(msg.error_msg)
        self.body_warning = int(msg.warning_msg)
        self.body_state_at = time.monotonic()

    def node_present(self, name):
        try:
            return any(
                node_name == name and namespace == '/'
                for node_name, namespace in self.get_node_names_and_namespaces()
            )
        except Exception:
            return False

    def topic_has_endpoint(self, topic, node_name, publisher):
        try:
            infos = (
                self.get_publishers_info_by_topic(topic)
                if publisher else self.get_subscriptions_info_by_topic(topic)
            )
            return any(
                info.node_name == node_name and info.node_namespace == '/'
                for info in infos
            )
        except Exception:
            return False

    def ros_voice_path_complete(self):
        return (
            self.node_present('voice_input_node')
            and self.node_present('voice_command_node')
            and self.node_present('safe_voice_pose_node')
            and self.topic_has_endpoint('/voice_text', 'voice_input_node', True)
            and self.topic_has_endpoint('/voice_text', 'voice_command_node', False)
            and self.topic_has_endpoint('/voice_cmd_de', 'voice_command_node', True)
            and self.topic_has_endpoint('/voice_cmd_de', 'safe_voice_pose_node', False)
            and self.topic_has_endpoint(
                '/diablo_motion_request', 'safe_voice_pose_node', True
            )
        )

    def body_state_is_healthy(self):
        return (
            self.body_state_at > 0.0
            and time.monotonic() - self.body_state_at
            <= self.BODY_STATE_FRESHNESS_SEC
            and self.body_error == 0
            and self.body_warning == 0
        )

    def interact_is_ready(self):
        voice_health_fresh = (
            self.voice_input_ready_at > 0.0
            and time.monotonic() - self.voice_input_ready_at
            <= self.HEALTH_FRESHNESS_SEC
        )
        return (
            self.voice_enabled
            and self.voice_is_running()
            and self.ros_voice_path_complete()
            and self.voice_input_ready
            and voice_health_fresh
            and self.body_state_is_healthy()
        )

    def publish_interact_ready(self):
        self.interact_ready_pub.publish(Bool(data=self.interact_is_ready()))

    def start_voice(self):
        if self.armed_status != 'ARMED_OFF':
            if not self.armed_voice_rejection_logged:
                self.get_logger().warn('VOICE_START_REJECTED_ARMED_ACTIVE')
                self.armed_voice_rejection_logged = True
            self.publish_voice_enabled(False)
            self.publish_interact_ready()
            return
        if self.voice_is_running():
            self.get_logger().info('VOICE_ON ignored: stack already running')
            return

        self.voice_process = None
        try:
            self.voice_process = subprocess.Popen(
                [self.LAUNCHER],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
                close_fds=True,
            )
            self.get_logger().info(
                'VOICE_ON: voice process group started, launcher pid=%d'
                % self.voice_process.pid
            )
            self.publish_voice_enabled(True)
            self.publish_interact_ready()
        except Exception as exc:
            self.get_logger().error('VOICE_ON failed: %s' % exc)
            self.voice_process = None
            self.publish_voice_enabled(False)
            self.publish_interact_ready()

    def stop_voice(self):
        process = self.voice_process
        self.voice_process = None
        if process is None or process.poll() is not None:
            self.publish_voice_enabled(False)
            self.publish_interact_ready()
            return True, 'already_stopped'

        try:
            os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=10.0)
        except subprocess.TimeoutExpired:
            self.get_logger().warn(
                'Voice process group did not stop in time; forcing cleanup'
            )
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait(timeout=3.0)
        except ProcessLookupError:
            pass
        except Exception as exc:
            self.get_logger().error('Voice process group stop failed: %s' % exc)
            return False, str(exc)

        self.get_logger().info('Voice process group stopped')
        self.publish_voice_enabled(False)
        self.publish_interact_ready()
        return True, 'stopped'

    def on_stop_service(self, request, response):
        success, reason = self.stop_voice()
        response.success = success
        response.message = reason
        return response

    def on_armed_status(self, msg):
        self.armed_status = msg.data.strip().upper()
        if self.armed_status == 'ARMED_OFF':
            self.armed_voice_rejection_logged = False
            return
        if self.armed_status != 'ARMED_STARTING' and self.voice_is_running():
            success, reason = self.stop_voice()
            if not success:
                self.get_logger().error(
                    'VOICE_RUNTIME_STOP_FAILED_ARMED reason=%s' % reason
                )

    def monitor_process(self):
        if self.voice_process is None:
            return
        return_code = self.voice_process.poll()
        if return_code is not None:
            self.get_logger().warn(
                'Voice launcher exited with code %d' % return_code
            )
            self.voice_process = None
            self.publish_voice_enabled(False)
            self.publish_interact_ready()

    def publish_hold(self):
        self.motion_pub.publish(String(data='HOLD_NO_MOVE'))

    def on_system_command(self, msg):
        command = msg.data.strip().upper()
        if command == 'VOICE_ON':
            self.start_voice()
        elif command == 'VOICE_OFF':
            self.stop_voice()
        elif command == 'STOP':
            self.stop_voice()
            self.publish_hold()

    def shutdown(self):
        self.stop_voice()


def main(args=None):
    rclpy.init(args=args)
    node = VoiceRuntimeManagerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
