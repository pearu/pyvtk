#!/usr/bin/env python
"""
DataSetAttr
"""
"""

Copyright 2001 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@ioc.ee>          
Permission to use, modify, and distribute this software is given under the
terms of the LGPL.  See http://www.fsf.org

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Revision: 1.2 $
$Date: 2001/05/31 17:48:54 $
Pearu Peterson
"""

__version__ = "$Id: DataSetAttr.py,v 1.2 2001/05/31 17:48:54 pearu Exp $"

import common

class DataSetAttr(common.Common):
    """Abstract class for VTK data."""
    counters = {}
    default_value = 0
    def _get_default_name(self):
        n = self.__class__.__name__
        try:
            self.counters[n] += 1
        except KeyError:
            self.counters[n] = 0
        return self.__class__.__name__+str(self.counters[n])
    def _get_name(self,name):
        if name is None:
            name = self._get_default_name()
            self.warning('Using name=%s'%(`name`))
            return name
        if common.is_string(name):
            name = name.strip().replace(' ','_')
            if name:
                return name
        raise ValueError,'name=%s must be non-empty string'%(`name`)
    def _get_lookup_table(self,name):
        if name is None:
            name = 'default'
            self.warning('Using lookup_table=%s'%(`name`))
            return name
        if common.is_string(name):
            name = name.strip().replace(' ','_')
            if name:
                return name
        raise ValueError,'lookup_table=%s must be nonempty string'%(`name`)

if __name__ == "__main__":
    pass
