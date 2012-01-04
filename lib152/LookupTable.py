#!/usr/bin/env python
"""

Copyright 2001 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@ioc.ee>          
Permission to use, modify, and distribute this software is given under the
terms of the LGPL.  See http://www.fsf.org

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Revision: 1.1 $
$Date: 2001/05/20 12:51:29 $
Pearu Peterson
"""

__version__ = "$Id: LookupTable.py,v 1.1 2001/05/20 12:51:29 pearu Exp $"

import common
import DataSetAttr
import string

class LookupTable(DataSetAttr.DataSetAttr):
    """Holds VTK LookupTable.
    """
    def __init__(self,table,name=None):
        self.name = self._get_name(name)
        self.table = self.get_n_seq_seq(table,[0,0,0,0])
        if len(self.table[0])!=4:
            raise ValueError,'expected sequence of 4-sequences but got %s'%(len(self.table[0]))
    def to_string(self,format='ascii'):
        ret = ['LOOKUP_TABLE %s %s'%(self.name,len(self.table))]
        seq = self.table
        if format=='binary':
            if not common.is_int255(seq):
                seq = self.float01_to_int255(seq)
            ret.append(self.seq_to_string(seq,format,'unsigned char'))
        else:
            if not common.is_float01(seq):
                seq = self.int255_to_float01(seq)
            ret.append(self.seq_to_string(seq,format,'float'))
        return string.join(ret,'\n')
    def get_size(self):
        return len(self.table)

if __name__ == "__main__":
    print LookupTable([[3,3],[4,3],240,3,2]).to_string()
