#!/usr/bin/env python
"""
Scalars
"""
__author__ = "Pearu Peterson <pearu.peterson@gmail.com>"
__license__ = "New BSD"

import pyvtk.DataSetAttr as DataSetAttr
import pyvtk.common as common

class Scalars(DataSetAttr.DataSetAttr):
    """Holds VTK scalars.
    Usage:
      Scalars(<sequence> ,name = <string>, lookup_table = 'default')
    Attributes:
      scalars
      name
      lookup_table
    Public methods:
      get_size()
      to_string(format = 'ascii')
    """
    def __init__(self,scalars,name=None,lookup_table=None):
        self.name = self._get_name(name)
        self.lookup_table = self._get_lookup_table(lookup_table)
        self.scalars = self.get_seq(scalars,[])
    def to_string(self,format='ascii'):
        t = self.get_datatype(self.scalars)
        ret = [('SCALARS %s %s %s'%(self.name,t,1)).encode(),
               ('LOOKUP_TABLE %s'%(self.lookup_table)).encode(),
               self.seq_to_string(self.scalars,format,t)]
        return b'\n'.join(ret)
    def get_size(self):
        return len(self.scalars)

def scalars_fromfile(f,n,sl):
    dataname = sl[0]
    datatype = sl[1].lower()
    assert datatype in ['bit','unsigned_char','char','unsigned_short','short','unsigned_int','int','unsigned_long','long','float','double'],repr(datatype)
    if len(sl)>2:
        numcomp = int(sl[2])
    else:
        numcomp = 1
    l = common._getline(f).decode('ascii')
    l = l.split(' ')
    assert len(l)==2 and l[0].lower() == 'lookup_table'
    tablename = l[1]
    scalars = []
    while len(scalars) < n:
        scalars += map(eval,common._getline(f).decode('ascii').split(' '))
    assert len(scalars)==n
    return Scalars(scalars,dataname,tablename)

if __name__ == "__main__":
    print(Scalars([3,4,240]).to_string('binary'))
