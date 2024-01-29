# Mesh generation from NIFTI files using Python and C Libraries

Authors: **Sacha Cruz, Mario Espinoza**

Date: **28/01/2024**
```c
________________________________
|                              |
|   NIFTI -> MESH GENERATION   |
|______________________________|

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
- Pymeshlab : [(GitHub)](https://github.com/neurolabusc/nii2mesh)
- VTK (Python) : [(GitHub)](https://github.com/Kitware/VTK)
- Nii2mesh (C) : [(GitHub)](https://github.com/cnr-isti-vclab/PyMeshLab)

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