#Add necessary imports
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

#USE:
use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
#pkg_irob_assignment_5 = "/home/parag/ros_as1_test/src/irob_assignment_5"
#pkg_irob_assignment_5 = get_package_share_directory('irob_assignment_5') #better way to do above!

# Launch node/executable goal_server , add parameter goal_params_SM.yaml or goal_params_BT.yaml as needed 
# Launch node/executable activation_server
# Launch node/executable at_goal_server 


def generate_launch_description():
    # Get the package share directory
    pkg_share = get_package_share_directory('irob_assignment_5')

    # Path to the goal parameters YAML file
    goal_params_file_path = os.path.join(pkg_share, 'config', 'goal_params_SM.yaml')

    # Goal Server Node with parameters
    goal_server_node = Node(
        package='irob_assignment_5',
        executable='goal_server',
        name='goal_server',
        output='screen',
        parameters=[goal_params_file_path]
    )

    # Activation Server Node
    activation_server_node = Node(
        package='irob_assignment_5',
        executable='activation_server',
        name='activation_server',
        output='screen'
    )

    # At Goal Server Node
    at_goal_server_node = Node(
        package='irob_assignment_5',
        executable='at_goal_server',
        name='at_goal_server',
        output='screen'
    )

    # Your State Machine Node
    sm_students_node = Node(
        package='irob_assignment_5',
        executable='SM_students',
        name='SM_students_node',
        output='screen'
    )

    return LaunchDescription([
        goal_server_node,
        activation_server_node,
        at_goal_server_node,
        sm_students_node
    ])
