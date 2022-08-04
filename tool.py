import pyrealsense2 as rs
import numpy as np
import cv2
import matplotlib.pyplot as plt

class cam:
    def __init__(self):
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))
        # config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
        # Start streaming
        self.pipeline.start(config)

    def read(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        return color_image

class laser_cam:
    def __init__(self) -> None:
        self.fig = plt.figure()
        self.cap = cam()
        self.x1 = np.linspace(0, 1280, 1280)

    def read(self, num_sample):
        img = self.cap.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.medianBlur(thresh,11)
        l = []
        for n in range(thresh.shape[1]):
            c = np.where(thresh[:,n]==255)[0]
            if len(c) == 0:
                l.append(-1)
            else:
                length = 4.0*(max(c)-458)/40
                length = round(length, 2)
                l.append(length)
        plt.ylim(-2,10)
        plt.plot(self.x1,l)
        plt.draw()  
        plt.pause(0.01)
        self.fig.clear()
        res = cv2.hconcat([cv2.resize(gray, (320,240)),cv2.resize(thresh, (320,240))])
        cv2.imshow("res", res)

        new_l = [l[n*thresh.shape[1]//num_sample] for n in range(num_sample)]
        return np.array(new_l)

def array2point(x,y,z):
    point = np.array([x,y,z])
    points = point.transpose()
    return points