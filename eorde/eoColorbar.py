import vtk


class Colorbar:

    def __init__(self, lookupTable, pos=(0.8, 0.2), size=14):

        self.lut = lookupTable
        self.actor = vtk.vtkScalarBarActor()
        self.actor.SetLookupTable(lookupTable)
        self.actor.SetPosition(pos)
        self.actor.GetLabelTextProperty().SetFontSize(size)


    def update(self, key):
        pass


    def getActor(self):
        return self.actor

###############################################################################

def test():
    from eoScene import Scene

    lut = vtk.vtkLookupTable()
    lut.SetHueRange(0.667, 0.)
    lut.Build()
    colorbar = Colorbar(lut)

    s = Scene()
    s.addPipelines([colorbar])
    s.setBackground(0.9, 0.9, 0.9)
    s.start()

if __name__ == '__main__':
    test()
