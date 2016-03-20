#!/usr/bin/env python
"""
PyVTK provides tools for manipulating VTK files in Python.

VtkData - create VTK files from Python / read VTK files to Python

"""
__author__ = "Pearu Peterson <pearu.peterson@gmail.com>"
__license__ = "New BSD"

from pyvtk.__version__ import __version__

__all__ = ['StructuredPoints','StructuredGrid','UnstructuredGrid',
           'RectilinearGrid','PolyData',
           'Scalars','ColorScalars','LookupTable','Vectors','Normals',
           'TextureCoordinates','Tensors','Field',
           'PointData','CellData',
           'VtkData']

import logging
log = logging.getLogger(__name__)
# Silence logs - it's up to applications to do things with them
log.addHandler(logging.NullHandler())

import pyvtk.common as common

from pyvtk.StructuredPoints import StructuredPoints, structured_points_fromfile
from pyvtk.StructuredGrid import StructuredGrid, structured_grid_fromfile
from pyvtk.UnstructuredGrid import UnstructuredGrid, unstructured_grid_fromfile
from pyvtk.RectilinearGrid import RectilinearGrid, rectilinear_grid_fromfile
from pyvtk.PolyData import PolyData, polydata_fromfile

from pyvtk.Scalars import Scalars, scalars_fromfile
from pyvtk.ColorScalars import ColorScalars, color_scalars_fromfile
from pyvtk.LookupTable import LookupTable, lookup_table_fromfile
from pyvtk.Vectors import Vectors, vectors_fromfile
from pyvtk.Normals import Normals, normals_fromfile
from pyvtk.TextureCoordinates import TextureCoordinates, texture_coordinates_fromfile
from pyvtk.Tensors import Tensors, tensors_fromfile
from pyvtk.Field import Field, field_fromfile

from pyvtk.Data import PointData,CellData, is_pointdata, is_celldata
from pyvtk.DataSet import is_dataset

parsers = {
    'structured_points': structured_points_fromfile,
    'structured_grid': structured_grid_fromfile,
    'unstructured_grid': unstructured_grid_fromfile,
    'rectilinear_grid': rectilinear_grid_fromfile,
    'polydata': polydata_fromfile,
    'scalars': scalars_fromfile,
    'color_scalars': color_scalars_fromfile,
    'lookup_table': lookup_table_fromfile,
    'vectors': vectors_fromfile,
    'normals': normals_fromfile,
    'tensors': tensors_fromfile,
    'texture_coordinates': texture_coordinates_fromfile,
    'field': field_fromfile,
}

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
        if type(args[0]) is str:
            if 'only_structure' in kws and kws['only_structure']:
                self.fromfile(args[0],1)
            else:
                self.fromfile(args[0])
            return
        else:
            structure = args[0]
            args = list(args)[1:]
        if not is_dataset(structure):
            raise TypeError('argument structure must be StructuredPoints|StructuredGrid|UnstructuredGrid|RectilinearGrid|PolyData but got %s'%(type(structure)))
        self.structure = structure
        for a in args:
            if common.is_string(a):
                if len(a)>255:
                    log.warning('striping header string to a length =255')
                self.header = a[:255]
            elif is_pointdata(a):
                self.point_data = a
            elif is_celldata(a):
                self.cell_data = a
            else:
                log.warning('unexpexted argument %s', type(a))
        if self.header is None:
            self.header = 'Really cool data'
            log.info('Using default header=%s'%(repr(self.header)))
        if self.point_data is None and self.cell_data is None:
            log.info('No point/cell data defined')

        if self.point_data is not None:
            s = self.structure.get_size()
            s1 = self.point_data.get_size()
            if s1 != s:
                raise ValueError('DataSet (size=%s) and PointData (size=%s) have different sizes'%(s,s1))
        else:
            self.point_data = PointData()
        if self.cell_data is not None:
            s = self.structure.get_cell_size()
            s1 = self.cell_data.get_size()
            if s1 != s:
                raise ValueError('DataSet (cell_size=%s) and CellData (size=%s) have different sizes'%(s,s1))
        else:
            self.cell_data = CellData()

    def to_string(self, format = 'ascii'):
        ret = [b'# vtk DataFile Version 2.0',
               self.header.encode(),
               format.upper().encode(),
               self.structure.to_string(format)
               ]
        if self.cell_data.data:
            ret.append(self.cell_data.to_string(format))
        if self.point_data.data:
            ret.append(self.point_data.to_string(format))
        return b'\n'.join(ret)

    def tofile(self, filename, format = 'ascii'):
        """Save VTK data to file.
        """
        if not common.is_string(filename):
            raise TypeError('argument filename must be string but got %s'%(type(filename)))
        if format not in ['ascii','binary']:
            raise TypeError('argument format must be ascii | binary')
        filename = filename.strip()
        if not filename:
            raise ValueError('filename must be non-empty string')
        if filename[-4:]!='.vtk':
            filename += '.vtk'
        f = open(filename,'wb')
        f.write(self.to_string(format))
        f.close()

    def fromfile(self,filename, only_structure = 0):
        filename = filename.strip()
        if filename[-4:]!='.vtk':
            filename += '.vtk'
        f = open(filename,'rb')
        l = f.readline()
        fileversion = l.strip().replace(b' ',b'').lower()
        if not fileversion == b'#vtkdatafileversion2.0':
            print('File %s is not in VTK 2.0 format, got %s but continuing anyway..' % (filename, fileversion))
        self.header = f.readline().rstrip().decode('ascii', 'replace')
        format = f.readline().strip().lower()
        if format not in [b'ascii', b'binary']:
            raise ValueError('Expected ascii|binary but got %s'%(repr(format)))
        if format == b'binary':
            raise NotImplementedError('reading vtk binary format')
        l = common._getline(f).decode('ascii').lower().split(' ')
        if l[0].strip() != 'dataset':
            raise ValueError('expected dataset but got %s'%(l[0]))
        try:
            ff = parsers[l[1]]
        except KeyError:
            raise NotImplementedError('%s_fromfile'%(l[1]))
        self.structure, l = ff(f,self)

        for i in range(2):
            if only_structure: break
            if not l:
                break
            l = [s.strip() for s in l.decode('ascii').lower().split(' ')]
            assert len(l)==2 and l[0] in ['cell_data','point_data'], l[0]
            data = l[0]
            n = int(l[1])
            lst = []
            while 1:
                l = common._getline(f)
                if not l:
                    break
                sl = [s.strip() for s in l.decode('ascii').split()]
                k = sl[0].lower()
                if k not in ['scalars','color_scalars','lookup_table','vectors',
                             'normals','texture_coordinates','tensors','field']:
                    break
                try:
                    ff = parsers[k]
                except KeyError:
                    raise NotImplementedError('%s_fromfile'%(k))
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
