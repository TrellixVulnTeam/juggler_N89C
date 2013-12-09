'''
Created on 08.12.2013

@author: Konfuzzyus
'''

import unittest
from juggler import version

class TestVersionInfo(unittest.TestCase):
    def test_PassNothing_RaiseInvalidType(self):
        self.check_invalid_input(None)
    
    def test_PassInteger_RaiseInvalidType(self):
        self.check_invalid_input(123)

    def test_PassDictionary_RaiseInvalidType(self):
        self.check_invalid_input({'a':'2.3.4', 'b':'3.4.5'})
        
    def test_PassArray_RaiseInvalidType(self):
        self.check_invalid_input(['2.3.4', '3.4.5'])
    
    def test_PassEmpty_GetLatest(self):
        self.check_version_parsing('', None, None, None)
    
    def test_PassNonNumericAsMajor_RaiseInvalidString(self):
        self.assertRaises(version.InvalidString, version.parse_version_request, 'four')

    def test_PassOnlyMajor_GetLatestOfThatMajor(self):
        self.check_version_parsing('3', 3, None, None)
    
    def test_PassNonNumericAsMinor_RaiseInvalidString(self):
        self.check_invalid_string('3.four')
        
    def test_PassMajorAndMinor_GetLatestRevision(self):
        self.check_version_parsing('4.2', 4, 2, None)
        
    def test_PassNonNumericAsMajorAndPassMinor_RaiseInvalidString(self):
        self.check_invalid_string('four.2')
        
    def test_PassFullVersion_GetSpecificVersion(self):
        self.check_version_parsing('5.8.29', 5, 8, 29)
    
    def check_invalid_input(self, string):
        return self.assertRaises(version.InvalidType, version.parse_version_request, string)

    def check_version_parsing(self, version_string, expected_major, expected_minor, expected_revision):
        version_request = version.parse_version_request(version_string)
        self.assertIsInstance(version_request, version.VersionInfo)
        self.assertEqual(version_request.getMajor(), expected_major)
        self.assertEqual(version_request.getMinor(), expected_minor)
        self.assertEqual(version_request.getRevision(), expected_revision)

    def check_invalid_string(self, string):
        return self.assertRaises(version.InvalidString, version.parse_version_request, string)

