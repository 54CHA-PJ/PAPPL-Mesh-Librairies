# Mesh generation from NIFTI files using Python and C Libraries

Authors: **Sacha Cruz, Mario Espinoza**

Date: **05/12/2023**
```c
________________________________
|                              |
|   NIFTI -> MESH GENERATION   |
|______________________________|

Requirements:
- To use the Nii2Mesh library, you need Windows OS because it requires Command Prompt.
- You can also write the command manually in Linux or Mac environments. (See the nii2mesh section)

Compatibility:
- The script works well on Python versions 3.8 - 3.11.
- Mesh visualization may not be compatible with Python 3.10 - 3.11.
```

## About the project

This script takes a single-labeled NIFTI file (.nii / .nii.gz) and converts it into a 3D mesh (.obj / .stl / .ply / .3ds). 

More precisely, the code allows to :
* Create a 3D mesh from a NIFTI file
    * Choose the library (Pymeshlab, VTK or Nii2Mesh)
    * Set a mesh-smoothing value 
    * Set a mesh-simplification value
* Show the mesh in a 3D object visualizer
* Store Mesh's details (Mesh volume, File size, etc.) in a TXT file


It uses already-existing libraries :
- Pymeshlab : [(Doc)](myLib/README.md)
- VTK (Python) : [(Doc)](myLib/README.md)
- Nii2mesh (C) : [(GitHub)](myLib/README.md)

## Project hierarchy and files

1. The main code is under the folder : **nii_mesh_generation** 
    * The main function is on the _*nii_mesh_gen.py*_ file
    * You can learn how it works on the _*test_nii_mesh_gen.py*_ file
    * It calls functions from internal libraries :
        * *mesh_gen_c.py* : calls nii2mesh library made on C
        * *mesh_gen_python.py* : calls pymeshlab and vtk libraries
        * *mesh_tools.py* : provides useful tools for mesh visualization and details

2. The additional code is under the folder : **additional_mesh_utils** 
    * _*test_libraries_311.py*_ --> Create a bunch of 3D objects (trying different libraries, methods and parameters)
    * _*objtools.py*_ --> provides a lot of useful tools :
        * Visualize a 3D Mesh in a 3D interactiuve window
        * Save the current 3D view of a Mesh in a flat 2D image
        * Save the current Mesh's details in an excel file
        * Automatizate these functions to a whole folder containing different meshes
    * --> The purpose is to call the function _*showFolder*_ in the folder where all the 3D meshes where created, to see every mesh one by one
    * _*test_mesh_simple.py*_ --> tests the showObj function
    * _*test_mesh_folder.py*_ --> tests the showFolder function

> nii_mesh_generation
> > *_nii_mesh_gen.py_* <br>
> > _test_niimeshgen.py_ <br>
> > source
> > > _mesh_gen_c_ <br>
> > > _mesh_gen_python_ <br>
> > > _mesh_tools_ <br>

> additional_mesh_utils <br>
> > *_objtools.py_* <br>
> > _test_libraries_311.py_ <br>
> > *_test_libraries_308.py_* <br>


## SPECIFICATIONS 

Here are the details of the function **generate_from_nii** in the code _nii_mesh_gen.py_

```python
def generate_from_nii(
        nii_dir, # location of the NIFTI file
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
```

Parameters are described below :

```sql   
nii_dir         (str):              Location of the NIFTI file.
grid_scale      (tuple, optional):  Grid normalization coefficients.
             
library         (str, optional):    Choose the library : "pymeshlab" / "nii2mesh" / "vtk".

simplify        (str, optional):    Choose the simplification method.           (DEPENDS OF THE LIBRARY)
smoothing       (str, optional):    Choose the smoothing method.                (DEPENDS OF THE LIBRARY)
smooth_val      (float, optional):  The coefficient of the smoothing method.    (DEPENDS OF THE LIBRARY)
simply_val      (float, optional):  The coefficient of the simplifying method.  (DEPENDS OF THE LIBRARY)
out_type        (str, optional):    Choose the output file type : "obj" / "stl".(DEPENDS OF THE LIBRARY)

out_dir         (str, optional):    Choose the output directory.
out_name        (str, optional):    Choose a name for the file. If no name is chosen, the default name is made using the other parameters.
info_doc        (bool, optional):   If true, creates a document containing useful information. (Volume, file size, volumetric error, ...)

visualize       (bool, optional):   If true, opens a wintow to visualize the 3D mesh after creating it.
```

### LIBRARY = "pymeshlab"

```sql   
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

```


### LIBRARY = "nii2mesh"

```sql

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

```

### LIBRARY = "vtk"

```sql
--> This library has not been completely researched, so library-specific parameters are unused

--> Only exports to ".obj"

```
