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

class UnstructuredGrid(DataSet.DataSet):
    _vtk_cell_types_map = {'vertex':1,'poly_vertex':2,'line':3,'poly_line':4,
                           'triangle':5,'triangle_strip':6,'polygon':7,'pixel':8,
                           'quad':9,'tetra':10,'voxel':11,'hexahedron':12,
                           'wedge':13,'pyramid':14}
    _vtk_cell_nums_map = {'vertex':1,'poly_vertex':-1,'line':2,'poly_line':-1,
                           'triangle':3,'triangle_strip':-1,'polygon':-1,'pixel':4,
                           'quad':4,'tetra':4,'voxel':8,'hexahedron':8,
                           'wedge':6,'pyramid':5}

    def __init__(self,points,vertex=[],poly_vertex=[],line=[],poly_line=[],
                 triangle=[],triangle_strip=[],polygon=[],pixel=[],
                 quad=[],tetra=[],voxel=[],hexahedron=[],wedge=[],pyramid=[]):
        self.points = self.get_3_tuple_list(points,(0,0,0))
        sz = len(self.points)
        for k in self._vtk_cell_types_map.keys():
            exec 'self.%s = self.get_seq_seq(%s,[])'%(k,k)
            if k=='vertex':
                r = []
                for v in self.vertex:
                    r = r + map(lambda a:[a],v)
                self.vertex = r
            if self._check_int_seq(getattr(self,k),sz):
                raise ValueError,'In cell %s: must be (seq of seq|seq) integers less than %s'%(k,sz)
        for k,n in self._vtk_cell_nums_map.items():
            if n==-1: continue
            kv = getattr(self,k)
            if kv==[] or kv[0]==[]: continue
            for v in kv:
                if len(v)!=n:
                    raise ValueError,'Cell %s requires exactly %s points but got %s: %s'%(`k`,n,len(v),v)

    def to_string(self,format='ascii'):
        t = self.get_datatype(self.points)
        ret = ['DATASET UNSTRUCTURED_GRID',
               'POINTS %s %s'%(self.get_size(),t)
               ]
        ret.append(self.seq_to_string(self.points,format,t))
        tps = []
        r = ''
        sz = 0
        for k in self._vtk_cell_types_map.keys():
            kv = getattr(self,k)
            if kv==[] or kv[0]==[]: continue
            r = r + self.seq_to_string(map(lambda v:[len(v)]+list(v),kv),format,'int')
            #r = r + self.seq_to_string([[len(v)]+list(v) for v in kv],format,'int')
            for v in kv:
                tps.append(self._vtk_cell_types_map[k])
                sz = sz + len(v)+1
        ret = ret + ['CELLS %s %s'%(len(tps),sz),
                r,
                'CELL_TYPES %s'%(len(tps)),
                self.seq_to_string(tps,format,'int')]
        return string.join(ret,'\n')

    def get_cell_size(self):
        sz = 0
        for k in self._vtk_cell_types_map.keys():
            kv = getattr(self,k)
            if kv==[] or kv[0]==[]: continue
            sz = sz + len(kv)
        return sz
if __name__ == "__main__":
    print UnstructuredGrid([[1,2],[2,4],3,5],
                           line = [[2,3],[1,2],[2,3]],
                           vertex=2)
