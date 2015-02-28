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

class TestVersionInfo(unittest.TestCase):
    def test_parse_version(self):
        version.parse_version('v1.2-b4')
        version.parse_version('v3.1-local')
        version.parse_version('v0.2-b0')
        version.parse_version('v4.15-b4')

    def test_parse_spec(self):
        version.parse_spec('v1')
        version.parse_spec('v1.2')
        version.parse_spec('latest')
        version.parse_spec('')

    def do_match(self, spec, vers):
        s = version.parse_spec(spec)
        v = version.parse_version(vers)
        return s.match(v)

    def test_matching(self):
        self.assertTrue(self.do_match('latest', 'v1.2.3'))
        self.assertTrue(self.do_match('latest', '1.2.3'))
        self.assertTrue(self.do_match('latest', '1.2-b4'))
        self.assertTrue(self.do_match('latest', '1.2-local'))

