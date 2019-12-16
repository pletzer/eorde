import vtk
import netCDF4
import numpy
from eoColormap import Colormap
from eoNCReader import NCReader

# read the data 
nc = netCDF4.Dataset('../data/tos_Omon_GFDL-CM4_historical_r1i1p1f1_gr_201001-201412.nc')

ncReader = NCReader('../data/tos_Omon_GFDL-CM4_historical_r1i1p1f1_gr_201001-201412.nc')
llons, llats = ncReader.get2DLonsLats()


"""
# the data are cell centred so getting the grid form the bounds
lons = numpy.append(nc.variables['lon_bnds'][:, 0], nc.variables['lon_bnds'][-1, 1])
lats = numpy.append(nc.variables['lat_bnds'][:, 0], nc.variables['lat_bnds'][-1, 1])

llons, llats = numpy.meshgrid(lons, lats, indexing='xy')
"""

data = nc.variables['tos'][0,...]
print(f'data min/max = {data.min()}/{data.max()}')

#print(llons)
print(data)

pointArray = vtk.vtkDoubleArray()
points = vtk.vtkPoints()
sgrid = vtk.vtkStructuredGrid()
mapper = vtk.vtkDataSetMapper()
actor = vtk.vtkActor()


# construct the mesh
nx1, ny1 = llons.shape[::-1]
numPoints = nx1 * ny1
xyz = numpy.zeros((numPoints, 3), numpy.float64)
xyz[:, 0] = llons.ravel()
xyz[:, 1] = llats.ravel()

nx = nx1 - 1
ny = ny1 - 1
numCells = nx * ny

pointArray.SetNumberOfComponents(3)
pointArray.SetName('coordinates')
pointArray.SetVoidArray(xyz, numPoints * 3, 1)

if data.dtype == 'float32':
    dataArray = vtk.vtkFloatArray()
elif data.dtype == 'float64':
    dataArray = vtk.vtkDoubleArray()

dataArray.SetNumberOfComponents(1)
dataArray.SetName('cellCentredData')
dataArray.SetVoidArray(data, numCells, 1)

colormap = Colormap(data.min(), data.max())

# connect
points.SetData(pointArray)
sgrid.SetDimensions(nx1, ny1, 1)
sgrid.SetPoints(points)
sgrid.GetCellData().SetScalars(dataArray)
mapper.SetInputData(sgrid)
mapper.SetLookupTable(colormap.getLookupTable())
mapper.UseLookupTableScalarRangeOn()
actor.SetMapper(mapper)

# render
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
iren = vtk.vtkRenderWindowInteractor()
renWin.AddRenderer(ren)
iren.SetRenderWindow(renWin)

ren.SetBackground(0.8, 0.8, 0.7)

ren.AddActor(actor)

renWin.Render()
iren.Start()
