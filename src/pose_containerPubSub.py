#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped


actualPose = PoseStamped()
def publishMsg(publisher,msg,log_text):
    rospy.loginfo(log_text)
    publisher.publish(msg)

def update_pose_cb(data):
    global actualPose
    actualPose = data

def get_pose(data):
    rospy.loginfo(actualPose.pose)
    publishMsg(poseToArduinoPub,actualPose,"pose requested")

def start():

    rospy.Subscriber("slam_out_pose", PoseStamped, update_pose_cb)
    rospy.Subscriber("POSITION_node", String, get_pose)
    global poseToArduinoPub
    poseToArduinoPub = rospy.Publisher('get_position_response', PoseStamped, queue_size=10)
    global poseNode
    poseNode = rospy.Publisher('position', String, queue_size=10)
    rospy.init_node('poseContainer', anonymous=True)
    
 
    rospy.spin()

if __name__ == '__main__':
    start()
