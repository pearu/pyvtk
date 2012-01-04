#!/usr/bin/env python
"""
Field
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

import DataSetAttr
import common

class Field(DataSetAttr.DataSetAttr):
    """Holds VTK Field.
    Usage:
      Field([<name string>,] arrname_1=<sequence of n_1-sequences>, ...,
                             arrname_k=<sequence of n_k-sequences>)

    Attributes:
      data - dictionary of arrays
      name
    Public methods:
      get_size()
      to_string(format = 'ascii')
    """
    def __init__(self,*args,**kws):
        if len(args): name = args[0]
        else: name = None
        if len(args)>1:
            self.warning('Ignoring all arguments except the first')
        self.name = self._get_name(name)
        data = {}
        mx = 0 
        for k,v in kws.items():
            data[k] = self.get_n_seq_seq(v,self.default_value)
        mx = max([len(l) for l in data.values()])
        for k,v in data.items():
            if len(v)<mx:
                self.warning('Filling array %s (size=%s) with default value (%s) to obtain size=%s'%(`k`,len(v),self.default_value,mx))
            while len(v)<mx:
                v.append([self.default_value]*len(v[0]))
        self.data = data
    def to_string(self,format='ascii'):
        ret = ['FIELD %s %s'%(self.name,len(self.data))]
        for k,v in self.data.items():
            t = self.get_datatype(v)
            ret += ['%s %s %s %s'%(k,len(v[0]),len(v),t),
                    self.seq_to_string(v,format,t)]
        return '\n'.join(ret)
    def get_size(self):
        return len(self.data.values()[0])

def field_fromfile(f,n,sl):
    dataname = sl[0]
    numarrays = eval(sl[1])
    dict = {}
    for i in range(numarrays):
        l = common._getline(f).split(' ')
        assert len(l)==4,`l`
        name = l[0].strip()
        numcomps = eval(l[1])
        numtuples = eval(l[2])
        datatype = l[3].lower()
        assert datatype in ['bit','unsigned_char','char','unsigned_short','short','unsigned_int','int','unsigned_long','long','float','double'],`datatype`   
        arr = []
        while len(arr)<numcomps*numtuples:
            arr += map(eval,common._getline(f).split(' '))
        assert len(arr)==numcomps*numtuples
        arr2 = []
        for j in range(0,numtuples*numcomps,numcomps):
            arr2.append(arr[j:j+numcomps])
        dict[name] = arr2
    return Field(dataname,**dict)
if __name__ == "__main__":
    print Field(a=[[2,23],3,3],c=[2,3,4,5]).to_string()
