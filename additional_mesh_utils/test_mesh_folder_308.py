# VERSION 3.8

from os import getcwd, chdir, path
from objtools import *

# _______________________________ INPUT ZONE ___________________________________

directory       = path.join( getcwd(), "additional_mesh_utils")
out_folder_dir  = path.join(directory, "3D_output", "generated_from_python")
pic_folder_dir  = path.join(directory, "3D_output_pictures","generated_from_python" )
xls_folder_dir  = path.join(directory, "3D_output_statistics")

# ______________________________________________________________________________

# -----------------------------
# GLUTEUS MAX
# -----------------------------

print("\n----- Gluteus Max -----")

# Cameras that provide the "best point of view" of a muscle
# Obtained with Vedo visualization interface

cam_gluteus = dict(
    position=(488.535, -228.916, 759.305),
    focal_point=(179.000, 287.500, 949.500),
    viewup=(-0.351876, -0.501907, 0.790109),
    distance=631.405,
    clipping_range=(114.342, 1283.80),
)

cam_sartorius = dict(
    position=(351.954, 165.403, 764.280),
    focal_point=(64.0750, 90.2000, 323.400),
    viewup=(0.0446983, -0.989206, 0.139548),
    distance=531.888,
    clipping_range=(1.21400, 1214.00),
)

cam_gluteus_nii2mesh = dict(
    position=(-250.991, 580.044, -277.731),
    focal_point=(-101.011, -55.4166, 82.7566),
    viewup=(0.463350, 0.517465, 0.719400),
    distance=745.825,
    clipping_range=(446.515, 1124.39),
)


out_1  = path.join(directory, "3D_output", "generated_from_python", "gluteus")
out_2  = path.join(directory, "3D_output", "generated_from_python", "sartorius")
out_3  = path.join(directory, "3D_output", "generated_from_c")

chdir(pic_folder_dir) # Switch to the meshs' pictures directory
showFolderCam(out_1, cam_gluteus, z=1.65, save_image = False, show_3d = False, show_details = True, name = "gluteus")
chdir(pic_folder_dir) # Switch to the meshs' pictures directory
showFolderCam(out_2, cam_sartorius, z=5, save_image = False, show_3d = False, show_details = True, name = "sartorius")
chdir(pic_folder_dir) # Switch to the meshs' pictures directory
showFolderCam(out_3, cam_gluteus_nii2mesh, z=1.65, save_image = False, show_3d = False, show_details = True, name = "nii2mesh")
