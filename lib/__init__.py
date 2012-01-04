#!/usr/bin/env python
"""
PyVTK provides tools for manipulating VTK files in Python.

VtkData - create VTK files from Python / read VTK files to Python

"""
"""
Copyright 2001 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@ioc.ee>          
Permission to use, modify, and distribute this software is given under the
terms of the LGPL.  See http://www.fsf.org

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Revision: 1.12 $
$Date: 2010-03-03 13:41:41 $
Pearu Peterson
"""

__author__ = "Pearu Peterson <pearu@cens.ioc.ee>"
__license__ = "LGPL (see http://www.fsf.org)"
from __version__ import __version__

__all__ = ['StructuredPoints','StructuredGrid','UnstructuredGrid',
           'RectilinearGrid','PolyData',
           'Scalars','ColorScalars','LookupTable','Vectors','Normals',
           'TextureCoordinates','Tensors','Field',
           'PointData','CellData',
           'VtkData']

import types
import os
import common

from StructuredPoints import StructuredPoints, structured_points_fromfile
from StructuredGrid import StructuredGrid, structured_grid_fromfile
from UnstructuredGrid import UnstructuredGrid, unstructured_grid_fromfile
from RectilinearGrid import RectilinearGrid, rectilinear_grid_fromfile
from PolyData import PolyData, polydata_fromfile

from Scalars import Scalars,scalars_fromfile
from ColorScalars import ColorScalars, color_scalars_fromfile
from LookupTable import LookupTable, lookup_table_fromfile
from Vectors import Vectors, vectors_fromfile
from Normals import Normals, normals_fromfile
from TextureCoordinates import TextureCoordinates, texture_coordinates_fromfile
from Tensors import Tensors, tensors_fromfile
from Field import Field, field_fromfile

from Data import PointData,CellData

class VtkData(common.Common):
    """
    VtkData
    =======

    Represents VTK file that has four relevant parts:
      header    - string up to length 255
      format    - string: ascii | binary
      DataSet   - StructuredPoints | StructuredGrid | UnstructuredGrid
                  | RectilinearGrid | PolyData
      Data      - PointData | CellData
      
    Usage:
    ------
      v = VtkData(<DataSet instance> [,<header string>,<Data instances>,..])
      v = VtkData(<filename>, only_structure = 0) - read VTK data from file.
      v.tofile(filename, format = 'ascii') - save VTK data to file.
    Attributes:
      header
      structure
      point_data
      cell_data
    Public methods:
      to_string(format = 'ascii')
      tofile(filename, format = 'ascii')

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
    def __init__(self,*args,**kws):
        assert args,'expected at least one argument'
        if type(args[0]) is types.StringType:
            if kws.has_key('only_structure') and kws['only_structure']:
                self.fromfile(args[0],1)
            else:
                self.fromfile(args[0])
            return
        else:
            structure = args[0]
            args = list(args)[1:]
        if not common.is_dataset(structure):
            raise TypeError,'argument structure must be StructuredPoints|StructuredGrid|UnstructuredGrid|RectilinearGrid|PolyData but got %s'%(type(structure))
        self.structure = structure
        for a in args:
            if common.is_string(a):
                if len(a)>255:
                    self.skipping('striping header string to a length =255')
                self.header = a[:255]
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
        else:
            self.point_data = PointData()
        if self.cell_data is not None:
            s = self.structure.get_cell_size()
            s1 = self.cell_data.get_size()
            if s1 != s:
                raise ValueError,'DataSet (cell_size=%s) and CellData (size=%s) have different sizes'%(s,s1)
        else:
            self.cell_data = CellData()
    def to_string(self, format = 'ascii'):
        ret = ['# vtk DataFile Version 2.0',
               self.header,
               format.upper(),
               self.structure.to_string(format)
               ]
        if self.cell_data.data:
            ret.append(self.cell_data.to_string(format))
        if self.point_data.data:
            ret.append(self.point_data.to_string(format))
        #print `ret`
        return '\n'.join(ret)

    def tofile(self, filename, format = 'ascii'):
        """Save VTK data to file.
        """
        if not common.is_string(filename):
            raise TypeError,'argument filename must be string but got %s'%(type(filename))
        if format not in ['ascii','binary']:
            raise TypeError,'argument format must be ascii | binary'
        filename = filename.strip()
        if not filename:
            raise ValueError,'filename must be non-empty string'
        if filename[-4:]!='.vtk':
            filename += '.vtk'
        #print 'Creating file',`filename`
        f = open(filename,'wb')
        f.write(self.to_string(format))
        f.close()

    def fromfile(self,filename, only_structure = 0):
        filename = filename.strip()
        if filename[-4:]!='.vtk':
            filename += '.vtk'
        #print 'Reading file',`filename`
        f = open(filename,'rb')
        l = f.readline()
        fileversion = l.strip().replace(' ','').lower()
        if not fileversion == '#vtkdatafileversion2.0':
            print 'File %s is not in VTK 2.0 format, got %s' % (filename, fileversion),
            print ' but continuing anyway..'
        self.header = f.readline().rstrip()
        format = f.readline().strip().lower()
        if format not in ['ascii','binary']:
            raise ValueError,'Expected ascii|binary but got %s'%(`format`)
        if format == 'binary':
            raise NotImplementedError,'reading vtk binary format'
        l = common._getline(f).lower().split(' ')
        if l[0].strip() != 'dataset':
            raise ValueError,'expected dataset but got %s'%(l[0])
        try:
            ff = eval(l[1]+'_fromfile')
        except NameError:
            raise NotImplementedError,'%s_fromfile'%(l[1])
        self.structure,l = ff(f,self)

        for i in range(2):
            if only_structure: break
            if not l: break
            l = [s.strip() for s in l.lower().split(' ')]
            assert len(l)==2 and l[0] in ['cell_data','point_data'], l[0]
            data = l[0]
            n = eval(l[1])
            lst = []
            while 1:
                l = common._getline(f)
                if not l: break
                sl = [s.strip() for s in l.split()]
                k = sl[0].lower()
                if k not in ['scalars','color_scalars','lookup_table','vectors',
                             'normals','texture_coordinates','tensors','field']:
                    break
                try:
                    ff = eval(k+'_fromfile')
                except NameError:
                    raise NotImplementedError,'%s_fromfile'%(k)
                lst.append(ff(f,n,sl[1:]))
            if data == 'point_data':
                self.point_data = PointData(*lst)
            if data == 'cell_data':
                self.cell_data = CellData(*lst)
        if self.point_data is None:
            self.point_data = PointData()
        if self.cell_data is None:
            self.cell_data = CellData()
        f.close()

if __name__ == "__main__":
    vtk = VtkData(StructuredPoints((3,1,1)),
                  'This is title',
                  PointData(Scalars([3,4,5]))
                  )
    vtk.tofile('test')
