# mesh_gen_c.py

import subprocess
import os
import shutil

def mesh_gen_nii2mesh(nii2mesh_path, input_file, out_name, out_dir, out_type, smoothing = "", smooth_val = 1, simplify = "", simply_val = 1, verbose = False):
    """    
    Generates a mesh using nii2mesh code, made on C.
    
    Args:
        nii2mesh_path (str): The path to the nii2mesh executable.
        input_file (str): The input file for generating the mesh.
        out_name (str): The name of the output file.
        out_dir (str): The directory where the output file will be saved.
        out_type (str): The file type of the output file.
        smoothing (str, optional): The smoothing parameter for the mesh generation. Defaults to "".
        smooth_val (int, optional): The value for the smoothing parameter. Defaults to 1.
        simplify (str, optional): The simplification parameter for the mesh generation. Defaults to "".
        simply_val (int, optional): The value for the simplification parameter. Defaults to 1.
        verbose (bool, optional): Whether to show verbose output. Defaults to False.
    
    Raises:
        FileNotFoundError: If the nii2mesh executable is not found.
        subprocess.CalledProcessError: If the nii2mesh command fails to execute.
    
    Notes:
        - This function may not work properly for different issues:
            - Your Web Browser can detect nii2mesh.exe as a Virus, please click on "Download Anyway".
            - Windows can detect nii2mesh.exe as a Virus, please click on "Run Anyway".
            - You may need to install some DLLs, please download them (64 bit version) on https://www.dll-files.com/ and place them into C:/Windows/System32. For example, "zlib1.dll" may be required.
            - To know the origin of an issue, please execute "nii2mesh.exe" directly, since Python won't explain the errors and just say something like "FileNotFound" Error (because the .obj file will not be generated).
        - Link to the source code: https://github.com/neurolabusc/nii2mesh
    """
    
    param = ""
    
    if (smoothing != ""):
        param += f"-s {str(smooth_val)} "
    
    if (simplify != ""):
        param += f"-r {str(simply_val)} "
    
    if verbose:
        param += "-v 1"
    
    command = f'nii2mesh {input_file} {param} {out_name}{"." + out_type}'
    full_command = f' cd /D {nii2mesh_path} && {command}'
    
    try:
        subprocess.run(['cmd', '/C', 'start', '/wait','cmd', '/C', f'cd /D {nii2mesh_path} && {full_command}'], check=True)
    except FileNotFoundError:
        raise FileNotFoundError("nii2mesh executable not found.")
    except subprocess.CalledProcessError:
        raise subprocess.CalledProcessError("nii2mesh command failed to execute.")
    
    file = f'{nii2mesh_path}\\{out_name}{"." + out_type}'
    
    # Create the directory if it doesn't exists
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    # Handle duplicates
    try:
        shutil.move(file, out_dir)
    except shutil.Error:
        suffix = 1
        new_file = file + f"_{suffix}"
        while os.path.exists(os.path.join(out_dir, new_file)):
            # Keep incrementing the suffix until we find a unique name
            suffix += 1
            new_file = file + f"_{suffix}"
        shutil.move(file, os.path.join(out_dir, new_file))
        print(f"Saved {new_file} in {out_dir}")
    else:
        print(f"Saved {file} in {out_dir}")

