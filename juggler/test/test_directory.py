'''
Created on 09.12.2013

@author: Konfuzzyus
'''
import unittest
import os
import tempfile
from xml.etree import ElementTree

class FileNotFound(Exception):
    pass

class InvalidFile(Exception):
    pass

class Listing():
    def __init__(self):
        self.__packages = []
    
    def is_empty(self):
        return len(self.__packages) == 0
    
    def add_package(self, name):
        self.__packages.append(name)
    
    def get_package(self, name):
        if name in self.__packages:
            return name
        return None

def load_listing_file(filename):
    if filename is None:
        return

    if not os.path.isfile(filename):
        raise FileNotFound('%s is a directory or missing' % filename)

    xmltree = None
    try:
        xmltree = ElementTree.parse(filename)
    except ElementTree.ParseError as error:
        raise InvalidFile('parsing error in %s: %s' % (filename, error))

    listing = Listing()
    entry = xmltree.find('./Package')
    if entry is not None:
        listing.add_package(entry.attrib['name'])

    return listing

class TestListing(unittest.TestCase):
    
    def setUp(self):
        handle, filename = tempfile.mkstemp()
        os.close(handle)
        self.__tempfilename = filename

    def tearDown(self):
        os.remove(self.__tempfilename)

    def test_AfterInit_ListingIsEmpty(self):
        directory = Listing()
        self.assertTrue(directory.is_empty())

    def test_LoadMissingFile_RaisesFileNotFound(self):
        self.assertRaises(FileNotFound, load_listing_file, 'RandomNonExistentFile')

    def test_LoadDirectory_RaisesFileNotFound(self):
        self.assertRaises(FileNotFound, load_listing_file, '..')

    def test_LoadEmptyFile_RaisesInvalidFile(self):
        self.assertRaises(InvalidFile, load_listing_file, self.__tempfilename)

    def test_LoadUnknownXMLFile_CreatesEmptyListing(self):
        listing = self.simulate_xml_load('<Thingy> <Something/> </Thingy>')
        self.assertTrue(listing.is_empty())

    def test_LoadEmptyListing_CreatesEmptyListing(self):
        listing = self.simulate_xml_load('<Listing/>')
        self.assertTrue(listing.is_empty())
    
    def test_RequestNonExistentPackage_GetNone(self):
        listing = Listing()
        self.assertEqual(listing.get_package('SomePackage'), None)
    
    def test_LoadSinglePacketData_CreatesNonEmptyListing(self):
        listing = self.simulate_xml_load('<Listing> <Package name="SomePackage"> <Build version="1.0.0"/> </Package> </Listing>')
        self.assertFalse(listing.is_empty())
        self.assertNotEqual(listing.get_package('SomePackage'), None)

    def simulate_xml_load(self, xml_data):
        with open(self.__tempfilename, 'w') as xmlfile:
            xmlfile.write(xml_data)
        listing = load_listing_file(self.__tempfilename)
        return listing