import cv2
import numpy as np
from tool import cam, laser_cam, array2point
import time
import matplotlib.pyplot as plt
import open3d as o3d

num_sample = 100
x = np.linspace(0,1280,num_sample)
y = np.zeros((num_sample))
z = np.zeros((num_sample))
points = array2point(x,y,z)
colors = np.full((num_sample,3), 1.0)

vis = o3d.visualization.Visualizer()
vis.create_window()
opt = vis.get_render_option()
opt.background_color = np.asarray([0, 0, 0])

source = o3d.geometry.PointCloud()
source.points = o3d.utility.Vector3dVector(points)
source.colors = o3d.utility.Vector3dVector(colors)

vis.add_geometry(source)

cap = laser_cam()

while(1):
    l = cap.read(num_sample)*50
    points[:,1] = l
    points[:,2] += 15
    new_source = o3d.geometry.PointCloud()
    new_source.points = o3d.utility.Vector3dVector(points)  # 定義點雲座標位置
    new_source.colors = o3d.utility.Vector3dVector(colors)
    # source.point_size = 0

    source += new_source

    vis.update_geometry(source)
    vis.poll_events()
    vis.update_renderer()
    
    key = cv2.waitKey(200)
    # cv2.waitKey(1)
    # o3d.io.write_point_cloud("test.ply", source)
    # o3d.io.write_triangle_mesh("test.ply", source)


# o3d.io.write_point_cloud("test.pcd", source)

