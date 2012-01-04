#!/usr/bin/env python
"""
PyVTK provides tools for manipulating VTK files in Python.

VtkData - create VTK files from Python objects.

"""
"""
Copyright 2001 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@ioc.ee>          
Permission to use, modify, and distribute this software is given under the
terms of the LGPL.  See http://www.fsf.org

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Revision: 1.1 $
$Date: 2001/05/20 12:51:29 $
Pearu Peterson
"""

__author__ = "Pearu Peterson <pearu@cens.ioc.ee>"
__license__ = "LGPL (see http://www.fsf.org)"
from __version__ import __version__

__all__ = ['StructuredPoints','StructuredGrid','UnstructuredGrid','RectilinearGrid',
           'RectilinearGrid','PolyData',
           'Scalars','ColorScalars','LookupTable','Vectors','Normals',
           'TextureCoordinates','Tensors','Field',
           'PointData','CellData',
           'VtkData']

import common
import string

from StructuredPoints import StructuredPoints
from StructuredGrid import StructuredGrid
from UnstructuredGrid import UnstructuredGrid
from RectilinearGrid import RectilinearGrid
from PolyData import PolyData

from Scalars import Scalars
from ColorScalars import ColorScalars
from LookupTable import LookupTable
from Vectors import Vectors
from Normals import Normals
from TextureCoordinates import TextureCoordinates
from Tensors import Tensors
from Field import Field

from Data import PointData,CellData

class VtkData(common.Common):
    """
    VtkData
    =======

    Represents VTK file that has four relevant parts:
      header    - string up to length 256
      format    - string: ascii | binary
      DataSet   - StructuredPoints | StructuredGrid | UnstructuredGrid
                  | RectilinearGrid | PolyData
      Data      - PointData | CellData
      
    Usage:
    ------
      v = VtkData(<DataSet instance> [,<header string>,<Data instances>,..])
      v.tofile(filename, format = 'ascii') - save VTK data to file.

    DataSet
    =======
    
      StructuredPoints(<3-sequence of dimensions>
                       [,<3-sequence of origin> [, <3-sequence of spacing>]])
      StructuredGrid(<3-sequence of dimensions>,
                     <sequence of 3-sequences of points>)
      UnstructuredGrid(<sequence of 3-sequences of points>
                       [,<cell> = <sequence of (sequences of) integers>])
        cell - vertex | poly_vertex | line | poly_line | triangle
               | triangle_strip | polygon | pixel | quad | tetra
               | voxel | hexahedron | wedge | pyramid
      RectilinearGrid([x = <sequence of x-coordinates>],
                      [y = <sequence of y-coordinates>],
                      [z = <sequence of z-coordinates>])
      PolyData(<sequence of 3-sequences of points>,
               [vertices = <sequence of (sequences of) integers>],
               [lines = <sequence of (sequences of) integers>],
               [polygons = <sequence of (sequences of) integers>],
               [triangle_strips = <sequence of (sequences of) integers>])

    Data
    ====

      PointData | CellData ([<DataSetAttr instances>]) - construct Data instance

    DataSetAttr
    ===========

      DataSetAttr - Scalars | ColorScalars | LookupTable | Vectors
                    | Normals | TextureCoordinates | Tensors | Field
      Scalars(<sequence of scalars> [,name[, lookup_table]])
      ColorScalars(<sequence of scalar sequences> [,name])
      LookupTable(<sequence of 4-sequences> [,name])
      Vectors(<sequence of 3-sequences> [,name])
      Normals(<sequence of 3-sequences> [,name])
      TextureCoordinates(<sequence of (1,2, or 3)-sequences> [,name])
      Tensors(<sequence of (3x3)-sequences> [,name])
      Field([name,] [arrayname_1 = sequence of n_1-sequences, ...
                     arrayname_m = sequence of n_m-sequences,])
        where len(array_1) == .. == len(array_m) must hold.
    """
    header = None
    point_data = None
    cell_data = None
    def __init__(self,structure,*args):
        if not common.is_dataset(structure):
            raise TypeError,'argument structure must be StructuredPoints|StructuredGrid|UnstructuredGrid|RectilinearGrid|PolyData but got %s'%(type(structure))
        self.structure = structure
        for a in args:
            if common.is_string(a):
                if len(a)>255:
                    self.skipping('striping header string to length 256')
                self.header = a[:256]
            elif common.is_pointdata(a):
                self.point_data = a
            elif common.is_celldata(a):
                self.cell_data = a
            else:
                self.skipping('unexpexted argument %s'%(type(a)))
        if self.header is None:
            self.header = 'Really cool data'
            self.warning('Using header=%s'%(`self.header`))
        if self.point_data is None and self.cell_data is None:
            self.warning('No data defined')

        if self.point_data is not None:
            s = self.structure.get_size()
            s1 = self.point_data.get_size()
            if s1 != s:
                raise ValueError,'DataSet (size=%s) and PointData (size=%s) have different sizes'%(s,s1)
        if self.cell_data is not None:
            s = self.structure.get_cell_size()
            s1 = self.cell_data.get_size()
            if s1 != s:
                raise ValueError,'DataSet (cell_size=%s) and CellData (size=%s) have different sizes'%(s,s1)
    def tofile(self, filename, format = 'ascii'):
        if not common.is_string(filename):
            raise TypeError,'argument filename must be string but got %s'%(type(filename))
        if format not in ['ascii','binary']:
            raise TypeError,'argument format must be ascii | binary'
        filename = string.strip(filename)
        if not filename:
            raise ValueError,'filename must be non-empty string'
        if filename[-4:]!='.vtk':
            filename = filename + '.vtk'
        f = open(filename,'wb')
        f.write('# vtk DataFile Version 2.0\n')
        f.write(self.header+'\n')
        f.write(string.upper(format)+'\n')
        f.write(self.structure.to_string(format)+'\n')
        if self.cell_data:
            f.write(self.cell_data.to_string(format)+'\n')
        if self.point_data:
            f.write(self.point_data.to_string(format))
        f.close()

if __name__ == "__main__":
    vtk = VtkData(StructuredPoints((3,1,1)),
                  'This is title',
                  PointData(Scalars([3,4,5]))
                  )
    vtk.tofile('test')
