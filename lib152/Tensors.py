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

class Tensors(DataSetAttr.DataSetAttr):
    """Holds VTK Tensors.
    """
    def __init__(self,tensors,name=None):
        self.name = self._get_name(name)
        self.tensors = self.get_3_3_tuple_list(tensors,(self.default_value,)*3)
    def to_string(self,format='ascii'):
        t = self.get_datatype(self.tensors)
        ret = ['TENSORS %s %s'%(self.name,t)]
        ret.append(self.seq_to_string(self.tensors,format,t))
        return string.join(ret,'\n')
    def get_size(self):
        return len(self.tensors)

if __name__ == "__main__":
    print Tensors([[[3,3]],[4,3.],[[240]],3,2,3]).to_string('ascii')
    print Tensors(3).to_string('ascii')
