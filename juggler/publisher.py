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
import tarfile
import listing

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
    
    def pack_into(self, tarfile):
        tarfile.add(name = self.__source, arcname = self.__target)

class Publisher:
    def __init__(self, root_xml_element, source_directory, binary_directory):
        self.__packers = []
        for path_element in root_xml_element.findall('BinaryPath'):
            source_path = path_element.text.strip()
            target_path = os.path.join(path_element.attrib['target'], os.path.basename(source_path))
            self.__packers.append(Packer(os.path.join(binary_directory, source_path), target_path))
        for path_element in root_xml_element.findall('SourcePath'):
            source_path = path_element.text.strip()
            target_path = os.path.join(path_element.attrib['target'], os.path.basename(source_path))
            self.__packers.append(Packer(os.path.join(source_directory, source_path), target_path))

    def check_packers(self):
        for packer in self.__packers:
            if not packer.check():
                raise PackedPathNotFound('I could not find the path %s needed for publishing' % packer.get_source())

    def publish(self, target_repository, name, version, flavor):
        listing.prepare_local_repository(target_repository)
        self.check_packers()
        local_listing = listing.load_local_listing(target_repository)
        new_entry = local_listing.add_package(name, str(version), flavor)
        archive_name = new_entry.get_filename()
        artifact = tarfile.TarFile.open(os.path.join(target_repository, archive_name), mode='w:gz')
        for packer in self.__packers:
            packer.pack_into(artifact)
        artifact.close()
        local_listing.store(target_repository)
