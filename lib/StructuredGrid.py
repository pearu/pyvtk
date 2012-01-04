#!/usr/bin/env python
"""
StructuredGrid
"""
"""

Copyright 2001 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@ioc.ee>          
Permission to use, modify, and distribute this software is given under the
terms of the LGPL.  See http://www.fsf.org

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Revision: 1.4 $
$Date: 2007-02-22 08:43:39 $
Pearu Peterson
"""

import DataSet
import common

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
            raise ValueError,'dimensions must be 3-tuple of ints >=1 and matching with the size of points'

    def to_string(self, format='ascii'):
        t = self.get_datatype(self.points)
        ret = ['DATASET STRUCTURED_GRID',
               'DIMENSIONS %s %s %s'%self.dimensions,
               'POINTS %s %s'%(self.get_size(),t),
               self.seq_to_string(self.points,format,t)]
        return '\n'.join(ret)

    def get_points(self):
        return self.points

    def get_cell_size(self):
        return len(self.points)

def structured_grid_fromfile(f,self):
    l = common._getline(f).split(' ')
    assert l[0].strip().lower() == 'dimensions'
    dims = map(eval,l[1:])
    assert len(dims)==3
    l = common._getline(f)
    k,n,datatype = [s.strip().lower() for s in l.split(' ')]
    if k!='points':
        raise ValueError, 'expected points but got %s'%(`k`)
    n = eval(n)
    assert datatype in ['bit','unsigned_char','char','unsigned_short','short','unsigned_int','int','unsigned_long','long','float','double'],`datatype`
    points = []
    self.message('\tgetting %s points'%n)
    while len(points) < 3*n:
        l = common._getline(f)
        points += map(eval,l.split(' '))
    assert len(points)==3*n
    return StructuredGrid(dims,points),common._getline(f)

if __name__ == "__main__":
    print StructuredGrid((1,2),[1,2,2,4,4,5.4])
