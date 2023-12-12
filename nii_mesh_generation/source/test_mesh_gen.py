# Test.py

from os import getcwd, chdir, path
from pathlib import Path

from mesh_gen_c import mesh_gen_nii2mesh      

this_path = Path(__file__).resolve()
dir = this_path.parent.parent
print(f"\n{dir}\n")

print("\n ------ TEST NII2MESH ------ \n")

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
