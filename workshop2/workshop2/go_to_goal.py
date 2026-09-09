import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import SetBool

class GoToGoal(Node):
    def __init__(self):
        super().__init__('go_to_goal')

        self.declare_parameter('TARGET_X', 0.0)
        self.declare_parameter('TARGET_Y', 0.0)
        self.declare_parameter('KP_LINEAR', 0.0)
        self.declare_parameter('KP_ANGULAR', 0.0)
        self.declare_parameter('DISTANCE_TOLERANCE', 0.0)
        self.declare_parameter('ANGLE_TOLERANCE', 0.0)
        self.declare_parameter('LOOP_RATE', 0.0)
        
        # Target Goal Coordinates
        self.goal_x = self.get_parameter('TARGET_X').value
        self.goal_y = self.get_parameter('TARGET_Y').value

        # Proportional Gains (K_p)
        self.kp_linear = self.get_parameter('KP_LINEAR').value
        self.kp_angular = self.get_parameter('KP_ANGULAR').value

        # Tolerances
        self.distance_tolerance = self.get_parameter('DISTANCE_TOLERANCE').value  # Distance error limit to consider goal reached
        self.angle_tolerance = self.get_parameter('ANGLE_TOLERANCE').value    # Heading alignment threshold before moving forward

        # State Variables
        self.current_pose = None
        self.goal_reached = False

        # ROS 2 Publisher & Subscriber
        self.cmd_vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_subscriber = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10
        )

        self.loop_rate = self.get_parameter('LOOP_RATE').value

        # Control Loop running at 20 Hz
        self.timer = self.create_timer(1.0 / self.loop_rate, self.control_loop)

        self.get_logger().info(f'Navigating turtle to target goal: ({self.goal_x}, {self.goal_y})')

        self.is_moving = False
        self.srv = self.create_service(SetBool, "toggle_turtle_moving_state", self.set_bool_callback)

    def set_bool_callback(self, request, response):
        self.is_moving = request.data
        response.success = True
        self.get_logger().info(f"Incoming request: {request.data}. Sending back response: success={response.success}")
        return response

    def pose_callback(self, msg: Pose):
        """Update current position and heading from /turtle1/pose stream."""
        self.current_pose = msg

    def normalize_angle(self, angle: float) -> float:
        """Keep heading angle within [-pi, pi] to avoid unnecessary 360-degree turns."""
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle

    def control_loop(self):
        """Proportional Control Loop."""
        if self.current_pose is None or self.goal_reached:
            return

        if not self.is_moving:
            return

        # 1. Calculate Cartesian Errors
        dx = self.goal_x - self.current_pose.x
        dy = self.goal_y - self.current_pose.y

        # Euclidean Distance Error: sqrt((x_g - x)^2 + (y_g - y)^2)
        distance_error = math.sqrt(dx**2 + dy**2)

        # Desired Heading Angle: atan2(dy, dx)
        target_angle = math.atan2(dy, dx)
        heading_error = self.normalize_angle(target_angle - self.current_pose.theta)

        msg = Twist()

        # 2. Check if Goal is Reached
        if distance_error < self.distance_tolerance:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.cmd_vel_publisher.publish(msg)
            self.goal_reached = True
            self.get_logger().info('Goal Reached Successfully!')
            return

        # 3. Proportional Control Logic
        # If heading error is large, align facing direction first before moving forward
        if abs(heading_error) > self.angle_tolerance:
            msg.linear.x = 0.0
            msg.angular.z = self.kp_angular * heading_error
        else:
            # Scale forward speed and heading alignment concurrently
            msg.linear.x = min(self.kp_linear * distance_error, 2.0)  # Cap speed at 2.0 m/s
            msg.angular.z = self.kp_angular * heading_error

        self.cmd_vel_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = GoToGoal()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
