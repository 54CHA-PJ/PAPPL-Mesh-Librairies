from vedo import load, Plotter
from os import listdir, path
import numpy as np
import time
import trimesh
import vtk

def showObj(mesh_path):
    print("_____________________")
    print(mesh_path)
    mesh = load(mesh_path).color('gray')
    plt = Plotter(bg='lightgray')
    plt += mesh
    plt.title=mesh_path
    plt.show(interactive=True)
    plt.close()