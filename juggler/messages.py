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

indent_level = 0

def Indent():
    global indent_level
    indent_level += 1

def Unindent():
    global indent_level
    indent_level -= 1

def GetIndent():
    global indent_level
    indent = ''
    i = 0
    while i < indent_level:
        indent += '  '
        i += 1
    return indent

def VERBOSE(msg):
    if msg is None:
        return
    print '%s%s' % (GetIndent(), msg)

def WARNING(msg, verbose=None):
    print "%sWarning: %s" % (GetIndent(), msg) 
    Indent()
    VERBOSE(verbose)
    Unindent()

def UnableToAccessRemoteRepository(url, reason):
    WARNING("Could not access remote repository %s" % url, reason)