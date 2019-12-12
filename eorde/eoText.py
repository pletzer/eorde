import vtk


class Text:

    def __init__(self, text='', pos=(0.8, 0.9), size=14, color=(0., 0., 0.)):

        self.text = text
        self.actor = vtk.vtkTextActor()
        self.actor.SetTextScaleMode(0)
        self.actor.SetPosition(pos)
        self.actor.GetTextProperty().SetFontSize(size)
        self.actor.GetTextProperty().SetColor(color)
        self.stepIndex = 0


    def update(self, key):
        self.actor.SetInput(self.text + ' {}'.format(self.stepIndex))
        self.actor.Modified()
        self.stepIndex += 1


    def getActor(self):
        return self.actor

###############################################################################

def test():
    from eoScene import Scene
    t = Text(text='hello', pos=(800, 500), size=52, color=(1., 0., 0.))

    s = Scene()
    s.addPipelines([t])
    s.setBackground(0.9, 0.9, 0.9)
    s.start()

if __name__ == '__main__':
    test()
