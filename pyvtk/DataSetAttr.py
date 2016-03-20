#!/usr/bin/env python
"""
DataSetAttr
"""
__author__ = "Pearu Peterson <pearu.peterson@gmail.com>"
__license__ = "New BSD"

import logging
log = logging.getLogger(__name__)

import pyvtk.common as common

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
            log.info('Using default name=%s'%(repr(name)))
            return name
        if common.is_string(name):
            name = name.strip().replace(' ','_')
            if name:
                return name
        raise ValueError('name=%s must be non-empty string'%(repr(name)))

    def _get_lookup_table(self,name):
        if name is None:
            name = 'default'
            log.info('Using default lookup_table=%s'%(repr(name)))
            return name
        if common.is_string(name):
            name = name.strip().replace(' ','_')
            if name:
                return name
        raise ValueError('lookup_table=%s must be nonempty string'%(repr(name)))

def is_datasetattr(obj):
    return isinstance(obj,DataSetAttr)

if __name__ == "__main__":
    pass
