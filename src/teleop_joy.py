#!/usr/bin/env python
import rospy
import copy
from video_capture import Capture
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import String

def publishMsg(twist,publish,name):
    rospy.loginfo(name)
    publish.publish(twist)
isDataToSend=False
armLButtonPressed=False
armRButtonPressed=False
resetangleButtonPressed=False
lastJoyCommand = Joy()

def send_joy_command(data):
    global isDataToSend
    if(isDataToSend):
        publishMsg(lastJoyCommand,motorPub,"motor message sended")
        isDataToSend=False
    
def callback(data):
    global armLButtonPressed
    global armRButtonPressed
    global resetangleButtonPressed
    global lastJoyCommand
    global isDataToSend
    
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
    if(not armRButtonPressed and not armLButtonPressed):
        lastJoyCommand=copy.deepcopy(data)
        isDataToSend = True
    
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
    global joyTimer
    rospy.init_node('joystickCommand', anonymous=True)
    joyTimer = rospy.Timer(rospy.Duration(0.05), send_joy_command)    
    rospy.spin()

if __name__ == '__main__':
    start()
