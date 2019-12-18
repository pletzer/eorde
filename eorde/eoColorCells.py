import vtk
import netCDF4
import numpy
from eoColormap import Colormap
from eoNCReader import NCReader


class ColorCells:


    def __init__(self, filename, varStandardName, level=0):

        self.radius = 1.0 + 0.01 * level
        self.varStandardName = varStandardName
        self.timeStep = 0

        # read the data 
        self.ncReader = NCReader(filename)
        self.llons, self.llats = self.ncReader.get2DLonsLats()
        self.ncVar = self.ncReader.getNetCDFVariableByStandardName(varStandardName)

        # find the time index positiuon in self.ncVar
        self.timeIndexPos = -1
        indx = 0
        for dimName in self.ncVar.dimensions:
            v = self.ncReader.getNetCDFVariableByName(dimName)
            sdnm = getattr(v, 'standard_name', '')
            if sdnm == 'time':
                self.timeIndexPos = indx
                break
            indx += 1
        self.numTimes = self.ncVar.shape[self.timeIndexPos]
        self.ndims = len(self.ncVar.shape)

        # build data slice (seeting it initially to the first time step)
        # slice(0, None) matcvhes to ":"
        self.dataTimeSlice = [slice(0, None) for i in range(self.timeIndexPos)] + \
                             [0] + \
                             [slice(0, None) for i in range(self.timeIndexPos + 1, self.ndims)]


        # construct the mesh
        self.nx1, self.ny1 = self.llons.shape[::-1]
        self.numPoints = self.nx1 * self.ny1
        self.xyz = numpy.zeros((self.numPoints, 3), numpy.float64)
        rr = self.radius  * numpy.cos(numpy.deg2rad(self.llats))
        zz = self.radius  * numpy.sin(numpy.deg2rad(self.llats))
        xx = rr * numpy.cos(numpy.deg2rad(self.llons))
        yy = rr * numpy.sin(numpy.deg2rad(self.llons))
        self.xyz[:, 0] = xx.ravel()
        self.xyz[:, 1] = yy.ravel()
        self.xyz[:, 2] = zz.ravel()

        nx = self.nx1 - 1
        ny = self.ny1 - 1
        self.numCells = nx * ny

        self.buildBasePipeline()

        self.data = self.getDataAtTime(0)

        if self.data.dtype == 'float32':
            self.dataArray = vtk.vtkFloatArray()
        elif self.data.dtype == 'float64':
            self.dataArray = vtk.vtkDoubleArray()

        self.dataArray.SetNumberOfComponents(1)
        self.dataArray.SetName(varStandardName)
        self.dataArray.SetVoidArray(self.data, self.numCells, 1)

        self.sgrid.GetCellData().SetScalars(self.dataArray)

        self.computeDataMinMax()
        print(f'data min/max = {self.dataMin}/{self.dataMax}')
        self.colormap = Colormap(self.dataMin, self.dataMax)
        self.mapper.SetLookupTable(self.colormap.getLookupTable())


    def buildBasePipeline(self):
        self.pointArray = vtk.vtkDoubleArray()
        self.points = vtk.vtkPoints()
        self.sgrid = vtk.vtkStructuredGrid()
        self.sgridGeomFilter = vtk.vtkStructuredGridGeometryFilter()
        self.mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()

        self.pointArray.SetNumberOfComponents(3)
        self.pointArray.SetName('coordinates')
        self.pointArray.SetVoidArray(self.xyz, self.numPoints * 3, 1)

        # connect
        self.points.SetData(self.pointArray)
        self.sgrid.SetDimensions(self.nx1, self.ny1, 1)
        self.sgrid.SetPoints(self.points)
        self.sgridGeomFilter.SetInputData(self.sgrid)
        self.mapper.SetInputConnection(self.sgridGeomFilter.GetOutputPort())
        self.mapper.UseLookupTableScalarRangeOn()
        self.actor.SetMapper(self.mapper)


    def getLookupTable(self):
        return self.colormap.getLookupTable()


    def getDateTimes(self):
        return self.ncReader.getDateTimes()


    def getDataAtTime(self, timeStep):
        if self.timeIndexPos < 0:
            # no time!
            return self.ncVar[...]
        self.dataTimeSlice[self.timeIndexPos] = timeStep
        return self.ncVar[self.dataTimeSlice]


    def computeDataMinMax(self):
        self.dataMin = float('inf')
        self.dataMax = -float('inf')
        for i in range(self.numTimes):
            d = self.getDataAtTime(i)
            dlo = d.min()
            dhi = d.max()
            self.dataMin = min(self.dataMin, dlo)
            self.dataMax = max(self.dataMax, dhi)


    def getActor(self):
        return self.actor


    def update(self, key):
        if key == 't':
            # update time
            self.data[:] = self.getDataAtTime(self.timeStep)
            print(f'info: updating time step = {self.timeStep}')
            self.timeStep = (self.timeStep + 1) % self.numTimes
            self.dataArray.Modified()



###############################################################################

def test():

    from eoScene import Scene
    from eoContinents import Continents
    from eoDateTimes import DateTimes
    from eoPlanet import Planet
    
    filename = '../data/tos_Omon_GFDL-CM4_historical_r1i1p1f1_gr_201001-201412.nc'
    varStandardName = 'sea_surface_temperature'
    color = ColorCells(filename=filename, varStandardName=varStandardName, level=0)

    planet = Planet(level=0)
    continents = Continents(level=1)

    dateTimes = DateTimes(dts=color.getDateTimes(), pos=(800, 900), size=52, color=(1., 0., 0.))

    s = Scene()
    s.setBackground(0.7, 0.7, 0.7)
    s.addPipelines([planet, color, continents, dateTimes])
    s.start()


if __name__ == '__main__':
    test()

