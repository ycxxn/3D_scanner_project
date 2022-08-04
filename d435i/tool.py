import pyrealsense2 as rs
import numpy as np
import cv2
import matplotlib.pyplot as plt
from time import sleep

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

    def read2img(self, ser, delay=0.15):
        for s in range(2):
            if s == 0:
                ser.write(b'on\n')
                # sleep(delay)

                frames = self.pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                img = np.asanyarray(color_frame.get_data())
                # img = cv2.rotate(img, cv2.ROTATE_180)
                # img = img[:,230:1030,:]
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = cv2.blur(gray, (3,3))
                # cv2.imshow("img1", gray)
                # while ser.in_waiting:
                #     mcu_feedback = ser.readline().decode()  # 接收回應訊息並解碼
                #     print('控制板回應：', mcu_feedback)
                img1 = np.copy(gray)
                sleep(delay)
            
            if s == 1:
                ser.write(b'off\n')
                # sleep(delay)
                frames = self.pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                img = np.asanyarray(color_frame.get_data())
                # img = cv2.rotate(img, cv2.ROTATE_180)     
                # img = img[:,230:1030,:]
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = cv2.blur(gray, (3,3))
                # cv2.imshow("img2", gray)
                # while ser.in_waiting:
                #     mcu_feedback = ser.readline().decode()  # 接收回應訊息並解碼
                #     print('控制板回應：', mcu_feedback)
                img2 = np.copy(gray)
                sleep(delay)
        return img1, img2

    def read2img_2(self, ser, cap_t = 0.5, delay=0.15):
        ser.write(b"move\n")
        sleep(cap_t)

        ser.write(b"on\n")
        sleep(delay)
        img_p = self.read()

        ser.write(b"off\n")
        sleep(delay)
        img_n = self.read()
        
        img = cv2.subtract(img_p, img_n)
        img = cv2.subtract(img, 30)

        h,w = img.shape[:2]
        x = 300
        img = img[:, x:w-x,:]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.multiply(gray, 5)

        th = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)[1]
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.erode(th, kernel, iterations = 1)
        # cv2.imshow("img", img)
        
        l = []
        for n in range(mask.shape[0]):
            c = np.where(mask[n,:]==255)[0]
            if len(c) == 0 or min(c) >= 320:
                    l.append(None)
            else:
                length = 68*(320-min(c))/110
                length = round(length, 2)
                l.append(length)

        return np.array(l), mask 

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