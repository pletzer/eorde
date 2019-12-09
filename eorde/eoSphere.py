import vtk


class Sphere:

    def __init__(self, level=0):

        self.sphere = vtk.vtkSphereSource()
        self.mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()

        # connect
        self.actor.SetMapper(self.mapper)
        self.mapper.SetInputConnection(self.sphere.GetOutputPort())

        self.sphere.SetRadius(100. + level)
        self.sphere.SetPhiResolution(32)
        self.sphere.SetThetaResolution(64)

    def getActor(self):
        return self.actor

###############################################################################

def test():
    from eoScene import Scene
    p = Sphere(level=1)
    s = Scene()
    s.addPipelines([p])
    s.setBackground(0.9, 0.9, 0.9)
    s.show()

if __name__ == '__main__':
    test()
