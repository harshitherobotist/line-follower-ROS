#!/usr/bin/env python
from __future__ import print_function
 
import roslib

import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist

class image_converter:
    def __init__(self):
        rospy.init_node('Line_follower_controller', anonymous=True)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.vel = Twist()
        self.vel.linear.x = 0
        self.vel.linear.y = 0
        self.vel.linear.z = 0
        self.vel.angular.x = 0
        self.vel.angular.y = 0
        self.vel.angular.z = 0

        self.left = "1"
        self.middle = "1"
        self.right = "1"
	  
        self.publish_vel()
	  
        self.sensor_middle = rospy.Subscriber("/middle",String,self.callback_m)
        self.sensor_right = rospy.Subscriber("/right",String,self.callback_r)
        self.sensor_left = rospy.Subscriber("/left",String,self.callback_l)

    def callback_l(self,data):
        if data.data == "0":
            self.left = "0"
        else:
            self.left = "1"
        self.publish_vel() 	

    def callback_m(self,data):

        if data.data == "0":
            self.middle = "0"
        else:
            self.middle = "1"
        self.publish_vel()

    def callback_r(self,data):
        if data.data == "0":
            self.right = "0"
        else:
            self.right = "1"
        self.publish_vel()

    def publish_vel(self):

        if(self.middle == "0" and self.right == "0" and self.left == "0"):  #considering all 8 possibilites of sensor output and accordingly setting the velocities
            self.vel.linear.x = 0.08
            self.vel.linear.y = 0
            self.vel.angular.z = 0

        elif(self.middle == "0" and self.right == "0" and self.left == "1"):
            self.vel.linear.x = 0.03
            self.vel.linear.y = 0
            self.vel.angular.z = -0.5

        elif(self.middle == "0" and self.right == "1" and self.left == "0"):
            self.vel.linear.x = 0.03
            self.vel.linear.y = 0
            self.vel.angular.z = 0.5
        elif(self.middle == "0" and self.right == "1" and self.left == "1"):
            self.vel.linear.x = 0.08
            self.vel.linear.y = 0
            self.vel.angular.z = 0
        elif(self.middle == "1" and self.right == "0" and self.left == "0"):
            self.vel.linear.x = 0
            self.vel.linear.y = 0
            self.vel.angular.z = 0
        elif(self.middle == "1" and self.right == "0" and self.left == "1"):
            self.vel.linear.x = 0
            self.vel.linear.y = 0
            self.vel.angular.z = -0.5
        elif(self.middle == "1" and self.right == "1" and self.left == "0"):
            self.vel.linear.x = 0
            self.vel.linear.y = 0
            self.vel.angular.z = 0.5
        elif(self.middle == "1" and self.right == "1" and self.left == "1"):
            self.vel.linear.x = 0
            self.vel.linear.y = 0
            self.vel.angular.z = 0
        else:
            self.vel.linear.x = 0
            self.vel.linear.y = 0
            self.vel.angular.z = 0
        self.pub.publish(self.vel)
		
        print (self.vel)
        print(self.left,self.right,self.middle)
	  	  
	  

def main(args):
    ic = image_converter()
  
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)