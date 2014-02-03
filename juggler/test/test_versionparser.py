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
        self.check_version_parsing('', None, None, None)
    
    def test_PassNonNumericAsMajor_RaiseInvalidString(self):
        self.assertRaises(version.InvalidString, version.parse_version, 'four')

    def test_PassOnlyMajor_GetLatestOfThatMajor(self):
        self.check_version_parsing('v3', 3, None, None)
    
    def test_PassNonNumericAsMinor_RaiseInvalidString(self):
        self.check_invalid_string('v3.four')
        
    def test_PassMajorAndMinor_GetLatestRevision(self):
        self.check_version_parsing('v4.2', 4, 2, None)
        
    def test_PassNonNumericAsMajorAndPassMinor_RaiseInvalidString(self):
        self.check_invalid_string('four.2')
        
    def test_PassFullVersion_GetSpecificVersion(self):
        self.check_version_parsing('v5.8-b29', 5, 8, 29)

    def test_PassFullVersion_GetSpecificLocalVersion(self):
        self.check_version_parsing('v5.8-local', 5, 8, 'local')

    def check_invalid_input(self, string):
        return self.assertRaises(version.InvalidType, version.parse_version, string)

    def check_version_parsing(self, version_string, expected_major, expected_minor, expected_revision):
        version_request = version.parse_version(version_string)
        self.assertIsInstance(version_request, version.VersionInfo)
        self.assertEqual(version_request.getMajor(), expected_major)
        self.assertEqual(version_request.getMinor(), expected_minor)
        self.assertEqual(version_request.getRevision(), expected_revision)

    def check_invalid_string(self, string):
        return self.assertRaises(version.InvalidString, version.parse_version, string)

