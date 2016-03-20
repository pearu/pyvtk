#!/usr/bin/env python

import os
from distutils.core import setup

version_file = os.path.join('pyvtk','__version__.py')
if 1 or not os.path.exists(version_file):
    major_version = 0
    minor_version = 4
    revisions_file =os.path.join('tools','get_revision.py')
    exec(open(revisions_file).read())
    __version__='%d.%d.%d'%(major_version,minor_version,revision_version)
    f = open(os.path.join('pyvtk/__version__.py'),'w')
    f.write('__version__ = "%s"\n'%(__version__))
    f.close()
exec(open(version_file).read())

print("PyVTK Version",__version__)
setup (name = "PyVTK",
       version = __version__,
       description = "PyVTK - tools for manipulating VTK files in Python",
       author = "Pearu Peterson",
       author_email = "pearu.peterson@gmail.com",
       maintainer = "Pearu Peterson",
       maintainer_email = "pearu.peterson@gmail.com",
       license = "New BSD",
       long_description= """\
PyVTK provides tools for manipulating VTK (Visualization Toolkit)
files in Python:
  VtkData - create VTK files from Python / read VTK files to Python.""",
       url = "https://github.com/pearu/pyvtk",
       packages = ['pyvtk'],
       keywords = ['VTK'],
       classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Visualization',
        ],
       platforms = 'All',
       install_requires = ['six'],
       )


