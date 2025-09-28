import rclpy
from rclpy.node import Node
from irob_interfaces.srv import Activate, Deactivate
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool


class ActivationServer(Node):
    def __init__(self):
        super().__init__('activation_server')

        self.active = False  # Robot starts inactive

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.state_pub = self.create_publisher(Bool, '/robot_active', 10)

        # Services
        self.activate_srv = self.create_service(Activate, 'activate', self.handle_activate)
        self.deactivate_srv = self.create_service(Deactivate, 'deactivate', self.handle_deactivate)

        # Timer to continuously send state and stop command if inactive (10 Hz)
        self.timer = self.create_timer(0.01, self.timer_callback)

        self.get_logger().info("Activation server is up. Services: /activate and /deactivate")

        if not self.active:
            # Immediately stop the robot
            stop_msg = Twist()
            stop_msg.linear.x = 0.0
            stop_msg.angular.z = 0.0
            self.cmd_vel_pub.publish(stop_msg)

    def handle_activate(self, request, response):
        if not self.active:
            self.active = True
            response.success = True
            response.message = "Robot activated successfully."
            self.get_logger().info("Robot ACTIVATED.")
        else:
            response.success = True
            response.message = "Robot is already active."
            self.get_logger().warn("Activation called, but robot is already active.")
        return response

    def handle_deactivate(self, request, response):
        if self.active:
            self.active = False
            response.success = True
            response.message = "Robot deactivated successfully."
            self.get_logger().info("Robot DEACTIVATED.")
        else:
            response.success = True
            response.message = "Robot is already inactive."
            self.get_logger().warn("Deactivation called, but robot is already inactive.")
        return response

    def timer_callback(self):
        # Publish robot active state
        state_msg = Bool()
        state_msg.data = self.active
        self.state_pub.publish(state_msg)

        # If inactive, also send stop cmd_vel
        if not self.active:
            stop_msg = Twist()
            stop_msg.linear.x = 0.0
            stop_msg.angular.z = 0.0
            self.cmd_vel_pub.publish(stop_msg)


def main(args=None):
    rclpy.init(args=args)
    node = ActivationServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
