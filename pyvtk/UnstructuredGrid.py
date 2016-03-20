#!/usr/bin/env python
"""
UnstructuredGrid
"""
__author__ = "Pearu Peterson <pearu.peterson@gmail.com>"
__license__ = "New BSD"

import logging
log = logging.getLogger(__name__)

import pyvtk.DataSet as DataSet
import pyvtk.common as common

class UnstructuredGrid(DataSet.DataSet):
    """
    Usage:
      UnstructuredGrid(<sequence of 3-tuples of points>,
                       vertex = <sequence [of 1-sequences]>
                       poly_vertex = <sequence of n-sequences>,
                       line = <sequence of 2-sequences>,
                       poly_line = <sequence of n-sequences>,
                       triangle = <sequence of 3-sequences>,
                       triangle_strip = <sequence of n-sequences>,
                       polygon = <sequence of n-sequences>,
                       pixel = <sequence of 4-sequences>,
                       quad = <sequence of 4-sequences>,
                       tetra = <sequence of 4-sequences>,
                       voxel = <sequence of 8-sequences>,
                       hexahedron = <sequence of 8-sequences>,
                       wedge = <sequence of 6-sequences>,
                       pyramid = <sequence of 5-sequences>,
                       quadratic_tetra = <sequence of 10-sequences>
                       )
    Attributes:
      points
      vertex
      poly_vertex, line, poly_line, triangle, triangle_strip,
      polygon, pixel, quad, tetra, voxel, hexahedron, wedge, pyramid
    Public methods:
      get_size()
      get_cell_size()
      to_string(format = 'ascii')
      get_points()
      <DataSetAttr class>(...)
    """
    _vtk_cell_types_map = {'vertex':1,'poly_vertex':2,'line':3,'poly_line':4,
                           'triangle':5,'triangle_strip':6,'polygon':7,'pixel':8,
                           'quad':9,'tetra':10,'voxel':11,'hexahedron':12,
                           'wedge':13,'pyramid':14,'quadratic_tetra':24}
    _vtk_cell_nums_map = {'vertex':1,'poly_vertex':-1,'line':2,'poly_line':-1,
                          'triangle':3,'triangle_strip':-1,'polygon':-1,'pixel':4,
                          'quad':4,'tetra':4,'voxel':8,'hexahedron':8,
                          'wedge':6,'pyramid':5,
                          'quadratic_tetra':10}
    _vtk_cell_types_imap = {1:'vertex',2:'poly_vertex',3:'line',4:'poly_line',
                            5:'triangle',6:'triangle_strip',7:'polygon',
                            8:'pixel',9:'quad',10:'tetra',11:'voxel',12:'hexahedron',
                            13:'wedge',14:'pyramid',24:'quadratic_tetra'}
    def __init__(self,points,vertex=[],poly_vertex=[],line=[],poly_line=[],
                 triangle=[],triangle_strip=[],polygon=[],pixel=[],
                 quad=[],tetra=[],voxel=[],hexahedron=[],wedge=[],pyramid=[],
                 quadratic_tetra=[]):
        self.points = self.get_3_tuple_list(points,(0,0,0))
        sz = len(self.points)
        for k in self._vtk_cell_types_map.keys():
            setattr(self, k, self.get_seq_seq(locals()[k], []))
            if k=='vertex':
                r = []
                for v in self.vertex:
                    r += map(lambda a:[a],v)
                self.vertex = r
            if self._check_int_seq(getattr(self,k),sz):
                raise ValueError('In cell %s: must be (seq of seq|seq) integers less than %s'%(k,sz))

        for k,n in self._vtk_cell_nums_map.items():
            if n==-1: continue
            kv = getattr(self,k)
            if kv==[] or kv[0]==[]: continue
            for v in kv:
                if len(v)!=n:
                    raise ValueError('Cell %s requires exactly %s points but got %s: %s'%(repr(k),n,len(v),v))

    def to_string(self,format='ascii'):
        t = self.get_datatype(self.points)
        ret = [b'DATASET UNSTRUCTURED_GRID',
               ('POINTS %s %s'%(self.get_size(),t)).encode(),
               self.seq_to_string(self.points,format,t)]
        tps = []
        r = []
        sz = 0
        for k in self._vtk_cell_types_map.keys():
            kv = getattr(self, k)
            if kv==[] or kv[0]==[]: continue
            s = self.seq_to_string([[len(v)]+list(v) for v in kv],format,'int')
            r.append(s)
            for v in kv:
                tps.append(self._vtk_cell_types_map[k])
                sz += len(v)+1
        sep = b'\n' if (format == 'ascii') else b''
        r = sep.join(r)
        ret += [('CELLS %s %s'%(len(tps),sz)).encode(),
                r,
                ('CELL_TYPES %s'%(len(tps))).encode(),
                self.seq_to_string(tps,format,'int')]
        return b'\n'.join(ret)

    def get_cell_size(self):
        sz = 0
        for k in self._vtk_cell_types_map.keys():
            kv = getattr(self,k)
            if kv==[] or kv[0]==[]: continue
            sz += len(kv)
        return sz
    def get_points(self):
        return self.points

def unstructured_grid_fromfile(f, self):
    l = common._getline(f).decode('ascii')
    k,n,datatype = [s.strip().lower() for s in l.split()]
    if k != 'points':
        raise ValueError( 'expected points but got %s'%(repr(k)))
    n = int(n)
    assert datatype in ['bit','unsigned_char','char','unsigned_short','short','unsigned_int','int','unsigned_long','long','float','double'],repr(datatype)
    points = []
    log.debug('\tgetting %s points'%n)
    while len(points) < 3*n:
        points += list(map(eval, common._getline(f).split()))
    assert len(points)==3*n

    l = common._getline(f).decode('ascii').split()
    assert len(l)==3 and l[0].strip().lower() == 'cells',repr(l)
    n = int(l[1])
    size = int(l[2])
    lst = []
    log.debug('\tgetting %s cell indexes'%size)
    while len(lst) < size:
        line = common._getline(f).decode('ascii')
        lst += list(map(eval, line.split()))
    assert len(lst)==size
    lst2 = []
    j = 0
    for i in range(n):
        lst2.append(lst[j+1:j+lst[j]+1])
        j += lst[j]+1
    l = common._getline(f).decode('ascii').split()
    assert len(l)==2 and l[0].strip().lower() == 'cell_types' and int(l[1])==n, repr(l)
    tps = []
    log.debug('\tgetting %s cell types'%n)
    while len(tps) < n:
        tps += list(map(int, common._getline(f).decode('ascii').split()))
    assert len(tps)==n
    dictionary = {}
    for i,t in zip(lst2,tps):
        k = UnstructuredGrid._vtk_cell_types_imap[t]
        if k not in dictionary:
            dictionary[k] = []
        dictionary[k].append(i)
    log.debug('unstructured_grid_fromfile done')
    return UnstructuredGrid(points,**dictionary), common._getline(f)

if __name__ == "__main__":
    print(UnstructuredGrid([[1,2],[2,4],3,5],
                           line = [[2,3],[1,2],[2,3]],
                           vertex=2))
