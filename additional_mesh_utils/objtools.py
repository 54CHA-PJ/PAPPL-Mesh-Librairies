from vedo import load, Plotter
from os import listdir, path
import numpy as np
import time
import trimesh
import vtk

# ----------------------------------
# Afficher un .obj
                
def showObj(mesh_path, pitch=-30, yaw=30, roll =0, z=1, save_image = False, show_3d = True, output_folder_path="."):
    """shows a 3d parametrable view of the object. has an option to save the view into a flat image file
    Args:
        mesh_path (_type_): path to the mesh
        pitch (int, optional): view angle parameter. Defaults to -30.
        yaw (int, optional): view angle parameter. Defaults to 30.
        roll (int, optional): view angle parameter. Defaults to 0.
        z (int, optional): zoom level. Defaults to 1.
        save_image (bool, optional): save the image as a jpg. Defaults to False.
        show_3d (bool, optional): if false, the plot is not showed 
    """
    print("_____________________")
    print(mesh_path)
    mesh = load(mesh_path).color('gray')
    if save_image: 
        plt = Plotter(bg='white', offscreen=True) # the plot will not be showed
        plt += mesh
        plt.camera.Pitch(pitch)
        plt.camera.Yaw(yaw)
        plt.camera.Roll(roll)
        plt.show(zoom=z, interactive=False)
        plt.screenshot(filename=path.join(output_folder_path, path.basename(mesh_path) + ".png"))
        plt.close()
    if show_3d: 
        plt2 = Plotter(bg='black')
        plt2 += mesh
        plt2.camera.Pitch(pitch)
        plt2.camera.Yaw(yaw)
        plt2.camera.Roll(roll)
        plt2.title=mesh_path
        plt2.show(zoom=z, interactive=True)
        plt2.close()
        
def showFolder(folder_path, pitch=-30, yaw=30, roll =0,  z=1, save_image=False, show_details=False, show_3d=True, name="", output_folder_path="."):
    print("\n ----- 3D FILES ----- \n")
    data = {'File Name': [], 'File Size (B)': [], 'File Size (MB)': [], 'Mesh Volume': []}
    for file in listdir(folder_path):
        if file.endswith(".obj") or file.endswith(".stl"):
            # Montrer l'objet
            showObj(path.join(folder_path, file), pitch, yaw, roll, z, save_image, show_3d, output_folder_path)
            # Donner la taille de l'objet
            if show_size:
                file_size = path.getsize(path.join(folder_path, file))
                # Save data in the dictionary
                data['File Name'].append(file)
                data['File Size (B)'].append(file_size)
                data['File Size (MB)'].append(file_size / (1024 * 1024))
                data['Mesh Volume'].append(volume(path.join(folder_path, file)))
    if show_details:
        import pandas as pd
        import openpyxl
        # Create a DataFrame
        df = pd.DataFrame(data)
        # Save DataFrame to Excel file
        excel_file_path = name + '_file_sizes.xlsx'
        df.to_excel(excel_file_path, index=False)
        print(f"File sizes saved to {excel_file_path}")
        

def showObjCam(mesh_path, cam, z=1, save_image=False, show_3d=True, output_folder_path="."):
    """shows a 3d parametrable view of the object. has an option to save the view into a flat image file
    Args:
        mesh_path (_type_): path to the mesh
        cam (dictionnary): camera to view and save the mesh
        z (int, optional): zoom level. Defaults to 1.
        save_image (bool, optional): save the image as a jpg. Defaults to False.
        show_3d (bool, optional): if false, the plot is not showed 
    """
    print("_____________________")
    print(mesh_path)
    try:
        mesh = load(mesh_path).color('gray')
    except FileNotFoundError:
        print("File not found")
        return 0

    if save_image:
        plt = Plotter(bg='white', offscreen=True)  # the plot will not be showed
        plt += mesh
        plt.camera.SetPosition(cam['position'])
        plt.camera.SetFocalPoint(cam['focal_point'])
        plt.camera.SetViewUp(cam['viewup'])
        plt.camera.SetDistance(cam['distance'])
        plt.camera.SetClippingRange(cam['clipping_range'])
        plt.show(zoom=z, interactive=False)
        plt.screenshot(filename=path.join(output_folder_path, path.basename(mesh_path) + ".png"))
        plt.close()
    if show_3d:
        plt2 = Plotter(bg='black')
        plt2 += mesh
        plt2.title = mesh_path
        plt2.camera.SetPosition(cam['position'])
        plt2.camera.SetFocalPoint(cam['focal_point'])
        plt2.camera.SetViewUp(cam['viewup'])
        plt2.camera.SetDistance(cam['distance'])
        plt2.camera.SetClippingRange(cam['clipping_range'])
        plt2.show(zoom=z, interactive=True)
        plt2.close()

def showFolderCam(folder_path, cam, z=1, save_image=False, show_details=False, show_3d=True, name="", output_folder_path="."):
    """show all the 3d meshes in the folder
    Args:
        folder_path (string): path to the folder containing the meshes
        show_size (bool, optional): shows each file's size and saves it in an Excel Spreadsheet. Defaults to False.
        name (string, optional): name of the Excel spreadsheet
    """
    print("\n ----- 3D FILES ----- \n")
    data = {'File Name': [], 'File Size (B)': [], 'File Size (MB)': [], 'Mesh Volume': []}
    for file in listdir(folder_path):
        if file.endswith(".obj") or file.endswith(".stl"):
            # Montrer l'objet
            showObjCam(path.join(folder_path, file), cam, z, save_image, show_3d, output_folder_path)
            # Donner la taille de l'objet
            if show_size:
                file_size = path.getsize(path.join(folder_path, file))
                # Save data in the dictionary
                data['File Name'].append(file)
                data['File Size (B)'].append(file_size)
                data['File Size (MB)'].append(file_size / (1024 * 1024))
                data['Mesh Volume'].append(volume(path.join(folder_path, file)))
    if show_details:
        import pandas as pd
        import openpyxl
        # Create a DataFrame
        df = pd.DataFrame(data)
        # Save DataFrame to Excel file
        excel_file_path = name + '_file_sizes.xlsx'
        df.to_excel(excel_file_path, index=False)
        print(f"File sizes saved to {excel_file_path}")

# ----------------------------------
# Volume d'un mesh

def convex_hull_volume(file_path):
    import pymeshlab
    from scipy.spatial import ConvexHull
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(file_path)
    mesh = ms.current_mesh()
    vertices = mesh.vertex_matrix() 
    hull = ConvexHull(vertices)
    return hull.volume 
    
def volume(file_path):
    import pymeshlab
    mset = pymeshlab.MeshSet()
    mset.load_new_mesh(file_path)
    return (pymeshlab_volume(mset))

def trimesh_volume(mesh):
    vol = abs(round(mesh.volume, 2))
    return vol

def pymeshlab_volume(meshset):
    try:
        out_dict = meshset.get_geometric_measures()
        mesh_volume = out_dict['mesh_volume']
        vol = abs(round(mesh_volume, 2))
        return vol
    except:
        return 0.00

def voxelfuse_volume(mesh):
    mesh_tri = trimesh.Trimesh(vertices=mesh.verts, faces=mesh.tris)
    return trimesh_volume(mesh_tri)

def vtk_volume(model_vtk):
    mass_vtk = vtk.vtkMassProperties()
    mass_vtk.SetInputConnection(model_vtk.GetOutputPort())
    vol = mass_vtk.GetVolume()
    return abs(round(vol, 2))

def pymeshlab_surface(meshset):
    out_dict = meshset.get_geometric_measures()
    surf_area = out_dict['surface_area']
    surf = abs(round(surf_area, 2))
    return surf

def showError(nbVoxels, volume):
    """shows the error between two volumes
    Args:
        nbVoxels (int): volume to be compared to
        volume (int): volume that is compared to nbVoxels
    """
    diff = abs(nbVoxels-volume)
    # print("Différence volumétrique: ", diff)
    
    print("Erreur volumétrique: \n",round((diff/nbVoxels)*100, 5), "%")

# ----------------------------------
# Temps d'execution

def affiche_temps(t_init):
    print(time.time()-t_init)
    return (time.time())

def show_size(file_path):
    file_size = path.getsize(file_path)
    print(f"{file_size/1024} kilo-bytes")
    
    