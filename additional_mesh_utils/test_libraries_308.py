from os import getcwd, chdir, path
from glob import glob

import time
import numpy as np
from skimage import measure

import nibabel as nib
import open3d
import trimesh
from objtools import trimesh_volume, showError, affiche_temps

# conda activate py38

print("\n\n---------------------------------------")
print("          TEST LIBRAIRIES - 3.8")
print("---------------------------------------\n\n")

# ------------------------------------------------------------------------------
#   FICHIER ORIGINAL
# ------------------------------------------------------------------------------

# Lire le fichier
directory = getcwd()
nom_fichier = "3d_source/sartorius.nii.gz"
lab = path.join(directory, nom_fichier)
test = nib.load(lab).get_fdata()

chdir(path.join(directory, "obj_generated_2"))

#start_time = time.time()
#elapsed_time = time.time() - start_time 
#print(f"Elapsed time: {elapsed_time:.1f} seconds")

# ------------------------------------------------------------------------------
#   MARCHING CUBES
# ------------------------------------------------------------------------------

verts, faces, normals, values = measure.marching_cubes(test)

# ------------------------------------------------------------------------------
#   CREATION DU MESH
# ------------------------------------------------------------------------------

m_trimesh = trimesh.Trimesh(vertices=verts, faces=faces, vertex_attributes={'normals': normals, 'values': values})

# ------------------------------------------------------------------------------
#   CALCUL DU VOLUME
# ------------------------------------------------------------------------------

# Volume "initial" = 3D numpy array
nbVoxels = np.count_nonzero(test)

# -------------------------
#       TRIMESH 

print("\n--- Trimesh ---\n")
liste_trimesh = {}

liste_trimesh["mesh_trimesh"] = m_trimesh
temps_init = affiche_temps(time.time())

""" 
USELESS

print("\nQuadratic Decimation 30")
mesh_trimesh_co_30 = m_trimesh.simplify_quadric_decimation(0.3)
liste_trimesh["mesh_trimesh_co_30"] = mesh_trimesh_co_30
temps_init = affiche_temps(temps_init)

print("\nQuadratic Decimation 50")
mesh_trimesh_co_50 = m_trimesh.simplify_quadric_decimation(0.5)
liste_trimesh["mesh_trimesh_co_50"] = mesh_trimesh_co_50
temps_init = affiche_temps(temps_init)

print("\nQuadratic Decimation 90")
mesh_trimesh_co_90 = m_trimesh.simplify_quadric_decimation(0.9)
liste_trimesh["mesh_trimesh_co_90"] = mesh_trimesh_co_90
temps_init = affiche_temps(temps_init) 
"""

print("\nSmoothing")
mesh_trimesh_sm = m_trimesh.smooth_shaded
liste_trimesh["mesh_trimesh_sm"] = mesh_trimesh_sm
temps_init = affiche_temps(temps_init)

# ------------------------------------------------------------------------------
#    EXPORTATION DES MESH
# ------------------------------------------------------------------------------

print("Volume du nuage de points (Nombre de voxels):\n", nbVoxels)

# ---------------------------------------
# Trimesh

print("\n--- Trimesh ---\n")

for key, mesh in liste_trimesh.items():
    mesh.export(key+".stl", file_type='stl')
    mesh.export(key+".obj", file_type='obj')
    print("\n"+key)
    vol = trimesh_volume(mesh)
    print("Volume : ", vol)
    showError(nbVoxels, vol)