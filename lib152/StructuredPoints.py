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
class StructuredPoints(DataSet.DataSet):
    """The topology of a dataset is described by
    dimensions - int|(1-3)-int sequence (>=1)
    origin - number|(1-3)-number sequence
    spacing - number|(1-3)-number sequence (>0)
    """

    def __init__(self,dimensions,origin=(0,0,0),spacing=(1,1,1)):
        self.dimensions = self.get_3_tuple(dimensions,(1,1,1))
        if self._check_dimensions():
            raise ValueError,'dimensions must be 3-tuple of ints >=1'
        self.origin = self.get_3_tuple(origin,(1,1,1))
        if self._check_origin():
            raise ValueError,'origin must be 3-tuple of numbers'
        self.spacing = self.get_3_tuple(spacing,(1,1,1))
        if self._check_spacing():
            raise ValueError,'spacing must be 3-tuple of positive numbers'

    def to_string(self,format = 'ascii'):
        ret = ['DATASET STRUCTURED_POINTS',
               'DIMENSIONS %s %s %s'%self.dimensions,
               'ORIGIN %s %s %s'%self.origin,
               'SPACING %s %s %s'%self.spacing]
        return string.join(ret,'\n')

if __name__ == "__main__":
    print StructuredPoints((2,3,4))
    print StructuredPoints((2,3))
    print StructuredPoints(5)
    print StructuredPoints([2,3,5,6]).get_size()
