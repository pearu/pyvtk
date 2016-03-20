#!/usr/bin/env python
"""
PointData, CellData
"""
__author__ = "Pearu Peterson <pearu.peterson@gmail.com>"
__license__ = "New BSD"

import logging
log = logging.getLogger(__name__)

__version__ = "$Id: Data.py,v 1.3 2001/06/13 08:35:00 pearu Exp $"

import pyvtk.common as common
import pyvtk.Scalars as Scalars
import pyvtk.LookupTable as LookupTable
from pyvtk.DataSetAttr import is_datasetattr

class Data(common.Common):
    data_type = None

    def __init__(self,*args):
        if self.__class__.__name__ not in ['PointData','CellData']:
            raise TypeError('use PointData or CellData instead of Data')
        self.data = []
        self.length = None
        list(map(self.append,args))

    def append(self,obj):
        if not is_datasetattr(obj):
            log.error('expected DataSetAttr argument but got %s'%(type(obj)))
            raise TypeError
        if self.length is None:
            self.length = obj.get_size()
        if not isinstance(obj,LookupTable) and self.length != obj.get_size():
            log.error('attribute data %s must be of length %s (as defined by first DataSetAttr) but got %s'%(repr(obj.__class__.__name__),self.length,obj.get_size()))
            raise ValueError
        self.data.append(obj)

    def get_size(self):
        return self.length

    def to_string(self,format='ascii'):
        if self.data_type is None:
            raise TypeError('use PointData or CellData instead of Data')
        ret = [('%s %s'%(self.data_type,self.length)).encode()]
        ret += [a.to_string(format) for a in self.data]
        return b'\n'.join(ret)

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

def is_pointdata(obj):
    return isinstance(obj,PointData)
def is_celldata(obj):
    return isinstance(obj,CellData)

if __name__ == "__main__":
    print(PointData(Scalars.Scalars([2,3])))




