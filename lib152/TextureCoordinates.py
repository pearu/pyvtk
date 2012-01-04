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

class TextureCoordinates(DataSetAttr.DataSetAttr):
    """Holds VTK Texture Coordinates.
    """
    def __init__(self,scalars,name=None):
        self.name = self._get_name(name)
        self.coords = self.get_n_seq_seq(scalars,self.default_value)
        if not 1<=len(self.coords[0])<=3:
            raise ValueError,'texture coordinates dimension must be 1, 2, or 3 but got %s'%(len(self.coords[0]))
    def to_string(self,format='ascii'):
        t = self.get_datatype(self.coords)
        ret = ['TEXTURE_COORDINATES %s %s %s'%(self.name,len(self.coords[0]),t)]
        ret.append(self.seq_to_string(self.coords,format,t))
        return string.join(ret,'\n')
    def get_size(self):
        return len(self.coords)

if __name__ == "__main__":
    print TextureCoordinates([[3,3],[4,3],240,3,2]).to_string()
