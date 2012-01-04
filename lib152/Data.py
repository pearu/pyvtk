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

__version__ = "$Id: Data.py,v 1.1 2001/05/20 12:51:29 pearu Exp $"

import string
import common

class Data(common.Common):
    data_type = None
    def __init__(self,*args):
        if self.__class__.__name__ not in ['PointData','CellData']:
            raise TypeError,'use PointData or CellData instead of Data'
        if not args:
            raise TypeError,self.__class__.__name__+'() takes at least 1 argument: Scalars|ColorScalars|LookupTable|Vectors|Normals|TextureCoordinates|Tensors|Field'
        args = list(args)
        length = None
        for a in args:
            if not common.is_datasetattr(a):
                self.skipping('expected DataSetAttr argument but got %s'%(type(a)))
                continue
            if length is None:
                length = a.get_size()
            elif length != a.get_size():
                self.skipping('attribute data %s must be of length %s (as defined by first DataSetAttr) but got %s'%(`a.__class__.__name__`,length,a.get_size()))
                continue
        self.length = length
        self.data = args
    def get_size(self):
        return self.length
    def to_string(self,format='ascii'):
        if self.data_type is None:
            raise TypeError,'use PointData or CellData instead of Data'
        ret = ['%s %s'%(self.data_type,self.length)]
        for a in self.data:
            ret.append(a.to_string(format))
        #ret += [a.to_string(format) for a in self.data]
        return string.join(ret,'\n')

class PointData(Data):
    data_type = 'POINT_DATA'

class CellData(Data):
    data_type = 'CELL_DATA'

if __name__ == "__main__":
    import Scalars
    print PointData(Scalars.Scalars([2,3]))
