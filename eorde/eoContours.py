import vtk
import numpy

class Contours:

    def __init__(self, level=1):
        
        self.data = []
        self.dataArray = vtk.vtkDoubleArray()
        self.xyz = []
        self.pointArray = vtk.vtkDoubleArray()
        self.points = vtk.vtkPoints()
        self.sgrid = vtk.vtkStructuredGrid()
        self.contour = vtk.vtkContourFilter()
        self.mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()

        self.pointArray.SetNumberOfComponents(3)
        self.points.SetData(self.pointArray)
        self.sgrid.SetPoints(self.points)
        self.contour.SetInputData(self.sgrid)
        self.mapper.SetInputConnection(self.contour.GetOutputPort())
        self.actor.SetMapper(self.mapper)

        self.radius = 100. + level

    def setPoints(self, lons, lats):
        n = numpy.prod(lons.shape)
        self.xyz = numpy.zeros((n, 3), numpy.float64)
        zz = self.radius * numpy.sin(numpy.pi * lats / 180.)
        rr = self.radius * numpy.cos(numpy.pi * lats / 180.)
        xx = rr * numpy.cos(numpy.pi * lons / 180.)
        yy = rr * numpy.sin(numpy.pi * lons / 180.)
        self.xyz[:, 0] = xx.flat
        self.xyz[:, 1] = yy.flat
        self.xyz[:, 2] = zz.flat
        self.points.SetNumberOfPoints(n)
        self.pointArray.SetVoidArray(self.xyz, n*3, 1)
        self.sgrid.SetDimensions(lons.shape[0], lons.shape[1], 1)

    def setData(self, data):
        n = numpy.prod(data.shape)
        self.dataArray.SetVoidArray(data, n, 1)
        self.sgrid.GetPointData().SetScalars(self.dataArray)

    def setContourValues(self, vals):
        for i in range(len(vals)):
            self.contour.SetValue(i, vals[i])

    def getActor(self):
        return self.actor

###############################################################################

def test():
    from eoScene import Scene

    nx1, ny1 = 21, 11
    x = numpy.linspace(0., 360., nx1)
    y = numpy.linspace(-90., 90., ny1)
    xx, yy = numpy.meshgrid(x, y, indexing='ij')
    data = numpy.cos(numpy.pi * xx / 180.0) * numpy.sin(numpy.pi * yy / 180.0)

    c = Contours()
    c.setPoints(lons=xx, lats=yy)
    c.setData(data)
    c.setContourValues([-1., -0.8, -.2, 0.3, 0.5, 0.9])

    s = Scene()
    s.addPipelines([c])
    s.show()

if __name__ == '__main__':
    test()