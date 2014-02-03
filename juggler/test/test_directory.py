"""
    Juggler - Dirty dependency management and packaging for compiled code
    Copyright (C) 2014  Christian Meyer

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
        self.assertEqual(directory.get_root(), '.')

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
    
    def test_RequestNonExistentPackage_GetNone(self):
        test_listing = listing.Listing()
        self.assertEqual(test_listing.get_package('SomePackage'), None)
    
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
        self.assertEqual(test_listing.get_package('SomePackage', version.VersionInfo(3, 3, 3)), None)

    def test_LoadSinglePacketMultipleBuildData_GetExactVersionWhenExactVersionIsPassed(self):
        test_listing = self.simulate_xml_load(self.get_single_packet_multiple_build_listing())
        self.assertFalse(test_listing.is_empty())
        package_1_0_0 = test_listing.get_package('SomePackage', version.VersionInfo(1, 0, 0))
        package_1_0_3 = test_listing.get_package('SomePackage', version.VersionInfo(1, 0, 3))
        self.assertNotEqual(package_1_0_0, None)
        self.assertNotEqual(package_1_0_3, None)
        self.assertEqual(package_1_0_0.get_version(), version.VersionInfo(1,0,0))
        self.assertEqual(package_1_0_3.get_version(), version.VersionInfo(1,0,3))

    def get_extensive_build_listing(self):
        return '''<Listing> 
                    <Package name="SomePackage">
                        <Build version="v2.1-local"/>
                        <Build version="v1.0-b0"/>
                        <Build version="v1.1-b2"/>
                        <Build version="v1.0-b3"/>
                        <Build version="v2.1-b2"/>
                        <Build version="v1.2-b2"/>
                    </Package>
                    <Package name="AnotherPackage">
                        <Build version="v0.0-b14"/>
                        <Build version="v0.2-b13"/>
                        <Build version="v1.0-b12"/>
                        <Build version="v0.1-b15"/>
                        <Build version="v1.0-b16"/>
                    </Package>
                </Listing>'''

    def test_LoadExtensiveListing_TestPackageRetrieval(self):
        test_listing = self.simulate_xml_load(self.get_extensive_build_listing())
        self.check_package_retrieval(test_listing, 'SomePackage', (None, None, None), (2, 1, 'local'))
        self.check_package_retrieval(test_listing, 'SomePackage', (1, None, None), (1, 2, 2))
        self.check_package_retrieval(test_listing, 'SomePackage', (1, 1, None), (1, 1, 2))
        self.check_package_retrieval(test_listing, 'SomePackage', (1, 0, 0), (1, 0, 0))
        self.check_package_retrieval(test_listing, 'AnotherPackage', (None, None, None), (1, 0, 16))
        self.check_package_retrieval(test_listing, 'AnotherPackage', (1, None, None), (1, 0, 16))
        self.check_package_retrieval(test_listing, 'AnotherPackage', (0, 1, None), (0, 1, 15))
        self.check_package_retrieval(test_listing, 'AnotherPackage', (1, 0, 12), (1, 0, 12))

    def check_package_retrieval(self, listing, package_name, requested_numbers, expected_numbers):
        package = listing.get_package(package_name, version.VersionInfo(*requested_numbers))
        self.assertEqual(package.get_name(), package_name)
        self.assertEqual(package.get_version(), version.VersionInfo(*expected_numbers))

    def test_LoadExtensiveListing_TestIgnoringLocalBuilds(self):
        test_listing = self.simulate_xml_load(self.get_extensive_build_listing())
        package = test_listing.get_package('SomePackage', version.VersionInfo(None, None, None), ignore_local_build=True)
        self.assertEqual(package.get_version(), version.VersionInfo(2, 1, 2))

    def simulate_xml_load(self, xml_data):
        with open(self.__tempfilename, 'w') as xmlfile:
            xmlfile.write(xml_data)
        test_listing = listing.load_listing_from_file(self.__tempfilename)
        return test_listing