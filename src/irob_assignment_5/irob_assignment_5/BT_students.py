import rclpy
from rclpy.node import Node
import py_trees

from irob_interfaces.srv import GetGoal, Activate, Deactivate
from geometry_msgs.msg import Twist, PointStamped
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


class CheckObstacle(py_trees.behaviour.Behaviour):
    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        
    def update(self):
        if self.node.should_avoid_obstacle():
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


class CheckGoalObstacle(py_trees.behaviour.Behaviour):
    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        
    def update(self):
        if self.node.is_goal_itself_obstacle():
            return py_trees.common.Status.SUCCESS
        return py_trees.common.Status.FAILURE


class AvoidObstacle(py_trees.behaviour.Behaviour):
    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        self.avoidance_start_time = None
        
    def initialise(self):
        self.avoidance_start_time = time.time()
        
    def update(self):
        # Check if we've been avoiding for too long (safety timeout)
        if time.time() - self.avoidance_start_time > 8.0:  # 8 second timeout
            self.node.get_logger().warn("Obstacle avoidance timeout - resuming navigation")
            return py_trees.common.Status.SUCCESS
            
        # Check if obstacle is still there
        if not self.node.should_avoid_obstacle():
            self.node.get_logger().info("Obstacle cleared, resuming navigation")
            return py_trees.common.Status.SUCCESS
            
        velocity = self.node.execute_coordinate_based_avoidance()
        self.node.cmd_vel_pub.publish(velocity)
        self.node.get_logger().info("Executing obstacle avoidance")
        return py_trees.common.Status.RUNNING


class NavigateToGoal(py_trees.behaviour.Behaviour):
    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        
    def update(self):
        # Check if new goal was detected from goal_point topic
        if self.node.new_goal_detected:
            self.node.get_logger().info("New goal detected from goal_point topic - switching to new goal!")
            self.node.publish_zero_velocity()
            self.node.new_goal_detected = False
            return py_trees.common.Status.FAILURE  # This will make BT go back to GetNewGoal
            
        if self.node.current_goal is None:
            self.node.get_logger().info("No goal available for navigation")
            return py_trees.common.Status.FAILURE
            
        if self.node.current_pose is None:
            self.node.get_logger().info("No pose available for navigation")
            return py_trees.common.Status.FAILURE
            
        # Calculate distance to goal
        dx = self.node.current_goal[0] - self.node.current_pose[0]
        dy = self.node.current_goal[1] - self.node.current_pose[1]
        distance = math.sqrt(dx**2 + dy**2)
        
        # Check if goal is reached (using 0.2m threshold as requested)
        if distance <= 0.05:
            self.node.get_logger().info("Final goal reached - deactivating robot")
            self.node.deactivate_robot()
            
            # If this was the last goal, deactivate the robot
            
            if distance < 0.2:
                self.node.get_logger().info(f"Goal reached! Distance: {distance:.2f}")
                self.node.publish_zero_velocity()
                self.node.current_goal = None
            
            return py_trees.common.Status.SUCCESS
        
        # Use the improved navigation
        velocity = self.node.navigate_to_goal()
        if isinstance(velocity, Twist):
            self.node.cmd_vel_pub.publish(velocity)
            self.node.get_logger().info(f"Navigating to goal: lin_x={velocity.linear.x:.2f}, ang_z={velocity.angular.z:.2f}, dist={distance:.2f}")
            return py_trees.common.Status.RUNNING
        else:
            self.node.get_logger().warn("Navigation returned unexpected result")
            return py_trees.common.Status.FAILURE


class GetNewGoal(py_trees.behaviour.Behaviour):
    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        self.goal_requested = False
        self.future = None
        
    def initialise(self):
        self.goal_requested = False
        self.future = None
        
    def update(self):
        # If we already have a goal (possibly from goal_point topic) and no new goal detected, keep it
        if self.node.current_goal is not None and not self.node.new_goal_detected:
            return py_trees.common.Status.SUCCESS
            
        if not self.goal_requested:
            if not self.node.goal_client.wait_for_service(timeout_sec=1.0):
                self.node.get_logger().warn("Goal service not available")
                return py_trees.common.Status.FAILURE
            
            self.node.get_logger().info("Requesting new goal from goal server...")
            request = GetGoal.Request()
            self.future = self.node.goal_client.call_async(request)
            self.goal_requested = True
            return py_trees.common.Status.RUNNING
        
        if self.future is not None and self.future.done():
            try:
                response = self.future.result()
                if response.goal_x != float('inf') and response.goal_y != float('inf'):
                    self.node.current_goal = (response.goal_x, response.goal_y)
                    self.node.get_logger().info(f"New goal received: {self.node.current_goal}")
                    self.goal_requested = False
                    return py_trees.common.Status.SUCCESS
                else:
                    self.node.get_logger().info("No more goals available")
                    self.goal_requested = False
                    return py_trees.common.Status.FAILURE
            except Exception as e:
                self.node.get_logger().error(f"Error getting goal: {e}")
                self.goal_requested = False
                return py_trees.common.Status.FAILURE
        
        return py_trees.common.Status.RUNNING


class HandleGoalAsObstacle(py_trees.behaviour.Behaviour):
    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        
    def update(self):
        self.node.get_logger().warn("Goal itself is detected as obstacle - requesting new goal")
        self.node.current_goal = None
        self.node.publish_zero_velocity()
        return py_trees.common.Status.SUCCESS


class DeactivateRobot(py_trees.behaviour.Behaviour):
    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        self.deactivation_requested = False
        self.future = None
        
    def initialise(self):
        self.deactivation_requested = False
        self.future = None
        
    def update(self):
        if not self.deactivation_requested:
            if not self.node.deactivate_client.wait_for_service(timeout_sec=1.0):
                self.node.get_logger().warn("Deactivate service not available")
                return py_trees.common.Status.FAILURE
            
            self.node.get_logger().info("Sending deactivation request...")
            request = Deactivate.Request()
            self.future = self.node.deactivate_client.call_async(request)
            self.deactivation_requested = True
            return py_trees.common.Status.RUNNING
        
        if self.future is not None and self.future.done():
            try:
                response = self.future.result()
                self.node.get_logger().info("Robot successfully deactivated")
                self.node.active = False
                self.deactivation_requested = False
                return py_trees.common.Status.SUCCESS
            except Exception as e:
                self.node.get_logger().error(f"Error deactivating robot: {e}")
                self.deactivation_requested = False
                return py_trees.common.Status.FAILURE
        
        return py_trees.common.Status.RUNNING


class CheckFinalGoalReached(py_trees.behaviour.Behaviour):
    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        
    def update(self):
        # Check if we received the last goal and don't have a current goal
        if self.node.last_goal_received and self.node.current_goal is None:
            self.node.get_logger().info("Final goal reached - should deactivate")
            return py_trees.common.Status.SUCCESS
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
        
        #Subscribe to goal_point topic to detect new goals
        self.goal_point_sub = self.create_subscription(PointStamped, 'goal_point', self.goal_point_callback, 10)

        # Internal state
        self.current_pose = None
        self.current_orientation = None        
        self.current_goal = None
        self.current_yaw = None
        self.active = False
        self.scan_data = None
        self.last_goal_received = False  # Track if we received the final goal
        
        # Track goal changes from goal_point topic
        self.new_goal_detected = False
        self.last_goal_from_topic = None
        self.goal_change_threshold = 0.01  # Minimum change to consider it a new goal

        # Coordinate-based obstacle avoidance parameters
        self.obstacle_detected = False
        self.obstacle_avoidance_mode = False
        self.obstacle_avoidance_start_time = None
        self.safe_distance = 0.2
        self.avoidance_direction_changes = 0
        self.detected_obstacles = []
        self.current_blocking_obstacle = None
        self.obstacle_detection_range = 0.6
        self.obstacle_avoidance_distance = 0.3

        # Create Behavior Tree
        self.create_behavior_tree()
        
        # Timer for BT ticking
        self.timer = self.create_timer(0.1, self.tick_bt)

        self.get_logger().info("BT Students Node with Obstacle Avoidance ready!")
        self.get_logger().info("Waiting for activation from activation server...")
        self.get_logger().info("Will react to new goals published on /goal_point topic")

    # Callback for goal_point topic
    def goal_point_callback(self, msg):
        new_goal = (msg.point.x, msg.point.y)
        
        # Check if this is a new goal (different from current goal)
        if self.current_goal is None:
            # First goal received
            self.current_goal = new_goal
            self.last_goal_from_topic = new_goal
            self.get_logger().info(f"Initial goal received from goal_point: {new_goal}")
        else:
            # Check if goal has changed significantly
            dx = new_goal[0] - self.current_goal[0]
            dy = new_goal[1] - self.current_goal[1]
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > self.goal_change_threshold:
                self.get_logger().info(f"New goal detected from goal_point topic: {new_goal} (was {self.current_goal})")
                self.current_goal = new_goal
                self.new_goal_detected = True
                self.last_goal_from_topic = new_goal

    def create_behavior_tree(self):
        """Create behavior tree that properly separates obstacle avoidance from goal-as-obstacle detection"""
        
        # Root selector: active vs inactive
        root = py_trees.composites.Selector("Root", memory=False)
        
        # Check activation condition
        check_activation = CheckActivation("CheckActivation", self)
        
        # Inactive behavior (do nothing)
        inactive_behavior = py_trees.behaviours.Running("Inactive")
        
        # Active behavior
        active_behavior = py_trees.composites.Sequence("ActiveBehavior", memory=False)
        
        # Get goal first
        get_goal_behavior = GetNewGoal("GetGoal", self)
        
        # Main navigation behavior
        main_navigation = py_trees.composites.Selector("MainNavigation", memory=False)
        
        # First priority: Check if goal itself is an obstacle (only when close to goal)
        goal_obstacle_handler = py_trees.composites.Sequence("GoalObstacleHandler", memory=False)
        check_goal_obstacle = CheckGoalObstacle("CheckGoalObstacle", self)
        handle_goal_obstacle = HandleGoalAsObstacle("HandleGoalAsObstacle", self)
        goal_obstacle_handler.add_children([check_goal_obstacle, handle_goal_obstacle])
        
        # Second priority: Regular obstacle avoidance
        obstacle_avoider = py_trees.composites.Sequence("ObstacleAvoider", memory=False)
        check_obstacle = CheckObstacle("CheckObstacle", self)
        avoid_obstacle = AvoidObstacle("AvoidObstacle", self)
        obstacle_avoider.add_children([check_obstacle, avoid_obstacle])
        
        # Third priority: Normal navigation
        navigate_to_goal = NavigateToGoal("NavigateToGoal", self)
        
        # Build the main navigation selector in correct priority order
        main_navigation.add_children([goal_obstacle_handler, obstacle_avoider, navigate_to_goal])
        
        # Check if we need to deactivate after final goal
        deactivate_after_final_goal = py_trees.composites.Sequence("DeactivateAfterFinal", memory=False)
        check_final_goal = CheckFinalGoalReached("CheckFinalGoalReached", self)
        deactivate_robot = DeactivateRobot("DeactivateRobot", self)
        deactivate_after_final_goal.add_children([check_final_goal, deactivate_robot])
        
        # Active behavior sequence - now includes deactivation check
        active_behavior_sequence = py_trees.composites.Selector("ActiveBehaviorSequence", memory=False)
        active_behavior_sequence.add_children([deactivate_after_final_goal, main_navigation])
        
        active_behavior.add_children([get_goal_behavior, active_behavior_sequence])
        
        # Use a repeater to continuously run the active behavior
        repeat_active = py_trees.decorators.Repeat(
            name="RepeatActive",
            child=active_behavior,
            num_success=None
        )
        
        # Build the tree
        active_sequence = py_trees.composites.Sequence("ActiveSequence", memory=False)
        active_sequence.add_children([check_activation, repeat_active])
        
        root.add_children([active_sequence, inactive_behavior])
        
        self.behaviour_tree = py_trees.trees.BehaviourTree(root)
        
        # Display the tree structure
        self.get_logger().info("Behavior Tree with Final Goal Deactivation:")
        print(py_trees.display.unicode_tree(root))

    def tick_bt(self):
        if hasattr(self, 'behaviour_tree'):
            self.behaviour_tree.tick()

    def deactivate_robot(self):
        if self.deactivate_client.wait_for_service(timeout_sec=1.0):
            request = Deactivate.Request()
            future = self.deactivate_client.call_async(request)
            # We don't wait for result here as it's handled in the behavior
        else:
            self.get_logger().warn("Deactivate service not available")

    def is_goal_itself_obstacle(self):
        if self.current_goal is None or not self.detected_obstacles:
            return False
        
        # Calculate distance to goal
        goal_dx = self.current_goal[0] - self.current_pose[0]
        goal_dy = self.current_goal[1] - self.current_pose[1]
        goal_distance = math.sqrt(goal_dx**2 + goal_dy**2)
        
        # Only check for goal-as-obstacle when we're close to the goal
        if goal_distance > 0.3:  # Goal is far away - don't treat as obstacle
            return False
        
        # Find obstacles that are very close to the goal coordinates
        for obstacle in self.detected_obstacles:
            obstacle_to_goal_distance = math.sqrt(
                (obstacle['x'] - self.current_goal[0])**2 + 
                (obstacle['y'] - self.current_goal[1])**2
            )
            
            # If obstacle is very close to goal coordinates and we're close to goal
            if obstacle_to_goal_distance < 0.15:
                self.get_logger().warn(f"Goal itself detected as obstacle! Goal distance: {goal_distance:.2f}, obs-to-goal: {obstacle_to_goal_distance:.2f}")
                return True
        
        return False

    def should_avoid_obstacle(self):
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
        
        # Check if obstacle is actually the goal (skip if it's the goal)
        obstacle_to_goal_distance = math.sqrt(
            (closest_obstacle['x'] - self.current_goal[0])**2 + 
            (closest_obstacle['y'] - self.current_goal[1])**2
        )
        
        # If this is likely the goal itself and we're close to goal, don't avoid
        goal_distance = math.sqrt(goal_dx**2 + goal_dy**2)
        if obstacle_to_goal_distance < 0.15 and goal_distance < 0.3:
            return False  # Let goal_obstacle_handler handle this
        
        # Normal obstacle avoidance
        if closest_obstacle['distance'] < self.obstacle_avoidance_distance:
            self.current_blocking_obstacle = closest_obstacle
            return True
        
        return False

    def odom_callback(self, msg):
        self.current_pose = (msg.pose.pose.position.x, msg.pose.pose.position.y)
        self.current_orientation = msg.pose.pose.orientation
        if self.current_orientation:
            q = self.current_orientation
            siny_cosp = 2 * (q.w * q.z + q.x * q.y)
            cosy_cosp = 1 - 2 * (q.y**2 + q.z**2)
            self.current_yaw = np.arctan2(siny_cosp, cosy_cosp)

    def active_callback(self, msg):
        old_active = self.active
        self.active = msg.data
        
        if self.active and not old_active:
            self.get_logger().info("Robot ACTIVATED via activation server - Starting Behavior Tree!")
            self.current_goal = None
        elif not self.active and old_active:
            self.get_logger().info("Robot DEACTIVATED via activation server - Stopping Behavior Tree!")
            self.publish_zero_velocity()
            self.current_goal = None

    def scan_callback(self, msg):
        self.scan_data = msg
        self.detect_obstacles()

    def detect_obstacles(self):
        if self.scan_data is None or self.current_pose is None:
            return
        
        ranges = self.scan_data.ranges
        angle_min = self.scan_data.angle_min
        angle_increment = self.scan_data.angle_increment
        
        self.detected_obstacles = []
        
        robot_x, robot_y = self.current_pose
        robot_yaw = self.current_yaw
        
        for i, distance in enumerate(ranges):
            if math.isinf(distance) or math.isnan(distance) or distance > self.obstacle_detection_range:
                continue
                
            scan_angle = angle_min + i * angle_increment
            world_angle = robot_yaw + scan_angle
            
            obstacle_x = robot_x + distance * math.cos(world_angle)
            obstacle_y = robot_y + distance * math.sin(world_angle)
            
            if distance < self.obstacle_detection_range:
                self.detected_obstacles.append({
                    'x': obstacle_x,
                    'y': obstacle_y,
                    'distance': distance,
                    'angle': scan_angle,
                    'world_angle': world_angle
                })

    def calculate_avoidance_direction(self):
        if self.current_blocking_obstacle is None:
            return 0
        
        robot_to_goal = [self.current_goal[0] - self.current_pose[0], 
                        self.current_goal[1] - self.current_pose[1]]
        robot_to_obstacle = [self.current_blocking_obstacle['x'] - self.current_pose[0],
                            self.current_blocking_obstacle['y'] - self.current_pose[1]]
        
        cross_product = (robot_to_goal[0] * robot_to_obstacle[1] - 
                        robot_to_goal[1] * robot_to_obstacle[0])
        
        if cross_product > 0:
            return -1  # Turn right
        else:
            return 1   # Turn left
        
    def execute_coordinate_based_avoidance(self):
        velocity = Twist()
        
        if self.current_blocking_obstacle is None:
            return velocity
        
        avoidance_direction = self.calculate_avoidance_direction()
        
        velocity.linear.x = 0.1
        velocity.angular.z = 0.4 * avoidance_direction
        
        if avoidance_direction == -1:
            self.get_logger().info("Avoiding obstacle: turning right") 
        else: 
            self.get_logger().info("Avoiding obstacle: turning left")
        
        return velocity

    def navigate_to_goal(self):
        """Improved navigation function"""
        if self.current_goal is None or self.current_pose is None:
            return None
            
        dx = self.current_goal[0] - self.current_pose[0]
        dy = self.current_goal[1] - self.current_pose[1]
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance < 0.05:
            self.get_logger().info(f"Reached goal! Distance: {distance:.2f}")
            self.publish_zero_velocity()
            return 'REACHED'

        velocity = Twist()
        
        q = self.current_orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y**2 + q.z**2)
        self.current_yaw = np.arctan2(siny_cosp, cosy_cosp)

        angle = np.arctan2(dy, dx)
        angular_error = angle - self.current_yaw
        angular_error = (angular_error + np.pi) % (2 * np.pi) - np.pi

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