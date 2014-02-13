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

class IllegalArgument(Exception):
    pass

class Build():
    def __init__(self, name, version, flavor=None):
        if name is None or name == '':
            raise IllegalArgument('I can not create a Build instance using an invalid name and you passed me "%s"' % name)
        if version is None:
            raise IllegalArgument('I can not create a Build instance using an invalid version andyou passed me "%s"' % version)
        if not version.is_complete():
            raise IllegalArgument('I can not create a Build instance with a partially specified version and you passed me "%s"' % version)
        self.name = name
        self.version = version
        self.flavor = flavor

class Package():
    def __init__(self, name):
        if name is None or name == '':
            raise IllegalArgument('I can not create a Package instance without a valid name and you passed me "%s"' % name)
        self.__name = name
        self.builds = []
    
    def get_build(self):
        if len(self.builds) > 0:
            return self.builds[0]
        return None
    
    def has_builds(self):
        return len(self.builds) > 0;
    
    def add_build(self, version_info):
        build = Build(self.__name, version_info)
        self.builds.append(build)

class TestPackage(unittest.TestCase):

    def test_CreatedPackage_IsEmpty(self):
        package = Package('TestPackage')
        self.assertFalse(package.has_builds())
    
    def test_GetLatestBuildWhenEmpty_ReturnNone(self):
        package = Package('TestPackage')
        self.assertEqual(package.get_build(), None)
    
    def test_AddNoneAsBuild_RaiseIllegalArgument(self):
        package = Package('TestPackage')
        self.assertRaises(IllegalArgument, package.add_build, None)

    def test_AddBuild_IsNotEmpty(self):
        package = Package('TestPackage')
        package.add_build(version.VersionInfo(1, 0, 0))
        self.assertTrue(package.has_builds())
        
    def test_GetLatestBuildWhenSingleBuildAvailable_ReturnThatBuild(self):
        package = Package('TestPackage')
        expected_version = version.VersionInfo(1, 0, 0)
        package.add_build(expected_version)
        self.assertEqual(package.get_build().version, expected_version)
