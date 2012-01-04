#!/usr/bin/env python
"""
Common functions/methods.
"""
"""

Copyright 2001 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@ioc.ee>          
Permission to use, modify, and distribute this software is given under the
terms of the LGPL.  See http://www.fsf.org

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Revision: 1.13 $
$Date: 2007-02-22 12:15:46 $
Pearu Peterson
"""


import types
import sys
import struct

def is_sequence(obj):
    """Check if obj is sequence."""
    try:
        len(obj)
        return 1
    except TypeError:
        return 0
def is_sequence2(obj):
    """Check if obj is sequence of sequences."""
    return is_sequence(obj) and len(obj) and is_sequence(obj[0])

def is_sequence3(obj):
    """Check if obj is sequence of sequences of sequences."""
    return is_sequence(obj) and len(obj) and is_sequence2(obj[0])

def is_number(obj):
    """Check if obj is number."""
    return isinstance(obj, (int, float))

def is_int(obj):
    """Check if obj is integer."""
    return isinstance(obj, int)

def is_float(obj):
    """Check if obj is float."""
    return isinstance(obj, float)

def is_string(obj):
    """Check if obj is string."""
    return isinstance(obj, str)

def is_int255(obj):
    if is_sequence(obj):
        for v in obj:
            r = is_int255(v)
            if not r: return 0
        return 1
    return 0<=obj<256

def is_float01(obj):
    if is_sequence(obj):
        for v in obj:
            r = is_float01(v)
            if not r: return 0
        return 1
    return 0<=obj<=1

def is_datasetattr(obj):
    return type(obj) is types.InstanceType and isinstance(obj,DataSetAttr.DataSetAttr)
def is_dataset(obj):
    return type(obj) is types.InstanceType and isinstance(obj,DataSet.DataSet)
def is_pointdata(obj):
    return type(obj) is types.InstanceType and isinstance(obj,Data.PointData)
def is_celldata(obj):
    return type(obj) is types.InstanceType and isinstance(obj,Data.CellData)

def _getline(f):
    l = ' '
    while l:
        l = f.readline()
        if l.strip():
            return l.strip()
    return None

class Common:
    """Abstract class. Defines output, checker, and getter functions."""
    struct_fmt_map = {'char':'c',
                      'long':'l','double':'d',
                      'int':'i','float':'f',
                      'unsigned char':'B'}
    default_int = 'int'
    default_float = 'float'
    def _get_trace(self,m):
        try:
            frame = sys._getframe().f_back
        except AttributeError: # Python 2.0 does not have sys._getframe
            frame = None
        n = ''
        while frame:
            i = frame.f_code.co_name
            n = '%s.%s'%(i,n)
            if i=='__init__':
                break
            frame = frame.f_back
            
        print >>sys.stderr,'%s.%s:\n\t%s'%(self.__class__.__name__,n[:-1],m)
    def warning(self,m=''):
        self._get_trace(m)
    def skipping(self,m=''):
        self._get_trace(m)
    def error(self,m=''):
        self._get_trace(m)
    def message(self,m=''):
        self._get_trace(m)
    def __str__(self):
        return self.to_string()
    def get_datatype(self,obj):
        typecode = None
        if hasattr(obj,'dtype'): # obj is numpy array
            typecode = obj.dtype.char
        elif hasattr(obj,'typecode'): # obj is Numeric array
            typecode = obj.typecode()

        if typecode is not None:
            r =  {'b':'unsigned_char', #'bit'??
                  'f':'float', 
                  'd':'double',
                  'i':'int',
                  'l':'long',
                  '1':'char',
                  's':'short',
                  'w':'unsigned_short',
                  'u':'unsigned_int'
                  #'?':'unsigned_long'
                  }.get(typecode)
            if r is not None:
                return r
        if is_int(obj): return self.default_int
        if is_float(obj): return self.default_float
        if not is_sequence(obj):
            raise ValueError,'expected int|float|non-empty sequence but got %s'\
                  %(type(obj))
        if not len(obj):
            self.warning('no data, no datatype, using int')
            r = 'int'
        for o in obj:
            r = self.get_datatype(o)
            if r==self.default_float:
                break
        return r
    def get_seq(self,obj,default=None):
        """Return sequence."""
        if is_sequence(obj):
            return obj
        if is_number(obj): return [obj]
        if obj is None and default is not None:
            self.warning('using default value (%s)'%(default))
            return self.get_seq(default)
        raise ValueError,'expected sequence|number but got %s'%(type(obj))
    def get_seq_seq(self,obj,default=None):
        """Return sequence of sequences."""
        if is_sequence2(obj):
            return [self.get_seq(o,default) for o in obj]
        else:
            return [self.get_seq(obj,default)]
    def get_n_seq_seq(self,obj,default):
        seq = self.get_seq_seq(obj,default)
        if is_sequence(default):
            n = len(default)
        else:
            n = max(map(len,seq))
            default = [default]*n
        ret = []
        flag = 0
        for v in seq:
            if len(v)!=n:
                ret.append(list(v)+default[len(v):])
                flag = 1
            else:
                ret.append(list(v))
        if flag:
            self.warning('Some items were filled with default value (%s) to obtain size=%s'%(default[0],n))
        return ret
    def get_3_tuple(self,obj,default=None):
        """Return 3-tuple from
        number -> (obj,default[1],default[2])
        0-sequence|None -> default
        1-sequence -> (obj[0],default[1],default[2])
        2-sequence -> (obj[0],obj[1],default[2])
        (3 or more)-sequence -> (obj[0],obj[1],obj[2])
        """
        if not (default is not None \
                and type(default) is types.TupleType \
                and len(default)==3):
            raise ValueError,'argument default must be 3-tuple|None but got %s'%(default)
        if is_sequence(obj):
            n = len(obj)
            if n>3:
                self.warning('expected 3-sequence but got %s-%s'%(n,type(obj)))
            if n>=3:
                return tuple(obj)
            self.warning('filling with default value (%s) to obtain size=3'%(default[0]))
            if default is not None:
                if n==0:
                    return default
                elif n==1:
                    return (obj[0],default[1],default[2])
                elif n==2:
                    return (obj[0],obj[1],default[2])
        elif is_number(obj) and default is not None:
            self.warning('filling with default value (%s) to obtain size=3'%(default[0]))
            return (obj,default[1],default[2])
        elif obj is None and default is not None:
            self.warning('filling with default value (%s) to obtain size=3'%(default[0]))
            return default
        raise ValueError,'failed to construct 3-tuple from %s-%s'%(n,type(obj))
    def get_3_tuple_list(self,obj,default=None):
        """Return list of 3-tuples from
        sequence of a sequence,
        sequence - it is mapped to sequence of 3-sequences if possible
        number
        """
        if is_sequence2(obj):
            return [self.get_3_tuple(o,default) for o in obj]
        elif is_sequence(obj):
            return [self.get_3_tuple(obj[i:i+3],default) for i in range(0,len(obj),3)]
        else:
            return [self.get_3_tuple(obj,default)]
    def get_3_3_tuple(self,obj,default=None):
        """Return tuple of 3-tuples
        """
        if is_sequence2(obj):
            ret = []
            for i in range(3):
                if i<len(obj):
                    ret.append(self.get_3_tuple(obj[i],default))
                else:
                    ret.append(self.get_3_tuple(default,default))
            return tuple(ret)
        if is_sequence(obj):
            if len(obj)>9:
                self.warning('ignoring elements obj[i], i>=9')
            r = obj[:9]
            r = [self.get_3_tuple(r[j:j+3],default) for j in range(0,len(r),3)]
            if len(r)<3:
                self.warning('filling with default value (%s) to obtain size=3'%(default[0]))
            while len(r)<3:
                r.append(self.get_3_tuple(default,default))
            return tuple(r)
        self.warning('filling with default value (%s) to obtain size=3'%(default[0]))
        r1 = self.get_3_tuple(obj,default)
        r2 = self.get_3_tuple(default,default)
        r3 = self.get_3_tuple(default,default)
        return (r1,r2,r3)
    def get_3_3_tuple_list(self,obj,default=None):
        """Return list of 3x3-tuples.
        """
        if is_sequence3(obj):
            return [self.get_3_3_tuple(o,default) for o in obj]
        return [self.get_3_3_tuple(obj,default)]

    def _get_nof_objs(self,seq):
        if is_sequence2(seq):
            return reduce(lambda x,y:x+y,map(self._get_nof_objs,seq),0)
            #return reduce(lambda x,y:x+y,[self._get_nof_objs(s) for s in seq],0)
        return len(seq)

    def seq_to_string(self,seq,format,datatype):
        assert is_sequence(seq),'expected sequence but got %s'%(type(seq))
        if format == 'ascii':
            if is_sequence2(seq):
                sep = '\n'
                if is_sequence3(seq):
                    sep = '\n\n'
                return sep.join([self.seq_to_string(v,format,datatype) for v in seq])
            else:
                return ' '.join(map(str,seq))
        elif format == 'binary':
            if is_sequence2(seq):
                r = ''.join([self.seq_to_string(v,format,datatype) for v in seq])
                return r
            else:
                try:
                    fmt = self.struct_fmt_map[datatype]
                except KeyError:
                    fmt = None
                if fmt:
                    r = struct.pack('!'+fmt*len(seq),*seq)
                    return r
        raise NotImplementedError,'format=%s, datatype=%s'%(format,datatype)

    def float01_to_int255(self,seq):
        assert is_float01(seq)
        if is_sequence(seq):
            return map(self.float01_to_int255,seq)
            #return [self.float01_to_int255(l) for l in seq]
        else:
            return int(seq*255)
    def int255_to_float01(self,seq):
        assert is_int255(seq)
        if is_sequence(seq):
            return map(self.int255_to_float01,seq)
            #return [self.int255_to_float01(l) for l in seq]
        else:
            return round(seq/255.0,6)

import Data
import DataSet
import DataSetAttr
