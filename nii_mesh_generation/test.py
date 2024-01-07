from os import path
from pathlib import Path

from nii_mesh_gen import generate_from_nii
from os import path
from pathlib import Path
from source.mesh_gen_python import mesh_gen_pylab
from source.mesh_gen_python import mesh_gen_vtk
from source.mesh_gen_c import mesh_gen_nii2mesh
from source.mesh_tools import show_obj, vol_obj, doc_obj

path = "C:\\Users\\sacha\\Documents\\VSCodeProjects\\PAPPL\\Mesh_Source\\nii_mesh_generation\\output_files\\TEST_N2M_2.obj"
#show_obj(path)

print(vol_obj(path))