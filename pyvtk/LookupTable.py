#!/usr/bin/env python
"""
LookupTable
"""
__author__ = "Pearu Peterson <pearu.peterson@gmail.com>"
__license__ = "New BSD"

import pyvtk.common as common
import pyvtk.DataSetAttr as DataSetAttr

class LookupTable(DataSetAttr.DataSetAttr):
    """Holds VTK LookupTable.
    Usage:
      LookupTable(<sequence of 4-sequences> ,name = <string>)
    Attributes:
      table
      name
    Public methods:
      get_size()
      to_string(format = 'ascii')
    """
    def __init__(self,table,name=None):
        self.name = self._get_name(name)
        self.table = self.get_n_seq_seq(table,[0,0,0,0])
        if len(self.table[0])!=4:
            raise ValueError('expected sequence of 4-sequences but got %s'%(len(self.table[0])))

    def to_string(self, format='ascii'):
        ret = [('LOOKUP_TABLE %s %s'%(self.name,len(self.table))).encode()]
        seq = self.table
        if format=='binary':
            if not common.is_int255(seq):
                seq = self.float01_to_int255(seq)
            ret.append(self.seq_to_string(seq,format,'unsigned char'))
        else:
            if not common.is_float01(seq):
                seq = self.int255_to_float01(seq)
            ret.append(self.seq_to_string(seq,format,'float'))
        return b'\n'.join(ret)

    def get_size(self):
        return len(self.table)

def lookup_table_fromfile(f,n,sl):
    tablename = sl[0]
    size = int(sl[1])
    table = []
    while len(table)<4*size:
        table += map(eval, common._getline(f).decode('ascii').split(' '))
    assert len(table) == 4*size
    table2 = []
    for i in range(0,len(table),4):
        table2.append(table[i:i+4])
    return LookupTable(table2,tablename)

if __name__ == "__main__":
    print(LookupTable([[3,3],[4,3],240,3,2]).to_string())
