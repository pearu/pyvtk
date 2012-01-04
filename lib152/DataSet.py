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

__version__ = "$Id: DataSet.py,v 1.1 2001/05/20 12:51:29 pearu Exp $"

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
            
