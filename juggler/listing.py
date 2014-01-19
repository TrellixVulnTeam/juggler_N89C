'''
Created on 09.01.2014

@author: Konfuzzyus
'''

import os
import urllib
import version
from xml.etree import ElementTree

class FileNotFound(Exception):
    pass

class InvalidFile(Exception):
    pass

class PackageNotAvailable(Exception):
    pass

class PackageVersionNotAvailable(Exception):
    pass

class PackageInfo():
    def __init__(self, name):
        self.__builds = []
        self.__name = name
    
    def add_build(self, build_version):
        self.__builds.append(build_version)
    
    def get_entry(self, match_version):
        best_match = None
        for build in self.__builds:
            if match_version.matches(build):
                if build > best_match:
                    best_match = build
        if best_match is None:
            raise PackageVersionNotAvailable('I could not find version "%s" in the listing information for package "%s"' % (match_version, self.__name))
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
    def __init__(self):
        self.__packages = {}
    
    def is_empty(self):
        return len(self.__packages) == 0
    
    def add_package(self, name, version_string):
        if not name in self.__packages:
            self.__packages[name] = PackageInfo(name)
        self.__packages[name].add_build(version.parse_version(version_string))
        
    
    def get_package(self, name, version=version.VersionInfo()):
        if name in self.__packages:
            return self.__packages[name].get_entry(version)
        else:
            raise PackageNotAvailable('The package "%s" you requested from the listing is not available' % name)

def load_listing_from_url(url):
    remotefile = None
    try:
        remotefile = urllib.urlopen(url)
    except IOError as error:
        raise FileNotFound('%s could not be accessed: %s' % (url, error))
    
    return load_listing(remotefile)

def load_listing_from_file(filename):
    if filename is None:
        return

    if not os.path.isfile(filename):
        raise FileNotFound('%s is a directory or missing' % filename)
    
    return load_listing(filename)

def load_listing(source):
    xmltree = None
    try:
        xmltree = ElementTree.parse(source)
    except ElementTree.ParseError as error:
        raise InvalidFile('parsing error in %s: %s' % (source, error))

    listing = Listing()
    entry = xmltree.find('./Package')
    if entry is not None:
        for build in entry.findall('./Build'):
            listing.add_package(entry.attrib['name'], build.attrib['version'])

    return listing
    
