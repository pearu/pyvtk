#!/usr/bin/env python
"""
PolyData
"""
"""

Copyright 2001 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@ioc.ee>          
Permission to use, modify, and distribute this software is given under the
terms of the LGPL.  See http://www.fsf.org

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Revision: 1.6 $
$Date: 2002/11/19 20:40:11 $
Pearu Peterson
"""

import DataSet
import common

class PolyData(DataSet.DataSet):
    """
    Usage:
      PolyData(<sequence of 3-tuples of points>,
               vertices = <sequence of sequences>
               lines = <sequence of sequences>,
               polygons = <sequence of sequences>
               triangle_strips = <sequence of sequences>,
               )
    Attributes:
      points
      vertices
      lines
      polygons
      triangle_strips
    Public methods:
      get_size()
      get_cell_size()
      to_string(format = 'ascii')
      get_points()
      <DataSetAttr class>(...)
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
               'POINTS %s %s'%(self.get_size(),t),
               self.seq_to_string(self.points,format,t)]
        for k in ['vertices','lines','polygons','triangle_strips']:
            kv = getattr(self,k)
            if kv==[] or kv[0]==[]: continue
            sz = self._get_nof_objs(kv)+len(kv)
            ret += ['%s %s %s'%(k.upper(),len(kv),sz),
                    self.seq_to_string([[len(v)]+list(v) for v in kv],format,'int')]
        return '\n'.join(ret)

    def get_cell_size(self):
        sz = 0
        for k in ['vertices','lines','polygons','triangle_strips']:
            kv = getattr(self,k)
            if kv==[] or kv[0]==[]: continue
            sz += len(kv)
        return sz

    def get_points(self):
        return self.points

def polydata_fromfile(f,self):
    """Use VtkData(<filename>)."""
    points = []
    vertices = []
    lines = []
    polygons = []
    triangle_strips = []
    l = common._getline(f)
    k,n,datatype = [s.strip().lower() for s in l.split(' ')]
    if k!='points':
        raise ValueError, 'expected points but got %s'%(`k`)
    n = eval(n)
    assert datatype in ['bit','unsigned_char','char','unsigned_short','short','unsigned_int','int','unsigned_long','long','float','double'],`datatype`

    self.message('\tgetting %s points'%n)
    while len(points) < 3*n:
        l = common._getline(f)
        points += map(eval,l.split(' '))
    assert len(points)==3*n
    while 1:
        l = common._getline(f)
        if l is None:
            break
        sl = l.split(' ')
        k = sl[0].strip().lower()
        if k not in ['vertices','lines','polygons','triangle_strips']:
            break
        assert len(sl)==3
        n,size = map(eval,[sl[1],sl[2]])
        lst = []
        while len(lst) < size:
            l = common._getline(f)
            lst += map(eval,l.split(' '))
        assert len(lst)==size
        lst2 = []
        j = 0
        for i in range(n):
            lst2.append(lst[j+1:j+lst[j]+1])
            j += lst[j]+1
        exec '%s = lst2'%k
    return PolyData(points,vertices,lines,polygons,triangle_strips),l

if __name__ == "__main__":
    print PolyData([[1,2],[2,4],4,5.4],[[1],[0]],[],[1,2,3])
