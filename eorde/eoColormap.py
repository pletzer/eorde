import numpy
import vtk

class Colormap:

    EPS = 1.e-6

    def __init__(self, dmin, dmax):
        self.lut = vtk.vtkLookupTable()
        n = 256 + 1
        self.lut.SetNumberOfTableValues(n)
        self.lut.SetTableRange(dmin - self.EPS, dmax + self.EPS)

        x = numpy.linspace(0., 1., n)
        r = numpy.maximum(0., x)
        g = -2. *numpy.fabs((x - 0.5)) + 1.
        b = numpy.maximum(0., 1 - x)
        a = numpy.ones(x.shape, numpy.float64)

        a[0] = 0.
        a[-1] = 0.

        for i in range(n):
            self.lut.SetTableValue(i, r[i], g[i], b[i], a[i])
        self.lut.Build()

    def getLookupTable(self):
        return self.lut