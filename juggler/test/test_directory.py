'''
Created on 09.12.2013

@author: Konfuzzyus
'''
import unittest
import os
import tempfile
from juggler import version
from juggler import listing

class TestListing(unittest.TestCase):
    
    def setUp(self):
        handle, filename = tempfile.mkstemp()
        os.close(handle)
        self.__tempfilename = filename

    def tearDown(self):
        os.remove(self.__tempfilename)

    def test_AfterInit_ListingIsEmpty(self):
        directory = listing.Listing()
        self.assertTrue(directory.is_empty())

    def test_LoadMissingFile_RaisesFileNotFound(self):
        self.assertRaises(listing.FileNotFound, listing.load_listing_from_file, 'RandomNonExistentFile')

    def test_LoadDirectory_RaisesFileNotFound(self):
        self.assertRaises(listing.FileNotFound, listing.load_listing_from_file, '..')

    def test_LoadEmptyFile_RaisesInvalidFile(self):
        self.assertRaises(listing.InvalidFile, listing.load_listing_from_file, self.__tempfilename)

    def test_LoadUnknownXMLFile_CreatesEmptyListing(self):
        test_listing = self.simulate_xml_load('<Thingy> <Something/> </Thingy>')
        self.assertTrue(test_listing.is_empty())

    def test_LoadEmptyListing_CreatesEmptyListing(self):
        test_listing = self.simulate_xml_load('<Listing/>')
        self.assertTrue(test_listing.is_empty())
    
    def test_RequestNonExistentPackage_GetPackageNotAvailable(self):
        test_listing = listing.Listing()
        self.assertRaises(listing.PackageNotAvailable, test_listing.get_package, 'SomePackage')
    
    def get_single_packet_listing(self):
        return '<Listing> <Package name="SomePackage"> <Build version="v1.0-b0"/> </Package> </Listing>'
    
    def test_LoadSinglePacketData_PacketCanBeAccessed(self):
        test_listing = self.simulate_xml_load(self.get_single_packet_listing())
        self.assertFalse(test_listing.is_empty())
        package = test_listing.get_package('SomePackage')
        self.assertEqual(package.get_version(), version.VersionInfo(1,0,0))

    def get_single_packet_multiple_build_listing(self):
        return '<Listing> <Package name="SomePackage"> <Build version="v1.0-b0"/> <Build version="v1.0-b3"/> </Package> </Listing>'

    def test_LoadSinglePacketMultipleBuildData_GetLatestWhenNoVersionIsPassed(self):
        test_listing = self.simulate_xml_load(self.get_single_packet_multiple_build_listing())
        package = test_listing.get_package('SomePackage')
        self.assertEqual(package.get_version(), version.VersionInfo(1,0,3))

    def test_LoadSinglePacketMultipleBuildData_GetLatestWhenUnspecifiedVersionIsPassed(self):
        test_listing = self.simulate_xml_load(self.get_single_packet_multiple_build_listing())
        package = test_listing.get_package('SomePackage', version.VersionInfo())
        self.assertEqual(package.get_version(), version.VersionInfo(1,0,3))
        
    def test_LoadSinglePacketMultipleBuildData_RequestNonexistentVersionGetNone(self):
        test_listing = self.simulate_xml_load(self.get_single_packet_multiple_build_listing())
        self.assertRaises(listing.PackageVersionNotAvailable, test_listing.get_package, 'SomePackage', version.VersionInfo(3, 3, 3))

    def test_LoadSinglePacketMultipleBuildData_GetExactVersionWhenExactVersionPassed(self):
        test_listing = self.simulate_xml_load(self.get_single_packet_multiple_build_listing())
        self.assertFalse(test_listing.is_empty())
        package_1_0_0 = test_listing.get_package('SomePackage', version.VersionInfo(1, 0, 0))
        package_1_0_3 = test_listing.get_package('SomePackage', version.VersionInfo(1, 0, 3))
        self.assertNotEqual(package_1_0_0, None)
        self.assertNotEqual(package_1_0_3, None)
        self.assertEqual(package_1_0_0.get_version(), version.VersionInfo(1,0,0))
        self.assertEqual(package_1_0_3.get_version(), version.VersionInfo(1,0,3))

    def simulate_xml_load(self, xml_data):
        with open(self.__tempfilename, 'w') as xmlfile:
            xmlfile.write(xml_data)
        test_listing = listing.load_listing_from_file(self.__tempfilename)
        return test_listing