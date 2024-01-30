# ADDITIONAL MESH UTILS (nii_mesh_gen.py)

Authors: **Sacha Cruz**
Date: **28/01/2024**
```c
________________________________
|                              |
|   NIFTI -> MESH GENERATION   |
|             ---              |
|    additional_mesh_utils     |
|______________________________|

These files generates plenty of meshes in one batch to compare each different parameter of conversion of each library. Python mesh libraries used here are : (TODO)
    - PyMeshLab (Mesh creation): 
    - VTK (Mesh creation):
    - Nii2Mesh (Mesh creation):
    - VoxelFuse (Mesh creation):
    - Trimesh (Mesh creation)
    - Vedo (Plotting):

COMPATIBILITY:
- The main script works well on Python versions 3.8 - 3.11.
- Mesh visualization may not be compatible with Python 3.10 - 3.11.
- Trimesh and Voxelfuse smoothing and simplification functions don't work yet
- Version of the libaries :
    - Pymeshlab : 2022.2.post4
    - VTK : 9.3.0
    - Nii2Mesh : 1.0.2
    - Trimesh : 4.0.4
    - Voxelfuse : 1.2.8
    - vedo : 2023.5.0 (Visualization)
```

### (MAIN) test_libraries_311.py

Main program that generates meshes from all the libraries mentionned above. Some not-working libraries are shown at the end of the code.

### (MAIN) objtools.py

This file contains some useful functions like :
- Mesh visualization (showObj and showObjCam)
- Volume calculation (vol_obj, vol_obj_2, etc.)
- Folder procedures (showFOlder, showFolderCam)
    - show all the meshes in a folder
    - save all pictures of the meshes
    - save all the meshes data (size, volume, etc.) under an Excel file

### (MAIN) test_mesh_folder.py

Main program that tests **objtools.py** functions on a folder of meshes generatew with **test_libraries_311.py**

### (USELESS) test_libraries_38.py

Small complementary program that was supposed to generate meshes from some libraries (Trimesh, VoxelFuse and Pymesh) that couldn't work with Python 3.11. However, most of the functions still don't work even with Python 3.8. 

### (USELESS) test_mesh_simple.py

Program that tests **objtools.py** functions on meshes one by one
