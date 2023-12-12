"""
Authors: Sacha Cruz, Mario Espinoza
Date: 05/12/2023
________________________________
|                              |
|   NIFTI -> MESH GENERATION   |
|______________________________|

This script takes a labeled NIFTI (.nii or .nii.gz) file and converts it into a 3D mesh. 

Notes:
- Refer to README.md for an extensive explanation of function parameters and usages.
- For other useful functions not required by this script, check the folder "additional_mesh_utils"."

Compatibility: 
- The script functions with Python versions 3.8 - 3.11.
- Mesh Visualization may have compatibility issues with Python 3.10 - 3.11.

Requirements: 
- For use of Nii2Mesh library, Windows OS is required because it needs Command Prompt.
- Linux or Mac environments can still manually write the command written on "mesh_gen_c.py" on their OS's language to make nii2mesh work.

Dependencies:
- numpy for array operations and computations.
- nibabel for reading NIFTI files.
- skimage.measure for applying the Marching Cubes algorithm.
- pymeshlab and vtk for advanced mesh manipulation.

Custom Modules:
- `mesh_gen_python.py`  provides Python-based mesh generation tools.
- `mesh_gen_c.py`          provides C-based mesh generation tools.
- `mesh_tools.py`       includes utilities for displaying a mesh and its details.
"""

from os import getcwd, chdir, path
from pathlib import Path

from source.mesh_gen_python import mesh_gen_pylab
from source.mesh_gen_python import mesh_gen_vtk
from source.mesh_gen_c import mesh_gen_nii2mesh

# ______________________________________________________________________________
# _______________________________ INPUT ZONE ___________________________________

directory           = (Path(__file__).resolve()).parent

labelmap_folder     = path.join(directory, "input_files")
labelmap_name       = "gluteus_max.nii.gz"

output_folder       = path.join(directory, "output_files")
output_name         = "test"
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

def generate_from_nii(
        nii_dir, 
        grid_scale  = (0.55, 0.55, 0.55),
        library     = "pymeshlab", 
        simplify    = "", 
        simply_val  = 0,
        smoothing   = "", 
        smooth_val  = 0,
        info_doc    = True,
        visualize   = True,
        out_type    = "obj",
        out_dir     = ".",
        out_name    = "" ):
    """
    Generates a Mesh (.obj / .stl) from a .nii file.
    Args:
        nii_dir         (str):              Location of the NIFTI file.
        grid_scale      (tuple, optional):  Grid normalization values.                  (DEPENDS ON THE LIBRARY)
        # -----------------------------------------------------------------------------------------------------------------------------------------
        library         (str, optional):    Choose the library : "pymeshlab" / "nii2mesh" / "vtk".
        simplify        (str, optional):    Choose the simplification method.           (DEPENDS ON THE LIBRARY)
        smoothing       (str, optional):    Choose the smoothing method.                (DEPENDS ON THE LIBRARY)
        smooth_val      (int, optional):  The coefficient of the smoothing method.    (DEPENDS ON THE LIBRARY)
        simply_val      (int, optional):  The coefficient of the simplifying method.  (DEPENDS ON THE LIBRARY)
        # -----------------------------------------------------------------------------------------------------------------------------------------
        out_type        (str, optional):    Choose the output file type : "obj" / "stl".(DEPENDS ON THE LIBRARY)
        out_dir         (str, optional):    Choose the output file directory.
        out_name        (str, optional):    Choose a name for the file. If no name is chosen, the default name is made using the other parameters.
        # -----------------------------------------------------------------------------------------------------------------------------------------
        info_doc        (bool, optional):   If true, creates a document containing useful information. (Volume, file size, volumetric error, ...)
        visualize       (bool, optional):   If true, opens a wintow to visualize the 3D mesh after creating it.
    """
    
    # Get the folder path
    this_path = Path(__file__).resolve()
    dir = this_path.parent
    print(f"\n{dir}\n")
        
    # Define the name of the 3D mesh generated
    if out_name == "":
        mesh_name = library[:3] + simplify[:3] + str(simply_val) + smoothing[:3] + str(smooth_val)
    else :
        mesh_name = out_name

    if (library == "pylab") or (library == "pymeshlab"):
        print("\n---------------------\n      PYMESHLAB      \n---------------------\n")
        mesh_gen_pylab()

    if library == "nii2mesh":
        print("\n--------------------\n      NII2MESH      \n--------------------\n")
        mesh_gen_nii2mesh(nii2mesh_path = path.join(dir, "source", "nii2mesh", "src"), 
                  input_file = path.join(dir, "input_files", "gluteus_max.nii.gz"), 
                  out_name = "test_nii2mesh", 
                  out_dir = path.join(dir, "output_files"), 
                  out_type = "obj", 
                  smoothing = "", 
                  smooth_val = 1, 
                  simplify = "", 
                  simply_val = 1, 
                  verbose = True)
        
        
if __name__ == "__main__":
    
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

    