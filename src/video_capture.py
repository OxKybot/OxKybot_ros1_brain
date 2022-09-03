
import cv2
import time
from sensor_msgs.msg import Joy
from threading import Thread
class Capture:

    def __init__(self):
        self.is_recording = False
        self.capturing=False
        self.captureButtonPressed=False
        self.isCaptureInitDone = False

    def init_cap(self):
        self.cap = cv2.VideoCapture(self.gstreamer_pipeline(), cv2.CAP_GSTREAMER)

    def gstreamer_pipeline(self,capture_width=3264,
        capture_height=2464,
        display_width=1632,
        display_height=1232,
        framerate=21,
        flip_method=0,
    ):
        return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
            )

    def get(self): 
        if self.cap.isOpened():
            while self.is_recording:                
                ret_val, img = self.cap.read()
                self.out.write(img)
                keyCode = cv2.waitKey(30) & 0xFF
            self.cap.release()
        else:
            print("Unable to open camera")

    def start(self):
        self.init_recorder()
        self.is_recording = True
        Thread(target=self.get, args=()).start()
        return self

    def init_recorder(self):
        self.vid_name='/home/kian/video_rec/video%s.avi' % int(round(time.time()))
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(self.vid_name,cv2.VideoWriter_fourcc(*'XVID'), 20.0, (1632,1232))

    def stop_cap(self):        
        self.is_recording = False

    def joy_command(self,data):
        if(data.buttons[9]==1 and not self.isCaptureInitDone and not self.captureButtonPressed):
            self.captureButtonPressed=True
        if(data.buttons[9]==1 and not self.isCaptureInitDone and self.captureButtonPressed):
            self.init_cap()
            self.isCaptureInitDone=True
            self.captureButtonPressed=False
        if(data.buttons[9]==1 and not self.capturing and not self.captureButtonPressed and self.isCaptureInitDone):
            self.captureButtonPressed=True
        if(data.buttons[9]==0 and not self.capturing and self.captureButtonPressed and self.isCaptureInitDone):
            self.capturing=True
            self.start()
            self.captureButtonPressed=False
        if(data.buttons[9]==1 and self.capturing and not self.captureButtonPressed and self.isCaptureInitDone):
            self.captureButtonPressed=True
        if(data.buttons[9]==0 and self.capturing and self.captureButtonPressed and self.isCaptureInitDone):
            self.capturing=True
            self.stop_cap()
            self.captureButtonPressed=False
        
