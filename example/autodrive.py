#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example Python node to publish Twist messages on the i2cpwm_board servos_drive topic.
"""

# Import required Python code.
import roslib
#roslib.load_manifest('autodrive_example')
import rospy
import sys

# Import custom message data and dynamic reconfigure variables.
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty

class DriveSquare:
    """ This example is in the form of a class. """

    def __init__(self):
        """ This is the constructor of our class. """
        # register this function to be called on shutdown
        rospy.on_shutdown(self.cleanup)

        # define publisher to topic
        self.pub = rospy.Publisher('servos_drive', Twist, queue_size=10)


        # give our node/publisher a bit of time to connect
        rospy.sleep(1)

        # use a rate to make sure the bot keeps moving
        r = rospy.Rate(5.0) # 5 cycles per second

        # go forever!
        # while not rospy.is_shutdown():
        self.square(-1)
        self.square(1)


    def square(self, direction):
        # there is no gyro accelerometer feedback to validate track
        # the mecanum wheels have some uneven drag so a little kludge adjustment
        drag = -0.015 # radians

        # create a Twist message, fill it in to drive forward
        twist = Twist()

        for i in range(4):
            # forward for 2 seconds
            twist.angular.z = drag;
            twist.linear.y = 0.35
            self.pub.publish(twist)
            rospy.sleep(2.0)
            # 2 second turn
            #twist.linear.y = 0.0 # zero radius turn
            twist.angular.z = (direction * (3.14/2/2)) + drag   # 45 deg/s
            self.pub.publish(twist)
            rospy.sleep(2.0) #  45 deg/s * 2sec = 90 degrees
        # stop motion
        self.stopeverything()


    def stopeverything(self):
        # call the service to power down the servos
        rospy.wait_for_service('stop_servos')
        stopservos = rospy.ServiceProxy('stop_servos', Empty)
        stopservos()


    def cleanup(self):
        # stop movement
        #twist = Twist()
        #self.pub.publish(twist)
        self.stopeverything()


# Main function.
if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node('autodrive')
    # Go to class functions that do all the heavy lifting. Do error checking.
    try:
        DriveSquare()
    except rospy.ROSInterruptException:
        pass

