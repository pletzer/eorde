import numpy
import vtk

class Colormap:

    def __init__(self, dmin, dmax):
        self.lut = vtk.vtkLookupTable()
        n = 256
        self.lut.SetNumberOfTableValues(n)
        self.lut.SetTableRange(dmin, dmax)
        self.lut.SetHueRange(0.667, 0.)

        self.lut.UseBelowRangeColorOn()
        self.lut.UseAboveRangeColorOn()

        self.lut.SetBelowRangeColor(0., 0., 0., 1.)
        self.lut.SetAboveRangeColor(1., 1., 1., 0.)
        self.lut.Build()

    def getLookupTable(self):
        return self.lut
