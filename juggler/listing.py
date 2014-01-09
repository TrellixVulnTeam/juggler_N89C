'''
Created on 09.01.2014

@author: Konfuzzyus
'''

import os
from xml.etree import ElementTree

class FileNotFound(Exception):
    pass

class InvalidFile(Exception):
    pass

class Listing():
    def __init__(self):
        self.__packages = []
    
    def is_empty(self):
        return len(self.__packages) == 0
    
    def add_package(self, name):
        self.__packages.append(name)
    
    def get_package(self, name):
        if name in self.__packages:
            return name
        return None

def load_listing_file(filename):
    if filename is None:
        return

    if not os.path.isfile(filename):
        raise FileNotFound('%s is a directory or missing' % filename)

    xmltree = None
    try:
        xmltree = ElementTree.parse(filename)
    except ElementTree.ParseError as error:
        raise InvalidFile('parsing error in %s: %s' % (filename, error))

    listing = Listing()
    entry = xmltree.find('./Package')
    if entry is not None:
        listing.add_package(entry.attrib['name'])

    return listing
