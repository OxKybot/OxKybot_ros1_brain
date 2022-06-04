from geometry_msgs.msg import PoseStamped
class SlamPose:
    def __init__(self):
        self.poseX=0
        self.poseY=0
        self.angle=0
    def fromHectorToOxKybot(self,data):
        self.poseX=data.pose.position.x*1000
        self.poseY=data.pose.position.y*1000
        self.angle = data.pose.orientation.z*1000
    def toString(self):
        return ""+str(self.poseX)+","+str(self.poseY)+","+str(self.angle)