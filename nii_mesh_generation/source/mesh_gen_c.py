# mesh_gen_c.py

import subprocess
import os
import shutil

def mesh_gen_nii2mesh(nii2mesh_path, input_file, out_name, out_dir, out_type, smooth_val = 0, simply_val = 100, verbose = False):
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
    
    param += f"-s {str(smooth_val)} "       # Value between 1 and 10
    param += f"-r {str(simply_val/100)} "   # Value between 0.05 and 1
    if verbose :
        param += "-v 1"
    
    print(param)
    command = f'nii2mesh {input_file} {param} {out_name}{"." + out_type}'
    full_command = f'cd {nii2mesh_path} && {command}'
    
    try:
        subprocess.run(full_command, shell=True, check=True, cwd=nii2mesh_path)
    except FileNotFoundError:
        raise FileNotFoundError("nii2mesh executable not found.")
    except subprocess.CalledProcessError:
        raise subprocess.CalledProcessError("nii2mesh command failed to execute.")
    
    file = os.path.join(nii2mesh_path, f'{out_name}{"." + out_type}')
    
    # Create the directory if it doesn't exists
    os.makedirs(out_dir, exist_ok=True)
    
    # Saving the file
    # Handles duplicates by creating "suffixes" of already existing names
    try:
        shutil.move(file, out_dir)
        new_file = file
    except shutil.Error:
        suffix = 1
        new_file_name = f"{out_name}_{suffix}.{out_type}" 
        new_file = os.path.join(out_dir, new_file_name) 
        while os.path.exists(new_file):
            suffix += 1
            new_file_name = f"{out_name}_{suffix}.{out_type}" 
            new_file = os.path.join(out_dir, new_file_name) 
        shutil.move(file, new_file)
    
    print("TREST#ETSTEET")
    return new_file




