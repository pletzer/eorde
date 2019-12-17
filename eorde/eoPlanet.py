import vtk
import re

class Planet:

    def __init__(self, level=0, textureFile='../data/2k_earth_daymap.jpeg', shift=0.5):

        self.transf = vtk.vtkTransform()
        self.globe = vtk.vtkTexturedSphereSource()
        self.texture = vtk.vtkTexture()


        #self.transf.Scale(0.25, 1., 1.)
        # may need to shift the picture to match the start longitude
        self.transf.Translate(shift, 0., 0.)
        self.texture.SetTransform(self.transf)
        self.texture.SetInterpolate(1)

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
        self.globe.SetRadius(1. + 0.01*level)


    def update(self, key):
        pass


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


