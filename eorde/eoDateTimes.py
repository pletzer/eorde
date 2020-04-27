import vtk


class DateTimes(object):

    def __init__(self, dts, pos=(0.6, 0.9), size=14, color=(0., 0., 0.)):

        self.dateTimes = dts
        self.actor = vtk.vtkTextActor()
        self.actor.SetTextScaleMode(0)
        self.actor.SetPosition(pos)
        self.actor.GetTextProperty().SetFontSize(size)
        self.actor.GetTextProperty().SetColor(color)
        self.stepIndex = 0
        self.numSteps = len(dts)


    def update(self, key):
        if key == 't':
            dt = self.dateTimes[self.stepIndex]
            txt = f'{dt.year}-{dt.month:02d}-{dt.day:02d} {self.stepIndex:4d}'
            print(txt)
            self.actor.SetInput(txt)
            self.actor.Modified()
            self.stepIndex = (self.stepIndex + 1) % self.numSteps


    def getActor(self):
        return self.actor

###############################################################################

def test():
    from eorde.eoScene import Scene
    from datetime import datetime

    dts = [datetime(year=2019, month=1, day=1), datetime(year=2019, month=1, day=2)]
    dateTimes = DateTimes(dts, pos=(800, 500), size=52, color=(1., 0., 0.))

    s = Scene()
    s.addPipelines([dateTimes])
    s.setBackground(0.9, 0.9, 0.9)
    s.start()

if __name__ == '__main__':
    test()
