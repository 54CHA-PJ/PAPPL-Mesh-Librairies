from vedo import load, Plotter
from pymeshlab import MeshSet

def showObj(mesh_path):
    print("_____________________")
    print(mesh_path)
    mesh = load(mesh_path).color('gray')
    plt = Plotter(bg='lightgray')
    plt += mesh
    plt.title=mesh_path
    plt.show(interactive=True)
    plt.close()
    
def volumeObj(mesh_path):
    """Calculates the volume of a Mesh
    Args:
        mesh_path (str): location of the Mesh
    Returns:
        float: volume calculated with Pymeshlab volume integrated function
    """
    mset = MeshSet()
    mset.load_new_mesh(mesh_path)
    return (pymeshlab_volume(mset))

def pymeshlab_volume(meshset):
    """Calculates the volume of a Pymeshlab-type Mesh
    Args:
        meshset (Pymeshlab.Meshset): Mesh Set containing only one mesh
    Returns:
        float: calculated volume if the mesh doesn't have holes
    """
    try:
        out_dict = meshset.get_geometric_measures()
        mesh_volume = out_dict['mesh_volume']
        vol = abs(round(mesh_volume, 2))
        return vol
    except:
        print("Couldn't calculate the volume of the Mesh")
        return 0.00