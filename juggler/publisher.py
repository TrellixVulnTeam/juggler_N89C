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

class PackedPathNotFound(Exception):
    pass

class Packer:
    def __init__(self, source, target):
        self.__source = source
        self.__target = target
    
    def check(self):
        return os.path.exists(self.__source)
    
    def get_source(self):
        return self.__source

class Publisher:
    def __init__(self, root_xml_element):
        self.__packers = []
        for path_element in root_xml_element.findall('Path'):
            target_path = path_element.attrib['target']
            source_path = path_element.text
            self.__packers.append(Packer(source_path, target_path))
    
    def publish(self, target_repository):
        for packer in self.__packers:
            if not packer.check():
                raise PackedPathNotFound('I could not find the path %s needed for publishing' % packer.get_source())
        # Check local repository (create if not existing)
        # Pack files
        # Update repository listing
        