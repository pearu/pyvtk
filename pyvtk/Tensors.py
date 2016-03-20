#!/usr/bin/env python
"""
Tensors
"""
__author__ = "Pearu Peterson <pearu.peterson@gmail.com>"
__license__ = "New BSD"

import pyvtk.DataSetAttr as DataSetAttr
import pyvtk.common as common

class Tensors(DataSetAttr.DataSetAttr):
    """Holds VTK Tensors.
    Usage:
      Tensors(<sequence of 3x3-tuples> , name = <string>)
    Attributes:
      tensors
      name
    Public methods:
      get_size()
      to_string(format = 'ascii')
    """
    def __init__(self,tensors,name=None):
        self.name = self._get_name(name)
        self.tensors = self.get_3_3_tuple_list(tensors,(self.default_value,)*3)
    def to_string(self,format='ascii'):
        t = self.get_datatype(self.tensors)
        ret = ['TENSORS %s %s'%(self.name,t),
               self.seq_to_string(self.tensors,format,t)]
        return '\n'.join(ret)
    def get_size(self):
        return len(self.tensors)

def tensors_fromfile(f,n,sl):
    assert len(sl)==2
    dataname = sl[0].strip()
    datatype = sl[1].strip().lower()
    assert datatype in ['bit','unsigned_char','char','unsigned_short','short','unsigned_int','int','unsigned_long','long','float','double'],repr(datatype)
    arr = []
    while len(arr)<9*n:
        arr += map(eval,common._getline(f).split(' '))
    assert len(arr)==9*n
    arr2 = []
    for i in range(0,len(arr),9):
        arr2.append(tuple(map(tuple,[arr[i:i+3],arr[i+3:i+6],arr[i+6:i+9]])))
    return Tensors(arr2,dataname)

if __name__ == "__main__":
    print(Tensors([[[3,3]],[4,3.],[[240]],3,2,3]).to_string('ascii'))
    print(Tensors(3).to_string('ascii'))
