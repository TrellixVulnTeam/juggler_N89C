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
from .. import version

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
    
    def test_SpecifyLocalVersion_IsLocalReturnsTrue(self):
        local_version = version.parse_version('v1.2-local')
        self.assertTrue(local_version.is_local())
        local_version = version.parse_version('v1.2-b3')
        self.assertFalse(local_version.is_local())

    def test_CreateVersion_CheckStringConversion(self):
        self.check_version_tostring(None, None, None, 'latest')
        self.check_version_tostring(1, None, None, 'v1')
        self.check_version_tostring(2, 1, None, 'v2.1')
        self.check_version_tostring(3, 2, 1, 'v3.2-b1')
        self.check_version_tostring(4, 5, 'local', 'v4.5-local')
    
    def test_Comparison_CheckEquality(self):
        self.check_equality((1,2,3), (1,2,3))
        self.check_equality((3,2,1), (3,2,1))
        self.check_equality((1,1,1), (1,1,1))
        self.check_equality((1,1,1), (1,1,1))

    def check_equality(self, lefthand, righthand):
        lefthand_version = version.VersionInfo(*lefthand)
        righthand_version = version.VersionInfo(*righthand)
        self.assertTrue(lefthand_version == righthand_version, '%s == %s should be true' % (lefthand_version, righthand_version))
        self.assertTrue(righthand_version == lefthand_version, '%s == %s should be true' % (righthand_version, lefthand_version))
        self.assertTrue(lefthand_version >= righthand_version, '%s >= %s should be true' % (lefthand_version, righthand_version))
        self.assertTrue(righthand_version >= lefthand_version, '%s >= %s should be true' % (righthand_version, lefthand_version))
        self.assertTrue(lefthand_version <= righthand_version, '%s <= %s should be true' % (lefthand_version, righthand_version))
        self.assertTrue(righthand_version <= lefthand_version, '%s <= %s should be true' % (righthand_version, lefthand_version))
        self.assertFalse(lefthand_version != righthand_version, '%s != %s should be false' % (lefthand_version, righthand_version))
        self.assertFalse(righthand_version != lefthand_version, '%s != %s should be false' % (righthand_version, lefthand_version))
        self.assertFalse(lefthand_version <> righthand_version, '%s <> %s should be false' % (lefthand_version, righthand_version))
        self.assertFalse(righthand_version <> lefthand_version, '%s <> %s should be false' % (righthand_version, lefthand_version))
        
    def test_Comparison_CheckOrdering(self):
        self.check_ordering((2,0,0), (1,0,0))
        self.check_ordering((1,1,0), (1,0,0))
        self.check_ordering((1,1,1), (1,1,0))
        self.check_ordering((1,1,0), (1,0,1))
        self.check_ordering((1,2,0), (1,1,'local'))
        self.check_ordering((1,0,'local'), (1,0,5))
        self.check_ordering((1,0,0), None)
    
    def convert_to_version_test_instance(self, version_numbers):
        if version_numbers is None:
            return None
        return version.VersionInfo(*version_numbers)
    
    def check_ordering(self, higher, lower):
        higher_version = self.convert_to_version_test_instance(higher)
        lower_version = self.convert_to_version_test_instance(lower)
        self.assertTrue(higher_version > lower_version, '%s > %s should be true' % (higher_version, lower_version))
        self.assertTrue(higher_version >= lower_version, '%s >= %s should be true' % (higher_version, lower_version))
        self.assertFalse(lower_version > higher_version, '%s > %s should be false' % (lower_version, higher_version))
        self.assertFalse(lower_version >= higher_version, '%s >= %s should be false' % (lower_version, higher_version))
        self.assertTrue(lower_version < higher_version, '%s < %s should be true' % (lower_version, higher_version))
        self.assertTrue(lower_version <= higher_version, '%s <= %s should be true' % (lower_version, higher_version))
        self.assertFalse(higher_version < lower_version, '%s < %s should be false' % (higher_version, lower_version))
        self.assertFalse(higher_version <= lower_version, '%s <= %s should be false' % (higher_version, lower_version))
        self.assertFalse(higher_version == lower_version, '%s == %s should be false' % (higher_version, lower_version))
        self.assertFalse(lower_version == higher_version, '%s == %s should be false' % (lower_version, higher_version))
        self.assertTrue(higher_version != lower_version, '%s != %s should be true' % (higher_version, lower_version))
        self.assertTrue(lower_version != higher_version, '%s != %s should be true' % (lower_version, higher_version))
        self.assertTrue(higher_version <> lower_version, '%s <> %s should be true' % (higher_version, lower_version))
        self.assertTrue(lower_version <> higher_version, '%s <> %s should be true' % (lower_version, higher_version))
    
    def test_Matching(self):
        self.check_matching((1,2,3), (1,2,3))
        self.check_matching((None,None,None), (1,2,3))
        self.check_matching((1,None,None), (1,2,3))
        self.check_matching((1,2,None), (1,2,3))
        self.check_matching((2,1,None), (2,1,'local'))
        self.check_not_matching((3,2,1), (1,2,3))
        self.check_not_matching((3,None,None), (2,1,0))
        self.check_not_matching((2,2,None), (2,1,0))
        self.check_not_matching((3,2,1), (3,2,'local'))
    
    def test_MatchingDegenrateCases(self):
        test_version = version.VersionInfo(3,2,1)
        self.assertFalse(test_version.matches(None))
        self.assertRaises(version.InvalidMatch, test_version.matches, version.VersionInfo(3, None, None))
    
    def check_matching(self, reference, subject):
        self.assertTrue(version.VersionInfo(*reference).matches(version.VersionInfo(*subject)))
        
    def check_not_matching(self, reference, subject):
        self.assertFalse(version.VersionInfo(*reference).matches(version.VersionInfo(*subject)))
    
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

