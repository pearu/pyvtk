#!/usr/bin/env python
"""
DataSet
"""
"""

Copyright 2001 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@ioc.ee>          
Permission to use, modify, and distribute this software is given under the
terms of the LGPL.  See http://www.fsf.org

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Revision: 1.3 $
$Date: 2001/05/31 17:48:54 $
Pearu Peterson
"""

__version__ = "$Id: DataSet.py,v 1.3 2001/05/31 17:48:54 pearu Exp $"

import common

class DataSet(common.Common):
    """Abstract class.
    It describes the geometry and topology of VTK dataset.
    """
    def get_size(self):
        if hasattr(self,'points'):
            return len(self.points)
        return reduce(lambda x,y:x*y,self.dimensions,1)
    def get_cell_size(self):
        return 0
    def _check_dimensions(self):
        for i in range(3):
            d = self.dimensions[i]
            if not common.is_int(d):
                self.error('dimensions[%s] must be int but got %s'%(i,type(d)))
                return 1
            if d<=0:
                self.error('dimensions[%s] must be positive int but got %s'%(i,d))
                return 1
        if hasattr(self,'points'):
            d = reduce(lambda x,y:x*y,self.dimensions,1)
            if len(self.points)!=d:
                self.error('mismatch of points length (%s) and dimensions size (%s)'%(len(self.points),d))
                return 1
        return 0
    def _check_origin(self):
        for i in range(3):
            d = self.origin[i]
            if not common.is_number(d):
                self.error('origin[%s] must be number but got %s'%(i,type(d)))
                return 1
        return 0
    def _check_spacing(self):
        for i in range(3):
            d = self.spacing[i]
            if not common.is_number(d):
                self.error('spacing[%s] must be number but got %s'%(i,type(d)))
                return 1
            if d<=0:
                self.error('spacing[%s] must be positive number but got %s'%(i,d))
                return 1
        return 0
    def _check_int_seq(self,obj,mx_int):
        if common.is_sequence(obj):
            for o in obj:
                if self._check_int_seq(o,mx_int):
                    return 1
        elif not common.is_int(obj) or obj>=mx_int:
            return 1
        return 0

    def Scalars(self,func,name = None,lookup_table = None):
        return Scalars.Scalars([func(*p) for p in self.get_points()],name,lookup_table)
    def ColorScalars(self,func,name = None):
        return ColorScalars.ColorScalars([func(*p) for p in self.get_points()],name)
    def LookupTable(self,func,name = None):
        return LookupTable.LookupTable([func(*p) for p in self.get_points()],name)
    def Vectors(self,func,name = None):
        return Vectors.Vectors([func(*p) for p in self.get_points()],name)
    def Normals(self,func,name = None):
        return Normals.Normals([func(*p) for p in self.get_points()],name)
    def TextureCoordinates(self,func,name = None):
        return TextureCoordinates.TextureCoordinates([func(*p) for p in self.get_points()],name)
    def Tensors(self,func,name = None):
        return Tensors.Tensors([func(*p) for p in self.get_points()],name)
    def Field(self,func,name = None, **kws):
        return Field.Field([func(*p) for p in self.get_points()],name, **kws)

import Scalars
import ColorScalars
import LookupTable
import Vectors
import Normals
import TextureCoordinates
import Tensors
import Field
