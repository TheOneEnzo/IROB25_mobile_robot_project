import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/afs/kth.se/home/t/m/tmatty/ros2_ws/src/KTH_DD2410_Assign5_2025-main/IROB25_mobile_robot_project/assign_5_IROB_pk/install/irob_assignment_5'
