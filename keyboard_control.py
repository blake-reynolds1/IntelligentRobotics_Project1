#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def keyboard_control():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.init_node('keyboard_control', anonymous=True)
    rate = rospy.Rate(10)  # 10 Hz

    twist = Twist()
    linear_speed = 0.2  # Adjust to your desired speed
    angular_speed = 0.2  # Adjust to your desired speed

    while not rospy.is_shutdown():
        key = getKey()
        if key == 'w':
            twist.linear.x = linear_speed
            twist.angular.z = 0.0
        elif key == 's':
            twist.linear.x = -linear_speed
            twist.angular.z = 0.0
        elif key == 'a':
            twist.linear.x = 0.0
            twist.angular.z = angular_speed
        elif key == 'd':
            twist.linear.x = 0.0
            twist.angular.z = -angular_speed
        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0

        pub.publish(twist)
        rate.sleep()

if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)
    try:
        keyboard_control()
    except rospy.ROSInterruptException:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
