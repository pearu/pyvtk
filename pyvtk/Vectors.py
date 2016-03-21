#!/usr/bin/env python
"""
Vectors
"""
__author__ = "Pearu Peterson <pearu.peterson@gmail.com>"
__license__ = "New BSD"

import pyvtk.DataSetAttr as DataSetAttr
import pyvtk.common as common

class Vectors(DataSetAttr.DataSetAttr):
    """Holds VTK Vectors.
    Usage:
      Vectors(<sequence of 3-tuples> ,name = <string>)
    Attributes:
      vectors
      name
    Public methods:
      get_size()
      to_string(format = 'ascii')
    """
    def __init__(self,vectors,name=None):
        self.name = self._get_name(name)
        self.vectors = self.get_3_tuple_list(vectors,(self.default_value,)*3)

    def to_string(self,format='ascii'):
        t = self.get_datatype(self.vectors)
        ret = [('VECTORS %s %s'%(self.name,t)).encode(),
               self.seq_to_string(self.vectors,format,t)]
        return b'\n'.join(ret)

    def get_size(self):
        return len(self.vectors)

def vectors_fromfile(f,n,sl):
    dataname = sl[0]
    datatype = sl[1].lower()
    assert datatype in ['bit','unsigned_char','char','unsigned_short','short','unsigned_int','int','unsigned_long','long','float','double'],repr(datatype)
    vectors = []
    while len(vectors) < 3*n:
        vectors += map(eval,common._getline(f).split(' '))
    assert len(vectors) == 3*n
    return Vectors(vectors,dataname)

if __name__ == "__main__":
    print(Vectors([[3,3],[4,3.],240,3,2]).to_string())
