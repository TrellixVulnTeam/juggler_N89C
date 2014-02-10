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

import listing
import messages
import os
import urllib
import tarfile

class RequiredPackageNotAvailable(Exception):
    pass

class DependencyManager:
    def __init__(self, local_repository, remote_repositories):
        listing.prepare_local_repository(local_repository)
        self.__local_listing = listing.load_local_listing(local_repository)
        self.__remote_listing = []
        for repo in remote_repositories:
            try:
                self.__remote_listing.append(listing.load_remote_listing('/'.join([repo, listing.get_listing_filename()])))
            except listing.FileNotFound as error:
                messages.UnableToAccessRemoteRepository(repo, error)
    
    def deploy(self, required_packages, target_directory, ignore_local_builds):
        for package in required_packages:
            source_info = self.find_best_source(package, ignore_local_builds)
            if source_info is None:
                raise RequiredPackageNotAvailable('None of the repositories known to me contain the required package %s with version %s' % (package['name'], package['version']))
            target_file = None
            if source_info['source_type'] == 'local':
                target_file = os.path.join(source_info['package'].get_path(), source_info['package'].get_filename())
            else:
                filename = source_info['package'].get_filename()
                source_url = '/'.join(source_info['package'].get_path(), filename)
                target_file = os.path.join(self.__local_listing.get_root(), filename)
                messages.DownloadingPackage(source_url)
                urllib.urlretrieve(source_url, target_file)
                self.__local_listing.add_package(source_info['package'].get_name(), str(source_info['package'].get_version()))
            # TODO only extract packages that are newer than the dependency in the build
            with tarfile.open(target_file, 'r') as archive:
                archive.extractall(target_directory)
        # TODO create a file with include directives (for CMake)
        # TODO remove unused dependencies from project dep folder
        self.__local_listing.store(self.__local_listing.get_root())
    
    def find_best_source(self, package, ignore_local_builds):
        best = {'package': self.__local_listing.get_package(package['name'], package['version'], ignore_local_builds),
                'source': self.__local_listing,
                'source_type': 'local'}
        for remote in self.__remote_listing:
            candidate_package = remote.get_package(package['name'], package['version'], ignore_local_builds)
            if best['package'] < candidate_package:
                best['package'] = candidate_package
                best['source'] = remote
                best['source_type'] = 'remote'
        if best['package'] is None:
            return None
        return best
        
