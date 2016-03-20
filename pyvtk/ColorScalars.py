#!/usr/bin/env python
"""
ColorScalars
"""
__author__ = "Pearu Peterson <pearu.peterson@gmail.com>"
__license__ = "New BSD"

import pyvtk.common as common
import pyvtk.DataSetAttr as DataSetAttr

class ColorScalars(DataSetAttr.DataSetAttr):
    """Holds VTK color scalars.
    Usage:
       ColorScalars(<sequence of n-sequences> ,name = <string>)
    Attributes:
       scalars
       name
    Public methods:
      get_size()
      to_string(format = 'ascii')
    """
    def __init__(self,scalars,name=None):
        self.name = self._get_name(name)
        self.scalars = self.get_n_seq_seq(scalars,self.default_value)
    def to_string(self,format='ascii'):
        ret = ['COLOR_SCALARS %s %s'%(self.name,len(self.scalars[0]))]
        seq = self.scalars
        if format=='binary':
            if not common.is_int255(seq):
                seq = self.float01_to_int255(seq)
            ret.append(self.seq_to_string(seq,format,'unsigned char'))
        else:
            if not common.is_float01(seq):
                seq = self.int255_to_float01(seq)
            ret.append(self.seq_to_string(seq,format,'float'))
        return '\n'.join(ret)
    def get_size(self):
        return len(self.scalars)

def color_scalars_fromfile(f,n,sl):
    assert len(sl)==2
    dataname = sl[0].strip()
    nvals = int(sl[1])
    scalars = []
    while len(scalars)<nvals*n:
        scalars += map(float, common._getline(f).decode('ascii').split(' '))
    assert len(scalars)==nvals*n
    scalars2 = []
    for i in range(0,len(scalars),nvals):
        scalars2.append(scalars[i:i+nvals])
    return ColorScalars(scalars2,dataname)
if __name__ == "__main__":
    print(ColorScalars([[3,3],[4,3],240,3,2]).to_string())
