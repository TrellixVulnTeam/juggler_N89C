'''
Created on 09.12.2013

@author: Konfuzzyus
'''
import unittest
import os
from xml.etree import ElementTree

class FileNotFound(Exception):
    pass

class InvalidFile(Exception):
    pass

class Directory():
    def __init__(self, filename=None):
        if filename is None:
            return
        
        if not os.path.isfile(filename):
            raise FileNotFound('%s is a directory or missing' % filename)
        try:
            ElementTree.parse(filename)
        except ElementTree.ParseError as error:
            raise InvalidFile('parsing error in %s: %s' % (filename, error))

    def is_empty(self):
        return True

class TestDirectory(unittest.TestCase):

    def test_ContructFromNothing_CreatesEmtpy(self):
        directory = Directory()
        self.assertTrue(directory.is_empty())

    def test_ConstructFromMissingFile_RaisesFileNotFound(self):
        self.assertRaises(FileNotFound, Directory, 'RandomNonExistentFile')

    def test_ConstructFromExistingDirectory_RaisesFileNotFound(self):
        self.assertRaises(FileNotFound, Directory, '..')
        
    def test_ConstructFromExistingNonXMLFile_RaisesInvalidFile(self):
        self.assertRaises(InvalidFile, Directory, 'test_directory.py')

    def test_ConstructFromEmptyFile_RaisesInvalidFile(self):
        testfile = 'SomeEmptyFileForTesting.xml'
        with open(testfile, 'w'):
            pass
        self.assertRaises(InvalidFile, Directory, testfile)
        os.remove(testfile)
    
    def test_ConstructFromEmptyXMLFile_CreatesEmpty(self):
        testfile = 'SomeEmptyXMLFileForTesting.xml'
        with open(testfile, 'w') as xmlfile:
            xmlfile.write('<None/>')
        directory = Directory(testfile)
        self.assertTrue(directory.is_empty())
        os.remove(testfile)
