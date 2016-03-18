#!/usr/bin/env python

"""
Test reading and writting vtk files.

Input files are taken from examples/ directory.
"""

import unittest
from shutil import  rmtree
from os.path import isdir, join
from os import mkdir

from pyvtk import *

class TestBase(unittest.TestCase):
    """
    Manage output and input directories and files.

    Directories hierarchy is as follow:

        output_dir/
            file1
            file2

        input_dir/
            file1
            file2
    """
    # Root directory containing output outputs.
    output_dir = "output"

    # Root directory containing input outputs.
    input_dir = "input"

    # Diff long strings.
    maxDiff = None

    @classmethod
    def output(cls, filename):
        """filepath in output directory"""
        return join(cls.output_dir, filename)

    @classmethod
    def input(cls, filename):
        """filepath in input directory"""
        return join(cls.input_dir, filename)

    def check_output_file(self, filename, binary=False):
        """Diff output and input files"""
        output_filepath = self.output(filename)
        input_filepath = self.input(filename)

        mode = 'rb' if binary else 'r'
        output_string = open(output_filepath,mode).read()
        input_string = open(input_filepath,mode).read()

        self.assertEqual(output_string, input_string)

class TestPolyData(TestBase):

    def test_read_write_ascii_file(self):
        vtk = VtkData(self.input('example1'))
        vtk.tofile(self.output('example1'), 'ascii')
        self.check_output_file('example1.vtk')

    def test_read_write_binary_file(self):
        vtk = VtkData(self.input('example1'))
        vtk.tofile(self.output('example1b'), 'binary')
        self.check_output_file('example1b.vtk', binary=True)

class TestStructuredPoints(TestBase):

    def test_read_write_ascii_file(self):
        vtk = VtkData(self.input('example2'))
        vtk.tofile(self.output('example2'), 'ascii')
        self.check_output_file('example2.vtk')

    def test_read_write_binary_file(self):
        vtk = VtkData(self.input('example2'))
        vtk.tofile(self.output('example2b'), 'binary')
        self.check_output_file('example2b.vtk', binary=True)

    def test_point_data_append(self):
        vtk = VtkData(self.input('example2'),only_structure = 1)
        vtk.point_data.append(vtk.structure.Scalars(f,'x*y*z'))
        vtk.tofile(self.output('example2f_sp'))
        self.check_output_file('example2f_sp.vtk')

class TestStructuredGrid(TestBase):

    def test_read_write_ascii_file(self):
        pp = [(i,j,k) for k in range(6) for j in range(4) for i in range(3)]
        vtk = VtkData(StructuredGrid([3,4,6],pp))
        vtk.point_data.append(vtk.structure.Scalars(f,'x*y*z'))
        vtk.tofile(self.output('example2f_sg'))
        self.check_output_file('example2f_sg.vtk')

class TestRectilinearGrid(TestBase):

    def test_read_write_ascii_file(self):
        vtk = VtkData(self.input('example2f_rg'))
        vtk.tofile(self.output('example2f_rg'), 'ascii')
        self.check_output_file('example2f_rg.vtk')

class TestUnstructuredGrid(TestBase):

    def test_read_write_ascii_file(self):
        vtk = VtkData(self.input('example2f_usg'))
        vtk.tofile(self.output('example2f_usg'), 'ascii')
        self.check_output_file('example2f_usg.vtk')

def f(x,y,z):
    return x*y*z

if __name__ == '__main__':

    # Create a fresh directory for ouptuts
    if isdir(TestBase.output_dir):
        rmtree(TestBase.output_dir)
    mkdir(TestBase.output_dir)

    unittest.main()
