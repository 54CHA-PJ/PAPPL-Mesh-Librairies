# VERSION 3.8

from os import getcwd, chdir, path
from objtools import *

# _______________________________ INPUT ZONE ___________________________________

directory       = path.join( getcwd(), "additional_mesh_utils")
out_folder_dir  = path.join(directory, "3D_output")
pic_folder_dir  = path.join(directory, "3D_output_pictures")
xls_folder_dir  = path.join(directory, "3D_output_statistics")

# ______________________________________________________________________________


# -----------------------------
# GLUTEUS MAX
# -----------------------------

print("\n----- Gluteus Max -----")

cam_gluteus = dict(
    position=(488.535, -228.916, 759.305),
    focal_point=(179.000, 287.500, 949.500),
    viewup=(-0.351876, -0.501907, 0.790109),
    distance=631.405,
    clipping_range=(114.342, 1283.80),
)

print(out_folder_dir)
chdir(out_folder_dir)
showFolderCam(".", cam_gluteus, z=1.65, save_image = True, show_3d = False, show_details = True, name = "gluteus_max")

# AUTRES FONCTIONS
# showObjCam("mesh_pylab.obj", cam_gluteus, z=2, save_image = False, show_3d = True)
# showFolder(".", yaw = -50, pitch = -50,z = 5, save_image = True, show_3d = False)
# showObj("mesh_pylab.obj", yaw = -50, pitch = -50,z = 5, save_image = True, show_3d = False)

