#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped, Pose
from robot_control_ros1_v1.srv import get_position, get_positionResponse

actualpose = PoseStamped()

def publishMsg(publisher,msg,log_text):
    rospy.loginfo(log_text)
    publisher.publish(msg)
def logInput(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
def update_pose_cb(data):
    global actualpose
    actualpose=data
def get_position_cb(req):
    return get_positionResponse(""+actualpose.pose.position.x+","+actualpose.pose.position.y+","+actualpose.pose.orientation.z)

def start():

    rospy.Subscriber("slam_out_pose", PoseStamped, update_pose_cb)
    
    s = rospy.Service('pose_container_service', get_position, get_position_cb)
    rospy.init_node('poseContainer', anonymous=True)
 
    rospy.spin()

if __name__ == '__main__':
    start()
