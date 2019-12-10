import vtk
import numpy
from eoBasePointScalar import BasePointScalar

class Contours(BasePointScalar):

    def __init__(self, level=1):
        super().__init__(level)
        self.contour = vtk.vtkContourFilter()

        # connect
        self.contour.SetInputData(self.sgrid)
        self.mapper.SetInputConnection(self.contour.GetOutputPort())
        self.actor.SetMapper(self.mapper)


    def setContourValues(self, vals):
        n = len(vals)
        self.contour.SetNumberOfContours(n)
        for i in range(n):
            self.contour.SetValue(i, vals[i])


###############################################################################

def test():
    from eoScene import Scene
    import eoUtils

    nx1, ny1 = 10 + 1, 5 + 1
    x = numpy.linspace(0., 360., nx1)
    y = numpy.linspace(-90., 90., ny1)
    xx, yy = eoUtils.get2D(x, y)
    data = numpy.sin(numpy.pi * xx / 180.0) * numpy.cos(numpy.pi * yy / 180.0)

    c = Contours()
    c.setPoints(lons=xx, lats=yy)
    c.setData(data)
    c.setContourValues(numpy.linspace(-1., 1., 21))

    s = Scene()
    s.addPipelines([c])
    s.show()

if __name__ == '__main__':
    test()