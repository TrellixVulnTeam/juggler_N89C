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
        self.check_invalid_input({'a':'v2.3-b4', 'b':'v3.4-b5'})
        
    def test_PassArray_RaiseInvalidType(self):
        self.check_invalid_input(['v2.3-b4', 'v3.4-b5'])
    
    def test_PassEmpty_GetLatest(self):
        self.check_version_parsing('', None, None, None, False)
        
    def test_PassLatest_GetLatest(self):
        self.check_version_parsing('latest', None, None, None, False)
    
    def test_PassNonNumericAsMajor_RaiseInvalidString(self):
        self.assertRaises(version.InvalidString, version.parse_version, 'four')

    def test_PassOnlyMajor_GetLatestOfThatMajor(self):
        self.check_version_parsing('v3', 3, None, None, False)
    
    def test_PassNonNumericAsMinor_RaiseInvalidString(self):
        self.check_invalid_string('v3.four')
        
    def test_PassMajorAndMinor_GetLatestRevision(self):
        self.check_version_parsing('v4.2', 4, 2, None, False)
        
    def test_PassNonNumericAsMajorAndPassMinor_RaiseInvalidString(self):
        self.check_invalid_string('four.2')
        
    def test_PassFullVersion_GetSpecificVersion(self):
        self.check_version_parsing('v5.8-b29', 5, 8, 29, True)

    def test_PassFullVersion_GetSpecificLocalVersion(self):
        self.check_version_parsing('v5.8-local', 5, 8, 'local', True)

    def test_CreateVersion_CheckStringConversion(self):
        self.check_version_tostring(None, None, None, 'latest')
        self.check_version_tostring(1, None, None, 'v1')
        self.check_version_tostring(2, 1, None, 'v2.1')
        self.check_version_tostring(3, 2, 1, 'v3.2-b1')
        self.check_version_tostring(4, 5, 'local', 'v4.5-local')

    def check_invalid_input(self, string):
        return self.assertRaises(version.InvalidType, version.parse_version, string)

    def check_version_parsing(self, version_string, expected_major, expected_minor, expected_revision, is_complete):
        version_request = version.parse_version(version_string)
        self.assertIsInstance(version_request, version.VersionInfo)
        self.assertEqual(version_request.getMajor(), expected_major)
        self.assertEqual(version_request.getMinor(), expected_minor)
        self.assertEqual(version_request.getRevision(), expected_revision)
        self.assertEqual(version_request.is_complete(), is_complete)

    def check_version_tostring(self, major, minor, revision, expected_string):
        version_info = version.VersionInfo(major, minor, revision)
        self.assertEqual(str(version_info), expected_string)

    def check_invalid_string(self, string):
        return self.assertRaises(version.InvalidString, version.parse_version, string)

