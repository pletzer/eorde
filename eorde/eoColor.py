import vtk
import numpy
from eoBasePointScalar import BasePointScalar


class Color(BasePointScalar):

    def __init__(self, level=1):
        super().__init__(level)
        self.gridFilter    = vtk.vtkStructuredGridGeometryFilter()

        # connect
        self.gridFilter.SetInputData(self.sgrid)
        self.mapper.SetInputConnection(self.gridFilter.GetOutputPort())
        self.actor.SetMapper(self.mapper)


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