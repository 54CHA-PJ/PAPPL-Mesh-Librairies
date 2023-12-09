import subprocess
import os
import shutil

def executer_nii2mesh(input_file, output_file, out_type, smoothing, simplify, verbose, nii2mesh_path,out_dir):
    #CONDITIONS
    param = ""
    
    if smoothing:
        smoothing_value = input("Insert a value between 1 and 10: ")
        param += f"-s {str(smoothing_value)} "

    # -r v    reduction factor (default 0.25)
    if simplify:
        simplify_value = input("Insert a value between 0.05 and 1: ")
        param += f"-r {str(simplify_value)} "
        # -v v    verbose (0=silent, 1=verbose, default 0)
    if verbose:
        param += "-v 1"

    ############################################################################   
    if (out_type == "obj"):
        out_type=".obj"
    elif (out_type == "stl"): 
        out_type=".stl"
    elif (out_type == "ply"):
        out_type=".ply"
    elif (out_type == "vtk"):
        out_type=".vtk"
    ############################################################################   
    command = f'nii2mesh {input_file} {param} {output_file}{out_type}'
    full_command = f' cd /D {nii2mesh_path} && {command}'
    ############################################################################
    # Execute the command
    subprocess.run(['cmd', '/C', 'start', '/wait','cmd', '/C', f'cd /D {nii2mesh_path} && {full_command}'], check=True)
    ############################################################################
    #STOCKAGE
    file = f'{nii2mesh_path}{output_file}{out_type}'
    print(out_dir)
    print (file)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    shutil.move(file, out_dir)  
    
    

if __name__ == "__main__":
    executer_nii2mesh('gluteus_max.nii', 'gluteus_max_PRUEBA_2', 'obj', True, True, True, 'C:\\Users\\bebom\\nii2mesh\\src\\','C:\\Users\\bebom\\nii2mesh\\src\\Archivos creados\\')
