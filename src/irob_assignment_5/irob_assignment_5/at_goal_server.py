#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PointStamped
from nav_msgs.msg import Odometry
from irob_interfaces.srv import AtGoal

import math


class AtGoalServiceNode(Node):
    def __init__(self):
        super().__init__('at_goal_service_node')

        self.threshold = 0.05

        self.goal_sub = self.create_subscription(
            PointStamped, '/goal_point', self.goal_callback, 10)
        self.odom_sub = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10)

        self.srv = self.create_service(AtGoal, 'at_goal', self.handle_at_goal)

        self.current_pose = None
        self.current_goal = None

        self.get_logger().info("AtGoal Service Node ready.")

    def goal_callback(self, msg):
        self.current_goal = (msg.point.x, msg.point.y)

    def odom_callback(self, msg):
        self.current_pose = (
            msg.pose.pose.position.x,
            msg.pose.pose.position.y
        )

    def handle_at_goal(self, request, response):
        if self.current_pose is None or self.current_goal is None:
            response.success = False
            response.message = "Missing robot pose or goal position"
            return response

        dx = self.current_goal[0] - self.current_pose[0]
        dy = self.current_goal[1] - self.current_pose[1]
        dist = math.sqrt(dx**2 + dy**2)

        if dist < self.threshold:
            response.success = True
            response.message = f"At goal (distance: {dist:.3f} m)"
        else:
            response.success = False
            response.message = f"Not at goal (distance: {dist:.3f} m)"

        self.get_logger().info(f"[AtGoal] {response.message}")
        return response


def main(args=None):
    rclpy.init(args=args)
    node = AtGoalServiceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
