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

import os
import urllib
import version
from xml.etree import ElementTree

class FileNotFound(Exception):
    pass

class InvalidFile(Exception):
    pass

class PackageInfo():
    def __init__(self, name):
        self.__builds = []
        self.__name = name
    
    def add_build(self, build_version):
        self.__builds.append(build_version)
    
    def get_entry(self, match_version, ignore_local_build):
        best_match = None
        for build in self.__builds:
            if ignore_local_build and build.is_local():
                continue
            if match_version.matches(build):
                if build > best_match:
                    best_match = build
        if best_match is None:
            return None
        return PackageEntry(self.__name, best_match)
        
    def get_name(self):
        return self.__name

class PackageEntry():
    def __init__(self, name, build_version):
        self.__name = name
        self.__version = build_version

    def get_name(self):
        return self.__name
    
    def get_version(self):
        return self.__version

class Listing():
    def __init__(self, root = '.'):
        self.__packages = {}
        self.__root = root
    
    def is_empty(self):
        return len(self.__packages) == 0
    
    def add_package(self, name, version_string):
        if not name in self.__packages:
            self.__packages[name] = PackageInfo(name)
        self.__packages[name].add_build(version.parse_version(version_string))
    
    def get_package(self, name, version=version.VersionInfo(), ignore_local_build=False):
        if name in self.__packages:
            return self.__packages[name].get_entry(version, ignore_local_build=ignore_local_build)
        else:
            return None
    
    def get_root(self):
        return self.__root

def load_listing_from_url(url):
    remotefile = None
    try:
        remotefile = urllib.urlopen(url)
    except IOError as error:
        raise FileNotFound('%s could not be accessed: %s' % (url, error))
    url_parts = url.split('/')
    root = '/'.join(url_parts[:-1])
    return load_listing(remotefile, root)

def load_listing_from_file(filename):
    if filename is None:
        return

    if not os.path.isfile(filename):
        raise FileNotFound('%s is a directory or missing' % filename)
    
    return load_listing(filename, os.path.dirname(filename))

def load_listing(source, root):
    xmltree = None
    try:
        xmltree = ElementTree.parse(source)
    except ElementTree.ParseError as error:
        raise InvalidFile('parsing error in %s: %s' % (source, error))

    listing = Listing(root)
    package_entries = xmltree.findall('./Package')
    for entry in package_entries:
        for build in entry.findall('./Build'):
            listing.add_package(entry.attrib['name'], build.attrib['version'])
    return listing
