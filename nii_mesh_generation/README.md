# NIIFTI MESH GENERATION (nii_mesh_gen.py)

Authors: **Sacha Cruz, Mario Espinoza**
Date: **28/01/2024**
```c
________________________________
|                              |
|   NIFTI -> MESH GENERATION   |
|             ---              |
|        nii_mesh_gen.py       |
|______________________________|

This code uses three functional libraries (Pymeshlab, VTK and Nii2Mesh) to convert a binary Label-map on a NIFTI format to a Mesh.

REQUIREMENTS:
- To use the Nii2Mesh library, you need Windows OS because it requires Command Prompt.
- You can also write the command manually in Linux or Mac environments. (See the nii2mesh section)

COMPATIBILITY:
- The script works well on Python versions 3.8 - 3.11.
- Mesh visualization may not be compatible with Python 3.10 - 3.11.
- Library versions :
    - Pymeshlab : 2022.2.post4
    - VTK : 9.3.0
    - Nii2Mesh : 1.0.2
    - vedo : 2023.5.0
```

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

simplify        (str, optional):    Choose the simplification method.           (DEPENDS ON THE LIBRARY)
smoothing       (str, optional):    Choose the smoothing method.                (DEPENDS ON THE LIBRARY)
smooth_val      (float, optional):  The coefficient of the smoothing method.    (DEPENDS ON THE LIBRARY)
simply_val      (float, optional):  The coefficient of the simplifying method.  (DEPENDS ON THE LIBRARY)
out_type        (str, optional):    Choose the output mesh file type.           (DEPENDS ON THE LIBRARY)

out_dir         (str, optional):    Choose the output directory.
out_name        (str, optional):    Choose a name for the file. If no name is chosen, the default name is made using the other parameters.
info_doc        (bool, optional):   If true, creates a TXT document containing useful information. (Volume, file size, volumetric error, ...)

visualize       (bool, optional):   If true, opens a window to visualize the 3D mesh after creating it.
```
## (DEPENDS ON THE LIBRARY) DETAILS :

### LIBRARY = "pymeshlab"

```python
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
    --> Most useful smoothing method, almost no volume loss
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

```python

For nii2mesh, the variables "simplify" and "smoothing" are not needed since there's only one method for each one.
Instead, the code will detect if you chose coherent "simply_val" and "smooth_val" values

----- SIMPLIFY ------

if (0 < simply_val < 100):
___ --> Quadratic Mesh Simplification (RECOMMENDED)
    --> Most popular simplification method
        --> simply_val = percentage of simplification
        --> example : simply_val = 5  # means 5% of simplification

else:
___ --> No simplification 

----- SMOOTHING ------

if (1 <= smooth_val <= 10):
___ --> Laplacian Coordinate Smoothing (RECOMMENDED)
    --> Most popular smoothing method
        --> smooth_val = number of iterations
        --> example : smooth_val = 5 # means 5 iterations of smoothing

else:
___ --> No smoothing 

------- OUTPUT -------

"obj" / "stl" / "ply" / "fbx"

```

### LIBRARY = "vtk"

```sql
--> This library has not been completely researched, so library-specific parameters are unused

--> Only exports to ".obj"

```
