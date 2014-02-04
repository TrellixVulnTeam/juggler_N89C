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

class Publisher:
    def __init__(self, root_xml_element):
        self.__packers = []
        
        for bin_element in root_xml_element.findall('Binary'):
            # files go into bin
            pass
        for lib_element in root_xml_element.findall('Library'):
            # files go into lib
            pass
        for header_element in root_xml_element.findall('HeaderDirectory'):
            # files go into include
            pass
        for source_element in root_xml_element.findall('SourceDirectory'):
            # files go into src
            pass
        