import open3d as o3d
import numpy as np
import cv2
from time import sleep
import serial
from tool import cam


points = np.array([[1.0,1.0,1.0],[0.0,0.0,0.0]])

vis = o3d.visualization.Visualizer()
vis.create_window()


source = o3d.geometry.PointCloud()
source.points = o3d.utility.Vector3dVector(points)

vis.add_geometry(source)

l = 1
n = 0
while(1):
    theta = np.pi/180 * n 
    points[1,0] = np.cos(theta)*l
    points[1,2] = np.sin(theta)*l
    n += 1

    if n == 360:
        n =0
        l+=1
        

    # points[1,2] += 0.001
    # points[1,1] += 0.001
    # points[1,0] += 0.001
    new_source = o3d.geometry.PointCloud()
    new_source.points = o3d.utility.Vector3dVector(points)  # 定義點雲座標位置
    print(source)
    source += new_source

    vis.update_geometry(source)
    vis.poll_events()
    vis.update_renderer()

    key = cv2.waitKey(1)