import vtk

class Scene:

    def __init__(self):
        self.ren = vtk.vtkRenderer()
        self.renWin = vtk.vtkRenderWindow()
        self.iren = vtk.vtkRenderWindowInteractor()

        self.camera = vtk.vtkCamera()
        self.camera.OrthogonalizeViewUp()
        self.camera.SetFocalPoint(0., 0., 0.)
        #self.camera.Roll(270. - self.midLon)

        #radius = 5.0
        #x = radius*numpy.cos(self.midLat*numpy.pi/180.)*numpy.cos(self.midLon*numpy.pi/180.)
        #y = radius*numpy.cos(self.midLat*numpy.pi/180.)*numpy.sin(self.midLon*numpy.pi/180.)
        #z = radius*numpy.sin(self.midLat*numpy.pi/180.)
        #self.camera.SetPosition(x, y, z)

        self.ren.SetActiveCamera(self.camera)
        self.renWin.AddRenderer(self.ren)
        self.iren.SetRenderWindow(self.renWin)



    def addPipelines(self, pips):
        for p in pips:
            self.ren.AddActor(p.getActor())

    def setWindowSize(self, width, height):
        self.renWin.SetSize(width, height)

    def setBackground(self, r, g, b):
        self.ren.SetBackground(r, g, b)

    def show(self):
        self.iren.Initialize()
        self.renWin.Render()
        self.iren.Start()

