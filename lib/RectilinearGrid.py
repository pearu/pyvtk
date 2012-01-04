#!/usr/bin/env python
"""
RectilinearGrid
"""
"""

Copyright 2001 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@ioc.ee>          
Permission to use, modify, and distribute this software is given under the
terms of the LGPL.  See http://www.fsf.org

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Revision: 1.3 $
$Date: 2001/05/31 17:48:54 $
Pearu Peterson
"""

import DataSet
import common

class RectilinearGrid(DataSet.DataSet):
    """
    Usage:
      RectilinearGrid(x = <sequence>, y = <sequence>, z = <sequence>)
    Attributes:
      x
      y
      z
      dimensions
    Public methods:
      get_size()
      get_cell_size()
      to_string(format = 'ascii')
      get_points()
      <DataSetAttr class>(...)
    """

    def __init__(self,x=None,y=None,z=None):
        self.x = self.get_seq(x,[0])
        self.y = self.get_seq(y,[0])
        self.z = self.get_seq(z,[0])
        self.dimensions = (len(self.x),len(self.y),len(self.z))
        if self._check_dimensions():
            raise ValueError,'dimensions must be 3-tuple of ints >=1'

    def to_string(self, format='ascii'):
        tx = self.get_datatype(self.x)
        ty = self.get_datatype(self.y)
        tz = self.get_datatype(self.z)
        ret = ['DATASET RECTILINEAR_GRID',
               'DIMENSIONS %s %s %s'%self.dimensions,
               'X_COORDINATES %s %s'%(len(self.x),tx),
               self.seq_to_string(self.x,format,tx),
               'Y_COORDINATES %s %s'%(len(self.y),ty),
               self.seq_to_string(self.y,format,ty),
               'Z_COORDINATES %s %s'%(len(self.z),tz),
               self.seq_to_string(self.z,format,tz)]
        return '\n'.join(ret)
    def get_points(self):
        if hasattr(self,'points'):
            return self.points
        arr = [(x,y,z) for z in self.z for y in self.y for x in self.x]
        self.points = arr
        return arr

def rectilinear_grid_fromfile(f,self):
    l = common._getline(f).split(' ')
    assert l[0].strip().lower() == 'dimensions'
    dims = map(eval,l[1:])
    assert len(dims)==3
    for c in 'xyz':
        l = common._getline(f)
        k,n,datatype = [s.strip().lower() for s in l.split(' ')]
        if k!=c+'_coordinates':
            raise ValueError, 'expected %s_coordinates but got %s'%(c,`k`)
        n = eval(n)
        assert datatype in ['bit','unsigned_char','char','unsigned_short','short','unsigned_int','int','unsigned_long','long','float','double'],`datatype`
        points = []
        while len(points) < n:
            points += map(eval,common._getline(f).split(' '))
        assert len(points)==n
        exec '%s_coords = points'%c
    assert map(len,[x_coords,y_coords,z_coords]) == dims
    return RectilinearGrid(x_coords,y_coords,z_coords),common._getline(f)

if __name__ == "__main__":
    print RectilinearGrid([1,2,2,4,4,5.4])
