
                         PyVTK
    "Collection of tools for manipulating VTK files in Python"
                          by
                     Pearu Peterson

http://cens.ioc.ee/projects/pyvtk/

INTRODUCTION
------------

     PyVTK provides tools for manipulating VTK files in Python:

     VtkData - Create VTK file from Python objects. It fully
         supports VTK File Formats Standard 2.0. The features
	 includes:
           *** ascii and binary output, ascii input
           *** DataSet formats:
                 StructuredPoints, StructuredGrid, RectilinearGrid,
                 PolyData, UnstructuredGrid
           *** Data formats:
                 PointData, CellData
           *** DataSetAttr formats:
                 Scalars, ColorScalars, LookupTable, Vectors, 
                 Normals, TextureCoordinates, Tensors, Field

LICENSE
-------

     GNU LGPL (see http://www.fsf.org)

REQUIREMENTS
------------

     Python  - pyvtk is developed under Python 2.1. But it is tested
               to work also under Python 2.0 and Python 1.5.2.
               In future, Python 1.5 will be supported only if one
               asks for it.

BUILDING and INSTALLING
-----------------------

     Python 2.x users, execute
         python setup.py install

     Python 1.x users, execute
         make install

USAGE
-----
     >>> import pyvtk

     To learn how to use pyvtk.VtkData, see examples in examples/ directory.
     For reference, execute

         pydoc pyvtk.VtkData

     or in Python:
 
     >>> from pydoc import help
     >>> help(pyvtk.VtkData)


--- Pearu Peterson, 21 May 2001
    <pearu@cens.ioc.ee>