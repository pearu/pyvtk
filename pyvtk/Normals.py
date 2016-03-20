#!/usr/bin/env python
"""
Normals
"""
__author__ = "Pearu Peterson <pearu.peterson@gmail.com>"
__license__ = "New BSD"

import logging
log = logging.getLogger(__name__)

import math

import pyvtk.DataSetAttr as DataSetAttr
import pyvtk.common as common

class Normals(DataSetAttr.DataSetAttr):
    """Holds VTK Normals.
    Usage:
      Normals(<sequence of 3-tuples> ,name = <string>)
    Attributes:
      normals
      name
    Public methods:
      get_size()
      to_string(format = 'ascii')
    """
    def __init__(self,normals,name=None):
        self.name = self._get_name(name)
        seq = []
        for v in self.get_3_tuple_list(normals,(self.default_value,)*3):
            n = math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])
            if n==0:
                log.warning('cannot normalize zero vector')
                seq.append(v)
            elif n==1:
                seq.append(v)
            else:
                seq.append(tuple([c/n for c in v]))
        self.normals = seq

    def to_string(self,format='ascii'):
        t = self.get_datatype(self.normals)
        ret = [('NORMALS %s %s'%(self.name,t)).encode(),
               self.seq_to_string(self.normals,format,t)]
        return b'\n'.join(ret)

    def get_size(self):
        return len(self.normals)

def normals_fromfile(f,n,sl):
    dataname = sl[0]
    datatype = sl[1].lower()
    assert datatype in ['bit','unsigned_char','char','unsigned_short','short','unsigned_int','int','unsigned_long','long','float','double'],repr(datatype)
    normals = []
    while len(normals) < 3*n:
        normals += map(eval,common._getline(f).decode('ascii').split(' '))
    assert len(normals) == 3*n
    return Normals(normals,dataname)

if __name__ == "__main__":
    print(Normals([[3,3],[4,3.],240,3,2]).to_string())
