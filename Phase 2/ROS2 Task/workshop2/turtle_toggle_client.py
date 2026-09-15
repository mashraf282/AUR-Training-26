import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
from functools import partial

class TurtleToggleClient(Node):
    def __init__(self):
        super().__init__("turtle_toggle_client")
        self.get_logger().info("Service Client Node Started!!")

        self.send_request()

    def send_request(self):
        self.client = self.create_client(SetBool, "toggle_turtle_moving_state")

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Service not available, waiting again...")

        self.request = SetBool.Request()
        self.request.data = True

        future = self.client.call_async(self.request)
        future.add_done_callback(partial(self.service_callback, data=self.request.data))

    def service_callback(self, future, data):
        try:
            response = future.result()
            self.get_logger().info(f"Service response: {response.success}")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")

def main():
    rclpy.init()
    node = TurtleToggleClient()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()