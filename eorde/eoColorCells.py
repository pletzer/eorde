import vtk
import netCDF4
import numpy
from eoColormap import Colormap
from eoNCReader import NCReader


class ColorCells:


    def __init__(self, filename, varStandardName, level=0):

        self.radius = 1.0 + 0.01 * level

        # read the data 
        self.ncReader = NCReader(filename)
        print(self.ncReader)
        self.llons, self.llats = self.ncReader.get2DLonsLats()

        self.data = self.ncReader.getNetCDFVariable(varStandardName)[0,...]
        print(f'data min/max = {self.data.min()}/{self.data.max()}')

        self.pointArray = vtk.vtkDoubleArray()
        self.points = vtk.vtkPoints()
        self.sgrid = vtk.vtkStructuredGrid()
        self.mapper = vtk.vtkDataSetMapper()
        self.actor = vtk.vtkActor()


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

        self.pointArray.SetNumberOfComponents(3)
        self.pointArray.SetName('coordinates')
        self.pointArray.SetVoidArray(self.xyz, self.numPoints * 3, 1)

        if self.data.dtype == 'float32':
            self.dataArray = vtk.vtkFloatArray()
        elif self.data.dtype == 'float64':
            self.dataArray = vtk.vtkDoubleArray()

        self.dataArray.SetNumberOfComponents(1)
        self.dataArray.SetName(varStandardName)
        self.dataArray.SetVoidArray(self.data, self.numCells, 1)

        self.colormap = Colormap(self.data.min(), self.data.max())

        # connect
        self.points.SetData(self.pointArray)
        self.sgrid.SetDimensions(self.nx1, self.ny1, 1)
        self.sgrid.SetPoints(self.points)
        self.sgrid.GetCellData().SetScalars(self.dataArray)
        self.mapper.SetInputData(self.sgrid)
        self.mapper.SetLookupTable(self.colormap.getLookupTable())
        self.mapper.UseLookupTableScalarRangeOn()
        self.actor.SetMapper(self.mapper)


    def getActor(self):
        return self.actor

    def update(self):
        pass


###############################################################################

def test():
    
    filename = '../data/tos_Omon_GFDL-CM4_historical_r1i1p1f1_gr_201001-201412.nc'
    varStandardName = 'sea_surface_temperature'
    c = ColorCells(filename=filename, varStandardName=varStandardName, level=0)

    # render
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    iren = vtk.vtkRenderWindowInteractor()
    renWin.AddRenderer(ren)
    iren.SetRenderWindow(renWin)

    ren.SetBackground(0.8, 0.8, 0.7)

    ren.AddActor(c.getActor())

    renWin.Render()
    iren.Start()


if __name__ == '__main__':
    test()

