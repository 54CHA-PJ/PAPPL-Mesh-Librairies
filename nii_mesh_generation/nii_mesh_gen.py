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

from os import makedirs, path
from pathlib import Path
from numpy import count_nonzero
import nibabel as nib
import time

from source.mesh_gen_python import mesh_gen_pylab
from source.mesh_gen_python import mesh_gen_vtk
from source.mesh_gen_c import mesh_gen_nii2mesh
from source.mesh_tools import show_obj, vol_obj, doc_obj

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
        out_type        (str, optional):    Choose the output file type                 (DEPENDS ON THE LIBRARY)
        out_dir         (str, optional):    Choose the output file directory.
        out_name        (str, optional):    Choose a name for the file. If no name is chosen, the default name is made using the other parameters.
        # -----------------------------------------------------------------------------------------------------------------------------------------
        info_doc        (bool, optional):   If true, creates a document containing useful information. (Volume, file size, volumetric error, ...)
        visualize       (bool, optional):   If true, opens a wintow to visualize the 3D mesh after creating it.
    
    /!\ If you want to know the (depends on the library) specifications :
        --> Check the README.md file 
        --> or check the end of *this code*
    """
    
    # ------------------------------
    # INITIALIZATION
    # ------------------------------

    # Define the paths
    dir_path = Path(__file__).resolve().parent
    nii2mesh_path = dir_path / "source" / "nii2mesh" / "src"
    mesh_path = None
    initial_time = time.time()
    
    # Validate input parameters
    if simply_val < 5 or simply_val > 100:
        raise ValueError("simply_val must be between 5 and 100. simply_val = 100 creates a mesh with no simplification.")
    if smooth_val < 0 or smooth_val > 10:
        raise ValueError("smooth_val must be between 0 and 10. smooth_val = 0 creates a mesh with no smoothing.")
    
    # Calculate NIFTI volume
    nifti_array = nib.load(nii_dir).get_fdata()
    nbVoxels = count_nonzero(nifti_array)
    ax,ay,az = grid_scale
    volVoxels = nbVoxels*ax*ay*az

    # Create output file's name if not provided
    if out_name == "":
        mesh_name_parts = ["mesh", str(library)]
        if simply_val < 100:
            mesh_name_parts.append(f"simp={simply_val}")
        if smooth_val > 0:
            mesh_name_parts.append(f"smooth={smooth_val}")
        out_name = "_".join(mesh_name_parts)
        
    # Create output folder if it doesn't exist
    makedirs(out_dir, exist_ok=True)
        
    # ------------------------------
    # CREATE THE MESH
    # ------------------------------
    
    if library == "pymeshlab":
        print("\n--------------------\n     PYMESHLAB      \n--------------------\n")
        mesh_path = mesh_gen_pylab(
            input_file = nii_dir, 
            out_name = out_name, 
            out_dir = out_dir, 
            out_type = out_type, 
            simplify = simplify,
            simply_val = simply_val,
            smoothing = smoothing,
            smooth_val = smooth_val,
            grid_scale = grid_scale)
        
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
        
    elif library == "vtk":
        print("\n--------------------\n        VTK        \n--------------------\n")
        mesh_path = mesh_gen_vtk(
                input_file = nii_dir, 
                out_name = out_name, 
                out_dir = out_dir)
        
    else:
        raise ValueError("Wrong Library Name")
    
    if mesh_path == None:
        raise TypeError("Mesh did not generate successfully")

    # ------------------------------
    # SHOW THE MESH
    # ------------------------------
    
    elapsed_time = time.time() - initial_time
    
    print("Calculating volume...")
    volMesh = vol_obj(mesh_path)
    print("Mesh Volume : ", volMesh )
    
    if visualize:
        print("Showing generated Mesh...")
        show_obj(mesh_path)
    
    # ------------------------------
    # SAVE MESH DATA
    # ------------------------------
    
    if info_doc:
        print("Saving Mesh info...")
        doc_obj(
            output_folder   = out_dir,
            name = path.basename(mesh_path),
            mesh_file       = path.basename(mesh_path),
            nifti_file      = path.basename(nii_dir),
            mesh_path       = mesh_path,
            label_volume    = volVoxels,
            mesh_volume     = volMesh,
            error           = abs(volVoxels-volMesh)/volVoxels,
            size            = path.getsize(mesh_path),
            library         = library,
            smoothing       = smoothing,
            smooth_val      = smooth_val,
            simplify        = simplify,
            simply_val      = simply_val,
            elapsed_time    = elapsed_time )



"""
------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------

(DEPENDS ON THE LIBRARY) specifications :

____________________________
____LIBRARY = "pymeshlab"___

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
        --> example : simply_val = 5  # means 5% of the vertices will be kept

___ --> no simplification (RECOMMENDED)
        --> Pymeshlab's simplification methods are likely to create too much volume loss... 
        --> But if you want to simplify the mesh then do "edmc" with some smoothing ("lap", 5)
        
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

------- OUTPUT -------

"obj" = Wavefront 3D Mesh 
    --> The most understandable mesh format
    --> Present in every 3D software
    
"stl" = Stereolithography
    --> Very compressed (50% reduction)
    --> File is not understandable by an human

----- GRID SCALE -----

Default -> (0.55, 0.55, 0.55). 
Without normalization -> (1,1,1).

--> This parameter is only used in Pymeshlab
--> VTK and Nii2mesh libraries have their own way to get the normalization of the labelmap, so grid_scale is not needed.

____________________________
____LIBRARY = "nii2mesh"____

----- SIMPLIFY ------

"(anything)" = Quadratic Mesh Simplification 
    --> The most popular simplification method
        --> simply_val = percentage of simplification
        --> example : simply_val = 5  # means 5% of simplification

""  --> no simplification 
        --> Quadratic Mesh Simplification has a pretty good 
        --> but if you want to simplify the mesh then do "edmc" with some smoothing ("lap", 5)

----- SMOOTHING ------

"(anything)" = Laplacian Coordinate Smoothing (RECOMMENDED)
    --> The most useful one, almost no volume loss
        --> smooth_val = number of iterations
        --> example : smooth_val = 5 # means 5 iterations of smoothing
 
___ --> no smoothing 

------- OUTPUT -------

"obj" / "stl" / "ply" / "fbx"
_________________________
_____LIBRARY = "vtk"_____

--> This library has not been completely researched, so library-specific parameters are unused
--> Only exports to ".obj"

"""