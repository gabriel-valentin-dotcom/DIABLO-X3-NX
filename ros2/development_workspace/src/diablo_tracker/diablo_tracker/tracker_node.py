#!/usr/bin/env python3

import re
import time
import serial

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String, Bool


class DiabloTrackerNode(Node):
    def __init__(self):
        super().__init__('diablo_tracker_node')

        self.track_enabled = False

        self.mode_sub = self.create_subscription(
            Bool,
            '/diablo/mode/track_enabled',
            self.on_track_mode,
            10
        )

        self.declare_parameter('port', '/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0')
        self.declare_parameter('baud', 115200)
        self.declare_parameter('command', 'AT+DISTANCE')
        self.declare_parameter('command_interval_sec', 1.0)
        self.declare_parameter('timeout_sec', 0.03)
        self.declare_parameter('serial_timeout_sec', 0.2)
        self.declare_parameter('response_window_sec', 1.3)
        self.declare_parameter('no_data_timeout_sec', 3.0)
        self.declare_parameter('scale', 1.0)
        self.declare_parameter('offset', 0.0)
        self.declare_parameter('stale_repeat_limit', 2)
        self.declare_parameter('stale_timeout_sec', 3.0)

        self.port = self.get_parameter('port').value
        self.baud = int(self.get_parameter('baud').value)
        self.command = self.get_parameter('command').value
        self.command_interval_sec = float(self.get_parameter('command_interval_sec').value)
        self.timeout_sec = float(self.get_parameter('timeout_sec').value)
        self.serial_timeout_sec = float(self.get_parameter('serial_timeout_sec').value)
        self.response_window_sec = float(self.get_parameter('response_window_sec').value)
        self.no_data_timeout_sec = float(self.get_parameter('no_data_timeout_sec').value)
        self.scale = float(self.get_parameter('scale').value)
        self.offset = float(self.get_parameter('offset').value)
        self.stale_repeat_limit = int(self.get_parameter('stale_repeat_limit').value)
        self.stale_timeout_sec = float(self.get_parameter('stale_timeout_sec').value)

        self.pub_distance = self.create_publisher(Float32, '/uwb_distance', 10)
        self.pub_status = self.create_publisher(String, '/tracker_status', 10)
        self.pub_raw = self.create_publisher(String, '/uwb_raw', 10)

        self.ser = None
        self.last_valid_data_time = None
        self.last_live_change_time = None
        self.last_raw_distance = None
        self.last_calibrated_distance = None
        self.repeat_count = 0
        self.last_command_time = 0.0
        self.last_status = ''

        self.get_logger().info('DIABLO tracker node FAST MODE READY')
        self.get_logger().info(f'Port: {self.port}')
        self.get_logger().info(f'Baud: {self.baud}')
        self.get_logger().info(
            f'Interval: {self.command_interval_sec}s serial_timeout={self.serial_timeout_sec}s '
            f'response_window={self.response_window_sec}s'
        )

        self.connect_serial()
        self.timer = self.create_timer(0.02, self.loop)

    def on_track_mode(self, msg):
        enabled = bool(msg.data)

        if enabled == self.track_enabled:
            return

        self.track_enabled = enabled

        if self.track_enabled:
            self.get_logger().info('TRACK MODE = ON')

            self.last_valid_data_time = None
            self.last_live_change_time = None
            self.last_raw_distance = None
            self.last_calibrated_distance = None
            self.repeat_count = 0
            self.last_command_time = 0.0

            if self.ser is None or not self.ser.is_open:
                self.connect_serial()

            self.last_command_time = 0.0

        else:
            self.get_logger().info('TRACK MODE = OFF')

    def publish_status(self, status):
        msg = String()
        msg.data = status
        self.pub_status.publish(msg)

        if status != self.last_status:
            self.get_logger().warn(f'STATUS: {status}')
            self.last_status = status

    def connect_serial(self):
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baud,
                timeout=self.serial_timeout_sec
            )

            time.sleep(0.05)
            if self.last_valid_data_time is None:
                self.publish_status('NO_DATA')
            elif (
                self.last_live_change_time is not None and
                time.time() - self.last_live_change_time > self.stale_timeout_sec
            ):
                self.publish_status('STALE')

        except Exception as e:
            self.ser = None
            self.publish_status('ERR')
            self.get_logger().error(f'Cannot open serial port: {e}')

    def compact_response(self, response):
        return ' '.join(response.replace('\r', '\n').split())

    def read_available_bytes(self, duration_sec):
        chunks = []
        deadline = time.time() + duration_sec

        while time.time() < deadline:
            waiting = self.ser.in_waiting if self.ser is not None and self.ser.is_open else 0
            if waiting > 0:
                chunks.append(self.ser.read(waiting))
            else:
                time.sleep(0.01)

        return b''.join(chunks)

    def request_distance_response(self):
        try:
            self.read_available_bytes(0.15)
            self.ser.reset_input_buffer()

            cmd = (self.command + '\r\n').encode()
            self.ser.write(cmd)
            self.ser.flush()
            self.last_command_time = time.time()

            chunks = []
            deadline = time.time() + self.response_window_sec

            while time.time() < deadline:
                waiting = self.ser.in_waiting
                if waiting > 0:
                    chunks.append(self.ser.read(waiting))
                else:
                    chunk = self.ser.read(1)
                    if chunk:
                        chunks.append(chunk)

                response_so_far = b''.join(chunks).decode(errors='ignore').upper()
                if 'ERR' in response_so_far:
                    break
                if re.search(r'distance:\s*[0-9.]+', response_so_far, re.IGNORECASE) and 'OK' in response_so_far:
                    break

            response = b''.join(chunks).decode(errors='ignore')
            raw_response = response
            return response, raw_response

        except Exception as e:
            self.publish_status('ERR')
            self.get_logger().error(f'Serial transaction error: {e}')

            try:
                self.ser.close()
            except Exception:
                pass

            self.ser = None
            return None, None

    def publish_raw_response(self, raw_response):
        raw_msg = String()
        raw_msg.data = self.compact_response(raw_response)
        self.pub_raw.publish(raw_msg)

    def process_response(self, response, raw_response, now):
        self.publish_raw_response(raw_response)
        transaction_response = raw_response
        compact = self.compact_response(transaction_response)

        if 'ERR' in transaction_response.upper():
            self.publish_status('ERR')
            self.get_logger().info(f"UWB response='{compact}' status=ERR")
            return

        match = re.search(r'distance:\s*([0-9.]+)', transaction_response)

        if not match:
            self.publish_status('NO_DATA')
            self.get_logger().info(f"UWB response='{compact}' status=NO_DATA")
            return

        try:
            raw_distance = float(match.group(1))
        except ValueError:
            self.publish_status('ERR')
            self.get_logger().info(f"UWB response='{compact}' status=ERR")
            return

        distance = raw_distance * self.scale + self.offset

        if raw_distance <= 0.0:
            self.publish_status('INVALID_ZERO')
            self.get_logger().info(
                f"UWB response='{compact}' raw={raw_distance:.6f} "
                f'cal={distance:.6f} repeat={self.repeat_count} status=INVALID_ZERO'
            )
            return

        if distance < 0.30 or distance > 8.0:
            self.publish_status('INVALID_RANGE')
            self.get_logger().info(
                f"UWB response='{compact}' raw={raw_distance:.6f} "
                f'cal={distance:.6f} repeat={self.repeat_count} status=INVALID_RANGE'
            )
            return

        if self.last_raw_distance is None:
            self.repeat_count = 0
            self.last_raw_distance = raw_distance
            self.last_calibrated_distance = distance
            self.last_live_change_time = now
        elif raw_distance == self.last_raw_distance:
            self.repeat_count += 1
        else:
            self.repeat_count = 0
            self.last_raw_distance = raw_distance
            self.last_calibrated_distance = distance
            self.last_live_change_time = now

        stale_by_repeat = self.repeat_count >= self.stale_repeat_limit
        stale_by_timeout = (
            self.last_live_change_time is not None and
            now - self.last_live_change_time > self.stale_timeout_sec
        )

        if self.repeat_count > 0:
            status = 'STALE' if stale_by_repeat or stale_by_timeout else self.last_status
            if status == 'STALE':
                self.publish_status(status)
            self.get_logger().info(
                f"UWB response='{compact}' raw={raw_distance:.6f} "
                f'cal={distance:.6f} repeat={self.repeat_count} status={status}'
            )
            return

        msg = Float32()
        msg.data = distance
        self.pub_distance.publish(msg)

        self.last_valid_data_time = now
        self.publish_status('OK')

        self.get_logger().info(
            f"UWB response='{compact}' raw={raw_distance:.6f} "
            f'cal={distance:.6f} repeat={self.repeat_count} status=OK'
        )

    def update_stale_status(self, now):
        if self.last_valid_data_time is None:
            self.publish_status('NO_DATA')
        elif (
            self.last_live_change_time is not None and
            now - self.last_live_change_time > self.stale_timeout_sec
        ):
            self.publish_status('STALE')
        elif now - self.last_valid_data_time > self.no_data_timeout_sec:
            self.publish_status('STALE')

    def loop(self):
        if not self.track_enabled:
            return

        now = time.time()

        if self.ser is None or not self.ser.is_open:
            self.connect_serial()
            return

        if now - self.last_command_time < self.command_interval_sec:
            self.update_stale_status(now)
            return

        response, raw_response = self.request_distance_response()

        if response is None:
            return

        self.process_response(response, raw_response, time.time())


def main(args=None):
    rclpy.init(args=args)
    node = DiabloTrackerNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        if node.ser:
            node.ser.close()

        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
