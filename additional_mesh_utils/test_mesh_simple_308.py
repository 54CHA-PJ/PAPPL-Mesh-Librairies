from os import getcwd, chdir, path
from glob import glob
from objtools import *
import time
import nibabel as nib
from skimage import measure
import pymeshlab
import numpy as np

# _______________________________ INPUT ZONE ___________________________________

directory       = path.join(getcwd(), "additional_mesh_utils")
labelmap_dir    = path.join(directory, "Labelmap_free_sources", "mni152.nii.gz")
out_folder_dir  = path.join(directory, "3D_output")
pic_folder_dir  = path.join(directory, "3D_output_pictures")
xls_folder_dir  = path.join(directory, "3D_output_statistics")

print(directory)

# _______________________________________________________________________________


# TEST CREATE MESH

filename = "test_mesh.obj"

print("Loading NIFTI...")
test = nib.load(labelmap_dir).get_fdata()
print("Marching Cubes...")
verts, faces, normals, values = measure.marching_cubes(test)
print("Pymesh Meshset...")
m_pymeshlab = pymeshlab.Mesh(verts, faces)

print("Saving...")
test_mesh = pymeshlab.MeshSet()
test_mesh.add_mesh(m_pymeshlab)
test_mesh.save_current_mesh(filename)

# TEST VIEW MESH

print("Show Mesh...")
chdir(pic_folder_dir)

m_path = path.join(out_folder_dir, filename)
showObj(m_path, save_image = True, show_3d = True)

# TEST Details


