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
        for i in range(len(vals)):
            self.contour.SetValue(i, vals[i])


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