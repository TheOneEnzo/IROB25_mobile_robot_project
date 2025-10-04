#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from irob_interfaces.srv import GetGoal, Activate, Deactivate, AtGoal
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry, OccupancyGrid
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool

import numpy as np
import time


class SMStudentsNode(Node):
    def __init__(self):
        super().__init__('SM_students_node')

        # Clients
        self.activate_client = self.create_client(Activate, 'activate')
        self.deactivate_client = self.create_client(Deactivate, 'deactivate')
        self.goal_client = self.create_client(GetGoal, 'get_goal')
        self.at_goal_client = self.create_client(AtGoal, 'at_goal')
        
        # Publisher
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Subscribers
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.active_sub = self.create_subscription(Bool, '/robot_active', self.active_callback, 10)
        self.map_sub = self.create_subscription(OccupancyGrid, '/map', self.map_callback, 10)

        # Services
        self.activate_sm_srv = self.create_service(Activate, 'activate_sm', self.handle_activate_robot)
        self.deactivate_sm_srv = self.create_service(Deactivate, 'deactivate_sm', self.handle_deactivate_robot)

        # Internal state
        self.current_pose = None
        self.current_orientation = None        
        self.current_goal = None
        self.current_yaw = None
        self.active = False
        self.scan_data = None
        self.start_time = None 
        self.last_distance = None
        self.map_data = None
        self.state = "INACTIVE"
        self.stuck_check_start_time = None
        self.stuck_check_initial_distance = None
        self.last_velocity_publish_time = None

        # For tracking async goal request
        self.goal_future = None

        # Timer to drive state machine
        self.timer = self.create_timer(0.1, self.state_machine_callback)

        self.get_logger().info("SM_students_node ready. Robot is inactive until activated.")

    # Callbacks
    def odom_callback(self, msg):
        self.current_pose = (msg.pose.pose.position.x, msg.pose.pose.position.y)
        self.current_orientation = msg.pose.pose.orientation

    def active_callback(self, msg):
        self.active = msg.data

    def scan_callback(self, msg):
        self.scan_data = msg

    def map_callback(self, msg):
        self.map_data = msg

    # Service Handlers
    def handle_activate_robot(self, request, response):
        self.get_logger().info("Activate SM service called!")

        if self.current_pose is None:
            self.get_logger().warn("Cannot activate state machine — no odometry received yet.")
            response.success = False
            response.message = "No odometry received yet."
            return response

        self.state = 'GET_GOAL'
        self.get_logger().info("State machine state set to GET_GOAL")
        response.success = True
        response.message = 'State machine activated.'
        return response


    def handle_deactivate_robot(self, request, response):
        future = self.deactivate_client.call_async(Deactivate.Request())
        rclpy.spin_until_future_complete(self, future)
        if future.result():
            self.get_logger().info(future.result().message)
        else:
            self.get_logger().error("Failed to deactivate robot.")
        self.publish_zero_velocity()
        self.state = 'INACTIVE'
        response.success = True
        response.message = 'State machine deactivated.'
        return response

    def publish_zero_velocity(self):
        velocity = Twist()
        velocity.linear.x = 0.0
        velocity.angular.z = 0.0
        self.cmd_vel_pub.publish(velocity)
        self.get_logger().debug("Published zero velocity")
        
    def goal_reachable(self):
        if self.current_goal is None:
            self.get_logger().warn("No current goal.")
            return False

        if self.current_pose is None:
            self.get_logger().warn("No current pose.")
            return False

        if self.map_data is None:
            self.get_logger().warn("No map data.")
            return False

        goal_map = self.map_data.info
        goal_x = (self.current_goal[0] - goal_map.origin.position.x) / goal_map.resolution
        goal_y = (self.current_goal[1] - goal_map.origin.position.y) / goal_map.resolution
        goal_idx = int(goal_y * goal_map.width + goal_x)

        self.get_logger().info(f"Goal index: {goal_idx} of {len(self.map_data.data)}")

        goal = self.map_data.data[goal_idx]
        return True

    def deactivate_robot(self):
        future = self.deactivate_client.call_async(Deactivate.Request())
        rclpy.spin_until_future_complete(self, future)
        if future.result():
            self.get_logger().info(future.result().message)
        else:
            self.get_logger().error("Failed to deactivate robot.")
        self.publish_zero_velocity()

    # Async callback for get_goal response
    def goal_response_callback(self, future):
        try:
            response = future.result()

            # Detect end of goal list
            if response.goal_x == float('inf') or response.goal_y == float('inf'):
                self.get_logger().info("No more goals. Deactivating robot.")
                self.publish_zero_velocity()
                self.deactivate_robot()
                self.state = 'INACTIVE'
                return

            goal = (response.goal_x, response.goal_y)
            self.get_logger().info(f'Goal received: {goal}')
            self.current_goal = goal

            # Always move to the goal first, then check if it's reachable
            self.get_logger().info("Moving to goal first, then will check if reachable.")
            self.start_time = time.time()
            self.last_distance = None
            self.stuck_check_start_time = None
            self.stuck_check_initial_distance = None
            self.last_velocity_publish_time = None
            self.state = 'GOTO_GOAL'

        except Exception as e:
            self.get_logger().error(f'Failed to get goal: {e}')
            self.state = 'GET_GOAL'

    def state_machine_callback(self):
        if self.state == 'INACTIVE':
            return

        if self.state == 'GET_GOAL':
            if not self.goal_client.wait_for_service(timeout_sec=1.0):
                self.get_logger().warn('get_goal service not available.')
                return

            # If we don't have a pending request, send one
            if self.goal_future is None or self.goal_future.done():
                self.get_logger().info("Calling get_goal service asynchronously...")
                request = GetGoal.Request()
                self.goal_future = self.goal_client.call_async(request)
                self.goal_future.add_done_callback(self.goal_response_callback)

        elif self.state == 'GOTO_GOAL':
            if self.current_goal is None or self.current_pose is None:
                self.get_logger().warn("Cannot navigate - missing goal or pose")
                return

            dx = self.current_goal[0] - self.current_pose[0]
            dy = self.current_goal[1] - self.current_pose[1]
            distance = np.sqrt(dx**2 + dy**2)

            if self.last_distance is None:
                self.last_distance = distance
                self.get_logger().info(f"Initial distance to goal: {distance:.2f}")

            # Initialize stuck detection after a short delay to let the robot start moving
            if self.stuck_check_start_time is None and time.time() - self.start_time > 3.0:
                self.stuck_check_start_time = time.time()
                self.stuck_check_initial_distance = distance
                self.get_logger().info(f"Starting stuck detection. Current distance: {distance:.2f}")

            # Check for timeout
            if time.time() - self.start_time > 60:
                self.get_logger().warn('Timeout while trying to reach goal.')
                self.publish_zero_velocity()
                self.state = 'GET_GOAL'
                return

            # Check if robot is stuck (only after stuck detection has started)
            if (self.stuck_check_start_time is not None and 
                time.time() - self.stuck_check_start_time > 10.0 and 
                abs(distance - self.stuck_check_initial_distance) < 0.1 and 
                distance > 0.1):
                self.get_logger().warn(f'Robot stuck, retrying... Distance: {distance:.2f}')
                self.publish_zero_velocity()
                self.state = 'GET_GOAL'
                return

            self.last_distance = distance

            # Orientation to yaw
            q = self.current_orientation
            siny_cosp = 2 * (q.w * q.z + q.x * q.y)
            cosy_cosp = 1 - 2 * (q.y**2 + q.z**2)
            self.current_yaw = np.arctan2(siny_cosp, cosy_cosp)

            angle = np.arctan2(dy, dx)
            angular_error = angle - self.current_yaw
            angular_error = (angular_error + np.pi) % (2 * np.pi) - np.pi

            if distance < 0.1:  # Increased tolerance
                self.get_logger().info(f"Reached goal! Distance: {distance:.2f}")
                self.publish_zero_velocity()
                # Now that we're at the goal, check if it's actually reachable/valid
                self.state = 'CHECK_GOAL_VALIDITY'
                return

            # Publish velocity command - only if we haven't published recently or orientation is good
            current_time = time.time()
            if (self.last_velocity_publish_time is None or 
                current_time - self.last_velocity_publish_time > 0.1 or 
                abs(angular_error) < 0.5):  # Only move if reasonably aligned
                
                velocity = Twist()
                
                # Only move forward if reasonably aligned with goal
                if abs(angular_error) < 1.0:  # ~57 degrees
                    velocity.linear.x = min(0.2, distance)  # Reduced max speed
                else:
                    velocity.linear.x = 0.0
                
                velocity.angular.z = np.clip(angular_error * 2.0, -1.0, 1.0)  # Increased gain, limited
                
                self.cmd_vel_pub.publish(velocity)
                self.last_velocity_publish_time = current_time
                
                if current_time - self.start_time < 5.0:  # Log more frequently at start
                    self.get_logger().info(f"Publishing velocity: lin_x={velocity.linear.x:.2f}, ang_z={velocity.angular.z:.2f}, dist={distance:.2f}, ang_err={angular_error:.2f}")

        elif self.state == 'CHECK_GOAL_VALIDITY':
            # Now check if the goal we just reached is valid/reachable
            if self.goal_reachable():
                self.get_logger().info('Goal reached successfully and is valid. Deactivating.')
                self.publish_zero_velocity()
                self.deactivate_robot()
                self.state = 'INACTIVE'
            else:
                self.get_logger().warn('Goal is in obstacle or unreachable. Requesting new goal.')
                self.publish_zero_velocity()
                self.state = 'GET_GOAL'

def main(args=None):
    rclpy.init(args=args)
    node = SMStudentsNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
