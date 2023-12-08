from objtools import *
from os import path, chdir, getcwd

directory       = path.join( getcwd(), "additional_mesh_utils")
out_folder_dir  = path.join(directory, "3D_output")
pic_folder_dir  = path.join(directory, "3D_output_pictures")
xls_folder_dir  = path.join(directory, "3D_output_statistics")

chdir(out_folder_dir)

print(volume("mesh_vtk.obj"))

print(volume( path.join(out_folder_dir, "mesh_vtk.obj")))