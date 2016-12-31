#!/usr/bin/env python

# Test example to generate 2D (embedded in 3D) and 3D Delaunay triangulations that output to VTK

import pyvtk
import numpy as np
from scipy.spatial import Delaunay

# Generate the random points
npoints = 1000
np.random.seed(1)
x = np.random.normal(size=npoints)*np.pi
y = np.random.normal(size=npoints)*np.pi
z = np.sin((x))+np.cos((y))
# Generate random data
pointPressure = np.random.rand(npoints)

# Compute the 2D Delaunay triangulation in the x-y plane
xTmp=list(zip(x,y))
tri=Delaunay(xTmp)

# Generate Cell Data
nCells=tri.nsimplex
cellTemp=np.random.rand(nCells)

# Zip the point co-ordinates for the VtkData input
points=list(zip(x,y,z))

vtk = pyvtk.VtkData(\
  pyvtk.UnstructuredGrid(points,
    triangle=tri.simplices
    ),
  pyvtk.PointData(pyvtk.Scalars(pointPressure,name='Pressure')),
  pyvtk.CellData(pyvtk.Scalars(cellTemp,name='Temperature')),
  '2D Delaunay Example'
  )
vtk.tofile('Delaunay2D')
vtk.tofile('Delaunay2Db','binary')

# Compute the 3D Delaunay triangulation in the x-y plane
xTmp=list(zip(x,y,z))
tri=Delaunay(xTmp)

# Generate Cell Data
nCells=tri.nsimplex
cellTemp=np.random.rand(nCells)

# Zip the point co-ordinates for the VtkData input
points=list(zip(x,y,z))

vtk = pyvtk.VtkData(\
  pyvtk.UnstructuredGrid(points,
    tetra=tri.simplices
    ),
  pyvtk.PointData(pyvtk.Scalars(pointPressure,name='Pressure')),
  pyvtk.CellData(pyvtk.Scalars(cellTemp,name='Temperature')),
  '3D Delaunay Example'
  )
vtk.tofile('Delaunay3D')
vtk.tofile('Delaunay3Db','binary')
