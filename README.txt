
                         PyVTK
    "Collection of tools for manipulating VTK files in Python"
                          by
                     Pearu Peterson

https://github.com/pearu/pyvtk

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

     New BSD

REQUIREMENTS
------------

     Python - pyvtk is developed under Python 2.1. Currently, it is
               tested to work under Python 2.7 and Python 3.x.

BUILDING and INSTALLING
-----------------------

     The preferred installation method is to use Python Index:
     
       pip install --upgrade pyvtk

USAGE
-----
     >>> import pyvtk

     To learn how to use pyvtk.VtkData, see examples in examples/ directory.
     For reference, execute

         pydoc pyvtk.VtkData

     or in Python:
 
     >>> from pydoc import help
     >>> help(pyvtk.VtkData)

TESTING
-------

    cd test
    python test_pyvtk.py

To test files under development, install in 'editable' mode:

    pip install -e .

--- Pearu Peterson, March 20, 2016
    <pearu.peterson@gmail.com>
