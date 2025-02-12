import numpy as np

def read_depthdata(fname: str):
    """Read sea depth data from the EMODNet ESRI ascii file.
    
    Args:
        fname (str): path to input ESRI ascii file
    """
    # The first 6 lines of the files are metadata on the grid span
    metadata = np.genfromtxt(fname, max_rows=6, converters = {0: lambda s: s}, encoding="utf-8")
    metadata = {m[0]: m[1] for m in metadata}
    
    # Longitudes and latitutes are defined from the bottom left corner with some step size
    lon = metadata["xllcenter"] + metadata["cellsize"] * np.arange(metadata["ncols"])
    lat = metadata["yllcenter"] + metadata["cellsize"] * np.arange(metadata["nrows"])
    
    # Latitudes should be flipped as the depth array is defined from the North-West corner
    lat = np.flipud(lat)
    grid_lon, grid_lat = np.meshgrid(lon, lat)  
    
    # Grid of depth in meters is defined from the North-West corner of above grid
    grid_depth = np.loadtxt(fname, skiprows=6)
    grid_depth[grid_depth < -10000] = 0
    
    return lon, lat, grid_lon, grid_lat, grid_depth