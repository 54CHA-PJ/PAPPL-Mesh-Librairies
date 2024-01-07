from os import path
from pathlib import Path

from nii_mesh_gen import generate_from_nii

# ______________________________________________________________________________
# _______________________ INPUT ZONE FOR MANUAL TESTING ________________________

manual_test = True

directory           = (Path(__file__).resolve()).parent

labelmap_folder     = path.join(directory, "input_files")
labelmap_name       = "gluteus_max.nii.gz"
output_folder       = path.join(directory, "output_files")
output_name         = ""
output_type         = "obj"
library     = "vtk"
simplify    = ""
simply_val  = 100
smoothing   = "lap"
smooth_val  = 10
info_doc    = True
visualize   = True

# ______________________________________________________________________________
# ______________________________________________________________________________
 
if manual_test:
    # Test avec tous les paramètres
    print("\n---- MANUAL TEST ----")
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
    #      PYMESHLAB
    # -------------------
    
    # Test basique
    generate_from_nii(
        nii_dir     = path.join(labelmap_folder, labelmap_name), 
        out_dir     = output_folder,
        library     = "pymeshlab")
    
    # Test avec lissage
    generate_from_nii(
        nii_dir     = path.join(labelmap_folder, labelmap_name), 
        out_dir     = output_folder,
        library     = "pymeshlab",
        smoothing   = "lap",
        smooth_val  = 10)

    # Test avec simplification (Edge Collapse for Marching Cubes) et lissage
    generate_from_nii(
        nii_dir     = path.join(labelmap_folder, labelmap_name), 
        out_dir     = output_folder,
        library     = "pymeshlab",
        smoothing   = "lap",
        smooth_val  = 10,
        simplify    = "edmc")
    
    # Test avec simplification (Mesh Decimation Clustering) et lissage
    generate_from_nii(
        nii_dir     = path.join(labelmap_folder, labelmap_name), 
        out_dir     = output_folder,
        library     = "pymeshlab",
        smoothing   = "lap",
        smooth_val  = 3,
        simplify    = "mdc",
        simply_val  = 80)

    # -------------------
    #      NII2MESH
    # -------------------

    # -------------------
    #      NII2MESH
    # -------------------

    # Test basique
    p1 = generate_from_nii(
                nii_dir     = path.join(labelmap_folder, labelmap_name), 
                out_dir     = output_folder,
                library     = "nii2mesh")

    # Test avec lissage
    p2 = generate_from_nii(
                nii_dir     = path.join(labelmap_folder, labelmap_name), 
                out_dir     = output_folder,
                library     = "nii2mesh", 
                smooth_val  = 10)

    # Test avec reduction et lissage
    p3 = generate_from_nii(
                nii_dir     = path.join(labelmap_folder, labelmap_name), 
                out_dir     = output_folder,
                library     = "nii2mesh", 
                simply_val  = 50,
                smooth_val  = 10) 