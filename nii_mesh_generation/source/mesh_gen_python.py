from os import path, getcwd, chdir

def mesh_gen_pylab(
    input_file,
    simplify    = "", 
    simply_val  = 100,
    smoothing   = "", 
    smooth_val  = 0,
    out_type    = "obj",
    out_dir     = ".",
    out_name    = "",
    grid_scale  = (0.55, 0.55, 0.55)):
    
    import pymeshlab
    import nibabel as nib
    from skimage import measure
    
    print("Marching Cubes")
    
    # Read the nii file
    nifti_array = nib.load(input_file).get_fdata()
    # Marching Cubes
    verts, faces, normals, values = measure.marching_cubes(nifti_array)
    # Create Mesh
    mesh = pymeshlab.Mesh(verts, faces)
    # Create Meshset
    mset = pymeshlab.MeshSet()
    mset.add_mesh(mesh)
    
    # ------- SIMPLIFY -------

    if simplify == "edmc":
        print("Edge Decimation for Marching Cubes Meshes")
        mset.meshing_decimation_edge_collapse_for_marching_cube_meshes()
    elif simplify == "edqe":
        print("Edge Decimation Quadratic Edge Collapse")
        mset.meshing_decimation_quadric_edge_collapse()
    elif simplify == "mdc":
        print("Meshing Decimation Clustering : ", simply_val, "%")
        mset.meshing_decimation_clustering(threshold = pymeshlab.Percentage(simply_val))
    else:
        print("No simplification")
    
    # ------- SMOOTHING -------

    if smoothing == "lap":
        print("Laplacian Coordinate Smoothing : ", smooth_val, " iterations")
        mset.apply_coord_laplacian_smoothing(stepsmoothnum = smooth_val) 
    elif smoothing == "tau":
        print("Taubin Coordinate Smoothing")
        mset.apply_coord_taubin_smoothing()
    elif smoothing == "hc":
        print("Laplacian Coordinate Smoothing - HC method")
        mset.apply_coord_hc_laplacian_smoothing() 
    else:
        print("No smoothing")
    
    # ------- SAVING -------
    
    # Grid Scale Normalization
    ax,ay,az = grid_scale
    mset.compute_matrix_from_scaling_or_normalization(axisx=ax, axisy=ay, axisz=az)
    
    # Handles duplicates by creating "suffixes" of already existing names
    new_file = path.join(out_dir, out_name + "." + out_type)
    suffix = 0
    while path.isfile(new_file):    
        suffix += 1
        new_file = path.join(out_dir, out_name + "_" + str(suffix) + "." + out_type)
    mset.save_current_mesh(new_file)
    print(new_file + " saved successfully")
    return new_file
    
def mesh_gen_vtk(input_file, out_dir = ".", out_name = ""):
    import vtk
    from os import getcwd, path, chdir
    # Keep the initial directory in memory
    initial_dir = getcwd()
    # Read the NIFTI file
    nifti_vtk = vtk.vtkNIFTIImageReader()
    nifti_vtk.SetFileName(input_file)
    nifti_vtk.Update()
    # Marching Cubes
    model_vtk = vtk.vtkMarchingCubes()
    model_vtk.SetInputConnection(nifti_vtk.GetOutputPort())
    model_vtk.SetValue(0, 0.5)
    # Create a 3D model from the mesh
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(model_vtk.GetOutputPort())
    # Create an actor for the model
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    # Create a renderer for the scene
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    # Create a render window for the scene
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    # Handles duplicates by creating "suffixes" of already existing names
    new_file_name = out_name
    new_file = path.join(out_dir, new_file_name)
    suffix = 0
    while path.isfile(new_file + ".obj"):    
        suffix += 1
        new_file_name = out_name + "_" + str(suffix)
        new_file = path.join(out_dir, new_file_name)
    # Create an exporter object
    chdir(out_dir)
    export_vtk = vtk.vtkOBJExporter()
    export_vtk.SetInput(render_window)
    # Remove the '.obj' extension when setting the file prefix
    export_vtk.SetFilePrefix(new_file)
    export_vtk.Write()
    chdir(initial_dir)
    print(new_file + ".obj saved successfully")
    return new_file + ".obj"