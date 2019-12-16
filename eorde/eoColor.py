import vtk
import numpy
from eoBasePointScalar import BasePointScalar


class Color(BasePointScalar):

    def __init__(self, level=1):
        super().__init__(level)
        #self.gridFilter    = vtk.vtkStructuredGridGeometryFilter()

        # connect
        #self.gridFilter.SetInputData(self.sgrid) #Connection(self.gridFilter.GetOutputPort())
        #self.actor.SetMapper(self.mapper)


###############################################################################

def test():
    from eoScene import Scene
    from eoColor import Color
    from eoNCReader import NCReader

    n = NCReader('../data/tos_Omon_GFDL-CM4_historical_r1i1p1f1_gr_201001-201412.nc')

    c = Color()
    c.setNetCDFVariable(n, 'sea_surface_temperature')

    s = Scene()
    s.setBackground(0.3, 0.3, 0.3)
    s.addPipelines([c])
    s.start()


if __name__ == '__main__':
    test()