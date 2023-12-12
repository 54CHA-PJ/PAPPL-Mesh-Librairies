from os import path
from pathlib import Path

from nii_mesh_gen import generate_from_nii
from source.mesh_tools import showObj

# ______________________________________________________________________________
# _______________________________ INPUT ZONE ___________________________________

manual_test = False

directory           = (Path(__file__).resolve()).parent

labelmap_folder     = path.join(directory, "input_files")
labelmap_name       = "gluteus_max.nii.gz"

output_folder       = path.join(directory, "output_files")
output_name         = "TEST_N2M"
output_type         = "obj"

library     = "nii2mesh"

simplify    = ""
simply_val  = 0
smoothing   = ""
smooth_val  = 0

info_doc    = False
visualize   = True

# ______________________________________________________________________________
# ______________________________________________________________________________

 
if manual_test:
    # Test avec tous les paramètres
    generate_from_nii(
                nii_dir     = path.join(labelmap_folder, labelmap_name), 
                library     = library, 
                simplify    = simplify, 
                simply_val  = simply_val,
                smoothing   = smoothing, 
                smooth_val  = smooth_val,
                info_doc    = info_doc,
                visualize   = visualize,
                out_type    = output_type,
                out_dir     = output_folder,
                out_name    = output_name)
else :

    # -------------------
    #      NII2MESH
    # -------------------

    # Test basique
    p1 = generate_from_nii(
                nii_dir     = path.join(labelmap_folder, labelmap_name), 
                library     = "nii2mesh", 
                out_dir     = output_folder, 
                visualize   = True)

    # Test avec lissage
    p2 = generate_from_nii(
                nii_dir     = path.join(labelmap_folder, labelmap_name), 
                out_dir     = output_folder,
                library     = "nii2mesh", 
                smooth_val  = 10, 
                visualize   = True)

    # Test avec reduction
    p3 = generate_from_nii(
                nii_dir     = path.join(labelmap_folder, labelmap_name), 
                out_dir     = output_folder,
                library     = "nii2mesh", 
                simply_val  = 50,
                smooth_val  = 10, 
                visualize   = True) 
    
    showObj("nii_mesh_generation\\output_files\\mesh_nii2mesh.obj")
    showObj("nii_mesh_generation\\output_files\\mesh_nii2mesh_smooth=10.obj")
    showObj("nii_mesh_generation\\output_files\\mesh_nii2mesh_simp=50_smooth=10.obj")