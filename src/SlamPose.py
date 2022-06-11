from geometry_msgs.msg import PoseStamped
import constants

class SlamPose:
    def __init__(self):
        self.poseX=0
        self.poseY=0
        self.angle=0

    def fromHectorToOxKybot(self,data):
        self.poseX=data.pose.position.x*constants.LIDAR_POSITION_FACTOR
        self.poseY=data.pose.position.y*constants.LIDAR_POSITION_FACTOR
        self.angle = data.pose.orientation.z*constants.LIDAR_ANGLE_FACTOR

    def toString(self):
        return ""+str(self.poseX)+","+str(self.poseY)+","+str(self.angle)