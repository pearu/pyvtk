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

__version__ = "$Id: ColorScalars.py,v 1.1 2001/05/20 12:51:29 pearu Exp $"

import common
import DataSetAttr
import string

class ColorScalars(DataSetAttr.DataSetAttr):
    """Holds VTK color scalars.
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
        return string.join(ret,'\n')
    def get_size(self):
        return len(self.scalars)

if __name__ == "__main__":
    print ColorScalars([[3,3],[4,3],240,3,2]).to_string()
