#!/usr/bin/env python
import rospy
from video_capture import Capture
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import String

def publishMsg(twist,publish,name):
    rospy.loginfo(name)
    publish.publish(twist)

armLButtonPressed=False
armRButtonPressed=False
resetangleButtonPressed=False

def callback(data):
    global armLButtonPressed
    global armRButtonPressed
    global resetangleButtonPressed

    capture.joy_command(data)

    if(data.buttons[4]==1):
        armLButtonPressed = True
        publishMsg(data,armLeftPub,"armLeftPub BUTTON PRESSED")
    elif(armLButtonPressed):
        armLButtonPressed = False
        publishMsg(data,armLeftPub,"armLeftPub")
    if(data.buttons[5]==1):
        armRButtonPressed = True
        publishMsg(data,armRightPub,"armRightPub BUTTON PRESSED")
    elif(armRButtonPressed):
        armRButtonPressed = False
        publishMsg(data,armRightPub,"armRightPub BUTTON RELEASED")
def logInput(data):
    rospy.loginfo("ARDUINO : %s", data.data)
    

# Intializes everything
def start():

    
    rospy.Subscriber("joy", Joy, callback)

    rospy.Subscriber("LXL_node", String, logInput)
    rospy.Subscriber("LXR_node", String, logInput)
    rospy.Subscriber("ANGLE_node", String, logInput)
    rospy.Subscriber("ARDUINO_LOG_node", String, logInput)
    
    global motorPub
    motorPub = rospy.Publisher('JoyCommandMotor', Joy, queue_size=10)
    global motorSlowPub
    motorSlowPub = rospy.Publisher('JoyCommandMotorSlow', Joy, queue_size=10)
    global armLeftPub
    armLeftPub = rospy.Publisher('JoyCommandArmLeft', Joy, queue_size=10)
    global armRightPub
    armRightPub = rospy.Publisher('JoyCommandArmRigth', Joy, queue_size=10)
    global resetAnglePub
    resetAnglePub = rospy.Publisher('ResetAngleCommand', String, queue_size=10)
    global gotoAnglePub
    gotoAnglePub = rospy.Publisher('GotoAngleCommand', String, queue_size=10)
    global gotoAngleJoyPub
    gotoAngleJoyPub = rospy.Publisher('JoyGotoAngleCommand', Joy, queue_size=10)
    global capture
    capture = Capture()
    rospy.init_node('joystickCommand', anonymous=True)
    rospy.spin()

if __name__ == '__main__':
    start()
