import vtk
import re

class Planet:

    def __init__(self, level=0, textureFile='../data/2k_earth_daymap.jpeg'):
        self.transf = vtk.vtkTransform()
        self.globe = vtk.vtkTexturedSphereSource()
        self.texture = vtk.vtkTexture()


        #self.transf.Scale(0.25, 1., 1.)
        self.texture.SetTransform(self.transf)
        self.texture.SetInterpolate(1)

        self.reader = None
        if re.search(r'jpe?g', textureFile.split('.')[-1]):
            self.reader = vtk.vtkJPEGReader()
        elif textureFile.split('.')[-1] == 'png':
            self.reader = vtk.vtkPNGReader()

        self.mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()

        # connect
        self.actor.SetMapper(self.mapper)
        self.actor.SetTexture(self.texture)

        self.mapper.SetInputConnection(self.globe.GetOutputPort())
        self.texture.SetInputConnection(self.reader.GetOutputPort())
        self.reader.SetFileName(textureFile)

        self.globe.SetThetaResolution(128)
        self.globe.SetPhiResolution(64)
        self.globe.SetRadius(100. + level)

    def getActor(self):
        return self.actor

###############################################################################

def test():
    from eoScene import Scene
    p = Planet()
    s = Scene()
    s.addPipelines([p])
    s.show()

if __name__ == '__main__':
    test()

