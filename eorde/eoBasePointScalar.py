import vtk
import numpy

class BasePointScalar(object):

    def __init__(self, level=1):
        
        self.data = []
        self.dataArray = vtk.vtkDoubleArray()
        self.xyz = []
        self.lut = vtk.vtkLookupTable()
        self.pointArray = vtk.vtkDoubleArray()
        self.points = vtk.vtkPoints()
        self.sgrid = vtk.vtkStructuredGrid()
        self.gridFilter    = vtk.vtkStructuredGridGeometryFilter()
        self.mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()

        self.pointArray.SetNumberOfComponents(3)
        self.points.SetData(self.pointArray)
        self.sgrid.SetPoints(self.points)
        self.mapper.SetLookupTable(self.lut)

        self.ndims = 0
        self.nx, self.ny = 0, 0
        self.ntot = 0

        self.radius = 100. + level

        self.timeIndex = -1

        self.timeCount = 0
        self.numTimes = 0

        self.ncVar = None


    def setNetCDFVariable(self, ncReader, standardName):

        self.ncVar = ncReader.getNetCDFVariable(standardName)
        nc = ncReader.getNetCDFFileHandle()

        self.ndims = len(self.ncVar.shape)

        # figure out the mapping of indices to time, lon, lat
        # NEED TO ADD SUPPORT FOR ELEVATION!
        self.timeIndex = -1
        self.latIndex = -1
        indx = 0
        for axis in self.ncVar.dimensions:
            standardName = getattr(nc.variables[axis], 'standard_name', '')
            if standardName == 'time':
                self.timeIndex = indx
                self.numTimes = self.ncVar.shape[indx]
            indx += 1

        # get the grid
        llons, llats = ncReader.get2DLonsLats()
        zz = self.radius * numpy.sin(numpy.pi * llats / 180.)
        rr = self.radius * numpy.cos(numpy.pi * llats / 180.)
        xx = rr * numpy.cos(numpy.pi * llons / 180.)
        yy = rr * numpy.sin(numpy.pi * llons / 180.)
        self.ntot = numpy.prod(llons.shape)
        self.xyz = numpy.zeros((self.ntot, 3), numpy.float64)
        self.xyz[:, 0] = xx.ravel()
        self.xyz[:, 1] = yy.ravel()
        self.xyz[:, 2] = zz.ravel()

        # 2D
        self.sgrid.SetDimensions(llons.shape[1], llons.shape[0], 1)
        self.points.SetNumberOfPoints(self.ntot)
        self.pointArray.SetVoidArray(self.xyz, self.ntot*3, 1)

        # compute min/max values and build the look up table
        data = self.ncVar[:]
        dataMin, dataMax = data.min(), data.max()
        self.lut.SetTableRange(dataMin, dataMax)
        self.lut.SetHueRange(0.677, 0.)
        self.lut.Build()

        self.dataArray.SetName(standardName)


    def update(self, key):
        if key == 't':
            # update time
            slc = [slice(0, None) for i in range(self.timeIndex)] + \
                  [self.timeCount] + \
                  [slice(0, None) for i in range(self.timeIndex + 1, self.ndims)]
            print(f'info: updating time count = {self.timeCount} slc = {slc}')
            data = self.ncVar[slc]
            self.dataArray.SetVoidArray(data, self.ntot, 1)
            self.sgrid.GetCellData().SetScalars(self.dataArray)
            print(self.sgrid)
            print(f'shape of data: {data.shape}')
            self.timeCount = (self.timeCount + 1) % self.numTimes
        else:
            print(f'Warning: not a valid key {key}')


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
    s.setBackground(0.3, 0.3, 0.3)
    s.addPipelines([c])
    s.start()

if __name__ == '__main__':
    test()