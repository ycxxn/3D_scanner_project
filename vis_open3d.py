import open3d as o3d
import numpy as np
import cv2
if __name__ == "__main__":
    # o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Debug)
    
    x = np.linspace(0,100,100)
    y = np.sin(x)
    z = np.zeros((100))
    point = np.array([x,y,z])
    points = point.transpose()
    # colors = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]

    
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    source = o3d.geometry.PointCloud()
    source.points = o3d.utility.Vector3dVector(points)  # 定義點雲座標位置
    # source.colors = o3d.utility.Vector3dVector(colors)  # 定義點雲的顏色

    axis_pcd = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1, origin=[0, 0, 0])

    # vis.add_geometry(axis_pcd)
    vis.add_geometry(source)

    while(1):
        points[:,0] += 0.1
        new_source = o3d.geometry.PointCloud()
        new_source.points = o3d.utility.Vector3dVector(points)  # 定義點雲座標位置
        new_source

        source += new_source

        vis.update_geometry(source)
        vis.poll_events()
        vis.update_renderer()

        key = cv2.waitKey(2)

    vis.destroy_window()
    # o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Info)