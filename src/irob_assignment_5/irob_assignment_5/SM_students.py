import rclpy
from rclpy.node import Node

from irob_interfaces.srv import GetGoal, Activate, Deactivate, AtGoal
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry, OccupancyGrid
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool

import numpy as np
import time
import math


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

        # Obstacle avoidance parameters
        self.obstacle_detected = False
        self.obstacle_avoidance_mode = False
        self.obstacle_avoidance_start_time = None
        self.last_obstacle_side = None  # 'left' or 'right'
        self.avoidance_direction_changes = 0  # Track direction changes to prevent oscillation
        
        # Navigation parameters
        self.safe_distance = 0.2  # Safe distance from obstacles
        self.min_obstacle_distance = 0.2  # Minimum obstacle distance
        self.obstacle_angle_range = 60  # Obstacle detection angle range (degrees)
        self.avoidance_duration = 2.0  # Avoidance duration
        self.avoidance_stuck_threshold = 2  # Maximum direction changes before giving up
        
        # Recovery behavior parameters
        self.recovery_mode = False
        self.recovery_start_time = None
        self.recovery_duration = 8.0  # Maximum recovery time
        self.last_recovery_pose = None  # Track position during recovery

        # For tracking async goal request
        self.goal_future = None
        # For tracking async activation request
        self.activate_future = None

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
        # Real-time obstacle detection
        self.detect_obstacles()

    def map_callback(self, msg):
        self.map_data = msg

    def detect_obstacles(self):
        """Use lidar data to detect obstacles"""
        if self.scan_data is None:
            return
            
        ranges = self.scan_data.ranges
        angle_min = self.scan_data.angle_min
        angle_increment = self.scan_data.angle_increment
        
        # Check if there are obstacles in front
        front_obstacle = False
        left_obstacle = False
        right_obstacle = False
        
        for i, distance in enumerate(ranges):
            if math.isinf(distance) or math.isnan(distance):
                continue
                
            angle = angle_min + i * angle_increment
            angle_deg = math.degrees(angle)
            
            # Front obstacle detection (-30 to 30 degrees)
            if -30 <= angle_deg <= 30 and distance < self.safe_distance:
                front_obstacle = True
                
            # Left obstacle detection (30 to 90 degrees)
            if 30 <= angle_deg <= 90 and distance < self.safe_distance * 1.2:
                left_obstacle = True
                
            # Right obstacle detection (-90 to -30 degrees)
            if -90 <= angle_deg <= -30 and distance < self.safe_distance * 1.2:
                right_obstacle = True
        
        # Update obstacle state
        self.obstacle_detected = front_obstacle
        
        # If in avoidance mode, check if we can return to normal navigation
        if self.obstacle_avoidance_mode and not front_obstacle:
            # No obstacle in front, can return to normal navigation
            if (self.obstacle_avoidance_start_time is not None and 
                time.time() - self.obstacle_avoidance_start_time > 2.0):
                self.obstacle_avoidance_mode = False
                self.avoidance_direction_changes = 0
                self.get_logger().info("Obstacle cleared, returning to normal navigation")

    # Service Handlers
    def handle_activate_robot(self, request, response):
        self.get_logger().info("Activate SM service called!")

        if self.current_pose is None:
            self.get_logger().warn("Cannot activate state machine — no odometry received yet.")
            response.success = False
            response.message = "No odometry received yet."
            return response

        
        if not self.activate_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('activate service not available.')
            response.success = False
            response.message = "Activate service not available."
            return response

        self.get_logger().info("Calling activate service to activate robot...")
        activate_request = Activate.Request()
        self.activate_future = self.activate_client.call_async(activate_request)
        self.activate_future.add_done_callback(self.activation_response_callback)

        response.success = True
        response.message = 'Activation request sent to robot.'
        return response

    def activation_response_callback(self, future):
        
        try:
            response = future.result()
            if response.success:
                self.get_logger().info("Robot activated successfully via activation server")
                self.state = 'GET_GOAL'
                self.get_logger().info("State machine state set to GET_GOAL")
            else:
                self.get_logger().error(f"Failed to activate robot: {response.message}")
        except Exception as e:
            self.get_logger().error(f'Activation service call failed: {str(e)}')

    def handle_deactivate_robot(self, request, response):
        
        if not self.deactivate_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('deactivate service not available.')
            response.success = False
            response.message = "Deactivate service not available."
            return response

        self.get_logger().info("Calling deactivate service to deactivate robot...")
        deactivate_request = Deactivate.Request()
        deactivate_future = self.deactivate_client.call_async(deactivate_request)
        
        
        start_time = time.time()
        while not deactivate_future.done():
            if time.time() - start_time > 5.0:  
                self.get_logger().warn("Deactivate service call timeout")
                break
            rclpy.spin_once(self, timeout_sec=0.1)

        if deactivate_future.done():
            try:
                deactivate_response = deactivate_future.result()
                if deactivate_response.success:
                    self.get_logger().info(f"Robot deactivated: {deactivate_response.message}")
                else:
                    self.get_logger().error(f"Failed to deactivate robot: {deactivate_response.message}")
            except Exception as e:
                self.get_logger().error(f"Exception in deactivate service: {str(e)}")

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
        """Improved goal reachability check"""
        if self.current_goal is None:
            self.get_logger().warn("No current goal.")
            return False

        if self.current_pose is None:
            self.get_logger().warn("No current pose.")
            return False

        if self.map_data is None:
            self.get_logger().warn("No map data.")
            return True  # If no map data, assume goal is reachable

        try:
            goal_map = self.map_data.info
            # Convert goal coordinates to map coordinates
            goal_x = int((self.current_goal[0] - goal_map.origin.position.x) / goal_map.resolution)
            goal_y = int((self.current_goal[1] - goal_map.origin.position.y) / goal_map.resolution)
            
            # Check if coordinates are within map bounds
            if (goal_x < 0 or goal_x >= goal_map.width or 
                goal_y < 0 or goal_y >= goal_map.height):
                self.get_logger().warn(f"Goal coordinates out of map bounds: ({goal_x}, {goal_y})")
                return False
            
            goal_idx = goal_y * goal_map.width + goal_x
            
            if goal_idx >= len(self.map_data.data):
                self.get_logger().warn(f"Goal index out of range: {goal_idx}")
                return False

            # Check goal point and surrounding area
            cell_value = self.map_data.data[goal_idx]
            
            # Typically, 0 means free, 100 means occupied, -1 means unknown
            if cell_value == 100:  # Goal is on obstacle
                self.get_logger().warn(f"Goal is in obstacle (cell value: {cell_value})")
                return False
            elif cell_value == -1:  # Goal is in unknown area
                self.get_logger().info("Goal is in unknown area, assuming reachable")
                return True
            else:  # Goal is in free space
                self.get_logger().info(f"Goal is in free space (cell value: {cell_value})")
                return True
                
        except Exception as e:
            self.get_logger().error(f"Error checking goal reachability: {str(e)}")
            return True  # If error occurs, assume goal is reachable

    def deactivate_robot(self):
        if not self.deactivate_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('deactivate service not available.')
            return

        deactivate_request = Deactivate.Request()
        deactivate_future = self.deactivate_client.call_async(deactivate_request)
        
        
        start_time = time.time()
        while not deactivate_future.done():
            if time.time() - start_time > 5.0: 
                self.get_logger().warn("Deactivate service call timeout")
                break
            rclpy.spin_once(self, timeout_sec=0.1)

        if deactivate_future.done():
            try:
                response = deactivate_future.result()
                if response.success:
                    self.get_logger().info(f"Robot deactivated: {response.message}")
                else:
                    self.get_logger().error(f"Failed to deactivate robot: {response.message}")
            except Exception as e:
                self.get_logger().error(f"Exception in deactivate service: {str(e)}")

        self.publish_zero_velocity()

    def get_best_avoidance_direction(self):
        """Determine the best direction to avoid obstacles based on lidar data"""
        if self.scan_data is None:
            return 'right'  # Default to right if no data
        
        ranges = self.scan_data.ranges
        num_ranges = len(ranges)
        
        # Analyze left and right sides
        left_ranges = ranges[:num_ranges//3]
        right_ranges = ranges[2*num_ranges//3:]
        
        # Filter out invalid readings
        left_valid = [r for r in left_ranges if not (math.isinf(r) or math.isnan(r))]
        right_valid = [r for r in right_ranges if not (math.isinf(r) or math.isnan(r))]
        
        # Calculate average distances
        left_avg = sum(left_valid) / len(left_valid) if left_valid else 0
        right_avg = sum(right_valid) / len(right_valid) if right_valid else 0
        
        # Choose direction with more space
        if left_avg > right_avg and left_avg > self.safe_distance:
            return 'left'
        else:
            return 'right'

    def obstacle_avoidance_behavior(self):
        """Improved obstacle avoidance behavior"""
        velocity = Twist()
        
        if self.obstacle_avoidance_start_time is None:
            self.obstacle_avoidance_start_time = time.time()
            # Determine the best direction to avoid
            self.last_obstacle_side = self.get_best_avoidance_direction()
            self.get_logger().info(f"Starting avoidance to the {self.last_obstacle_side}")
        
        # Calculate time in avoidance mode
        avoidance_time = time.time() - self.obstacle_avoidance_start_time
        
        # If stuck in avoidance for too long, try recovery
        if avoidance_time > self.avoidance_duration:
            self.get_logger().warn("Avoidance taking too long, entering recovery mode")
            self.recovery_mode = True
            self.recovery_start_time = time.time()
            self.last_recovery_pose = self.current_pose
            self.obstacle_avoidance_mode = False
            return self.recovery_behavior()
        
        # Execute avoidance based on chosen direction
        if self.last_obstacle_side == 'right':
            # Turn left and move slightly backward
            velocity.linear.x = -0.1
            velocity.angular.z = 0.8
        else:
            # Turn right and move slightly backward
            velocity.linear.x = -0.1
            velocity.angular.z = -0.8
            
        return velocity

    def recovery_behavior(self):
        """Recovery behavior when robot is stuck between obstacles"""
        velocity = Twist()
        
        if self.recovery_start_time is None:
            self.recovery_start_time = time.time()
            self.last_recovery_pose = self.current_pose
            self.get_logger().info("Starting recovery behavior")
        
        recovery_time = time.time() - self.recovery_start_time
        
        # If recovery takes too long, give up and request new goal
        if recovery_time > self.recovery_duration:
            self.get_logger().warn("Recovery failed, requesting new goal")
            self.recovery_mode = False
            self.publish_zero_velocity()
            return 'FAILED'
        
        # Check if we've moved significantly during recovery
        if self.last_recovery_pose and self.current_pose:
            dx = self.current_pose[0] - self.last_recovery_pose[0]
            dy = self.current_pose[1] - self.last_recovery_pose[1]
            distance_moved = math.sqrt(dx**2 + dy**2)
            
            # If we've moved enough, try to resume navigation
            if distance_moved > 0.5 and recovery_time > 3.0:
                self.get_logger().info("Recovery successful, resuming navigation")
                self.recovery_mode = False
                self.obstacle_avoidance_mode = False
                return 'RECOVERED'
        
        # Execute recovery: move backward and turn
        if recovery_time < 2.0:
            # First phase: move straight back
            velocity.linear.x = -0.3
            velocity.angular.z = 0.0
        elif recovery_time < 5.0:
            # Second phase: turn in place
            velocity.linear.x = 0.0
            velocity.angular.z = 0.5
        else:
            # Third phase: move forward while turning
            velocity.linear.x = 0.2
            velocity.angular.z = 0.3
            
        return velocity

    def navigate_to_goal(self):
        """Improved navigation function with better obstacle handling"""
        if self.current_goal is None or self.current_pose is None:
            return None
            
        dx = self.current_goal[0] - self.current_pose[0]
        dy = self.current_goal[1] - self.current_pose[1]
        distance = np.sqrt(dx**2 + dy**2)
        
        # Check if goal is reached
        if distance < 0.15:  # Goal tolerance
            self.get_logger().info(f"Reached goal! Distance: {distance:.2f}")
            self.publish_zero_velocity()
            return 'REACHED'
            
        # If in recovery mode, handle that first
        if self.recovery_mode:
            result = self.recovery_behavior()
            if result == 'FAILED':
                return 'FAILED'
            elif result == 'RECOVERED':
                # Continue with normal navigation
                pass
            else:
                return result
            
        # If obstacle detected and not already avoiding, start avoidance
        if self.obstacle_detected and not self.obstacle_avoidance_mode:
            self.get_logger().warn("Obstacle detected! Starting avoidance behavior")
            self.obstacle_avoidance_mode = True
            self.obstacle_avoidance_start_time = None
            
        # If in avoidance mode, execute avoidance behavior
        if self.obstacle_avoidance_mode:
            return self.obstacle_avoidance_behavior()
            
        # Normal navigation
        velocity = Twist()
        
        # Calculate target direction
        q = self.current_orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y**2 + q.z**2)
        self.current_yaw = np.arctan2(siny_cosp, cosy_cosp)

        angle = np.arctan2(dy, dx)
        angular_error = angle - self.current_yaw
        angular_error = (angular_error + np.pi) % (2 * np.pi) - np.pi

        # Adjust speed based on lidar data
        safe_speed = 0.3  # Default safe speed
        
        if self.scan_data:
            # Check minimum distance in front area
            front_ranges = self.scan_data.ranges[len(self.scan_data.ranges)//3:2*len(self.scan_data.ranges)//3]
            valid_ranges = [r for r in front_ranges if not (math.isinf(r) or math.isnan(r))]
            if valid_ranges:
                min_front_distance = min(valid_ranges)
                # Adjust speed based on front obstacle distance
                if min_front_distance < 0.5:
                    safe_speed = 0.1
                elif min_front_distance < 1.0:
                    safe_speed = 0.2
        
        # Set linear and angular velocity
        if abs(angular_error) < 0.2:  # Well aligned
            velocity.linear.x = min(safe_speed, distance * 0.5)
        elif abs(angular_error) < 0.5:  # Moderately aligned
            velocity.linear.x = min(safe_speed * 0.7, distance * 0.3)
        else:  # Need significant turning
            velocity.linear.x = 0.0
            
        # Angular velocity control with smoothing
        velocity.angular.z = np.clip(angular_error * 1.5, -0.8, 0.8)
        
        return velocity

    # Async callback for get_goal response
    def goal_response_callback(self, future):
        try:
            response = future.result()

            # Detect end of goal list
            if response.goal_x == float('inf') or response.goal_y == float('inf'):
                self.get_logger().info("No more goals. Deactivating robot.")
                self.deactivate_robot()
                self.state = 'INACTIVE'
                return

            goal = (response.goal_x, response.goal_y)
            self.get_logger().info(f'Goal received: {goal}')
            self.current_goal = goal

            # Reset states
            self.get_logger().info("Moving to goal with improved obstacle avoidance.")
            self.start_time = time.time()
            self.last_distance = None
            self.stuck_check_start_time = None
            self.stuck_check_initial_distance = None
            self.obstacle_avoidance_mode = False
            self.obstacle_detected = False
            self.recovery_mode = False
            self.avoidance_direction_changes = 0
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

            # Use improved navigation function
            result = self.navigate_to_goal()
            
            if result == 'REACHED':
                # Goal reached, check validity
                self.state = 'CHECK_GOAL_VALIDITY'
                return
            elif result == 'FAILED':
                # Navigation failed, request new goal
                self.get_logger().warn("Navigation failed, requesting new goal")
                self.publish_zero_velocity()
                self.state = 'GET_GOAL'
                return
            elif isinstance(result, Twist):
                # Publish calculated velocity
                self.cmd_vel_pub.publish(result)
                
                # Log navigation info
                dx = self.current_goal[0] - self.current_pose[0]
                dy = self.current_goal[1] - self.current_pose[1]
                distance = np.sqrt(dx**2 + dy**2)
                
                if self.recovery_mode:
                    self.get_logger().info(f"RECOVERY: lin_x={result.linear.x:.2f}, ang_z={result.angular.z:.2f}, dist={distance:.2f}")
                elif self.obstacle_avoidance_mode:
                    self.get_logger().info(f"AVOIDING: lin_x={result.linear.x:.2f}, ang_z={result.angular.z:.2f}, dist={distance:.2f}")
                else:
                    self.get_logger().info(f"NAVIGATING: lin_x={result.linear.x:.2f}, ang_z={result.angular.z:.2f}, dist={distance:.2f}")

            # Check timeout
            if time.time() - self.start_time > 120:  # 2 minute timeout
                self.get_logger().warn('Timeout while trying to reach goal.')
                self.publish_zero_velocity()
                self.state = 'GET_GOAL'
                return

        elif self.state == 'CHECK_GOAL_VALIDITY':
            # Check if the goal we reached is valid/reachable
            if self.goal_reachable():
                self.get_logger().info('Goal reached successfully and is valid.')
                self.state = 'GET_GOAL'  # Request next goal
            else:
                self.get_logger().warn('Goal is in obstacle or unreachable. Requesting new goal.')
                self.state = 'GET_GOAL'

def main(args=None):
    rclpy.init(args=args)
    node = SMStudentsNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()