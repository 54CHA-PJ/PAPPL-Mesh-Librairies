def show_obj(mesh_path):
    from vedo import load, Plotter
    print("_____________________")
    print(mesh_path)
    mesh = load(mesh_path).color('gray')
    plt = Plotter(bg='lightgray')
    plt += mesh
    plt.title=mesh_path
    plt.show(interactive=True)
    plt.close()
    
def vol_obj(file_path):
    import vtk
    reader = vtk.vtkOBJReader()
    reader.SetFileName(file_path)
    reader.Update()
    # Create a mass properties filter and set the input
    mass = vtk.vtkMassProperties()
    mass.SetInputConnection(reader.GetOutputPort())
    # Print the volume
    volume = mass.GetVolume()
    return(volume)
    
def doc_obj(
    mesh_file,
    nifti_file,
    mesh_path,
    label_volume,
    mesh_volume,
    error,
    size,
    library,
    smoothing,
    smooth_val,
    simplify,
    simply_val,
    elapsed_time):
    
    import datetime
    current_date_time = datetime.datetime.now().strftime("%m/%d/%Y - %H:%M:%S")

    with open("output.txt", "w") as file:
        file.write("Mesh file\t: {}\n".format(mesh_file))
        file.write("Nifti file\t: {}\n\n".format(nifti_file))
        file.write("--- INFO ---\n")
        file.write("\nLabel-map Volume (cm^3)\t: {}\n".format(label_volume))
        file.write("Mesh Volume (cm^3)\t: {}\n\n".format(mesh_volume))
        file.write("Conversion Volumetric Error : {} %\n".format(error))
        file.write("Size\t: {}\n\n".format(size))
        file.write("--- PARAMETERS ---\n")
        file.write("\nlibrary\t: {}\n".format(library))
        file.write("smoothing\t: {}\n".format(smoothing))
        file.write("smooth_val\t: {}\n".format(smooth_val))
        file.write("simplify\t: {}\n".format(simplify))
        file.write("simply_val\t: {}\n\n".format(simply_val))
        file.write("--- OTHER ---\n")
        file.write("\nElapsed time\t: {} s\n".format(elapsed_time))
        file.write("Date\t: {}\n".format(current_date_time))
        file.write("\n{}".format(mesh_path))

        
