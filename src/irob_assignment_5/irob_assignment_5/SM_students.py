#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from GetGoal.srv import GetGoal
from Activate.srv import Activate
from Deactivate.srv import Deactivate
from AtGoal.srv import AtGoal
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry, OccupancyGrid#get map without Laserscan
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool

import numpy as np
import time
#necessary imports here , follow basic Ros2 node stuff


#import necessary services below
#from Somewhere import XX{get goal}, {activtion service}, {deactivtion service}, {Check at Goal service} 

# IMPORT necessary messages, you need to use cmd_vel and more

# import necessary sensory messages if needed:

class SMStudentsNode(Node):
    def __init__(self):
        super().__init__('SM_students_node')

        #clients
        self.activate_client = self.create_client(Activate, 'activate')
        self.deactivate_client = self.create_client(Deactivate, 'deactivate')
        self.goal_client = self.create_client(GetGoal, 'get_goal')
        self.at_goal_client = self.create_client(AtGoal, 'at_goal')
        
        #publisher
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        #subscriber
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.active_sub = self.create_subscription(Bool, '/robot_active', self.active_callback, 10)

        #services
        self.activate_sm_srv = self.create_service(Activate, 'activate_sm', self.handle_activate_robot)
        self.deactivate_sm_srv = self.create_service(Deactivate, 'deactivate_sm', self.handle_deactivate_robot)

        #variables
        self.current_pose = None
        self.current_orientation = None        
        self.current_goal = None
        self.current_yaw = None
        self.active = False
        self.scan_data = None # not sure if we need it for E part
        self.start_time = None 
        self.last_distance = None
        self.map_data = None

        #state machine
        self.state = "INACTIVE"

        #add important initializations here
        self.get_logger().info("SM_students_node ready. Robot is inactive until activated.")

    def odom_callback(self, msg):
        self.current_pose = (msg.pose.pose.position.x, msg.pose.pose.position.y)
        self.current_orientation = msg.pose.pose.orientation

    def active_callback(self, msg):
        self.active = msg.data

    def scan_callback(self, msg):
        self.scan_data = msg

    def map_callback(self, msg):
        self.map_data = msg

    def handle_activate_robot(self, request, response):
        #Do some awesome stuff here!
        activate_response = self.activate_client.call(Activate.Request())
        self.get_logger().info(activate_response.message)
        self.state = 'GET_GOAL'
        response.success = True
        response.message = 'State machine activated.'
        return response    

    def handle_deactivate_robot(self, request, response):
        deactivate_response = self.deactivate_client.call(Deactivate.Request())
        self.get_logger().info(deactivate_response.message)
        #should we set 0 velocity by ourselves?
        self.state = 'INACTIVE'
        response.success = True
        response.message = 'State machine deactivated.'
        return response

    def publish_zero_velocity(self):
        #two vectors (vector3), linear and angular
        velocity = Twist()
        velocity.linear.x = 0.0
        velocity.angular.z = 0.0
        self.cmd_vel_pub.publish(velocity)

    def goal_reachable(self):
        if self.current_goal == None or current_pose == None:
            return False
        
        goal_map = self.map_data.info
        goal_x = (self.current_goal[0] - goal_map.origin.position.x) / goal_map.resolution
        goal_y = (self.current_goal[1] - goal_map.origin.position.y) / goal_map.resolution
        #index for 1D array
        goal_idx = int(goal_y * goal_map.width + goal_x)

        if goal_idx < 0 or goal_idx >= len(self.map_data.data):
            return False

        goal = self.map_data.data[goal_idx]
        if goal == 0:
            return True
        else:
            return False

#??? when shall we deactive the robot for E part? Once we reach the goal?
    def state_machine_callback(self):
        #inactive
        if self.state == 'INACTIVE' or self.active == False:
            return
        
        #get a goal / going to goal / checking if reached 
        if self.state == 'GET_GOAL':
            request = GetGoal.Request()
            response = self.goal_client.call(request)
            goal = (response.goal_x, response.goal_y)
            self.get_logger().info('Goal received: ')
            self.get_logger().info(goal)

            self.current_goal = goal

            # any other way to check?
            if self.goal_reachable():
                #initialize
                self.start_time = time.time()
                self.last_distance = None
                self.state = 'GOTO_GOAL'
            
            else:
                self.get_logger().warn('Not a reachable goal.')
        
        elif self.state == 'GOTO_GOAL':
            if self.current_goal == None or current_pose == None:
                return

            dx = current_goal[0] - current_pose[0]
            dy = current_goal[1] - current_pose[1]
            distance = np.sqrt(dx**2 + dy**2)
            if self.last_distance == None:
                self.last_distance = distance

            #checking timeout
            if time.time() - self.start_time > 60:
                self.get_logger().warn('Timeout: failed to reach goal')
                self.publish_zero_velocity()
                self.start_time = None
                self.state = "GET_GOAL"
                return

            #checking stuck
            if abs(distance - self.last_distance) < 0.01 and distance > 0.1:
                self.get_logger().warn('Stuck: failed to reach goal')
                self.publish_zero_velocity()
                self.start_time = None
                self.state = "GET_GOAL"
                return
            
            self.last_distance = distance
            #calculate yaw and angular error
            angle = np.arctan2(dy,dx)
            q = self.current_orientation
            siny_cosp = 2 * (q.w * q.z + q.x * q.y)
            cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
            self.current_yaw = np.arctan2(siny_cosp, cosy_cosp)
            angular_error = angle - self.current_yaw
            angular_error = (angular_error + np.pi) % (2 * np.pi) - np.pi
            
            #move to goal
            
            #hardcode first
            if distance < 0.05: #threshold
                self.publish_zero_velocity()
                self.state = 'AT_GOAL'
                return

            velocity = Twist()
            velocity.linear.x = min(0.5, distance) #max v = 0.5
            velocity.angular.z = angular_error * 1.0 #try kp = 1
            self.cmd_vel_pub.publish(velocity)

        elif self.state == 'AT_GOAL':
            request = AtGoal.Request()
            response = self.at_goal_client.call(request)
            if response.success:
                self.get_logger().info('Goal reached. Stop now yah!')
                self.state = 'INACTIVE'
            else:
                self.get_logger().warn('Not at goal! Check your code!')
                self.state = 'GOTO_GOAL'

def main(args=None):
    # what to do here?
    rclpy.init(args=args)
    node = SMStudentsNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
