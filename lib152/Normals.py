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
import math
import string

class Normals(DataSetAttr.DataSetAttr):
    """Holds VTK Normals.
    """
    def __init__(self,normals,name=None):
        self.name = self._get_name(name)
        seq = []
        for v in self.get_3_tuple_list(normals,(self.default_value,)*3):
            n = math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])
            if n==0:
                self.warning('Cannot normalize zero vector to 1-length')
                seq.append(v)
            elif n==1:
                seq.append(v)
            else:
                seq.append(tuple(map(lambda c,n=n:c/n,v)))
                #seq.append(tuple([c/n for c in v]))
        self.normals = seq
    def to_string(self,format='ascii'):
        t = self.get_datatype(self.normals)
        ret = ['NORMALS %s %s'%(self.name,t)]
        ret.append(self.seq_to_string(self.normals,format,t))
        return string.join(ret,'\n')
    def get_size(self):
        return len(self.normals)

if __name__ == "__main__":
    print Normals([[3,3],[4,3.],240,3,2]).to_string()
