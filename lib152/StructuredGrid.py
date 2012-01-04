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

class StructuredGrid(DataSet.DataSet):
    """The topology of a dataset is described by
    dimensions - 3-sequence of positive integers
    points - sequence of 3-sequences|3x-sequence
    """

    def __init__(self,dimensions,points):
        self.dimensions = self.get_3_tuple(dimensions,(1,1,1))
        self.points = self.get_3_tuple_list(points,(0,0,0))
        if self._check_dimensions():
            raise ValueError,'dimensions must be 3-tuple of ints >=1 and matching with the size of points'

    def to_string(self, format='ascii'):
        t = self.get_datatype(self.points)
        ret = ['DATASET STRUCTURED_GRID',
               'DIMENSIONS %s %s %s'%self.dimensions,
               'POINTS %s %s'%(self.get_size(),t)
               ]
        ret.append(self.seq_to_string(self.points,format,t))
        return string.join(ret,'\n')

if __name__ == "__main__":
    print StructuredGrid((1,2),[1,2,2,4,4,5.4])
