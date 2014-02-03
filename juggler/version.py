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

import re

class InvalidString(Exception):
    pass

class InvalidType(Exception):
    pass

class InvalidMatch(Exception):
    pass

class VersionInfo():
    def __convert_int(self, number):
        converted = None
        if not number is None:
            converted = int(number)
        return converted

    def __init__(self, major=None, minor=None, revision=None):
        self.__major = self.__convert_int(major) 
        self.__minor = self.__convert_int(minor)
        if revision == 'local':
            self.__revision = 'local'
        else:
            self.__revision = self.__convert_int(revision) 

    def getMajor(self):
        return self.__major
    
    def getMinor(self):
        return self.__minor
    
    def getRevision(self):
        return self.__revision
    
    def is_complete(self):
        return not (self.__major is None or self.__minor is None or self.__revision is None)
    
    def __str__(self):
        if self.getMajor() is None:
            return 'latest'
        textual = 'v%d' % self.getMajor()
        if self.getMinor() is None:
            return textual
        textual += '.%d' % self.getMinor()
        if self.getRevision() is None:
            return textual
        if self.getRevision() == 'local':
            textual += '-' + self.getRevision()
        else:
            textual += '-b' + str(self.getRevision())
        return textual
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, VersionInfo):
            return False
        if other.getMajor() == self.getMajor() and other.getMinor() == self.getMinor() and other.getRevision() == self.getRevision():
            return True
        return False
    
    def __lt__(self, other):
        if not isinstance(other, VersionInfo):
            return NotImplemented
        if self.__eq__(other):
            return False
        return other.__gt__(self)
    
    def __gt__(self, other):
        if not isinstance(other, VersionInfo):
            return NotImplemented
        if self.getMajor() > other.getMajor():
            return True
        if self.getMajor() == other.getMajor() and self.getMinor() > other.getMinor():
            return True
        if self.getMajor() == other.getMajor() and self.getMinor() == other.getMinor() and self.getRevision() > other.getRevision():
            return True
        return False
    
    def __ge__(self, other):
        if not isinstance(other, VersionInfo):
            return NotImplemented
        if self.__gt__(other) or self.__eq__(other):
            return True
        return False
    
    def matches(self, other):
        if not isinstance(other, VersionInfo):
            return False
        if not other.is_complete():
            raise InvalidMatch("Can only match against completely specified VersionInfo instances, you passed %s" % other)
        if self == other:
            return True
        if self.getMajor() == None:
            return True
        if self.getMajor() == other.getMajor() and self.getMinor() == None:
            return True
        if self.getMajor() == other.getMajor() and self.getMinor() == other.getMinor() and self.getRevision() == None:
            return True
        return False

def parse_build_tag(string, match):
    build = None
    tag = match.group(3)
    if not tag is None:
        number_match = re.match('b([0-9]+)\Z', tag)
        if number_match:
            build = number_match.group(1)
        elif tag == 'local':
            build = 'local'
        else:
            raise InvalidString('%s is not a valid version string' % string)
    return build

def parse_version(string):
    '''Parse a version request from a string.
    All version parts that are undefined are interpreted as a request for latest. 

    string - str representation of a version request
    
    returns a VersionInfo instance
    raises InvalidString when there are components on the string that can not be parsed
    raises InvalidType when the parameter is not a str
    '''
    if not isinstance(string, str):
        raise InvalidType('string argument of type %s instead of str' % type(string))
    string = str(string)
    
    if string == '' or string == 'latest':
        return VersionInfo()
    
    build = None
    match = re.match('v([0-9]+)(?:.([0-9]+))?(?:-([a-zA-Z0-9]+))?\Z', string)
    if match:
        build = parse_build_tag(string, match)
        return VersionInfo(major=match.group(1), minor=match.group(2), revision=build)
    
    raise InvalidString('%s is not a valid version string' % string)
