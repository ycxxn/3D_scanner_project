import open3d as o3d
import open3d_tutorial as o3dtut

pcd = o3d.io.read_point_cloud("test.pcd")

pri
nt(pcd)
# o3d.visualization.draw_geometries([pcd],
#                                   zoom=0.00100,
#                                   front=[-0.4761, -0.4698, -0.7434],
#                                   lookat=[1.8900, 3.2596, 0.9284],
#                                   up=[0.2304, -0.8825, 0.4101])