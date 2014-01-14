'''
Created on 09.12.2013

@author: Konfuzzyus
'''
import unittest
import os
from juggler import version

class IllegalArgument(Exception):
    pass

class Build():
    def __init__(self, name, version, flavor=None):
        if name is None or name == '':
            raise IllegalArgument('I can not create a Build instance without a valid name and you passed me "%s"' % name)
        if version is None:
            raise IllegalArgument('I can not create a Build instance without a valid version.')
        self.name = name
        self.version = version
        self.flavor = flavor

class Package():
    def __init__(self, name):
        if name is None or name == '':
            raise IllegalArgument('I can not create a Package instance without a valid name and you passed me "%s"' % name)
        self.__name = name
        self.__builds = []
    
    def get_build(self):
        if len(self.__builds) > 0:
            return self.__builds[0]
        return None
    
    def has_builds(self):
        return len(self.__builds) > 0;
    
    def add_build(self, version_info):
        build = Build(self.__name, version_info)
        self.__builds.append(build)

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
