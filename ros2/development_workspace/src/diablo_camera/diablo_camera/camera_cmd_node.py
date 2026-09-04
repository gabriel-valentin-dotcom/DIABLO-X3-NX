import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import SetBool


class CameraCmdNode(Node):
    def __init__(self):
        super().__init__('camera_cmd_node')

        self.enabled = True

        self.sub = self.create_subscription(
            String,
            '/camera/cmd',
            self.cmd_callback,
            10
        )

        self.client = self.create_client(SetBool, '/camera/enable')

        self.get_logger().info("Camera CMD Node bereit: /camera/cmd")

    def cmd_callback(self, msg):
        cmd = msg.data.strip().upper()

        if cmd == "CAM_ON":
            self.call_enable(True)

        elif cmd == "CAM_OFF":
            self.call_enable(False)

        elif cmd == "CAM_TOGGLE":
            self.enabled = not self.enabled
            self.call_enable(self.enabled)

        else:
            self.get_logger().warn(f"Unbekannter CAM Befehl: {cmd}")

    def call_enable(self, state):
        if not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("Service /camera/enable nicht erreichbar")
            return

        req = SetBool.Request()
        req.data = state
        future = self.client.call_async(req)
        future.add_done_callback(self.done_callback)

    def done_callback(self, future):
        try:
            res = future.result()
            self.get_logger().info(res.message)
        except Exception as e:
            self.get_logger().error(str(e))


def main(args=None):
    rclpy.init(args=args)
    node = CameraCmdNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
