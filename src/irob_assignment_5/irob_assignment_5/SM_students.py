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

        # Improved obstacle avoidance parameters
        self.obstacle_detected = False
        self.obstacle_avoidance_mode = False
        self.obstacle_avoidance_start_time = None
        
        # Navigation parameters - adjusted for better performance
        self.safe_distance = 0.4  # Increased for large chassis
        self.critical_distance = 0.2  # Increased for large chassis
        self.robot_radius = 0.1  # Increased robot radius estimate
        self.avoidance_duration = 20.0  # Increased avoidance time
        self.avoidance_stuck_threshold = 8  # Increased threshold
        
        # Collision and stuck detection
        self.collision_count = 0
        self.max_collisions = 5  # Maximum collisions before giving up
        self.last_collision_time = None
        self.collision_cooldown = 2.0  # Time between collision counts
        
        # Recovery behavior parameters
        self.recovery_mode = False
        self.recovery_start_time = None
        self.recovery_duration = 20.0  # Increased recovery time
        self.last_recovery_pose = None

        # Goal unreachable detection - more lenient
        self.goal_unreachable = False
        self.last_progress_time = None
        self.min_progress_distance = 0.15  # Increased minimum progress
        self.progress_check_interval = 20.0  # Increased progress check interval

        # For tracking async goal request
        self.goal_future = None
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
        self.detect_obstacles()

    def map_callback(self, msg):
        self.map_data = msg

    def detect_obstacles(self):
        """Use lidar data to detect obstacles - improved for large chassis"""
        if self.scan_data is None:
            return
            
        ranges = self.scan_data.ranges
        angle_min = self.scan_data.angle_min
        angle_increment = self.scan_data.angle_increment
        
        front_obstacle = False
        left_obstacle = False
        right_obstacle = False
        critical_obstacle = False
        side_obstacle_near = False  # For detecting obstacles during turns
        
        front_min_distance = float('inf')
        left_min_distance = float('inf')
        right_min_distance = float('inf')
        side_min_distance = float('inf')
        
        for i, distance in enumerate(ranges):
            if math.isinf(distance) or math.isnan(distance):
                continue
                
            angle = angle_min + i * angle_increment
            angle_deg = math.degrees(angle)
            
            # Front obstacle detection (-70 to 70 degrees) - wider for better turn detection
            if -70 <= angle_deg <= 70:
                if distance < front_min_distance:
                    front_min_distance = distance
                if distance < self.safe_distance:
                    front_obstacle = True
                if distance < self.critical_distance:
                    critical_obstacle = True
                    
            # Left obstacle detection (70 to 130 degrees)
            if 70 <= angle_deg <= 130:
                if distance < left_min_distance:
                    left_min_distance = distance
                if distance < self.safe_distance * 1.2:
                    left_obstacle = True
                if distance < self.critical_distance * 1.5:  # More sensitive for turns
                    side_obstacle_near = True
                    
            # Right obstacle detection (-130 to -70 degrees)
            if -130 <= angle_deg <= -70:
                if distance < right_min_distance:
                    right_min_distance = distance
                if distance < self.safe_distance * 1.2:
                    right_obstacle = True
                if distance < self.critical_distance * 1.5:  # More sensitive for turns
                    side_obstacle_near = True
        
        self.obstacle_detected = front_obstacle or critical_obstacle
        self.critical_obstacle = critical_obstacle
        self.side_obstacle_near = side_obstacle_near
        
        self.current_obstacle_info = {
            'front': front_min_distance,
            'left': left_min_distance,
            'right': right_min_distance,
            'front_obstacle': front_obstacle,
            'left_obstacle': left_obstacle,
            'right_obstacle': right_obstacle,
            'critical': critical_obstacle,
            'side_near': side_obstacle_near
        }

    def detect_collision(self):
        """Detect if robot is colliding with obstacles"""
        if not hasattr(self, 'current_obstacle_info'):
            return False
            
        # Check if any obstacle is very close (potential collision)
        front_distance = self.current_obstacle_info['front']
        left_distance = self.current_obstacle_info['left'] 
        right_distance = self.current_obstacle_info['right']
        
        collision_threshold = 0.2  # Very close distance indicating collision
        
        # Check if we should count this as a collision
        if (front_distance < collision_threshold or 
            left_distance < collision_threshold or 
            right_distance < collision_threshold):
            
            # Apply cooldown to avoid counting the same collision multiple times
            current_time = time.time()
            if (self.last_collision_time is None or 
                current_time - self.last_collision_time > self.collision_cooldown):
                
                self.collision_count += 1
                self.last_collision_time = current_time
                self.get_logger().warn(f"Collision detected! Count: {self.collision_count}/{self.max_collisions}")
                return True
                
        return False

    def calculate_goal_relative_angle(self):
        """Calculate the angle to goal relative to robot's current orientation"""
        if self.current_goal is None or self.current_pose is None:
            return 0.0
            
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
        
        # Normalize to [-pi, pi]
        relative_angle = (relative_angle + math.pi) % (2 * math.pi) - math.pi
        
        return relative_angle

    # Service Handlers (remain the same)
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
        
    def is_goal_reachable_by_laserscan(self, distance_to_goal):
        """Check if goal is reachable using laser scan data"""
        if self.scan_data is None or self.current_goal is None or self.current_pose is None:
            return True
            
        goal_relative_angle = self.calculate_goal_relative_angle()
        
        # Get laser scan parameters
        angle_min = self.scan_data.angle_min
        angle_increment = self.scan_data.angle_increment
        
        # Calculate laser scan index for the goal direction
        goal_index = int((goal_relative_angle - angle_min) / angle_increment)
        
        # Check if goal index is within valid range
        if goal_index < 0 or goal_index >= len(self.scan_data.ranges):
            return True
        
        # Get distance to obstacle in goal direction
        obstacle_distance = self.scan_data.ranges[goal_index]
        
        # Check a small cone around the goal direction
        cone_width = 20  # Increased cone width for large chassis
        cone_indices = int(cone_width / math.degrees(angle_increment))
        
        min_obstacle_distance = float('inf')
        for i in range(max(0, goal_index - cone_indices), min(len(self.scan_data.ranges), goal_index + cone_indices + 1)):
            dist = self.scan_data.ranges[i]
            if not (math.isinf(dist) or math.isnan(dist)):
                min_obstacle_distance = min(min_obstacle_distance, dist)
        
        clearance_needed = self.robot_radius + 0.2  # Increased clearance
        if (min_obstacle_distance < distance_to_goal + clearance_needed and
            distance_to_goal < 0.8):  # Increased check distance
            self.get_logger().warn(f"Goal unreachable: obstacle at {min_obstacle_distance:.2f}m, goal at {distance_to_goal:.2f}m")
            return False
            
        return True

    def check_progress_toward_goal(self):
        if self.current_goal is None or self.current_pose is None:
            return True
            
        dx = self.current_goal[0] - self.current_pose[0]
        dy = self.current_goal[1] - self.current_pose[1]
        current_distance = math.sqrt(dx**2 + dy**2)
        
        if self.last_progress_time is None:
            self.last_progress_time = time.time()
            self.last_distance = current_distance
            return True
            
        if time.time() - self.last_progress_time < self.progress_check_interval:
            return True
            
        progress = self.last_distance - current_distance
        
        # More lenient progress requirements
        if self.obstacle_avoidance_mode or self.recovery_mode:
            required_progress = self.min_progress_distance * 0.2  # Only 20% required in difficult situations
            self.get_logger().info(f"Progress check (in avoidance/recovery): moved {progress:.2f}m in {self.progress_check_interval}s")
        else:
            required_progress = self.min_progress_distance
            self.get_logger().info(f"Progress check: moved {progress:.2f}m in {self.progress_check_interval}s")
        
        self.last_progress_time = time.time()
        self.last_distance = current_distance
        
        if progress < required_progress:
            self.get_logger().warn(f"Insufficient progress ({progress:.2f}m < {required_progress:.2f}m), goal might be unreachable")
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

    def get_best_navigation_direction(self):
        """Calculate the best navigation direction - improved for large chassis"""
        if self.scan_data is None or self.current_goal is None or self.current_pose is None:
            return 0.0
        
        # Calculate goal direction relative to robot
        goal_relative_angle = self.calculate_goal_relative_angle()
        
        # Get laser scan data
        angle_min = self.scan_data.angle_min
        angle_increment = self.scan_data.angle_increment
        ranges = self.scan_data.ranges
        
        # Check if goal is behind the robot
        goal_behind = abs(goal_relative_angle) > math.pi / 2
        
        # Analyze directions - full 360 degrees
        directions = []
        
        for angle_deg in range(-180, 181, 15):
            angle_rad = math.radians(angle_deg)
            
            # Calculate laser index for this direction
            laser_index = int((angle_rad - angle_min) / angle_increment)
            laser_index = laser_index % len(ranges) if len(ranges) > 0 else 0
                
            # Get distance in this direction
            distance = ranges[laser_index] if 0 <= laser_index < len(ranges) else 10.0
            if math.isinf(distance) or math.isnan(distance):
                distance = 10.0
                
            # Calculate score for this direction
            distance_score = min(distance / 5.0, 1.0)
            
            # Alignment score
            alignment_score = 1.0 - (abs(angle_rad - goal_relative_angle) / math.pi)
            
            # Penalize directions that would cause turning collisions for large chassis
            turning_penalty = 1.0
            if abs(angle_rad) > math.radians(30):  # Turning directions
                # Check side obstacles more carefully during turns
                if hasattr(self, 'current_obstacle_info') and self.current_obstacle_info['side_near']:
                    if (angle_rad > 0 and self.current_obstacle_info['left'] < self.safe_distance * 1.5) or \
                       (angle_rad < 0 and self.current_obstacle_info['right'] < self.safe_distance * 1.5):
                        turning_penalty = 0.3  # Heavy penalty for turning towards close side obstacles
            
            # Weight the scores
            if goal_behind:
                if abs(angle_rad) < math.radians(30):
                    total_score = (distance_score * 0.3 + alignment_score * 0.7) * turning_penalty
                else:
                    total_score = (distance_score * 0.4 + alignment_score * 0.6) * turning_penalty
            else:
                if distance < self.critical_distance:
                    total_score = (distance_score * 0.8 + alignment_score * 0.2) * turning_penalty
                elif distance < self.safe_distance:
                    total_score = (distance_score * 0.6 + alignment_score * 0.4) * turning_penalty
                else:
                    total_score = (distance_score * 0.3 + alignment_score * 0.7) * turning_penalty
                
            directions.append({
                'angle': angle_rad,
                'distance': distance,
                'score': total_score
            })
        
        # Find the best direction
        if not directions:
            return goal_relative_angle
            
        best_direction = max(directions, key=lambda x: x['score'])
        
        # Special handling for goals behind the robot
        if goal_behind and abs(best_direction['angle']) < math.radians(30):
            turning_directions = [d for d in directions if abs(d['angle']) > math.radians(45)]
            if turning_directions:
                best_turning = max(turning_directions, key=lambda x: x['score'])
                self.get_logger().info(f"Goal behind: choosing turn {math.degrees(best_turning['angle']):.1f}° over forward {math.degrees(best_direction['angle']):.1f}°")
                best_direction = best_turning
        
        goal_deg = math.degrees(goal_relative_angle)
        best_deg = math.degrees(best_direction['angle'])
        self.get_logger().info(f"Goal at {goal_deg:.1f}°, Best direction: {best_deg:.1f}°, "
                              f"distance: {best_direction['distance']:.2f}m, "
                              f"score: {best_direction['score']:.2f}")
        
        return best_direction['angle']

    def obstacle_avoidance_behavior(self):
        """Improved obstacle avoidance behavior - prevents turning collisions"""
        velocity = Twist()
        
        if self.obstacle_avoidance_start_time is None:
            self.obstacle_avoidance_start_time = time.time()
            self.get_logger().info("Starting improved obstacle avoidance")
        
        avoidance_time = time.time() - self.obstacle_avoidance_start_time
        
        # Check collision count before giving up
        if self.collision_count >= self.max_collisions:
            self.get_logger().warn(f"Too many collisions ({self.collision_count}), goal might be unreachable")
            return 'UNREACHABLE'
            
        if avoidance_time > self.avoidance_duration:
            self.get_logger().warn(f"Avoidance taking too long ({avoidance_time:.1f}s), goal might be unreachable")
            return 'UNREACHABLE'
        
        # Get the best navigation direction
        best_direction = self.get_best_navigation_direction()
        
        # Check if goal is behind us
        goal_relative_angle = self.calculate_goal_relative_angle()
        goal_behind = abs(goal_relative_angle) > math.pi / 2
        
        if hasattr(self, 'current_obstacle_info'):
            front_distance = self.current_obstacle_info['front']
            left_distance = self.current_obstacle_info['left']
            right_distance = self.current_obstacle_info['right']
            side_near = self.current_obstacle_info['side_near']
            
            min_side_distance = min(left_distance, right_distance)
            closest_obstacle = min(front_distance, min_side_distance)
            
            # Detect collisions
            self.detect_collision()
            
            if goal_behind:
                # When goal is behind and side obstacles are near, be more careful
                if side_near and abs(best_direction) > math.radians(30):
                    # Move backward first to create space for turning
                    velocity.linear.x = -0.1
                    velocity.angular.z = np.clip(best_direction * 0.5, -0.4, 0.4)
                elif closest_obstacle < self.critical_distance:
                    velocity.linear.x = -0.15
                    velocity.angular.z = np.clip(best_direction * 1.2, -1.0, 1.0)
                else:
                    velocity.linear.x = 0.0
                    velocity.angular.z = np.clip(best_direction * 1.0, -0.8, 0.8)
            else:
                # Normal behavior for goals in front
                if closest_obstacle < self.critical_distance:
                    velocity.linear.x = -0.2
                    velocity.angular.z = np.clip(best_direction * 1.5, -1.2, 1.2)
                elif closest_obstacle < self.safe_distance:
                    # When turning with side obstacles near, reduce angular speed
                    if side_near and abs(best_direction) > math.radians(20):
                        velocity.linear.x = 0.05
                        velocity.angular.z = np.clip(best_direction * 0.8, -0.6, 0.6)
                    else:
                        velocity.linear.x = 0.1
                        velocity.angular.z = np.clip(best_direction * 1.2, -1.0, 1.0)
                else:
                    velocity.linear.x = 0.2
                    velocity.angular.z = np.clip(best_direction * 1.0, -0.8, 0.8)
        else:
            if goal_behind:
                velocity.linear.x = 0.0
                velocity.angular.z = np.clip(best_direction * 1.0, -0.8, 0.8)
            else:
                velocity.linear.x = 0.1
                velocity.angular.z = np.clip(best_direction * 1.2, -1.0, 1.0)
            
        return velocity

    def recovery_behavior(self):
        """Improved recovery behavior - prevents turning collisions"""
        velocity = Twist()
        
        if self.recovery_start_time is None:
            self.recovery_start_time = time.time()
            self.last_recovery_pose = self.current_pose
            self.get_logger().info("Starting recovery behavior")
        
        recovery_time = time.time() - self.recovery_start_time
        
        if recovery_time > self.recovery_duration:
            self.get_logger().warn("Recovery failed, goal might be unreachable")
            self.recovery_mode = False
            self.publish_zero_velocity()
            return 'UNREACHABLE'
        
        if self.last_recovery_pose and self.current_pose:
            dx = self.current_pose[0] - self.last_recovery_pose[0]
            dy = self.current_pose[1] - self.last_recovery_pose[1]
            distance_moved = math.sqrt(dx**2 + dy**2)
            
            if distance_moved > 0.5 and recovery_time > 4.0:  # Increased required movement
                self.get_logger().info("Recovery successful, resuming navigation")
                self.recovery_mode = False
                self.obstacle_avoidance_mode = False
                # Reset collision count after successful recovery
                self.collision_count = 0
                return 'RECOVERED'
        
        # Check goal position during recovery
        goal_relative_angle = self.calculate_goal_relative_angle()
        goal_behind = abs(goal_relative_angle) > math.pi / 2
        
        # Check side obstacles during recovery
        side_near = hasattr(self, 'current_obstacle_info') and self.current_obstacle_info['side_near']
        
        if recovery_time < 4.0:  # Longer backward phase
            velocity.linear.x = -0.2
            # Gentle turning while backing up to avoid scraping
            if side_near:
                velocity.angular.z = 0.1  # Gentle turn away from obstacles
            else:
                velocity.angular.z = 0.0
        elif recovery_time < 12.0:  # Longer turning phase
            # During turning phase, be careful about side obstacles
            if side_near:
                # If side obstacles are near, turn slowly
                velocity.linear.x = 0.0
                velocity.angular.z = np.clip(goal_relative_angle * 0.4, -0.3, 0.3)
            else:
                velocity.linear.x = 0.0
                if goal_behind:
                    velocity.angular.z = np.clip(goal_relative_angle * 0.6, -0.5, 0.5)
                else:
                    velocity.angular.z = 0.4
        else:
            # Final phase: move forward while turning gently
            velocity.linear.x = 0.15
            velocity.angular.z = 0.2
            
        return velocity

    def navigate_to_goal(self):
        """Improved navigation function with collision prevention"""
        if self.current_goal is None or self.current_pose is None:
            return None
            
        dx = self.current_goal[0] - self.current_pose[0]
        dy = self.current_goal[1] - self.current_pose[1]
        distance = np.sqrt(dx**2 + dy**2)
        
        # Check if goal is reached
        if distance < 0.05:  # Increased tolerance for large chassis
            self.get_logger().info(f"Reached goal! Distance: {distance:.2f}")
            self.publish_zero_velocity()
            # Reset collision count when goal is reached
            self.collision_count = 0
            return 'REACHED'

        # Use laser scan to check if goal is reachable
        elif distance < 0.8:  # Increased check distance
            if not self.is_goal_reachable_by_laserscan(distance):
                self.get_logger().warn("Goal is blocked by obstacle, requesting new goal")
                return 'IN_OBSTACLE'
            
        # Check collision count - if too many collisions, give up
        if self.collision_count >= self.max_collisions:
            self.get_logger().warn(f"Too many collisions ({self.collision_count}), requesting new goal")
            return 'UNREACHABLE'
            
        # Check if we're making progress toward goal
        if not self.check_progress_toward_goal():
            if not self.recovery_mode and not self.obstacle_avoidance_mode:
                self.get_logger().warn("Not making sufficient progress, trying recovery")
                self.recovery_mode = True
                self.recovery_start_time = None
                return self.recovery_behavior()
            
        # If in recovery mode, handle that first
        if self.recovery_mode:
            result = self.recovery_behavior()
            if result == 'UNREACHABLE':
                return 'UNREACHABLE'
            elif result == 'RECOVERED':
                self.last_progress_time = None
                pass
            else:
                return result
            
        # If obstacle detected and not already avoiding, start avoidance
        if (self.obstacle_detected or self.critical_obstacle) and not self.obstacle_avoidance_mode:
            self.get_logger().warn("Obstacle detected! Starting improved avoidance behavior")
            self.obstacle_avoidance_mode = True
            self.obstacle_avoidance_start_time = None
            self.last_progress_time = None
            
        # If in avoidance mode, execute improved avoidance behavior
        if self.obstacle_avoidance_mode:
            result = self.obstacle_avoidance_behavior()
            if result == 'UNREACHABLE':
                return 'UNREACHABLE'
            else:
                return result
            
        # Normal navigation
        velocity = Twist()
        
        # Get the best navigation direction
        best_direction = self.get_best_navigation_direction()
        
        # Check if goal is behind us
        goal_relative_angle = self.calculate_goal_relative_angle()
        goal_behind = abs(goal_relative_angle) > math.pi / 2
        
        # Check side obstacles
        side_near = hasattr(self, 'current_obstacle_info') and self.current_obstacle_info['side_near']
        
        # Adjust speed based on obstacle distances and goal position
        safe_speed = 0.3
        
        if hasattr(self, 'current_obstacle_info'):
            front_distance = self.current_obstacle_info['front']
            if front_distance < 1.2:  # Increased threshold
                safe_speed = 0.15
            elif front_distance < 2.5:  # Increased threshold
                safe_speed = 0.25
        
        # Set velocities based on best direction and obstacles
        if goal_behind:
            if abs(best_direction) < 0.3:
                velocity.linear.x = safe_speed * 0.3
            else:
                velocity.linear.x = 0.0
        else:
            # Reduce speed when turning near obstacles to prevent scraping
            if side_near and abs(best_direction) > math.radians(20):
                velocity.linear.x = safe_speed * 0.4
            elif abs(best_direction) < 0.3:
                velocity.linear.x = min(safe_speed, distance * 0.5)
            else:
                velocity.linear.x = safe_speed * 0.6
        
        # Reduce angular speed when near side obstacles to prevent scraping
        if side_near and abs(best_direction) > math.radians(20):
            velocity.angular.z = np.clip(best_direction * 0.8, -0.6, 0.6)
        else:
            velocity.angular.z = np.clip(best_direction * 1.0, -0.8, 0.8)
        
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

            # Reset states including collision count
            self.get_logger().info("Moving to goal with improved collision prevention.")
            self.start_time = time.time()
            self.last_distance = None
            self.stuck_check_start_time = None
            self.stuck_check_initial_distance = None
            self.obstacle_avoidance_mode = False
            self.obstacle_detected = False
            self.recovery_mode = False
            self.last_progress_time = None
            self.collision_count = 0
            self.last_collision_time = None
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

            if self.goal_future is None or self.goal_future.done():
                self.get_logger().info("Calling get_goal service asynchronously...")
                request = GetGoal.Request()
                self.goal_future = self.goal_client.call_async(request)
                self.goal_future.add_done_callback(self.goal_response_callback)

        elif self.state == 'GOTO_GOAL':
            if self.current_goal is None or self.current_pose is None:
                self.get_logger().warn("Cannot navigate - missing goal or pose")
                return

            result = self.navigate_to_goal()
            
            if result == 'REACHED':
                self.get_logger().info('Goal reached successfully and is valid.')
                self.state = 'GET_GOAL'
                return
            elif result == 'IN_OBSTACLE':
                self.get_logger().warn('Goal is blocked by obstacle. Requesting new goal.')
                self.state = 'GET_GOAL'
                return
            elif result == 'UNREACHABLE':
                self.get_logger().warn("Goal is unreachable, requesting new goal")
                self.publish_zero_velocity()
                self.state = 'GET_GOAL'
                return
            elif isinstance(result, Twist):
                self.cmd_vel_pub.publish(result)
                
                dx = self.current_goal[0] - self.current_pose[0]
                dy = self.current_goal[1] - self.current_pose[1]
                distance = np.sqrt(dx**2 + dy**2)
                
                if self.recovery_mode:
                    self.get_logger().info(f"RECOVERY: lin_x={result.linear.x:.2f}, ang_z={result.angular.z:.2f}, dist={distance:.2f}")
                elif self.obstacle_avoidance_mode:
                    self.get_logger().info(f"AVOIDING: lin_x={result.linear.x:.2f}, ang_z={result.angular.z:.2f}, dist={distance:.2f}")
                else:
                    self.get_logger().info(f"NAVIGATING: lin_x={result.linear.x:.2f}, ang_z={result.angular.z:.2f}, dist={distance:.2f}")

            if time.time() - self.start_time > 240:  # Increased timeout to 4 minutes
                self.get_logger().warn('Timeout while trying to reach goal.')
                self.publish_zero_velocity()
                self.state = 'GET_GOAL'
                return
def main(args=None):
    rclpy.init(args=args)
    node = SMStudentsNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()