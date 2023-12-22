"""
Authors: Sacha Cruz, Mario Espinoza
Date: 05/12/2023
________________________________
|                              |
|   NIFTI -> MESH GENERATION   |
|______________________________|

This script takes a labeled NIFTI (.nii or .nii.gz) file and converts it into a 3D mesh. 

(IMPORTANT) Notes:
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

from os import path
from pathlib import Path

from source.mesh_gen_python import mesh_gen_pylab
from source.mesh_gen_python import mesh_gen_vtk
from source.mesh_gen_c import mesh_gen_nii2mesh


def generate_from_nii(
        nii_dir, 
        grid_scale  = (0.55, 0.55, 0.55),
        library     = "pymeshlab", 
        simplify    = "", 
        simply_val  = 100,
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
        smooth_val      (int, optional):  The coefficient of the smoothing method.      (DEPENDS ON THE LIBRARY)
        simply_val      (int, optional):  The coefficient of the simplifying method.    (DEPENDS ON THE LIBRARY)
        # -----------------------------------------------------------------------------------------------------------------------------------------
        out_type        (str, optional):    Choose the output file type : "obj" / "stl".(DEPENDS ON THE LIBRARY)
        out_dir         (str, optional):    Choose the output file directory.
        out_name        (str, optional):    Choose a name for the file. If no name is chosen, the default name is made using the other parameters.
        # -----------------------------------------------------------------------------------------------------------------------------------------
        info_doc        (bool, optional):   If true, creates a document containing useful information. (Volume, file size, volumetric error, ...)
        visualize       (bool, optional):   If true, opens a wintow to visualize the 3D mesh after creating it.
    
    --> If you want to know the (depends on the library) specifications, please take a look at the README.md file
    """

    # Define the paths
    dir_path = Path(__file__).resolve().parent
    nii2mesh_path = dir_path / "source" / "nii2mesh" / "src"
    mesh_path = None
    
    # Validate input parameters
    if simply_val < 5 or simply_val > 100:
        raise ValueError("simply_val must be between 5 and 100. simply_val = 100 creates a mesh with no simplification.")
    if smooth_val < 0 or smooth_val > 10:
        raise ValueError("smooth_val must be between 0 and 10. smooth_val = 0 creates a mesh with no smoothing.")

    # Construct output file name if not provided
    if not out_name:
        mesh_name_parts = ["mesh", str(library)]
        if simply_val < 100:
            mesh_name_parts.append(f"simp={simply_val}")
        if smooth_val > 0:
            mesh_name_parts.append(f"smooth={smooth_val}")
        out_name = "_".join(mesh_name_parts)
    
    if library == "pymeshlab":
        print("\n--------------------\n     PYMESHLAB      \n--------------------\n")
        
    elif library == "nii2mesh":
        print("\n--------------------\n      NII2MESH      \n--------------------\n")
        mesh_path = mesh_gen_nii2mesh(
                nii2mesh_path = str(nii2mesh_path),  
                input_file = nii_dir, 
                out_name = out_name, 
                out_dir = out_dir, 
                out_type = out_type, 
                simply_val = simply_val,
                smooth_val = smooth_val,
                verbose = True)
        print("mesh path :", mesh_path)
    else:
        raise ValueError("Wrong Library Name")

    return mesh_path


"""
____________________________

    LIBRARY = "pymeshlab"
____________________________




---------------------
----- SIMPLIFY ------

"edmc" = Edge Decimation for Marching Cubes 
    --> The most useful one, but the simplification may be a bit too intense
        --> simply_val not needed
        
"edqe" = Edge Decimation Quadratic Edge Collapse (~ USELESS)  
    --> Empirically useless - mesh is not simplified - maybe it's useful for non-marching cubes meshes
        --> simply_val not needed

"mdc"  = Meshing Decimation Clustering            
    --> Simplification is too intense, mesh loses its volume properties
        --> simply_val = percentage of simplification
        --> example : simply_val = 5  # means 5% of simplification

___ --> no simplification (RECOMMENDED)
        --> Pymeshlab's simplification methods are likely to create too much volume loss... 
        --> But if you want to simplify the mesh then do "edmc" with some smoothing ("lap", 5)
        
----------------------
----- SMOOTHING ------

"lap" = Laplacian Coordinate Smoothing (RECOMMENDED)
    --> The most useful one, almost no volume loss
        --> smooth_val = number of iterations
        --> example : smooth_val = 5 # means 5 iterations of smoothing
    
"hc" = Laplacian Coordinate Smoothing - HC method (~ USELESS)  
    --> Empirically useless - mesh is not smoothed - maybe it's useful for non-marching cubes meshes
        --> smooth_val not needed
    
"tau"  = Taubin Coordinate Smoothing (~ USELESS)      
    --> Empirically useless - mesh is not smoothed - maybe it's useful for non-marching cubes meshes
        --> smooth_val not needed
        
___ --> no smoothing 

----------------------
------- OUTPUT -------

"obj" = Wavefront 3D Mesh 
    --> The most understandable mesh format
    --> Present in every 3D software
    
"stl" = Stereolithography
    --> Very compressed (50% reduction)
    --> File is not understandable by an human
    
----------------------
----- GRID SCALE -----

Default -> (0.55, 0.55, 0.55). 
Without normalization -> (1,1,1).

--> This parameter is only used in Pymeshlab
--> VTK and Nii2mesh libraries have their own way to get the normalization of the labelmap, so grid_scale is not needed.




____________________________

    LIBRARY = "nii2mesh"
____________________________




---------------------
----- SIMPLIFY ------

"(anything)" = Quadratic Mesh Simplification 
    --> The most popular simplification method
        --> simply_val = percentage of simplification
        --> example : simply_val = 5  # means 5% of simplification

""  --> no simplification 
        --> Quadratic Mesh Simplification has a pretty good 
        --> but if you want to simplify the mesh then do "edmc" with some smoothing ("lap", 5)
        
----------------------
----- SMOOTHING ------

"(anything)" = Laplacian Coordinate Smoothing (RECOMMENDED)
    --> The most useful one, almost no volume loss
        --> smooth_val = number of iterations
        --> example : smooth_val = 5 # means 5 iterations of smoothing
 
___ --> no smoothing 

----------------------
------- OUTPUT -------

"obj" / "stl" / "ply" / "fbx"




_________________________

     LIBRARY = "vtk"
_________________________




--> This library has not been completely researched, so library-specific parameters are unused

--> Only exports to ".obj"


"""