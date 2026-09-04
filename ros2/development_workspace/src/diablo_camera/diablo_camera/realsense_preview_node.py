#!/usr/bin/env python3
import os
import traceback
import cv2
import numpy as np
import rclpy

from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from ultralytics import YOLO


class RealSensePreview(Node):

    def __init__(self):
        super().__init__('realsense_preview_node')

        preview_env = os.environ.get('DIABLO_ENABLE_PREVIEW', '').strip().lower()
        self.preview_enabled = preview_env in {'1', 'true', 'yes', 'on'}
        if self.preview_enabled:
            os.environ.setdefault('DISPLAY', ':1')

        self.lidar_text = 'LIDAR: WAIT'
        self.lidar_safe = False

        self.gesture_text = 'GESTURE: WAIT'
        self.vision_text = 'VISION: WAIT'
        self.auto_text = 'AUTO: WAIT'
        self.yolo_object_text = 'OBJECTS: none'

        self.left_depth = '?'
        self.center_depth = '?'
        self.right_depth = '?'
        self.frame_count = 0

        self.yolo = YOLO("/home/diablo/diablo_ws/yolov8n.pt")
        self.yolo_classes = {
            'person',
            'chair',
            'table',
            'dining table',
            'couch',
            'bottle'
        }

        self.yolo_interval = 4
        self.yolo_boxes = []

        self._warmup_yolo()

        self.img_sub = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.on_image,
            10
        )

        self.lidar_sub = self.create_subscription(
            String,
            '/diablo/safety/lidar_status',
            self.on_lidar_status,
            10
        )

        self.gesture_sub = self.create_subscription(
            String,
            '/gesture/status',
            self.on_gesture_status,
            10
        )

        self.vision_sub = self.create_subscription(
            String,
            '/vision_track/target',
            self.on_vision_target,
            10
        )

        self.auto_sub = self.create_subscription(
            String,
            '/diablo_motion_request',
            self.on_auto_cmd,
            10
        )

        self.object_pub = self.create_publisher(
            String,
            '/vision_object/status',
            10
        )

        mode = 'preview' if self.preview_enabled else 'headless'
        self.get_logger().info(
            f'RealSense Preview aktiv: Kamera + LiDAR + Gesture Overlay ({mode})'
        )

    def _warmup_yolo(self):
        # Keep CUDA startup latency out of the first live camera inference.
        dummy_rgb = np.zeros((480, 640, 3), dtype=np.uint8)
        dummy_bgr = cv2.cvtColor(dummy_rgb, cv2.COLOR_RGB2BGR)
        try:
            for _ in range(5):
                self.yolo(
                    dummy_bgr,
                    verbose=False,
                    conf=0.45,
                    imgsz=320,
                    device=0,
                )
            self.get_logger().info('YOLO_CUDA_READY')
        except Exception:
            self.get_logger().error(
                'YOLO CUDA warmup failed:\n' + traceback.format_exc()
            )
            raise

    def on_lidar_status(self, msg):

        text = msg.data.strip()

        if text.startswith('SAFE'):
            self.lidar_safe = True
        else:
            self.lidar_safe = False

        self.lidar_text = 'LIDAR: ' + text

    def on_gesture_status(self, msg):

        self.gesture_text = 'GESTURE: ' + msg.data.strip()

    def on_vision_target(self, msg):

        data = msg.data.strip()

        left = '?'
        center = '?'
        right = '?'
        state = 'UNKNOWN'
        best = '?'

        for part in data.split(','):
            part = part.strip()

            if part.startswith('left_depth_m='):
                left = part.split('=', 1)[1]

            elif part.startswith('center_depth_m='):
                center = part.split('=', 1)[1]

            elif part.startswith('right_depth_m='):
                right = part.split('=', 1)[1]

            elif part.startswith('state='):
                state = part.split('=', 1)[1]

            elif part.startswith('best_side='):
                best = part.split('=', 1)[1]

        self.left_depth = left
        self.center_depth = center
        self.right_depth = right

        self.vision_text = f'VISION: {state} best={best}'

    def on_auto_cmd(self, msg):

        self.auto_text = 'AUTO: ' + msg.data.strip()

    def on_image(self, msg):

        self.frame_count += 1
        if self.frame_count % 2 != 0:
            return

        try:

            img = np.frombuffer(msg.data, dtype=np.uint8)
            img = img.reshape((msg.height, msg.width, 3))

            if msg.encoding.lower() == 'rgb8':
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            img = cv2.resize(img, (640, 480))

            try:

                if self.frame_count % self.yolo_interval == 0:
                    results = self.yolo(
                        img,
                        verbose=False,
                        conf=0.45,
                        imgsz=320,
                        device=0,
                    )

                    self.yolo_boxes = []
                    center_objects = []

                    for r in results:
                        for b in r.boxes:
                            cls_id = int(b.cls[0])
                            name = self.yolo.names[cls_id]

                            if name not in self.yolo_classes:
                                continue

                            x1, y1, x2, y2 = map(int, b.xyxy[0])
                            self.yolo_boxes.append((name, x1, y1, x2, y2))

                            cx = int((x1 + x2) / 2)
                            if 220 <= cx <= 420:
                                center_objects.append(name)

                    if center_objects:
                        self.yolo_object_text = 'OBJECTS_CENTER: ' + ','.join(center_objects)
                    else:
                        self.yolo_object_text = 'OBJECTS_CENTER: none'

                    if self.yolo_boxes:
                        box_parts = []
                        for name, x1, y1, x2, y2 in self.yolo_boxes:
                            cx = int((x1 + x2) / 2)
                            cy = int((y1 + y2) / 2)
                            area = max(0, x2 - x1) * max(0, y2 - y1)
                            box_parts.append(
                                f'{name}:x1={x1}:y1={y1}:x2={x2}:y2={y2}:cx={cx}:cy={cy}:area={area}'
                            )
                        self.yolo_object_text += ' boxes=' + '|'.join(box_parts)

                    self.object_pub.publish(String(data=self.yolo_object_text))

                results = []

                for name, x1, y1, x2, y2 in self.yolo_boxes:

                    cv2.rectangle(
                        img,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        img,
                        name.upper(),
                        (x1, max(20, y1 - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2
                    )

            except Exception as e:
                self.get_logger().error(f'YOLO ERROR: {e}')


            # Vision Text
            cv2.putText(
                img,
                self.vision_text,
                (20, 400),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )


            cv2.putText(
                img,
                f'L:{self.left_depth}m  C:{self.center_depth}m  R:{self.right_depth}m',
                (20, 375),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )

            # Auto Command Text
            cv2.putText(
                img,
                self.auto_text,
                (20, 430),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (0, 255, 255),
                1,
                cv2.LINE_AA
            )

            # Gesture Text
            cv2.putText(
                img,
                self.gesture_text,
                (20, 455),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (255, 255, 0),
                1,
                cv2.LINE_AA
            )

            # LiDAR Text
            color = (0, 255, 0) if self.lidar_safe else (0, 0, 255)

            cv2.putText(
                img,
                self.lidar_text,
                (20, 475),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                color,
                1,
                cv2.LINE_AA
            )

            if self.preview_enabled:
                cv2.imshow('DIABLO RealSense Preview', img)
                cv2.waitKey(1)

        except Exception as e:

            self.get_logger().warn(f'Preview Fehler: {e}')

    def destroy_node(self):
        if self.preview_enabled:
            cv2.destroyAllWindows()
        super().destroy_node()


def main():

    rclpy.init()

    node = RealSensePreview()

    try:
        rclpy.spin(node)

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
