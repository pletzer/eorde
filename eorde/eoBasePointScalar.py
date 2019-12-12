import vtk
import numpy

class BasePointScalar(object):

    def __init__(self, level=1):
        
        self.data = []
        self.dataArray = vtk.vtkDoubleArray()
        self.xyz = []
        self.pointArray = vtk.vtkDoubleArray()
        self.points = vtk.vtkPoints()
        self.sgrid = vtk.vtkStructuredGrid()
        self.gridFilter    = vtk.vtkStructuredGridGeometryFilter()
        self.mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()

        self.pointArray.SetNumberOfComponents(3)
        self.points.SetData(self.pointArray)
        self.sgrid.SetPoints(self.points)

        self.ndims = 0
        self.nx, self.ny = 0, 0
        self.ntot = 0

        self.radius = 100. + level

        self.timeIndex = -1
        self.latIndex = -1
        self.lonIndex = -1

        self.timeCount = 0
        self.numTimes = 0

        self.ncVar = None


    def setPoints(self, lons, lats):
        self.sgrid.SetDimensions(lons.shape[1], lons.shape[0], 1)
        self.ntot = numpy.prod(lons.shape)
        self.xyz = numpy.zeros((self.ntot, 3), numpy.float64)
        zz = self.radius * numpy.sin(numpy.pi * lats / 180.)
        rr = self.radius * numpy.cos(numpy.pi * lats / 180.)
        xx = rr * numpy.cos(numpy.pi * lons / 180.)
        yy = rr * numpy.sin(numpy.pi * lons / 180.)
        self.xyz[:, 0] = xx.ravel()
        self.xyz[:, 1] = yy.ravel()
        self.xyz[:, 2] = zz.ravel()
        self.points.SetNumberOfPoints(self.ntot)
        self.pointArray.SetVoidArray(self.xyz, self.ntot*3, 1)


    def setNetCDFVariable(self, nc, ncVar):
        self.ncVar = ncVar
        self.ndims = len(self.ncVar.shape)
        # figure out which dimension are time and elev
        self.timeIndex = -1
        self.latIndex = -1
        self.lonIndex = -1
        self.ntot = 1
        indx = 0
        for axis in ncVar.dimensions:
            standardName = getattr(nc.variables[axis], 'standard_name', '')
            if standardName == 'time':
                self.timeIndex = indx
                self.numTimes = ncVar.shape[indx]
            else:
                # lon or lat WOULD NEED TO CHECK FOR ELEVATION AS WELL
                self.ntot *= ncVar.shape[indx]
                if standardName == 'longitude':
                    self.nx = ncVar.shape[indx]
                    self.lonIndex = indx
                elif standardName == 'latitude':
                    self.ny = ncVar.shape[indx]
                    self.latIndex = indx
            indx += 1


    def update(self, key):
        if key == 't':
            # update time
            slc = [slice(0, None) for i in range(self.timeIndex)] + \
                  [self.timeCount] + \
                  [slice(0, None) for i in range(self.timeIndex + 1, self.ndims)]
            print(f'info: updating time count = {self.timeCount} slc = {slc}')
            data = self.ncVar[slc].data
            validRange = (data > -10) * (data < 100)
            data *= validRange
            print(f'*** data.min() = {data.min()} data.max() = {data.max()} ')
            print(f'type(data) = {type(data)}')
            self.dataArray.SetVoidArray(data, self.ntot, 1)
            self.sgrid.GetPointData().SetScalars(self.dataArray)
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
    nc = n.getNetCDFFileHandle()
    llons, llats = n.get2DLonsLats()

    c = Color()
    c.setPoints(llons, llats)
    c.setNetCDFVariable(nc, n.getNetCDFVariable('sea_surface_temperature'))

    s = Scene()
    s.setBackground(0.3, 0.3, 0.3)
    s.addPipelines([c])
    s.start()

if __name__ == '__main__':
    test()