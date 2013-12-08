'''
Created on 08.12.2013

@author: Konfuzzyus
'''

import re

class InvalidString(Exception):
    pass

class InvalidType(Exception):
    pass


class VersionRequest():
    def __convert_int(self, number):
        converted = None
        if not number is None:
            converted = int(number)
        return converted

    def __init__(self, major=None, minor=None, revision=None):
        self.__major = self.__convert_int(major) 
        self.__minor = self.__convert_int(minor) 
        self.__revision = self.__convert_int(revision) 
            
    def getMajor(self):
        return self.__major
    
    def getMinor(self):
        return self.__minor
    
    def getRevision(self):
        return self.__revision

def parse_version_request(string):
    '''Parse a version request from a string.
    All version parts that are undefined are interpreted as a request for latest. 

    string - str representation of a version request
    
    returns a VersionRequest instance
    raises InvalidString when there are components on the string that can not be parsed
    raises InvalidType when the parameter is not a str        
    '''
    if not isinstance(string, str):
        raise InvalidType
    string = str(string)
    
    if string == '':
        return VersionRequest()
    
    match = re.match('([0-9]+)(?:.([0-9]+))?(?:.([0-9]+))?\Z', string)
    if match:
        return VersionRequest(major=match.group(1), minor=match.group(2), revision=match.group(3))
    
    raise InvalidString