"""
Authors : Sacha Cruz , Mario Espinoza
Date : 05/12/2023

Works with Python versions : 3.8 - 3.11
_____________________________
|                           |
|   NIFTI MESH GENERATION   |
|___________________________|

This program takes a label-map NIFTI (.nii /.nii.gz) file and creates a 3D Mesh from it 

Please refer to the "additional_mesh_utils" to see other useful functions that weren't needed for this function

"""

from os import getcwd, chdir, path
import numpy as np
from nii_mesh_tools import *    # Necessary mesh tools
import nibabel as nib           # Lecture of NIFTI files
from skimage import measure     # Marching Cubes algorithm
import pymeshlab                # Mesh manipulation library
import vtk                      # Mesh manipulation library

dir = getcwd()
print(dir)

def generate_from_nii(
    nii_dir, 
    library     = "pymeshlab", 
    simplify    = "", 
    smoothing   = "", 
    smoothing_value = 0.,
    simplify_value  = 0.,
    info_doc    = True,
    visualize   = True,
    out_type    = "obj",
    out_dir     = ".",
    out_name    = "" ):
    """
    Generates a Mesh (.obj / .stl) from a .nii file.

    Args:
        nii_dir         (str):              Location of the NIFTI file.
        library         (str, optional):    Choose the library : "pymeshlab" / "nii2mesh" / "vtk".
        simplify        (str, optional):    Choose the simplification method.       (DEPENDS ON THE LIBRARY)
        smoothing       (str, optional):    Choose the smoothing method.            (DEPENDS ON THE LIBRARY)
        smoothing_value (float, optional):  The coefficient of the smoothing method.      (DEPENDS ON THE LIBRARY)
        simplify_value  (float, optional):  The coefficient of the simplifying method.    (DEPENDS ON THE LIBRARY)
        info_doc        (bool, optional):   If true, creates a document containing useful information. (Volume, file size, volumetric error, ...)
        visualize       (bool, optional):   If true, opens a wintow to visualize the 3D mesh after creating it.
        out_type        (str, optional):    Choose the output file type : "obj" / "stl".
        out_dir         (str, optional):    Choose the output directory.
        out_name        (str, optional):    Choose a name for the file. If no name is chosen, the default name is made using the other parameters.
    
    -------------------------------------------------------------------------------------------------------------------------------------------------
    
    (DEPENDS ON THE LIBRARY) : SPECIFICATIONS
    
    ---------------------------
    library = "pymeshlab"
    ---------------------------
    
    
    ---------------------------
    library = "nii2mesh"
    ---------------------------
    
    
    ---------------------------
    library = "vtk"
    ---------------------------
    
    """