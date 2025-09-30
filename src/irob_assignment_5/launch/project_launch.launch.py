#Add necessary imports
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
#USE:
use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
pkg_irob_assignment_5 = "/home/y/i/yikunw/DD2410_5/src/irob_assignment_5"
#pkg_irob_assignment_5 = get_package_share_directory('irob_assignment_5') #better way to do above!

# Launch node/executable goal_server , add parameter goal_params_SM.yaml or goal_params_BT.yaml as needed 
# Launch node/executable activation_server
# Launch node/executable at_goal_server 
    pkg_share = get_package_share_directory('<your_package_name>')
    goals_param = os.path.join(pkg_share, 'config', 'goals_set.yaml')

    return LaunchDescription([
        Node(
            package='irob_assignment_5',
            executable='goal_server.py',
            name='goal_service_node',
            parameters=[goals_param]
        ),
        Node(
            package='irob_assignment_5',
            executable='at_goal_server.py',
            name='at_goal_service_node'
        ),
        Node(
            package='irob_assignment_5',
            executable='activation_server.py',
            name='activation_server'
        )
    ])

