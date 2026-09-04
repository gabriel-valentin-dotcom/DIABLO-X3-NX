#!/usr/bin/env python3

import math
import struct
import time
from collections import deque
import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from std_msgs.msg import String


class VisionTrackNode(Node):

    def __init__(self):
        super().__init__('vision_track_node')

        self.last_depth = None
        self.last_color = None
        self.last_object_status = ''
        self.last_depth_time = 0.0
        self.last_color_time = 0.0
        self.last_object_time = 0.0
        self.frame_timeout_s = 1.0
        self.object_timeout_s = 4.0
        self.last_idle_publish_time = 0.0
        self.idle_publish_interval_s = 1.0

        self.warn_m = 0.60
        self.hard_m = 0.45
        self.far_m = 3.00

        # DEPTH_SAFETY_V1
        self.edge_far_m = 2.20
        self.edge_min_valid_ratio = 0.20
        # STAIR_DETECT_V1: valid lower image depth can still mean floor drops away.
        self.stair_bottom_min_m = 1.10
        self.stair_delta_m = 0.65
        self.small_threshold_bottom_max_m = 1.20
        self.small_threshold_min_ratio = 0.55
        self.small_threshold_max_drop_m = 0.35
        self.floor_history = deque(maxlen=5)
        self.floor_drop_min_votes = 3
        self.floor_unknown_min_votes = 4
        self.target_min_area_px = 450
        self.target_front_deadband = 0.16
        self.target_hold_s = 0.45
        self.last_valid_target = None
        self.last_valid_target_time = 0.0

        self.create_subscription(
            Image,
            '/camera/camera/depth/image_rect_raw',
            self.on_depth,
            qos_profile_sensor_data,
        )
        self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.on_color,
            qos_profile_sensor_data,
        )
        self.create_subscription(
            String,
            '/vision_object/status',
            self.on_object_status,
            10,
        )

        self.pub_status = self.create_publisher(String, '/vision_track/status', 10)
        self.pub_target = self.create_publisher(String, '/vision_track/target', 10)

        self.timer = self.create_timer(0.25, self.tick)

        self.get_logger().info('VISION_LIGHT_V2_DEPTH_SAFETY aktiv')

    def on_depth(self, msg):
        self.last_depth = msg
        self.last_depth_time = time.monotonic()

    def on_color(self, msg):
        self.last_color = msg
        self.last_color_time = time.monotonic()

    def on_object_status(self, msg):
        self.last_object_status = msg.data.strip()
        self.last_object_time = time.monotonic()

    def read_zone_stats(self, msg, cx, cy, radius_x=45, radius_y=35, step_px=15):
        samples = []
        total = 0
        valid = 0

        for dy in range(-radius_y, radius_y + 1, step_px):
            for dx in range(-radius_x, radius_x + 1, step_px):
                total += 1
                x = max(0, min(msg.width - 1, cx + dx))
                y = max(0, min(msg.height - 1, cy + dy))
                idx = y * msg.step + x * 2

                if idx + 2 <= len(msg.data):
                    raw = struct.unpack_from('<H', msg.data, idx)[0]
                    if raw > 0:
                        m = raw / 1000.0
                        if math.isfinite(m) and 0.10 <= m <= self.far_m:
                            valid += 1
                            samples.append(m)

        if not samples:
            return None, 0.0

        samples.sort()
        median = samples[len(samples) // 2]
        ratio = valid / float(total) if total > 0 else 0.0
        return median, ratio

    def fmt_depth(self, value):
        if value is None:
            return 'nan'
        return f'{value:.2f}'

    def best_side(self, left_m, right_m):
        l = left_m if left_m is not None else 0.0
        r = right_m if right_m is not None else 0.0
        return 'LEFT' if l > r else 'RIGHT'

    def image_to_bgr(self, msg):
        channels = 3
        frame = np.frombuffer(msg.data, dtype=np.uint8)
        frame = frame.reshape((msg.height, msg.width, channels))
        encoding = (msg.encoding or '').lower()
        if encoding == 'rgb8':
            return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame

    def classify_target_side(self, target_x, width):
        if target_x is None or width <= 0:
            return 'UNKNOWN', 'UNKNOWN'

        center_x = width / 2.0
        deadband_px = width * self.target_front_deadband
        error_x = target_x - center_x

        if abs(error_x) <= deadband_px:
            return 'CENTER', 'FRONT'
        if error_x < 0:
            return 'LEFT', 'LEFT'
        return 'RIGHT', 'RIGHT'

    def detect_color_target(self):
        if self.last_color is None:
            return {
                'visible': False,
                'center_x': None,
                'center_y': None,
                'area': 0,
                'side': 'UNKNOWN',
                'dir': 'UNKNOWN',
                'depth_m': None,
                'source': 'color_green',
            }

        try:
            bgr = self.image_to_bgr(self.last_color)
            hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
            lower_green = np.array([35, 70, 60])
            upper_green = np.array([90, 255, 255])
            mask = cv2.inRange(hsv, lower_green, upper_green)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                raise ValueError('no_contours')

            contour = max(contours, key=cv2.contourArea)
            area = int(cv2.contourArea(contour))
            if area < self.target_min_area_px:
                raise ValueError('target_too_small')

            x, y, w, h = cv2.boundingRect(contour)
            target_x = int(x + w / 2)
            target_y = int(y + h / 2)
            side, direction = self.classify_target_side(target_x, self.last_color.width)
            depth_m = None
            if self.last_depth is not None:
                depth_m, _ = self.read_zone_stats(
                    self.last_depth,
                    target_x,
                    target_y,
                    radius_x=35,
                    radius_y=35,
                    step_px=10,
                )

            return {
                'visible': True,
                'center_x': target_x,
                'center_y': target_y,
                'area': area,
                'side': side,
                'dir': direction,
                'depth_m': depth_m,
                'source': 'color_green',
            }
        except Exception:
            return {
                'visible': False,
                'center_x': None,
                'center_y': None,
                'area': 0,
                'side': 'UNKNOWN',
                'dir': 'UNKNOWN',
                'depth_m': None,
                'source': 'color_green',
            }

    def parse_object_boxes(self):
        text = self.last_object_status
        marker = 'boxes='
        if marker not in text:
            return []

        boxes_text = text.split(marker, 1)[1].strip()
        boxes = []
        for raw_box in boxes_text.split('|'):
            raw_box = raw_box.strip()
            if not raw_box:
                continue

            parts = raw_box.split(':')
            name = parts[0].strip().lower()
            fields = {}
            for part in parts[1:]:
                if '=' not in part:
                    continue
                key, value = part.split('=', 1)
                try:
                    fields[key] = float(value)
                except Exception:
                    fields[key] = None

            if name != 'person':
                continue
            if fields.get('cx') is None or fields.get('cy') is None:
                continue

            boxes.append({
                'name': name,
                'cx': fields.get('cx'),
                'cy': fields.get('cy'),
                'area': fields.get('area') or 0.0,
            })

        return boxes

    def detect_person_target(self):
        now = time.monotonic()
        if now - self.last_object_time > self.object_timeout_s:
            return {
                'visible': False,
                'center_x': None,
                'center_y': None,
                'area': 0,
                'side': 'UNKNOWN',
                'dir': 'UNKNOWN',
                'depth_m': None,
                'source': 'yolo_person',
            }

        boxes = self.parse_object_boxes()
        if not boxes:
            return {
                'visible': False,
                'center_x': None,
                'center_y': None,
                'area': 0,
                'side': 'UNKNOWN',
                'dir': 'UNKNOWN',
                'depth_m': None,
                'source': 'yolo_person',
            }

        box = max(boxes, key=lambda item: item['area'])
        target_x = int(box['cx'])
        target_y = int(box['cy'])
        width = self.last_color.width if self.last_color is not None else 640
        side, direction = self.classify_target_side(target_x, width)
        depth_m = None
        if self.last_depth is not None:
            depth_m, _ = self.read_zone_stats(
                self.last_depth,
                target_x,
                target_y,
                radius_x=35,
                radius_y=45,
                step_px=10,
            )

        return {
            'visible': True,
            'center_x': target_x,
            'center_y': target_y,
            'area': int(box['area']),
            'side': side,
            'dir': direction,
            'depth_m': depth_m,
            'source': 'yolo_person',
        }

    def detect_target(self):
        color_target = self.detect_color_target()
        if color_target['visible']:
            return color_target
        return self.detect_person_target()

    def stabilize_target(self, target, now):
        if target['visible']:
            self.last_valid_target = dict(target)
            self.last_valid_target_time = now
            return target

        if (
            self.last_valid_target is not None and
            now - self.last_valid_target_time <= self.target_hold_s
        ):
            held = dict(self.last_valid_target)
            held['source'] = f'{held["source"]}_hold'
            return held

        return target

    def classify_floor_raw(self, top_m, center_m, floor_values, floor_ratios):
        valid_pairs = [
            (v, r)
            for v, r in zip(floor_values, floor_ratios)
            if v is not None and r >= self.edge_min_valid_ratio
        ]

        if len(valid_pairs) < 2:
            return 'FLOOR_UNKNOWN'

        valid_values = [v for v, _ in valid_pairs]
        floor_center = (
            floor_values[1]
            if floor_values[1] is not None and floor_ratios[1] >= self.edge_min_valid_ratio
            else None
        )
        floor_near = min(valid_values)
        floor_far = max(valid_values)
        ref_values = [v for v in [top_m, center_m] if v is not None]
        ref_m = min(ref_values) if ref_values else None

        if floor_far > self.edge_far_m:
            return 'FLOOR_DROP_STOP'

        if ref_m is not None and floor_far - ref_m >= self.stair_delta_m:
            return 'FLOOR_DROP_STOP'

        if (
            floor_center is not None and
            center_m is not None and
            floor_center <= self.small_threshold_bottom_max_m and
            abs(floor_center - center_m) <= self.small_threshold_max_drop_m
        ):
            return 'SMALL_EDGE_OK'

        if floor_near <= self.edge_far_m:
            return 'FLOOR_OK'

        return 'FLOOR_UNKNOWN'

    def smooth_floor_state(self, raw_state):
        self.floor_history.append(raw_state)
        votes = {}
        for state in self.floor_history:
            votes[state] = votes.get(state, 0) + 1

        if votes.get('FLOOR_DROP_STOP', 0) >= self.floor_drop_min_votes:
            return 'FLOOR_DROP_STOP'

        if votes.get('FLOOR_UNKNOWN', 0) >= self.floor_unknown_min_votes:
            return 'FLOOR_UNKNOWN'

        if votes.get('SMALL_EDGE_OK', 0) >= 3:
            return 'SMALL_EDGE_OK'

        if votes.get('FLOOR_OK', 0) > 0 or votes.get('SMALL_EDGE_OK', 0) > 0:
            return 'FLOOR_OK'

        if raw_state == 'FLOOR_DROP_STOP':
            return 'FLOOR_UNKNOWN'

        return raw_state

    def tick(self):
        now = time.monotonic()
        depth_fresh = (
            self.last_depth is not None and
            now - self.last_depth_time <= self.frame_timeout_s
        )
        color_fresh = (
            self.last_color is not None and
            now - self.last_color_time <= self.frame_timeout_s
        )

        if not depth_fresh:
            if now - self.last_idle_publish_time >= self.idle_publish_interval_s:
                self.last_idle_publish_time = now
                self.pub_status.publish(String(data='NO_DEPTH'))
                self.pub_target.publish(String(
                    data=(
                        'target_visible=False,'
                        'target_center_x=-1,'
                        'target_center_y=-1,'
                        'image_width=0,'
                        'image_height=0,'
                        'target_dir=UNKNOWN,'
                        'target_side=UNKNOWN,'
                        'target_depth_m=nan,'
                        'target_area_px=0,'
                        'target_source=color_green,'
                        'vision_state=TARGET_LOST,'
                        'left_depth_m=nan,'
                        'center_depth_m=nan,'
                        'right_depth_m=nan,'
                        'top_depth_m=nan,'
                        'bottom_depth_m=nan,'
                        'bottom_ratio=0.00,'
                        'floor_state=FLOOR_UNKNOWN,'
                        'floor_left_m=nan,'
                        'floor_center_m=nan,'
                        'floor_right_m=nan,'
                        'floor_confidence=0.00,'
                        'center_x=0,center_y=0,'
                        'best_side=UNKNOWN,'
                        'state=NO_DEPTH'
                    )
                ))
            return

        if not color_fresh:
            self.last_color = None

        w = self.last_depth.width
        h = self.last_depth.height

        left_x = w // 4
        center_x = w // 2
        right_x = (w * 3) // 4

        top_y = int(h * 0.30)
        mid_y = h // 2
        floor_y = int(h * 0.82)

        left_m, _ = self.read_zone_stats(self.last_depth, left_x, mid_y)
        center_m, _ = self.read_zone_stats(self.last_depth, center_x, mid_y)
        right_m, _ = self.read_zone_stats(self.last_depth, right_x, mid_y)

        top_m, top_ratio = self.read_zone_stats(
            self.last_depth, center_x, top_y, radius_x=80, radius_y=30, step_px=15
        )

        floor_left_m, floor_left_ratio = self.read_zone_stats(
            self.last_depth, left_x, floor_y, radius_x=70, radius_y=35, step_px=15
        )
        floor_center_m, floor_center_ratio = self.read_zone_stats(
            self.last_depth, center_x, floor_y, radius_x=70, radius_y=35, step_px=15
        )
        floor_right_m, floor_right_ratio = self.read_zone_stats(
            self.last_depth, right_x, floor_y, radius_x=70, radius_y=35, step_px=15
        )

        side = self.best_side(left_m, right_m)
        target = self.stabilize_target(self.detect_target(), now)
        floor_values = [floor_left_m, floor_center_m, floor_right_m]
        floor_ratios = [floor_left_ratio, floor_center_ratio, floor_right_ratio]
        floor_confidence = sum(floor_ratios) / float(len(floor_ratios))
        raw_floor_state = self.classify_floor_raw(
            top_m, center_m, floor_values, floor_ratios
        )
        floor_state = self.smooth_floor_state(raw_floor_state)

        # DEPTH SAFETY
        front_stop = (
            center_m is not None and
            center_m < self.hard_m
        )

        if floor_state == 'FLOOR_DROP_STOP':
            state = 'DEPTH_STAIR_STOP'
        elif front_stop:
            state = 'DEPTH_FRONT_STOP'
        elif center_m is not None and center_m < self.warn_m:
            state = 'VISION_WARN'
        else:
            state = 'VISION_CLEAR'

        vision_state = 'TARGET_VISIBLE' if target['visible'] else 'TARGET_LOST'

        self.pub_status.publish(String(data=vision_state if target['visible'] else state))
        target_center_x = target['center_x'] if target['center_x'] is not None else -1
        target_center_y = target['center_y'] if target['center_y'] is not None else -1

        self.pub_target.publish(String(
            data=(
                f'target_visible={str(target["visible"])},'
                f'target_center_x={target_center_x},'
                f'target_center_y={target_center_y},'
                f'image_width={w},'
                f'image_height={h},'
                f'target_dir={target["dir"]},'
                f'target_side={target["side"]},'
                f'target_depth_m={self.fmt_depth(target["depth_m"])},'
                f'target_area_px={target["area"]},'
                f'target_source={target["source"]},'
                f'vision_state={vision_state},'
                f'left_depth_m={self.fmt_depth(left_m)},'
                f'center_depth_m={self.fmt_depth(center_m)},'
                f'right_depth_m={self.fmt_depth(right_m)},'
                f'top_depth_m={self.fmt_depth(top_m)},'
                f'bottom_depth_m={self.fmt_depth(floor_center_m)},'
                f'bottom_ratio={floor_center_ratio:.2f},'
                f'floor_state={floor_state},'
                f'floor_left_m={self.fmt_depth(floor_left_m)},'
                f'floor_center_m={self.fmt_depth(floor_center_m)},'
                f'floor_right_m={self.fmt_depth(floor_right_m)},'
                f'floor_confidence={floor_confidence:.2f},'
                f'center_x={center_x},center_y={mid_y},'
                f'best_side={side},'
                f'state={state}'
            )
        ))


def main():
    rclpy.init()
    node = VisionTrackNode()

    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
