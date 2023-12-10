<python>
________________________________
|                              |
|   NIFTI -> MESH GENERATION   |
|______________________________|

Authors : Sacha Cruz , Mario Espinoza
Date : 05/12/2023

Works perfectly with Python versions    : 3.8 - 3.9
Also works with Python versions         : 3.8 - 3.11 (if you dont visualize the mesh)

This program takes a label-map NIFTI (.nii /.nii.gz) file and creates a 3D Mesh from it 

--> If you want to see other useful functions that weren't needed for this function
    --> check "additional_mesh_utils" 

Args (generate_from_nii) :

    nii_dir         (str):              Location of the NIFTI file.
    grid_scale      (tuple, optional):  Grid normalization values.                  (DEPENDS ON THE LIBRARY)
    
    library         (str, optional):    Choose the library : "pymeshlab" / "nii2mesh" / "vtk".
    
    simplify        (str, optional):    Choose the simplification method.           (DEPENDS ON THE LIBRARY)
    smoothing       (str, optional):    Choose the smoothing method.                (DEPENDS ON THE LIBRARY)
    smooth_val      (float, optional):  The coefficient of the smoothing method.    (DEPENDS ON THE LIBRARY)
    simply_val      (float, optional):  The coefficient of the simplifying method.  (DEPENDS ON THE LIBRARY)
    
    out_type        (str, optional):    Choose the output file type : "obj" / "stl".(DEPENDS ON THE LIBRARY)
    out_dir         (str, optional):    Choose the output directory.
    out_name        (str, optional):    Choose a name for the file. If no name is chosen, the default name is made using the other parameters.
    
    info_doc        (bool, optional):   If true, creates a document containing useful information. (Volume, file size, volumetric error, ...)
    visualize       (bool, optional):   If true, opens a wintow to visualize the 3D mesh after creating it.


** SPECIFICATIONS **

___________________________

LIBRARY = "pymeshlab"
___________________________

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

--> Only used in Pymeshlab
--> VTK and Nii2mesh libraries have their own way to get the normalization of the labelmap, so grid_scale is not needed.
    
___________________________

LIBRARY = "nii2mesh"
___________________________

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

___________________________

LIBRARY = "vtk"
___________________________

--> This library has not been completely researched, so library-specific parameters are unused

--> Only exports to ".obj"
