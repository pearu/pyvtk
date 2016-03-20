#!/usr/bin/env python
"""
TextureCoordinates
"""
__author__ = "Pearu Peterson <pearu.peterson@gmail.com>"
__license__ = "New BSD"

import pyvtk.DataSetAttr as DataSetAttr
from . import common

class TextureCoordinates(DataSetAttr.DataSetAttr):
    """Holds VTK Texture Coordinates.
    Usage:
      TextureCoordinates(<sequence of (1,2, or 3)-sequences> ,name = <string>)
    Attributes:
      coords
      name
    Public methods:
      get_size()
      to_string(format = 'ascii')
    """
    def __init__(self,scalars,name=None):
        self.name = self._get_name(name)
        self.coords = self.get_n_seq_seq(scalars,self.default_value)
        if not 1<=len(self.coords[0])<=3:
            raise ValueError('texture coordinates dimension must be 1, 2, or 3 but got %s'%(len(self.coords[0])))
    def to_string(self,format='ascii'):
        t = self.get_datatype(self.coords)
        ret = ['TEXTURE_COORDINATES %s %s %s'%(self.name,len(self.coords[0]),t),
               self.seq_to_string(self.coords,format,t)]
        return '\n'.join(ret)
    def get_size(self):
        return len(self.coords)

def texture_coordinates_fromfile(f,n,sl):
    assert len(sl)==3
    dataname = sl[0].strip()
    dim = int(sl[1])
    datatype = sl[2].strip().lower()
    assert datatype in ['bit','unsigned_char','char','unsigned_short','short','unsigned_int','int','unsigned_long','long','float','double'],repr(datatype)
    arr = []
    while len(arr)<dim*n:
        arr += map(eval, common._getline(f).split(' '))
    assert len(arr)==dim*n
    arr2 = []
    for i in range(0,len(arr),dim):
        arr2.append(arr[i:i+dim])
    return TextureCoordinates(arr2,dataname)

if __name__ == "__main__":
    print(TextureCoordinates([[3,3],[4,3],240,3,2]).to_string())
