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

from semantic_version import Version, Spec
import re

class InvalidString(Exception):
    pass

class InvalidType(Exception):
    pass

class InvalidMatch(Exception):
    pass

class VersionInfo():
    def __init__(self, major=0, minor=0, revision=0, actual_revision=0):
        if isinstance(revision, tuple):
            revision = str(revision[0])
        vstr = '%d.%d.%d-%s' % (major, minor, actual_revision, revision)
        self._version = Version.coerce(vstr)

    def getMajor(self):
        return self._version.major

    def getMinor(self):
        return self._version.minor

    def getRevision(self):
        return self._version.prerelease

    def is_complete(self):
        return True

    def is_local(self):
        return self._version.prerelease == 0

    def __str__(self):
        return str(self._version)

    def __ne__(self, other):
        return self._version.__ne__(other._version)

    def __eq__(self, other):
        return self._version.__eq__(other._version)

    def __lt__(self, other):
        return self._version.__lt__(other._version)

    def __gt__(self, other):
        return self._version.__gt__(other._version)

    def __ge__(self, other):
        return self._version.__ge__(other._version)

    def matches(self, spec):
        return spec.match(self._version)

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
            raise InvalidString('%s is not a valid version string, I am expecting something like v1.2-b34 or v5.6-local' % string)
    return build

def parse_version(string):
    cleaned = string.replace('v', '')
    version = Version.coerce(cleaned)
    return VersionInfo(version.major, version.minor, version.prerelease, version.patch)