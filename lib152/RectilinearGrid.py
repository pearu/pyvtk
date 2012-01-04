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

import DataSet
import string

class RectilinearGrid(DataSet.DataSet):
    """The topology of a dataset is described by
    x-coordinates
    y-coordinates
    z-coordinates
    """

    def __init__(self,x=None,y=None,z=None):
        self.x = self.get_seq(x,[0])
        self.y = self.get_seq(y,[0])
        self.z = self.get_seq(z,[0])
        self.dimensions = (len(self.x),len(self.y),len(self.z))
        if self._check_dimensions():
            raise ValueError,'dimensions must be 3-tuple of ints >=1'

    def to_string(self, format='ascii'):
        tx = self.get_datatype(self.x)
        ty = self.get_datatype(self.y)
        tz = self.get_datatype(self.z)
        ret = ['DATASET RECTILINEAR_GRID',
               'DIMENSIONS %s %s %s'%self.dimensions,
               'X_COORDINATES %s %s'%(len(self.x),tx),
               self.seq_to_string(self.x,format,tx),
               'Y_COORDINATES %s %s'%(len(self.y),ty),
               self.seq_to_string(self.y,format,ty),
               'Z_COORDINATES %s %s'%(len(self.z),tz),
               self.seq_to_string(self.z,format,tz)]
        return string.join(ret,'\n')

if __name__ == "__main__":
    print RectilinearGrid([1,2,2,4,4,5.4])
