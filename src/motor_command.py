#!/usr/bin/env python
import rospy
from SlamPose import SlamPose
from std_msgs.msg import Int32
from std_msgs.msg import String
import constants
actualPose =SlamPose()
goalPose=SlamPose()


def update_pose_cb(data):
    global actualPose
    actualPose=data

def goto_positionX_cb(data):
    global goalPose
    global posexTimer
    goalPose=actualPose
    goalPose.poseX = data
    resetAnglePub.publish("reset angle")
    posexTimer.run()

def timer_got_positionX_cb():

    if(abs(goalPose.poseX - actualPose.poseX)<constants.POSITION_TRACKING_LAMBDA):
        motorPub.publish("STOP")
        posexTimer.shutdown()

    #go forward
    if(goalPose.poseX>actualPose.poseX):
        motorPub.publish("Go FORWARD")
    
    #go backward
    if(goalPose.poseX<actualPose.poseX):
        motorPub.publish("Go BACWARD")



# Intializes everything
def start():
    rospy.Subscriber("position", SlamPose, update_pose_cb)
    rospy.Subscriber("goto_positionX", Int32, goto_positionX_cb)
    global motorPub
    motorPub = rospy.Publisher('GoToPositionX', String, queue_size=10)
    global resetAnglePub
    resetAnglePub = rospy.Publisher('ResetAngleCommand', String, queue_size=10)
    global gotoAnglePub
    gotoAnglePub = rospy.Publisher('GotoAngleCommand', String, queue_size=10)
    global posexTimer
    posexTimer = rospy.Timer(rospy.Duration(1), timer_got_positionX_cb)
    rospy.init_node('motorCommandNode', anonymous=True)
    rospy.spin()

if __name__ == '__main__':
    start()
