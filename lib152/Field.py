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

import DataSetAttr
import string

class Field(DataSetAttr.DataSetAttr):
    """Holds VTK Field.
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
        mx = max(map(len,data.values()))
        #mx = max([len(l) for l in data.values()])
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
            ret = ret + ['%s %s %s %s'%(k,len(v[0]),len(v),t),
                    self.seq_to_string(v,format,t)]
        return string.join(ret,'\n')
    def get_size(self):
        return len(self.data.values()[0])

if __name__ == "__main__":
    print Field(a=[[2,23],3,3],c=[2,3,4,5]).to_string()
