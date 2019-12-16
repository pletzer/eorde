import numpy
import vtk

class Colormap:

    def __init__(self, dmin, dmax):
        self.lut = vtk.vtkLookupTable()
        n = 256
        self.lut.SetNumberOfTableValues(n)
        self.lut.SetTableRange(dmin, dmax)

        x = numpy.linspace(0., 1., n)
        r = numpy.maximum(0., x)
        g = -2. *numpy.fabs((x - 0.5)) + 1.
        b = numpy.maximum(0., 1 - x)
        a = numpy.ones(x.shape, numpy.float64)

        for i in range(n):
            self.lut.SetTableValue(i, r[i], g[i], b[i], a[i])

        self.lut.UseBelowRangeColorOn()
        self.lut.UseAboveRangeColorOn()

        self.lut.SetBelowRangeColor(0., 0., 0., 1.)
        self.lut.SetAboveRangeColor(1., 1., 1., 1.)
        self.lut.Build()

    def getLookupTable(self):
        return self.lut