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
import re

class PackedPathNotFound(Exception):
    pass

class FilePacker:
    def __init__(self, source, target):
        self.__source = source
        self.__target = target
    
    def check(self):
        if not os.path.exists(self.__source):
            raise PackedPathNotFound('I could not find the path %s needed for publishing' % self.__source)
    
    def pack_into(self, tarfile):
        tarfile.add(name = self.__source, arcname = self.__target)

class HeaderPacker:
    def __init__(self, source_dir, target_dir):
        self.__source_dir = source_dir
        self.__target_dir = target_dir

    def check(self):
        if not os.path.exists(self.__source_dir):
            raise PackedPathNotFound('I could not find the path %s needed for publishing' % self.__source)
    
    def pack_into(self, tarfile):
        for (dirpath, _, filenames) in os.walk(self.__source_dir):
            rel_dir = os.path.normpath(os.path.relpath(dirpath, self.__source_dir))
            for filename in filenames:
                if not re.match('.*\.h$', filename) is None:
                    full_src = os.path.join(self.__source_dir, rel_dir, filename)
                    full_tgt = os.path.join(self.__target_dir, rel_dir, filename)
                    tarfile.add(name = full_src, arcname = full_tgt)

class Publisher:
    def __init__(self, root_xml_element, source_directory, binary_directory):
        self.__packers = []
        for path_element in root_xml_element.findall('BinaryPath'):
            source_path = path_element.text.strip()
            target_path = os.path.join(path_element.attrib['target'], os.path.basename(source_path))
            self.__packers.append(FilePacker(os.path.join(binary_directory, source_path), target_path))
        for path_element in root_xml_element.findall('SourcePath'):
            source_path = path_element.text.strip()
            target_path = os.path.join(path_element.attrib['target'], os.path.basename(source_path))
            self.__packers.append(FilePacker(os.path.join(source_directory, source_path), target_path))
        for path_element in root_xml_element.findall('Headers'):
            source_path = path_element.text.strip()
            target_path = os.path.join(path_element.attrib['target'], os.path.basename(source_path))
            self.__packers.append(HeaderPacker(os.path.join(source_directory, source_path), target_path))
        
    def check_packers(self):
        for packer in self.__packers:
            packer.check()

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
