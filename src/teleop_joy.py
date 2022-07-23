#!/usr/bin/env python
import rospy
from video_capture import Capture
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import String

def publishMsg(twist,publish,name):
    rospy.loginfo(name)
    publish.publish(twist)

motorButtonPressed=False
motorSlowButtonPressed=False
armLButtonPressed=False
armRButtonPressed=False
angleButtonPressed=False
resetangleButtonPressed=False
def callback(data):
    global motorButtonPressed
    global motorSlowButtonPressed
    global armLButtonPressed
    global armRButtonPressed
    global angleButtonPressed
    global resetangleButtonPressed

    capture.joy_command(data)
    
    if(data.buttons[4]==1):
       rospy.loginfo('button4444444444 PRESSSSSSSSSSEEEEEEEDDDD')
    
    if(data.buttons[3]==1 and !motorSlowButtonPressed):
        motorSlowButtonPressed = True
        publishMsg(data,motorSlowPub,"motor BUTTON PRESSED")
    elif(motorSlowButtonPressed):
        motorSlowButtonPressed = False
        publishMsg(data,motorSlowPub,"motor BUTTON RELEASED")

    if(data.buttons[0]==1 and !motorButtonPressed):
        motorButtonPressed = True
        publishMsg(data,motorPub,"motor BUTTON PRESSED")
    elif(motorButtonPressed):
        motorButtonPressed = False
        publishMsg(data,motorPub,"motor BUTTON RELEASED")

    if(data.buttons[1]==1 and !gotoAngleJoyPub):
        angleButtonPressed = True
        publishMsg(data,gotoAngleJoyPub,"go to angle BUTTON PRESSED")
    elif(angleButtonPressed):
        angleButtonPressed = False
        publishMsg(data,gotoAngleJoyPub,"go to angle BUTTON RELEASED")

    if(data.buttons[2]==1 and !resetangleButtonPressed):
        resetangleButtonPressed = True
    elif(resetangleButtonPressed):
        resetangleButtonPressed = False
        publishMsg("reset angle",resetAnglePub,"reset angle BUTTON RELEASED")

    if(data.buttons[6]==1 and !armLButtonPressed):
        armLButtonPressed = True
        publishMsg(data,armLeftPub,"armLeftPub BUTTON PRESSED")
    elif(armLButtonPressed):
        armLButtonPressed = False
        publishMsg(data,armLeftPub,"armLeftPub")
    if(data.buttons[7]==1 and !armRButtonPressed):
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
