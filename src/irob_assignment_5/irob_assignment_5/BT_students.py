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


class BTStudentsNode(Node):
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

        # NEW: Coordinate-based obstacle avoidance parameters
        self.obstacle_detected = False
        self.obstacle_avoidance_mode = False
        self.obstacle_avoidance_start_time = None
        self.safe_distance = 0.5  # Safe distance from obstacles
        self.avoidance_direction_changes = 0  # Track direction changes to prevent oscillation
        self.detected_obstacles = []  # List of obstacles with coordinates
        self.current_blocking_obstacle = None  # The obstacle currently blocking our path
        self.obstacle_detection_range = 1.0  # meters
        self.obstacle_avoidance_distance = 0.8  # meter
        # Recovery behavior parameters
        self.recovery_mode = False
        self.recovery_start_time = None
        self.recovery_duration = 8.0  # Maximum recovery time
        self.last_recovery_pose = None  # Track position during recovery

        # Goal unreachable detection
        self.goal_unreachable = False
        self.last_progress_time = None
        self.min_progress_distance = 0.1  # Minimum progress in 10 seconds
        self.progress_check_interval = 10.0  # Check progress every 10 seconds

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
        # Update current yaw when we get new odometry
        if self.current_orientation:
            q = self.current_orientation
            siny_cosp = 2 * (q.w * q.z + q.x * q.y)
            cosy_cosp = 1 - 2 * (q.y**2 + q.z**2)
            self.current_yaw = np.arctan2(siny_cosp, cosy_cosp)

    def active_callback(self, msg):
        self.active = msg.data

    def scan_callback(self, msg):
        self.scan_data = msg
        # Real-time obstacle detection using coordinate-based method
        self.detect_obstacles()

    def map_callback(self, msg):
        self.map_data = msg

    # NEW: Coordinate-based obstacle detection methods
    def detect_obstacles(self):
        """Use lidar data to detect obstacles and calculate their world coordinates"""
        if self.scan_data is None or self.current_pose is None:
            return
        
        ranges = self.scan_data.ranges
        angle_min = self.scan_data.angle_min
        angle_increment = self.scan_data.angle_increment
        
        # Clear previous obstacles
        self.detected_obstacles = []
        
        # Get robot's current position and orientation
        robot_x, robot_y = self.current_pose
        robot_yaw = self.current_yaw
        
        for i, distance in enumerate(ranges):
            if math.isinf(distance) or math.isnan(distance) or distance > self.obstacle_detection_range:
                continue
                
            # Calculate angle relative to robot
            scan_angle = angle_min + i * angle_increment
            # Convert to world angle (relative to global frame)
            world_angle = robot_yaw + scan_angle
            
            # Calculate obstacle coordinates in world frame
            obstacle_x = robot_x + distance * math.cos(world_angle)
            obstacle_y = robot_y + distance * math.sin(world_angle)
            
            # Only consider obstacles within our detection range
            if distance < self.obstacle_detection_range:
                self.detected_obstacles.append({
                    'x': obstacle_x,
                    'y': obstacle_y,
                    'distance': distance,
                    'angle': scan_angle,  # Relative to robot front
                    'world_angle': world_angle  # Relative to global frame
                })

    def should_avoid_obstacle(self):
        """Check if we need to avoid obstacles based on goal direction"""
        if self.current_goal is None or not self.detected_obstacles:
            return False
        
        # Calculate angle to goal
        goal_dx = self.current_goal[0] - self.current_pose[0]
        goal_dy = self.current_goal[1] - self.current_pose[1]
        goal_angle = math.atan2(goal_dy, goal_dx)
        
        # Find obstacles that are in the direction of the goal
        blocking_obstacles = []
        for obstacle in self.detected_obstacles:
            # Calculate angle from robot to obstacle
            obstacle_angle = math.atan2(obstacle['y'] - self.current_pose[1], 
                                    obstacle['x'] - self.current_pose[0])
            
            # Check if obstacle is in the path to goal (within ±30 degrees)
            angle_diff = abs(goal_angle - obstacle_angle)
            angle_diff = min(angle_diff, 2*math.pi - angle_diff)  # Handle wrap-around
            
            if angle_diff < math.pi/6:  # 30 degrees
                blocking_obstacles.append(obstacle)
        
        if not blocking_obstacles:
            return False
        
        # Find the closest blocking obstacle
        closest_obstacle = min(blocking_obstacles, key=lambda o: o['distance'])
        
        # Check if obstacle is actually the goal
        obstacle_to_goal_distance = math.sqrt(
            (closest_obstacle['x'] - self.current_goal[0])**2 + 
            (closest_obstacle['y'] - self.current_goal[1])**2
        )
        
        # If the "obstacle" is very close to the goal coordinates, it's probably the goal itself
        if obstacle_to_goal_distance < 0.3:  # 30cm threshold
            self.get_logger().info("Obstacle is likely the goal itself, proceeding")
            return False
        
        # Check if obstacle is close enough to require avoidance
        if closest_obstacle['distance'] < self.obstacle_avoidance_distance:
            self.current_blocking_obstacle = closest_obstacle
            return True
        
        return False

    def calculate_avoidance_direction(self):
        """Calculate the best direction to avoid the blocking obstacle"""
        if self.current_blocking_obstacle is None:
            return 0  # No avoidance needed
        
        # Calculate vectors
        robot_to_goal = [self.current_goal[0] - self.current_pose[0], 
                        self.current_goal[1] - self.current_pose[1]]
        robot_to_obstacle = [self.current_blocking_obstacle['x'] - self.current_pose[0],
                            self.current_blocking_obstacle['y'] - self.current_pose[1]]
        
        # Calculate cross product to determine left/right
        cross_product = (robot_to_goal[0] * robot_to_obstacle[1] - 
                        robot_to_goal[1] * robot_to_obstacle[0])
        
        # Positive cross product means obstacle is to the left, so turn right
        # Negative cross product means obstacle is to the right, so turn left
        if cross_product > 0:
            return -1  # Turn right (clockwise)
        else:
            return 1   # Turn left (counter-clockwise)
        
    def execute_coordinate_based_avoidance(self):
        """Execute obstacle avoidance using coordinate-based strategy"""
        velocity = Twist()
        
        if self.current_blocking_obstacle is None:
            return velocity
        
        avoidance_direction = self.calculate_avoidance_direction()
        
        # For differential drive robots, use angular velocity to turn
        # and limited forward motion
        velocity.linear.x = 0.1  # Slow forward motion
        velocity.angular.z = 0.3 * avoidance_direction  # Turn away from obstacle
        
        self.get_logger().info(f"Avoiding obstacle: turning {'right' if avoidance_direction == -1 else 'left'}")
        
        return velocity

    # Service Handlers
    def handle_activate_robot(self, request, response):
        self.get_logger().info("Activate SM service called!")

        if self.current_pose is None:
            self.get_logger().warn("Cannot activate state machine — no odometry received yet.")
            response.success = False
            response.message = "No odometry received yet."
            return response

        
        if not self.activate_client.wait_for_service(timeout_sec=2.0):
            self.get_logger().warn('activate service not available.')
            response.success = False
            response.message = "Activate service not available."
            return response

        self.get_logger().info("Calling activate service to activate robot...")
        activate_request = Activate.Request()
        self.activate_future = self.create_client(Activate, 'activate').call_async(activate_request)
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
        
        if not self.deactivate_client.wait_for_service(timeout_sec=2.0):
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
        
    def is_goal_reachable(self, distance_to_goal):
        """Check if goal is reachable using laser scan data"""
        if self.scan_data is None or self.current_goal is None or self.current_pose is None:
            return True  # Can't check, assume reachable
            
        # Calculate the angle to the goal
        dx = self.current_goal[0] - self.current_pose[0]
        dy = self.current_goal[1] - self.current_pose[1]
        goal_angle = math.atan2(dy, dx)
        
        # Get robot's current orientation
        q = self.current_orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y**2 + q.z**2)
        robot_yaw = math.atan2(siny_cosp, cosy_cosp)
        
        # Calculate relative angle to goal in robot's frame
        relative_angle = goal_angle - robot_yaw
        relative_angle = (relative_angle + math.pi) % (2 * math.pi) - math.pi  # Normalize to [-pi, pi]
        
        # Convert to degrees
        relative_angle_deg = math.degrees(relative_angle)
        
        # Get laser scan parameters
        angle_min = math.degrees(self.scan_data.angle_min)
        angle_max = math.degrees(self.scan_data.angle_max)
        angle_increment = math.degrees(self.scan_data.angle_increment)
        
        # Calculate laser scan index for the goal direction
        goal_index = int((relative_angle_deg - angle_min) / angle_increment)
        
        # Check if goal index is within valid range
        if goal_index < 0 or goal_index >= len(self.scan_data.ranges):
            return True  # Goal outside laser scan range, assume reachable
        
        # Get distance to obstacle in goal direction
        obstacle_distance = self.scan_data.ranges[goal_index]
        
        # Also check a small cone around the goal direction
        cone_width = 5  # degrees
        cone_indices = int(cone_width / angle_increment)
        
        min_obstacle_distance = float('inf')
        for i in range(max(0, goal_index - cone_indices), min(len(self.scan_data.ranges), goal_index + cone_indices + 1)):
            dist = self.scan_data.ranges[i]
            if not (math.isinf(dist) or math.isnan(dist)):
                min_obstacle_distance = min(min_obstacle_distance, dist)
        
        # If there's an obstacle closer than the goal, and we're close to the goal, it's unreachable
        if (min_obstacle_distance < distance_to_goal + 0.1 and  # Obstacle is closer than goal + small margin
            distance_to_goal < 0.4):  # Only check when we're close to goal
            self.get_logger().warn(f"Goal unreachable: obstacle at {min_obstacle_distance:.2f}m, goal at {distance_to_goal:.2f}m")
            return False
            
        return True

    def check_progress_toward_goal(self):
        #Check stuck
        if self.current_goal is None or self.current_pose is None:
            return True  # Can't check progress, assume we're making progress
            
        # Calculate current distance to goal
        dx = self.current_goal[0] - self.current_pose[0]
        dy = self.current_goal[1] - self.current_pose[1]
        current_distance = math.sqrt(dx**2 + dy**2)
        
        # Initialize progress tracking
        if self.last_progress_time is None:
            self.last_progress_time = time.time()
            self.last_distance = current_distance
            return True
            
        # Check if enough time has passed to evaluate progress
        if time.time() - self.last_progress_time < self.progress_check_interval:
            return True
            
        # Check if we've made sufficient progress
        progress = self.last_distance - current_distance
        self.get_logger().info(f"Progress check: moved {progress:.2f}m in {self.progress_check_interval}s")
        
        # Reset progress tracking
        self.last_progress_time = time.time()
        self.last_distance = current_distance
        
        # If we haven't made sufficient progress, goal might be unreachable
        if progress < self.min_progress_distance:
            self.get_logger().warn(f"Insufficient progress ({progress:.2f}m), goal might be unreachable")
            return False
            
        return True

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
            self.get_logger().warn("Recovery failed, goal might be unreachable")
            self.recovery_mode = False
            self.publish_zero_velocity()
            return 'UNREACHABLE'
        
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
            velocity.angular.z = 0.3
        else:
            # Third phase: move forward while turning
            velocity.linear.x = 0.2
            velocity.angular.z = 0.3
            
        return velocity

    def navigate_to_goal(self):
        """Improved navigation function with coordinate-based obstacle handling"""
        if self.current_goal is None or self.current_pose is None:
            return None
            
        dx = self.current_goal[0] - self.current_pose[0]
        dy = self.current_goal[1] - self.current_pose[1]
        distance = np.sqrt(dx**2 + dy**2)
        
        # Check if goal is reached
        if distance < 0.05:  # Goal tolerance
            self.get_logger().info(f"Reached goal! Distance: {distance:.2f}")
            self.publish_zero_velocity()
            return 'REACHED'

        # Check if goal is unreachable using laser scan when we're close
        elif distance < 0.4:
            # Use laser scan to check if goal is blocked by obstacle
            if not self.is_goal_reachable(distance):
                self.get_logger().warn("Goal is blocked by obstacle, requesting new goal")
                return 'IN_OBSTACLE'
            
        # Check if we're making progress toward goal
        if not self.check_progress_toward_goal():
            self.get_logger().warn("Not making sufficient progress, goal might be unreachable")
            return 'UNREACHABLE'
            
        # If in recovery mode, handle that first
        if self.recovery_mode:
            result = self.recovery_behavior()
            if result == 'UNREACHABLE':
                return 'UNREACHABLE'
            elif result == 'RECOVERED':
                # Continue with normal navigation
                pass
            else:
                return result
            
        # FIXED: Use the coordinate-based obstacle detection
        avoid_obstacle = self.should_avoid_obstacle()
        
        if avoid_obstacle and not self.obstacle_avoidance_mode:
            self.get_logger().warn("Obstacle detected in path! Starting coordinate-based avoidance")
            self.obstacle_avoidance_mode = True
            self.obstacle_avoidance_start_time = time.time()
            
        # If in avoidance mode, let the state machine handle coordinate-based avoidance
        # We'll return to normal navigation here, and the state machine will handle avoidance
        if self.obstacle_avoidance_mode:
            # Check if we should exit avoidance mode
            if not avoid_obstacle:
                if (self.obstacle_avoidance_start_time is not None and 
                    time.time() - self.obstacle_avoidance_start_time > 2.0):
                    self.get_logger().info("Path cleared, returning to normal navigation")
                    self.obstacle_avoidance_mode = False
                    self.avoidance_direction_changes = 0
            else:
                # Continue avoidance - but let state machine handle this
                if self.obstacle_avoidance_start_time is not None:
                    avoidance_time = time.time() - self.obstacle_avoidance_start_time
                    if avoidance_time > 15.0:  # Avoidance timeout
                        self.get_logger().warn("Avoidance taking too long, goal might be unreachable")
                        return 'UNREACHABLE'
                
                # Return normal navigation - the state machine will override with avoidance
                pass
            
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
                    safe_speed = 0.2
                elif min_front_distance < 1.0:
                    safe_speed = 0.4
        
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
            self.get_logger().info("Moving to goal. Will check if goal is valid after reaching it.")
            self.start_time = time.time()
            self.last_distance = None
            self.stuck_check_start_time = None
            self.stuck_check_initial_distance = None
            self.obstacle_avoidance_mode = False
            self.obstacle_detected = False
            self.recovery_mode = False
            self.avoidance_direction_changes = 0
            self.last_progress_time = None
            self.detected_obstacles = []  # Clear previous obstacles
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

            # Calculate current yaw from orientation (needed for coordinate-based avoidance)
            q = self.current_orientation
            siny_cosp = 2 * (q.w * q.z + q.x * q.y)
            cosy_cosp = 1 - 2 * (q.y**2 + q.z**2)
            self.current_yaw = np.arctan2(siny_cosp, cosy_cosp)

            # Detect obstacles and their world coordinates
            self.detect_obstacles()
            
            # Check if we need to avoid obstacles using coordinate-based approach
            if self.should_avoid_obstacle():
                # Use coordinate-based obstacle avoidance
                velocity = self.execute_coordinate_based_avoidance()
                avoidance_status = "COORD_AVOIDANCE"
            else:
                # Use normal navigation (your existing navigate_to_goal function)
                result = self.navigate_to_goal()
                
                if result == 'REACHED':
                    # Goal reached and validated, request next goal
                    self.get_logger().info('Goal reached successfully and is valid.')
                    self.state = 'GET_GOAL'  # Request next goal
                    return
                elif result == 'IN_OBSTACLE':
                    # Goal is in obstacle, request new goal
                    self.get_logger().warn('Goal is blocked by obstacle. Requesting new goal.')
                    self.state = 'GET_GOAL'
                    return
                elif result == 'UNREACHABLE':
                    # Goal is unreachable, request new goal
                    self.get_logger().warn("Goal is unreachable, requesting new goal")
                    self.publish_zero_velocity()
                    self.state = 'GET_GOAL'
                    return
                elif isinstance(result, Twist):
                    velocity = result
                    avoidance_status = "NORMAL"
                else:
                    # Fallback to zero velocity if something unexpected happens
                    velocity = Twist()
                    avoidance_status = "STOPPED"

            # Publish the velocity command
            self.cmd_vel_pub.publish(velocity)
            
            # Log navigation info
            dx = self.current_goal[0] - self.current_pose[0]
            dy = self.current_goal[1] - self.current_pose[1]
            distance = np.sqrt(dx**2 + dy**2)
            
            if avoidance_status == "COORD_AVOIDANCE":
                if self.current_blocking_obstacle:
                    self.get_logger().info(f"COORD_AVOID: lin_x={velocity.linear.x:.2f}, ang_z={velocity.angular.z:.2f}, "
                                        f"dist={distance:.2f}, obs=({self.current_blocking_obstacle['x']:.2f}, "
                                        f"{self.current_blocking_obstacle['y']:.2f})")
                else:
                    self.get_logger().info(f"COORD_AVOID: lin_x={velocity.linear.x:.2f}, ang_z={velocity.angular.z:.2f}, dist={distance:.2f}")
            elif avoidance_status == "NORMAL":
                if self.recovery_mode:
                    self.get_logger().info(f"RECOVERY: lin_x={velocity.linear.x:.2f}, ang_z={velocity.angular.z:.2f}, dist={distance:.2f}")
                elif self.obstacle_avoidance_mode:
                    self.get_logger().info(f"AVOIDING: lin_x={velocity.linear.x:.2f}, ang_z={velocity.angular.z:.2f}, dist={distance:.2f}")
                else:
                    self.get_logger().info(f"NAVIGATING: lin_x={velocity.linear.x:.2f}, ang_z={velocity.angular.z:.2f}, dist={distance:.2f}")
            else:
                self.get_logger().info(f"STOPPED: dist={distance:.2f}")

            # Check timeout
            if time.time() - self.start_time > 120:  # 2 minute timeout
                self.get_logger().warn('Timeout while trying to reach goal.')
                self.publish_zero_velocity()
                self.state = 'GET_GOAL'
                return

def main(args=None):
    rclpy.init(args=args)
    node = BTStudentsNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()