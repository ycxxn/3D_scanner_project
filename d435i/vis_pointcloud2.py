import open3d as o3d
import numpy as np
import cv2
from time import sleep
import serial
from tool import cam

def deal_depth2yz(depth):
    yz = []
    y = np.where(depth!=None)[0]
    
    for yi in y:
        z = depth[yi]
        yz.append([720-yi, z])
        # print(x,yi)
    # print(xy)
    return np.array(yz)


if __name__ == "__main__":
    # o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)
    
    num_sample = 200
    # x = np.linspace(0,1280,100)
    # y = np.zeros((num_sample))
    # z = np.zeros((num_sample))
    n = np.linspace(0,360,num_sample)
    x = 400*np.cos(n)
    y = np.full(num_sample, 0)
    z = 400*np.sin(n)
    point = np.array([x,y,z])
    points = point.transpose()
    # colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]

    
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    source = o3d.geometry.PointCloud()
    source.points = o3d.utility.Vector3dVector(points)  # 定義點雲座標位置
    # source.colors = o3d.utility.Vector3dVector(colors)  # 定義點雲的顏色

    # axis_pcd = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=[0, 0, 0])

    # vis.add_geometry(axis_pcd)
    vis.add_geometry(source)

    COM_PORT = 'COM5'    # 指定通訊埠名稱
    BAUD_RATES = 115200    # 設定傳輸速率
    ser = serial.Serial(COM_PORT, BAUD_RATES)
    ser.write(b"off\n")
    print("---init----")
    sleep(1)
    print("Done!")
    cap = cam()
    # x = np.zeros((s))
    # nn = 0 

    num_scan = 245
    for nn in range(num_scan):
        depth, mask = cap.read2img_2(ser,cap_t=0.1)
        print(depth.shape)
        yz = deal_depth2yz(depth)
        cv2.imshow("yz", mask)
        
        
        yz[:,1] *= 12
        s = yz.shape[0]
        theta = (np.pi/180)*360/num_scan*nn
        point = np.array([yz[:,1]*np.cos(theta),yz[:,0], yz[:,1]*np.sin(theta)])
        points = point.transpose()
        # nn +=1
        # print(points.shape)
        print("scanning {}/{}".format(nn+1, num_scan))
    
        new_source = o3d.geometry.PointCloud()
        new_source.points = o3d.utility.Vector3dVector(points)  # 定義點雲座標位置

        source += new_source
        vis.update_geometry(source)
        vis.poll_events()
        vis.update_renderer()

        key = cv2.waitKey(1)
    
    print("---scanning finish---")
    while(1):
        vis.update_geometry(source)
        vis.poll_events()
        vis.update_renderer()

    vis.destroy_window()
    # o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Info)