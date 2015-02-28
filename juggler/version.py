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

def parse_version(string):
    cleaned = string.replace('v', '')
    return Version.coerce(cleaned)

def parse_spec(string):
    if string == '' or string == 'latest':
        return Spec('*')
    if string[0] == 'v':
        cleaned = string.replace('v', '>=')
        spec = Spec(cleaned)
        v = spec.specs[0].spec
        if v.minor is None:
            return Spec('%s,<%d' % (cleaned, v.major + 1))
        elif not v.prerelease is None:
            return Spec('==%s' % v)
        else:
            return Spec('%s,<%d.%d' % (cleaned, v.major, v.minor + 1))
        
    return Spec(string)
