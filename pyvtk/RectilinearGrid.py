#!/usr/bin/env python
"""
RectilinearGrid
"""
__author__ = "Pearu Peterson <pearu.peterson@gmail.com>"
__license__ = "New BSD"

import pyvtk.DataSet as DataSet
import pyvtk.common as common

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
            raise ValueError('dimensions must be 3-tuple of ints >=1')

    def to_string(self, format='ascii'):
        tx = self.get_datatype(self.x)
        ty = self.get_datatype(self.y)
        tz = self.get_datatype(self.z)
        ret = [b'DATASET RECTILINEAR_GRID',
               ('DIMENSIONS %s %s %s'%self.dimensions).encode(),
               ('X_COORDINATES %s %s'%(len(self.x),tx)).encode(),
               self.seq_to_string(self.x,format,tx),
               ('Y_COORDINATES %s %s'%(len(self.y),ty)).encode(),
               self.seq_to_string(self.y,format,ty),
               ('Z_COORDINATES %s %s'%(len(self.z),tz)).encode(),
               self.seq_to_string(self.z,format,tz)]
        return b'\n'.join(ret)

    def get_points(self):
        if hasattr(self,'points'):
            return self.points
        arr = [(x,y,z) for z in self.z for y in self.y for x in self.x]
        self.points = arr
        return arr

def rectilinear_grid_fromfile(f,self):
    l = common._getline(f).decode('ascii').split(' ')
    assert l[0].strip().lower() == 'dimensions'
    dims = list(map(int, l[1:]))
    assert len(dims)==3
    coords = {}
    for c in 'xyz':
        l = common._getline(f).decode('ascii')
        k,n,datatype = [s.strip().lower() for s in l.split(' ')]
        if k!=c+'_coordinates':
            raise ValueError('expected %s_coordinates but got %s'%(c, repr(k)))
        n = int(n)
        assert datatype in ['bit','unsigned_char','char','unsigned_short','short','unsigned_int','int','unsigned_long','long','float','double'],repr(datatype)
        points = []
        while len(points) < n:
            points += map(eval, common._getline(f).decode('ascii').split(' '))
        assert len(points)==n
        coords[c] = points
    assert list(map(len, [coords['x'], coords['y'], coords['z']])) == dims
    return RectilinearGrid(coords['x'], coords['y'], coords['z']),common._getline(f)

if __name__ == "__main__":
    print(RectilinearGrid([1,2,2,4,4,5.4]))
