from rasterstats import zonal_stats
import os
import matplotlib.pyplot as plt
import numpy as np


# class CanopyCover:
#     """
#     This class use the route of the main folder that contains
#     the principal photos to binarize, and save it into the
#     route_out folder with the same name
#     """
#     def __init__(self, raster, poly):
#         self.raster = raster
#         self.poly = poly
#
#     def binarize(self):
#         """
#         takes the files into the route folder and gets the projection
#         to create a new binarized file using green and blue mask
#         """


def zone_canopy(raster,polygone,res):
    """
     Run zonal statistics to extract plot information
     get the values and converts into an array
    """
    print (raster)
    stats = zonal_stats(polygone, raster, stats=['sum'])
    stat = [((stat['sum']/255)*res) for stat in stats]

    return stat


def canopy_cover(rute,poly):
    resol = [0.0000675684,0.0000722500,0.0000685584,0.0000736164,0.0000736164,0.0000748225,0.0000762129,0.0000763876,0.0000693889,0.0000744769,0.0000770884,0.0000788544,0.0000772641,0.0000815409,0.0000680625,0.0000703921]
    files = os.listdir(rute)
    matrix = ([zone_canopy(rute+files[i],poly,resol[i]) for i in range(0, len(files))])
    return matrix

class GetStats:

    """
    Extract the zonal statistics based on a digital elevation model(DEM) and a shape file (.shp)
    """
    def __init__(self, raster, poly):
        self.raster = raster
        self.poly = poly

    def zone_stats(self):
        """
         Run zonal statistics to extract plot information
         get the values and converts into an array
        """
        stats = zonal_stats(self.poly, self.raster, stats=['max'])
        stat = [stat['max'] for stat in stats]
        return stat


def features_extraction(rute, poly):
    files = os.listdir(rute)
    matrix = ([GetStats(rute+files[i], poly).zone_stats() for i in range(0, len(files))])
    return matrix


def plot_matrix(matrix, plot, n_files):
    a = [66, 73, 81, 88, 95, 101, 109, 115, 123, 130, 144, 151, 165, 202, 258]
    x = np.asarray(a[0:int(n_files)])
    y = np.asarray([i[plot] for i in matrix])
    func1 = np.polyfit(x, y, 2)
    p1 = np.poly1d(func1)
    _ = plt.plot(x, y, '.', x, p1(x), '-', color='green')
    # plt.plot(x, y, '.', color='green')
    plt.ylabel('Plant height (MASL)')
    plt.xlabel('Days since planting')
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    #raster = r'./ignored_files/1DEM_03_10_17.tif'
    rute = r'./ignored_files/mascarasgdr/'
    poly = r'./ignored_files/roi_def.shp'
    gs = canopy_cover(rute,poly)
    print(gs)
