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

import DataSetAttr
import string
class Vectors(DataSetAttr.DataSetAttr):
    """Holds VTK Vectors.
    """
    def __init__(self,vectors,name=None):
        self.name = self._get_name(name)
        self.vectors = self.get_3_tuple_list(vectors,(self.default_value,)*3)
    def to_string(self,format='ascii'):
        t = self.get_datatype(self.vectors)
        ret = ['VECTORS %s %s'%(self.name,t),
               self.seq_to_string(self.vectors,format,t)]
        return string.join(ret,'\n')
    def get_size(self):
        return len(self.vectors)

if __name__ == "__main__":
    print Vectors([[3,3],[4,3.],240,3,2]).to_string()
