#!/usr/bin/env python3


#necessary imports here , follow basic Ros2 node stuff


#import necessary services below
#from Somewhere import XX{get goal}, {activtion service}, {deactivtion service}, {Check at Goal service} 

# IMPORT necessary messages, you need to use cmd_vel and more

# import necessary sensory messages if needed:

class SMStudentsNode(Node):
    def __init__(self):
        super().__init__('SM_students_node')

        #add important initializations here
        self.get_logger().info("SM_students_node ready. Robot is inactive until activated.")

    def handle_activate_robot(self, request, response):
        pass
        #Do some awesome stuff here!
        
        
def main(args=None):
    pass
    # what to do here?


if __name__ == '__main__':
    main()
