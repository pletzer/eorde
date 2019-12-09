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

        self.radius = 100. + level

    def connect(self):
        self.gridFilter.SetInputData(self.sgrid)
        self.mapper.SetInputConnection(self.gridFilter.GetOutputPort())
        self.actor.SetMapper(self.mapper)


    def get2DLonsLats(self, lons1D, lats1D):
        return numpy.meshgrid(lons1D, lats1D, indexing='ij')


    def setXYZPoints(self, xyz):
        n = xyz.shape[0]
        self.points.SetNumberOfPoints(n)
        self.pointArray.SetVoidArray(xyz, n*3, 1)


    def setPoints(self, lons, lats):
        self.sgrid.SetDimensions(lons.shape[1], lons.shape[0], 1)
        n = numpy.prod(lons.shape)
        self.xyz = numpy.zeros((n, 3), numpy.float64)
        zz = self.radius * numpy.sin(numpy.pi * lats / 180.)
        rr = self.radius * numpy.cos(numpy.pi * lats / 180.)
        xx = rr * numpy.cos(numpy.pi * lons / 180.)
        yy = rr * numpy.sin(numpy.pi * lons / 180.)
        print(xx.shape)
        print(self.xyz.shape)
        print(xx[:])
        self.xyz[:, 0] = xx.ravel()
        self.xyz[:, 1] = yy.ravel()
        self.xyz[:, 2] = zz.ravel()
        self.setXYZPoints(self.xyz)

    def setData(self, data):
        n = numpy.prod(data.shape)
        self.dataArray.SetVoidArray(data, n, 1)
        self.sgrid.GetPointData().SetScalars(self.dataArray)

    def getActor(self):
        return self.actor

###############################################################################

def test():
    from eoScene import Scene

    nx1, ny1 = 8+1, 4+1
    x = numpy.linspace(0., 360., nx1)
    y = numpy.linspace(-90., 90., ny1)
    xx, yy = numpy.meshgrid(x, y, indexing='ij')
    data = numpy.cos(numpy.pi * xx / 180.0) * numpy.sin(numpy.pi * yy / 180.0)

    c = Color()
    c.setPoints(lons=xx, lats=yy)
    c.setData(data)

    s = Scene()
    s.addPipelines([c])
    s.show()

if __name__ == '__main__':
    test()