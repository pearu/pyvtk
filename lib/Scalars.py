#!/usr/bin/env python
"""
Scalars
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

__version__ = "$Id: Scalars.py,v 1.3 2001/05/31 17:48:54 pearu Exp $"

import DataSetAttr
import common

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
        ret = ['SCALARS %s %s %s'%(self.name,t,1),
               'LOOKUP_TABLE %s'%(self.lookup_table),
               self.seq_to_string(self.scalars,format,t)]
        return '\n'.join(ret)
    def get_size(self):
        return len(self.scalars)

def scalars_fromfile(f,n,sl):
    dataname = sl[0]
    datatype = sl[1].lower()
    assert datatype in ['bit','unsigned_char','char','unsigned_short','short','unsigned_int','int','unsigned_long','long','float','double'],`datatype`
    if len(sl)>2:
        numcomp = eval(sl[2])
    else:
        numcomp = 1
    l = common._getline(f)
    l = l.split(' ')
    assert len(l)==2 and l[0].lower() == 'lookup_table'
    tablename = l[1]
    scalars = []
    while len(scalars) < n:
        scalars += map(eval,common._getline(f).split(' '))
    assert len(scalars)==n
    return Scalars(scalars,dataname,tablename)

if __name__ == "__main__":
    print Scalars([3,4,240]).to_string('binary')
