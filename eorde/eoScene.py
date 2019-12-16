import vtk

class CallBack(object):
    def __init__(self, pipelines, ren):
        self.pipelines = pipelines
        self.ren = ren

    def execute(self, obj, event):
        #print(obj.GetClassName(), "Event Id:", event)
        #print(dir(event))
        key = obj.GetKeySym()
        for p in self.pipelines:
            p.update(key)
        self.ren.Render()


class Scene:

    def __init__(self):
        self.ren = vtk.vtkRenderer()
        self.renWin = vtk.vtkRenderWindow()
        self.iren = vtk.vtkRenderWindowInteractor()

        self.camera = vtk.vtkCamera()
        self.camera.OrthogonalizeViewUp()
        self.camera.SetFocalPoint(0., 0., 0.)
        self.camera.SetDistance(5.)

        self.ren.SetActiveCamera(self.camera)
        self.renWin.AddRenderer(self.ren)
        self.iren.SetRenderWindow(self.renWin)

        self.renWin.SetSize(1200, 960)
        self.ren.SetBackground(0.1, 0.1, 0.2)

        self.pipelines = []
        self.callBack = None



    def addPipelines(self, pips):
        self.pipelines += pips


    def setWindowSize(self, width, height):
        self.renWin.SetSize(width, height)


    def setBackground(self, r, g, b):
        self.ren.SetBackground(r, g, b)


    def start(self):
        self.callBack = CallBack(self.pipelines, self.ren)
        for p in self.pipelines:
            self.ren.AddActor(p.getActor())

        self.iren.AddObserver('KeyPressEvent', self.callBack.execute)
        self.renWin.Render()
        self.iren.Initialize()
        self.iren.Start()


