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

import DataSet
import string

class PolyData(DataSet.DataSet):
    """The topology of a dataset is described by
    points
    vertices
    lines
    polygons
    triangle_strips
    """

    def __init__(self,points,
                 vertices=[],lines=[],polygons=[],triangle_strips=[]):
        self.points = self.get_3_tuple_list(points,(0,0,0))
        self.vertices = self.get_seq_seq(vertices,[])
        self.lines = self.get_seq_seq(lines,[])
        self.polygons = self.get_seq_seq(polygons,[])
        self.triangle_strips = self.get_seq_seq(triangle_strips,[])
        sz = len(self.points)
        for k in ['vertices','lines','polygons','triangle_strips']:
            if self._check_int_seq(getattr(self,k),sz):
                raise ValueError,'%s must be (seq of seq|seq) integers less than %s'%(k,sz)

    def to_string(self, format='ascii'):
        t = self.get_datatype(self.points)
        ret = ['DATASET POLYDATA',
               'POINTS %s %s'%(self.get_size(),t)]
        ret.append(self.seq_to_string(self.points,format,t))
        for k in ['vertices','lines','polygons','triangle_strips']:
            kv = getattr(self,k)
            if kv==[] or kv[0]==[]: continue
            sz = self._get_nof_objs(kv)+len(kv)
            ret = ret + ['%s %s %s'%(string.upper(k),len(kv),sz),
                    self.seq_to_string(map(lambda v:[len(v)]+list(v),kv),format,'int')]
            #ret = ret + ['%s %s %s'%(k.upper(),len(kv),sz),
            #        self.seq_to_string([[len(v)]+list(v) for v in kv],format,'int')]
        return string.join(ret,'\n')

    def get_cell_size(self):
        sz = 0
        for k in ['vertices','lines','polygons','triangle_strips']:
            kv = getattr(self,k)
            if kv==[] or kv[0]==[]: continue
            sz = sz + len(kv)
        return sz

if __name__ == "__main__":
    print PolyData([[1,2],[2,4],4,5.4],[[1],[0]],[],[1,2,3])
