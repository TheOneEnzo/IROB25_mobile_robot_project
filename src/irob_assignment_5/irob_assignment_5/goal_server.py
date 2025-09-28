#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from irob_interfaces.srv import GetGoal
from geometry_msgs.msg import PointStamped


class GoalServiceNode(Node):
    def __init__(self):
        super().__init__('goal_service_node')  # Node name must match YAML

        # Declare the parameter (required in ROS 2 Foxy)
        self.declare_parameter('goal_sequence', [])

        #Get the goal sequence parameter (provided externally via YAML)
        try:
            goal_param_list = self.get_parameter('goal_sequence').get_parameter_value().string_array_value
        except Exception:
            self.get_logger().error("Missing required parameter 'goal_sequence'. Check your YAML or launch file. CONTACT TA")
            raise

        #Convert list of "x,y" strings to list of (x, y) tuples
        try:
            self.goals = [tuple(map(float, g.strip().split(','))) for g in goal_param_list]
        except Exception:
            self.get_logger().error("Invalid format in 'goal_sequence'. Expected list of strings like '1.0,2.0'")
            raise

        self.get_logger().info(f"Loaded goals: {self.goals}")

        # Initialize state
        self.call_count = 0
        self.last_goal = None

        # Create publisher for RViz visualization
        self.point_pub = self.create_publisher(PointStamped, 'goal_point', 10)

        # Create the service server
        self.srv = self.create_service(GetGoal, 'get_goal', self.handle_get_goal)

        # Timer to re-publish the goal every second
        self.timer = self.create_timer(1.0, self.publish_last_point)

        self.get_logger().info('Goal service node is ready and waiting for requests.')

    def handle_get_goal(self, request, response):
        self.call_count += 1

        # Get the goal based on call number
        if self.call_count <= len(self.goals):
            goal_x, goal_y = self.goals[self.call_count - 1]
        else:
            goal_x, goal_y = self.goals[-1]  # Repeat the last one if list is exhausted

        # Respond
        response.goal_x = goal_x
        response.goal_y = goal_y

        # Publish for visualization
        self.last_goal = (goal_x, goal_y)
        self.publish_point(goal_x, goal_y)

        self.get_logger().info(f"[Call #{self.call_count}] Sent goal: x={goal_x}, y={goal_y}")
        return response

    def publish_last_point(self):
        if self.last_goal:
            self.publish_point(*self.last_goal)

    def publish_point(self, x, y):
        point = PointStamped()
        point.header.frame_id = "map"  # Adjust if needed
        point.header.stamp = self.get_clock().now().to_msg()
        point.point.x = x
        point.point.y = y
        point.point.z = 0.0
        self.point_pub.publish(point)
        self.get_logger().info(f"Published PointStamped at x={x}, y={y}")


def main(args=None):
    rclpy.init(args=args)
    node = GoalServiceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
