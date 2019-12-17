import numpy
import vtk

class Colormap:

    def __init__(self, dmin, dmax):
        self.lut = vtk.vtkLookupTable()
        n = 256
        self.lut.SetNumberOfTableValues(n)
        self.lut.SetTableRange(dmin, dmax)

        for i in range(n):
            x = float(i)/float(n - 1)
            r = max(0., x)
            g = 1. - 2.*abs(x - 0.5)
            b = max(0., 1 - x)
            a = 1.
            self.lut.SetTableValue(i, r, g, b, a)

        self.lut.UseBelowRangeColorOn()
        self.lut.UseAboveRangeColorOn()

        self.lut.SetBelowRangeColor(0., 0., 0., 1.)
        self.lut.SetAboveRangeColor(1., 1., 1., 0.)
        self.lut.Build()

    def getLookupTable(self):
        return self.lut