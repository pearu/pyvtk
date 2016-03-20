#!/usr/bin/env python
"""
StructuredGrid
"""
__author__ = "Pearu Peterson <pearu.peterson@gmail.com>"
__license__ = "New BSD"

import logging
log = logging.getLogger(__name__)

import pyvtk.DataSet as DataSet
import pyvtk.common as common

class StructuredGrid(DataSet.DataSet):
    """
    Usage:
      StructuredGrid(<3-tuple of dimensions>, <sequence of 3-tuples of points>)
    Attributes:
      dimensions
      points
    Public methods:
      get_points()
      get_size()
      get_cell_size()
      to_string(format = 'ascii')
      get_points()
      <DataSetAttr class>(...)
    """

    def __init__(self,dimensions,points):
        self.dimensions = self.get_3_tuple(dimensions,(1,1,1))
        self.points = self.get_3_tuple_list(points,(0,0,0))
        if self._check_dimensions():
            raise ValueError('dimensions must be 3-tuple of ints >=1 and matching with the size of points')

    def to_string(self, format='ascii'):
        t = self.get_datatype(self.points)
        ret = [b'DATASET STRUCTURED_GRID',
               ('DIMENSIONS %s %s %s'%self.dimensions).encode(),
               ('POINTS %s %s'%(self.get_size(),t)).encode(),
               self.seq_to_string(self.points,format,t)]
        return b'\n'.join(ret)

    def get_points(self):
        return self.points

    def get_cell_size(self):
        return len(self.points)

def structured_grid_fromfile(f,self):
    l = common._getline(f).split(' ')
    assert l[0].strip().lower() == 'dimensions'
    dims = list(map(int, l[1:]))
    assert len(dims)==3
    l = common._getline(f)
    k,n,datatype = [s.strip().lower() for s in l.split(' ')]
    if k!='points':
        raise ValueError( 'expected points but got %s'%(repr(k)))
    n = int(n)
    assert datatype in ['bit','unsigned_char','char','unsigned_short','short','unsigned_int','int','unsigned_long','long','float','double'],repr(datatype)
    points = []
    log.debug('\tgetting %s points'%n)
    while len(points) < 3*n:
        l = common._getline(f)
        points += map(eval,l.split(' '))
    assert len(points)==3*n
    return StructuredGrid(dims,points),common._getline(f)

if __name__ == "__main__":
    print(StructuredGrid((1,2),[1,2,2,4,4,5.4]))
