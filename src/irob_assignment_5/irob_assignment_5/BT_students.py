import rclpy
from rclpy.node import Node
import py_trees

from irob_interfaces.srv import GetGoal, Activate, Deactivate
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool

import numpy as np
import time
import math


class CheckActivation(py_trees.behaviour.Behaviour):
    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        
    def update(self):
        if self.node.active:
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


class GetGoalAction(py_trees.behaviour.Behaviour):
    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        self.goal_future = None
        
    def initialise(self):
        self.node.get_logger().info("Requesting new goal...")
        request = GetGoal.Request()
        self.goal_future = self.node.goal_client.call_async(request)
        
    def update(self):
        if self.goal_future is None:
            return py_trees.common.Status.RUNNING
            
        if self.goal_future.done():
            try:
                response = self.goal_future.result()
                
                # Check for end of goals
                if response.goal_x == float('inf') or response.goal_y == float('inf'):
                    self.node.get_logger().info("No more goals")
                    return py_trees.common.Status.FAILURE
                
                goal = (response.goal_x, response.goal_y)
                self.node.current_goal = goal
                self.node.get_logger().info(f'Goal received: {goal}')
                
                # Reset navigation state
                self.node.start_time = time.time()
                self.node.obstacle_avoidance_mode = False
                self.node.recovery_mode = False
                self.node.collision_count = 0
                
                return py_trees.common.Status.SUCCESS
                
            except Exception as e:
                self.node.get_logger().error(f'Failed to get goal: {e}')
                return py_trees.common.Status.FAILURE
                
        return py_trees.common.Status.RUNNING


class CheckGoalReached(py_trees.behaviour.Behaviour):
    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        
    def update(self):
        if self.node.current_goal is None or self.node.current_pose is None:
            return py_trees.common.Status.FAILURE
            
        dx = self.node.current_goal[0] - self.node.current_pose[0]
        dy = self.node.current_goal[1] - self.node.current_pose[1]
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < 0.05:
            self.node.get_logger().info(f"Goal reached! Distance: {distance:.2f}")
            self.node.publish_zero_velocity()
            return py_trees.common.Status.SUCCESS
            
        return py_trees.common.Status.FAILURE


class CheckObstacle(py_trees.behaviour.Behaviour):
    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        
    def update(self):
        if self.node.should_avoid_obstacle():
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


class AvoidObstacleAction(py_trees.behaviour.Behaviour):
    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        
    def update(self):
        velocity = self.node.execute_coordinate_based_avoidance()
        self.node.cmd_vel_pub.publish(velocity)
        return py_trees.common.Status.RUNNING


class NavigateToGoalAction(py_trees.behaviour.Behaviour):
    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        
    def update(self):
        result = self.node.navigate_to_goal()
        if isinstance(result, Twist):
            self.node.cmd_vel_pub.publish(result)
            return py_trees.common.Status.RUNNING
        elif result == 'REACHED':
            return py_trees.common.Status.SUCCESS
        else:
            # If navigation fails, return failure to get new goal
            return py_trees.common.Status.FAILURE


class BTStudentsNode(Node):
    def __init__(self):
        super().__init__('bt_students_node')

        # Clients
        self.activate_client = self.create_client(Activate, 'activate')
        self.deactivate_client = self.create_client(Deactivate, 'deactivate')
        self.goal_client = self.create_client(GetGoal, 'get_goal')
        
        # Publisher
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Subscribers
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.active_sub = self.create_subscription(Bool, '/robot_active', self.active_callback, 10)

        # Services
        self.activate_sm_srv = self.create_service(Activate, 'activate_sm', self.handle_activate_robot)
        self.deactivate_sm_srv = self.create_service(Deactivate, 'deactivate_sm', self.handle_deactivate_robot)

        # Internal state - same as your state machine
        self.current_pose = None
        self.current_orientation = None        
        self.current_goal = None
        self.current_yaw = None
        self.active = False
        self.scan_data = None
        self.start_time = None 
        self.last_distance = None
        self.state = "INACTIVE"

        # Coordinate-based obstacle avoidance parameters
        self.obstacle_detected = False
        self.obstacle_avoidance_mode = False
        self.obstacle_avoidance_start_time = None
        self.safe_distance = 0.5
        self.avoidance_direction_changes = 0
        self.detected_obstacles = []
        self.current_blocking_obstacle = None
        self.obstacle_detection_range = 1.0
        self.obstacle_avoidance_distance = 0.8

        # Recovery behavior parameters
        self.recovery_mode = False
        self.recovery_start_time = None
        self.recovery_duration = 8.0
        self.last_recovery_pose = None

        # Goal unreachable detection
        self.goal_unreachable = False
        self.last_progress_time = None
        self.min_progress_distance = 0.1
        self.progress_check_interval = 10.0

        # For tracking async goal request
        self.goal_future = None
        self.activate_future = None

        # Create Behavior Tree
        self.create_behavior_tree()
        
        # Timer for BT ticking
        self.timer = self.create_timer(0.1, self.tick_bt)

        self.get_logger().info("BT_students_node ready with Behavior Tree.")

    def create_behavior_tree(self):
        """Create the main behavior tree"""
        
        # Main navigation sequence
        navigation_sequence = py_trees.composites.Sequence("NavigationSequence", memory=True)
        
        # Get goal action
        get_goal_behavior = GetGoalAction("GetGoal", self)
        
        # Navigation subtree - keeps running until goal is reached
        navigation_subtree = py_trees.composites.Selector("NavigateToGoal", memory=True)
        
        # Check if goal is reached (if yes, success and we get new goal)
        check_goal_reached = CheckGoalReached("CheckGoalReached", self)
        
        # Obstacle avoidance vs normal navigation
        obstacle_navigation_selector = py_trees.composites.Selector("ObstacleNavigation", memory=True)
        
        # Obstacle avoidance sequence
        obstacle_avoidance = py_trees.composites.Sequence("AvoidObstacle", memory=True)
        obstacle_avoidance.add_children([
            CheckObstacle("CheckObstacle", self),
            AvoidObstacleAction("AvoidObstacleAction", self)
        ])
        
        # Normal navigation
        normal_navigation = NavigateToGoalAction("NavigateToGoal", self)
        
        # Build the tree hierarchy
        obstacle_navigation_selector.add_children([obstacle_avoidance, normal_navigation])
        navigation_subtree.add_children([check_goal_reached, obstacle_navigation_selector])
        navigation_sequence.add_children([get_goal_behavior, navigation_subtree])
        
        # Root with activation check
        root = py_trees.composites.Selector("Root", memory=True)
        
        # Check activation condition
        check_activation = CheckActivation("CheckActivation", self)
        
        # Inactive behavior (do nothing)
        inactive_behavior = py_trees.behaviours.Success("Inactive")
        
        # Build final tree
        activation_sequence = py_trees.composites.Sequence("ActivationSequence", memory=True)
        activation_sequence.add_children([check_activation, navigation_sequence])
        
        root.add_children([activation_sequence, inactive_behavior])
        
        self.behaviour_tree = py_trees.trees.BehaviourTree(root)
        
        # Display the tree structure
        self.get_logger().info("Behavior Tree created:")
        print(py_trees.display.unicode_tree(root))

    def tick_bt(self):
        """Tick the behavior tree"""
        self.behaviour_tree.tick()

    # Callbacks - same as your state machine
    def odom_callback(self, msg):
        self.current_pose = (msg.pose.pose.position.x, msg.pose.pose.position.y)
        self.current_orientation = msg.pose.pose.orientation
        if self.current_orientation:
            q = self.current_orientation
            siny_cosp = 2 * (q.w * q.z + q.x * q.y)
            cosy_cosp = 1 - 2 * (q.y**2 + q.z**2)
            self.current_yaw = np.arctan2(siny_cosp, cosy_cosp)

    def active_callback(self, msg):
        self.active = msg.data

    def scan_callback(self, msg):
        self.scan_data = msg
        self.detect_obstacles()

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
                    'angle': scan_angle,
                    'world_angle': world_angle
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
            angle_diff = min(angle_diff, 2*math.pi - angle_diff)
            
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
        if obstacle_to_goal_distance < 0.3:
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
            return 0
        
        # Calculate vectors
        robot_to_goal = [self.current_goal[0] - self.current_pose[0], 
                        self.current_goal[1] - self.current_pose[1]]
        robot_to_obstacle = [self.current_blocking_obstacle['x'] - self.current_pose[0],
                            self.current_blocking_obstacle['y'] - self.current_pose[1]]
        
        # Calculate cross product to determine left/right
        cross_product = (robot_to_goal[0] * robot_to_obstacle[1] - 
                        robot_to_goal[1] * robot_to_obstacle[0])
        
        if cross_product > 0:
            return -1  # Turn right
        else:
            return 1   # Turn left
        
    def execute_coordinate_based_avoidance(self):
        """Execute obstacle avoidance using coordinate-based strategy"""
        velocity = Twist()
        
        if self.current_blocking_obstacle is None:
            return velocity
        
        avoidance_direction = self.calculate_avoidance_direction()
        
        velocity.linear.x = 0.1
        velocity.angular.z = 0.3 * avoidance_direction
        
        self.get_logger().info(f"Avoiding obstacle: turning {'right' if avoidance_direction == -1 else 'left'}")
        
        return velocity

    def navigate_to_goal(self):
        """Navigation function with coordinate-based obstacle handling"""
        if self.current_goal is None or self.current_pose is None:
            return None
            
        dx = self.current_goal[0] - self.current_pose[0]
        dy = self.current_goal[1] - self.current_pose[1]
        distance = np.sqrt(dx**2 + dy**2)
        
        # Check if goal is reached
        if distance < 0.05:
            self.get_logger().info(f"Reached goal! Distance: {distance:.2f}")
            self.publish_zero_velocity()
            return 'REACHED'

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
        safe_speed = 0.3
        
        if self.scan_data:
            front_ranges = self.scan_data.ranges[len(self.scan_data.ranges)//3:2*len(self.scan_data.ranges)//3]
            valid_ranges = [r for r in front_ranges if not (math.isinf(r) or math.isnan(r))]
            if valid_ranges:
                min_front_distance = min(valid_ranges)
                if min_front_distance < 0.5:
                    safe_speed = 0.2
                elif min_front_distance < 1.0:
                    safe_speed = 0.4
        
        # Set linear and angular velocity
        if abs(angular_error) < 0.2:
            velocity.linear.x = min(safe_speed, distance * 0.5)
        elif abs(angular_error) < 0.5:
            velocity.linear.x = min(safe_speed * 0.7, distance * 0.3)
        else:
            velocity.linear.x = 0.0
            
        velocity.angular.z = np.clip(angular_error * 1.5, -0.8, 0.8)
        
        return velocity

    def publish_zero_velocity(self):
        velocity = Twist()
        velocity.linear.x = 0.0
        velocity.angular.z = 0.0
        self.cmd_vel_pub.publish(velocity)

    # Service Handlers
    def handle_activate_robot(self, request, response):
        self.get_logger().info("Activate BT service called!")
        self.active = True
        response.success = True
        response.message = 'Behavior Tree activated.'
        return response

    def handle_deactivate_robot(self, request, response):
        self.get_logger().info("Deactivate BT service called!")
        self.active = False
        self.publish_zero_velocity()
        response.success = True
        response.message = 'Behavior Tree deactivated.'
        return response


def main(args=None):
    rclpy.init(args=args)
    node = BTStudentsNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()