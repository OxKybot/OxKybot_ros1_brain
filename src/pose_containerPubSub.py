#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from SlamPose import SlamPose

actualPose = SlamPose()
def publishMsg(publisher,msg,log_text):
    rospy.loginfo(log_text)
    publisher.publish(msg)

def update_pose_cb(data):
    actualPose.fromHectorToOxKybot(data)
    actualPose.publish(actualPose)

def get_pose(data):
    pose = str(actualPose.poseX)
    pose += ","+str(actualPose.poseY)
    pose += ","+str(actualPose.angle)
    publishMsg(poseToArduinoPub,pose,"pose requested")

def start():

    rospy.Subscriber("slam_out_pose", PoseStamped, update_pose_cb)
    rospy.Subscriber("POSITION_node", String, get_pose)
    global poseToArduinoPub
    poseToArduinoPub = rospy.Publisher('get_position_response', String, queue_size=10)
    global poseNode
    poseNode = rospy.Publisher('position', String, queue_size=10)
    rospy.init_node('poseContainer', anonymous=True)
    
 
    rospy.spin()

if __name__ == '__main__':
    start()
