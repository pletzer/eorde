import numpy
import vtk

class Colormap:

    def __init__(self, dmin, dmax):
        self.lut = vtk.vtkLookupTable()
        n = 256
        self.lut.SetNumberOfTableValues(n)
        self.lut.SetTableRange(dmin, dmax)

        #self.lut.SetHueRange(0.667, 0.)
        dx = 1.0/float(n - 1)
        for i in range(n):
            x = i*dx
            # r = max(2*x - 1, 0)
            # g = numpy.cos(numpy.pi*((x-0.5)))
            # b = max(1 - 2*x, 0)


            # # negative part
            # r = 0.
            # g = 2*x
            # b = 1.0
            # alpha = 1.0 # opaque
            # if x >= 0.5:
            #     # positive side
            #     r = 1.0
            #     g = 2*(1. - x)
            #     b = 0.

            r = 4*(0.25 - x)
            g = 0
            b = 1
            if 0.25 <= x < 0.5:
                r = 0
                g = 0
                b = 4*(0.5 - x)
            elif 0.5 <= x < 0.75:
                r = 4*(x - 0.5)
                g = 0
                b = 0
            elif 0.75 <= x:
                r = 1
                g = 4*(x - 0.75)
                b = 0

            self.lut.SetTableValue(i, r, g, b, 1.0)

        self.lut.UseBelowRangeColorOn()
        self.lut.UseAboveRangeColorOn()

        self.lut.SetBelowRangeColor(0., 0., 0., 1.)
        self.lut.SetAboveRangeColor(1., 1., 1., 0.)
        self.lut.Build()

    def getLookupTable(self):
        return self.lut
