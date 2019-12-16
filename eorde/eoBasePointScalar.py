import vtk
import numpy
from eoColormap import Colormap


class BasePointScalar(object):

    """
    Base pipeline for colour plots of scalar fields
    """

    def __init__(self, level=1):
        
        # numpy array to store the lat-lon data
        self.data = []
        # vtk array, will store the pointer to the self.data values
        self.dataArray = None

        # Cartesian coordinates, numpy array
        self.xyz = []
        # vtk array to store the x,y,z coordinates
        self.pointArray = vtk.vtkDoubleArray()

        # vtk objects
        self.points = vtk.vtkPoints()
        self.sgrid = vtk.vtkStructuredGrid()
        # lookup table
        self.colormap = None
        self.mapper = vtk.vtkDataSetMapper()
        self.actor = vtk.vtkActor()

        # connect
        self.pointArray.SetNumberOfComponents(3)
        self.points.SetData(self.pointArray)
        self.sgrid.SetPoints(self.points)
        # zonal data
        self.sgrid.GetCellData().SetScalars(self.dataArray)
        self.mapper.SetInputData(self.sgrid)
        self.actor.SetMapper(self.mapper)

        # some settings
        self.mapper.UseLookupTableScalarRangeOn()
        self.mapper.ScalarVisibilityOn()

        # number of data dimensions 
        self.ndims = 0

        # number of lons and lats
        self.nx1, self.ny1 = 0, 0

        # radius of the sphere
        self.radius = 1. + 0.01*level

        # index of the time axis in self.data
        self.timeIndex = -1

        self.numTimes = 0
        self.timeCount = 0

        self.ncVar = None


    def setNetCDFVariable(self, ncReader, standardName):

        self.ncVar = ncReader.getNetCDFVariable(standardName)
        if self.ncVar.dtype == 'float64':
            self.dataArray = vtk.vtkDoubleArray()
        elif self.ncVar.dtype == 'float32':
            self.dataArray = vtk.vtkFloatArray()
        else:
            raise(f'ERROR: unknown type {self.ncVar.dtype}')

        self.ndims = len(self.ncVar.shape)

        # find the time index location
        nc = ncReader.getNetCDFFileHandle()
        indx = 0
        for dimName in self.ncVar.dimensions:
            v = nc.variables[dimName]
            sdnm = getattr(v, 'standard_name', '')
            if sdnm == 'time':
                self.timeIndex = indx
                break
            indx += 1
        self.numTimes = self.ncVar.shape[self.timeIndex]


        # get the grid
        llons, llats = ncReader.get2DLonsLats()
        self.nx1, self.ny1 = llons.shape[::-1]

        # project onto x, y, z coordinates
        zz = self.radius * numpy.sin(numpy.pi * llats / 180.)
        rr = self.radius * numpy.cos(numpy.pi * llats / 180.)
        xx = rr * numpy.cos(numpy.pi * llons / 180.)
        yy = rr * numpy.sin(numpy.pi * llons / 180.)

        # interleave the x, y, z coordinates
        ntot = numpy.prod(llons.shape)
        self.xyz = numpy.zeros((ntot, 3), numpy.float64)
        self.xyz[:, 0] = xx.ravel()
        self.xyz[:, 1] = yy.ravel()
        self.xyz[:, 2] = zz.ravel()

        # 2D
        self.points.SetNumberOfPoints(ntot)
        self.pointArray.SetVoidArray(self.xyz, ntot*3, 1)
        self.dataArray.SetName(standardName)
        self.sgrid.SetDimensions(llons.shape[0], llons.shape[1], 1)

        # compute min/max values across all times and build the look up table
        dataMin, dataMax = self.getDataMinMax()
        print(f'dataMin = {dataMin} dataMax = {dataMax}')
        self.colormap = Colormap(dataMin, dataMax)
        self.mapper.SetLookupTable(self.colormap.getLookupTable())

        numCells = (self.nx1 - 1) * (self.ny1 - 1)

        self.data = numpy.zeros((self.ny1 - 1, self.nx1 - 1), self.ncVar.dtype)
        self.dataArray.SetVoidArray(self.data, numCells, 1)


    def update(self, key):
        if key == 't':
            # update time
            self.data[:] = self.getDataAtTime(self.timeCount)
            print(f'info: updating time count = {self.timeCount} slc = {slc}')
            self.timeCount = (self.timeCount + 1) % self.numTimes
        else:
            print(f'Warning: not a valid key {key}')


    def getDataAtTime(self, timeCount):
        slc = [slice(0, None) for i in range(self.timeIndex)] + \
              [timeCount] + \
              [slice(0, None) for i in range(self.timeIndex + 1, self.ndims)]
        return self.ncVar[slc]


    def getDataMinMax(self):
        dmin = float('inf')
        dmax = -float('inf')
        for i in range(self.numTimes):
            d = self.getDataAtTime(i)
            dlo = d.min()
            dhi = d.max()
            dmin = min(dmin, dlo)
            dmax = max(dmax, dhi)
        return dmin, dmax


    def getActor(self):
        return self.actor

###############################################################################

def test():
    from eoScene import Scene
    from eoColor import Color
    from eoNCReader import NCReader

    n = NCReader('../data/tos_Omon_GFDL-CM4_historical_r1i1p1f1_gr_201001-201412.nc')

    c = Color()
    c.setNetCDFVariable(n, 'sea_surface_temperature')

    s = Scene()
    s.setBackground(0.7, 0.7, 0.7)
    s.addPipelines([c])
    s.start()

if __name__ == '__main__':
    test()