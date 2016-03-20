#!/usr/bin/env python
"""
StructuredPoints
"""
__author__ = "Pearu Peterson <pearu.peterson@gmail.com>"
__license__ = "New BSD"

import pyvtk.DataSet as DataSet
import pyvtk.common as common

class StructuredPoints(DataSet.DataSet):
    """
    Usage:
      StructuredPoints(<3-tuple of dimensions>, origin = <3-tuple>, spacing = <3-tuple>)
    Attributes:
      dimensions
      origin
      spacing
    Public methods:
      get_size()
      get_cell_size()
      to_string(format = 'ascii')
      get_points()
      <DataSetAttr class>(...)
    """

    def __init__(self,dimensions,origin=(0,0,0),spacing=(1,1,1)):
        self.dimensions = self.get_3_tuple(dimensions,(1,1,1))
        if self._check_dimensions():
            raise(ValueError,'dimensions must be 3-tuple of ints >=1')
        self.origin = self.get_3_tuple(origin,(1,1,1))
        if self._check_origin():
            raise(ValueError,'origin must be 3-tuple of numbers')
        self.spacing = self.get_3_tuple(spacing,(1,1,1))
        if self._check_spacing():
            raise(ValueError,'spacing must be 3-tuple of positive numbers')

    def to_string(self,format = 'ascii'):
        ret = ['DATASET STRUCTURED_POINTS',
               'DIMENSIONS %s %s %s'%self.dimensions,
               'ORIGIN %s %s %s'%self.origin,
               'SPACING %s %s %s'%self.spacing]
        return '\n'.join(ret).encode()

    def get_points(self):
        if hasattr(self,'points'):
            return self.points
        arr = []
        for k in range(self.dimensions[2]):
            z = self.origin[2] + k * self.spacing[2]
            for j in range(self.dimensions[1]):
                y = self.origin[1] + j * self.spacing[1]
                for i in range(self.dimensions[0]):
                    x = self.origin[0] + i * self.spacing[0]
                    arr.append((x,y,z))
        self.points = arr
        return arr

def structured_points_fromfile(f,self):
    l = common._getline(f).decode('ascii').split(' ')
    assert l[0].strip().lower() == 'dimensions'
    dims = list(map(int, l[1:]))
    assert len(dims)==3
    l = common._getline(f).decode('ascii').split(' ')
    assert l[0].strip().lower() == 'origin'
    origin = list(map(eval,l[1:]))
    assert len(origin)==3
    l = common._getline(f).decode('ascii').split(' ')
    assert l[0].strip().lower() == 'spacing'
    spacing = list(map(eval,l[1:]))
    assert len(spacing)==3
    return StructuredPoints(dims,origin,spacing),common._getline(f)
    
if __name__ == "__main__":
    print(StructuredPoints((2,3,4)))
    print(StructuredPoints((2,3)))
    print(StructuredPoints(5))
    print(StructuredPoints([2,3,5,6]).get_size())
