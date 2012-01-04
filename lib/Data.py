#!/usr/bin/env python
"""
PointData, CellData
"""
"""

Copyright 2001 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@ioc.ee>          
Permission to use, modify, and distribute this software is given under the
terms of the LGPL.  See http://www.fsf.org

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Revision: 1.3 $
$Date: 2001/06/13 08:35:00 $
Pearu Peterson
"""

__version__ = "$Id: Data.py,v 1.3 2001/06/13 08:35:00 pearu Exp $"


import common

class Data(common.Common):
    data_type = None
    def __init__(self,*args):
        if self.__class__.__name__ not in ['PointData','CellData']:
            raise TypeError,'use PointData or CellData instead of Data'
        self.data = []
        self.length = None
        map(self.append,args)
    def append(self,obj):
        if not common.is_datasetattr(obj):
            self.error('expected DataSetAttr argument but got %s'%(type(obj)))
            raise TypeError
        if self.length is None:
            self.length = obj.get_size()
        if not isinstance(obj,LookupTable.LookupTable) and self.length != obj.get_size():
            self.error('attribute data %s must be of length %s (as defined by first DataSetAttr) but got %s'%(`obj.__class__.__name__`,self.length,obj.get_size()))
            raise ValueError
        self.data.append(obj)
    def get_size(self):
        return self.length
    def to_string(self,format='ascii'):
        if self.data_type is None:
            raise TypeError,'use PointData or CellData instead of Data'
        ret = ['%s %s'%(self.data_type,self.length)]
        ret += [a.to_string(format) for a in self.data]
        return '\n'.join(ret)

class PointData(Data):
    """
    Usage:
      PointData(<DataSetAttr instances>)
    Attributes:
      data - list of DataSetAttr instances
    Public methods:
      get_size()
      to_string(format = 'ascii')
      append(<DataSetAttr instance>)
    """
    data_type = 'POINT_DATA'

class CellData(Data):
    """
    Usage:
      CellData(<DataSetAttr instances>)
    Attributes:
      data - list of DataSetAttr instances
    Public methods:
      get_size()
      to_string(format = 'ascii')
      append(<DataSetAttr instance>)
    """
    data_type = 'CELL_DATA'

import LookupTable

if __name__ == "__main__":
    import Scalars
    print PointData(Scalars.Scalars([2,3]))




