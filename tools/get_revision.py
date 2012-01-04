#!/usr/bin/env python
"""

This file is executed from ../setup.py only.

Calculate cumulative version from Revision strings.

Copyright 2000 Pearu Peterson all rights reserved,
Pearu Peterson <pearu@ioc.ee>          
Permission to use, modify, and distribute this software is given under the
terms of the LGPL.  See http://www.fsf.org

NO WARRANTY IS EXPRESSED OR IMPLIED.  USE AT YOUR OWN RISK.
$Revision: 1.1 $ 
$Date: 2001/05/20 12:51:29 $
Pearu Peterson
"""

import os,fileinput,re

files=[]
for d in ['lib']:
    for f in os.listdir(d):
        if f[-3:]=='.py' or f[-2:]=='.c':
            fn = os.path.join(d,f)
            if os.path.exists(fn): files.append(fn)
            else: print 'File "%s" does not exists. Skipping.'%(fn)

revision_version = 0
for l in fileinput.input(files):
    m = re.match(r'.*?\$Re[v]ision:\s*\d+[.](?P<rev>\d+)\s*\$',l)
    if m:
        revision_version = revision_version + eval(m.group('rev'))
        fileinput.nextfile()
