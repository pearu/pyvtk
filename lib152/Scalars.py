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

__version__ = "$Id: Scalars.py,v 1.1 2001/05/20 12:51:29 pearu Exp $"

import DataSetAttr
import string

class Scalars(DataSetAttr.DataSetAttr):
    """Holds VTK scalars.
    """
    def __init__(self,scalars,name=None,lookup_table=None):
        self.name = self._get_name(name)
        self.lookup_table = self._get_lookup_table(lookup_table)
        self.scalars = self.get_seq(scalars,[])
    def to_string(self,format='ascii'):
        t = self.get_datatype(self.scalars)
        ret = ['SCALARS %s %s %s'%(self.name,t,1),
               'LOOKUP_TABLE %s'%(self.lookup_table)]
        ret.append(self.seq_to_string(self.scalars,format,t))
        return string.join(ret,'\n')
    def get_size(self):
        return len(self.scalars)

if __name__ == "__main__":
    print Scalars([3,4,240]).to_string('binary')
