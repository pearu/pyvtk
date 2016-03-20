#!/usr/bin/env python

import sys
sys.path = ['..']+sys.path

from pyvtk import *

structure = PolyData(points=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],
                             [0,0,1],[1,0,1],[1,1,1],[0,1,1]],
                     polygons=[[0,1,2,3],[4,5,6,7],[0,1,5,4],
                               [2,3,7,6],[0,4,7,3],[1,2,6,5]])
pointdata = PointData(\
    Scalars([0,1,2,3,4,5,6,7],
            name='sample_scalars',
            lookup_table='my_table'),
    LookupTable([[0,0,0,1],[1,0,0,1],[0,1,0,1],[1,1,0,1],
                 [0,0,1,1],[1,0,1,1],[0,1,1,1],[1,1,1,1]],
                name='my_table'))

celldata = CellData(\
    Scalars([0,1,2,3,4,5],
            name='cell_scalars'),
    Normals([[0,0,-1],[0,0,1],[0,-1,0],
             [0,1,0],[-1,0,0],[1,0,0]],
            name='cell_normals'),
    Field('FieldData',
          cellIds=[[0],[1],[2],[3],[4],[5]],
          faceAttributes=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,6]]))

vtk = VtkData(structure,pointdata,celldata)
vtk.tofile('example1','ascii')
vtk.tofile('example1b','binary')

vtk2 = VtkData('example1')
