import vtk


class Continents:

    def __init__(self, level=0):

        self.radius = 1. + 0.01 * level

        self.continents = vtk.vtkEarthSource()
        self.mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()

        # connect
        self.actor.SetMapper(self.mapper)
        self.mapper.SetInputConnection(self.continents.GetOutputPort())

        self.continents.SetRadius(self.radius)
        self.actor.GetProperty().SetColor(0., 0., 0.)


    def update(self, key):
        pass


    def getActor(self):
        return self.actor

###############################################################################

def test():
    from eoScene import Scene
    c = Continents(level=1)
    s = Scene()
    s.addPipelines([c])
    s.setBackground(0.9, 0.9, 0.9)
    s.show()

if __name__ == '__main__':
    test()
