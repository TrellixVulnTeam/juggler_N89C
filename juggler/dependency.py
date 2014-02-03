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

def get_listing_filename():
    return 'juggler_listing.xml'

class DependencyManager:
    def __init__(self, local_repository, remote_repositories):
        # download/read listings
        self.__local_listing = listing.load_listing_from_file(os.path.join(local_repository, get_listing_filename()))
        self.__remote_listing = []
        for repo in remote_repositories:
            print repo
            try:
                self.__remote_listing.append(listing.load_listing_from_url('/'.join([repo, get_listing_filename()])))
            except listing.FileNotFound as error:
                messages.UnableToAccessRemoteRepository(repo, error)
    
    def deploy(self, required_packages, target_directory, flavor):
        for package in required_packages:
            # - if not found in local repo, download from remote repo
            # - if found in local repo, touch
            # - unpack from local repo to project dependency folder
            pass
        # create a file with include directives for gcc
        # remove unused dependencies from project dep folder
        pass