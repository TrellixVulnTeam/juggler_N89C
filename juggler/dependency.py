'''
Created on 10.01.2014

@author: Konfuzzyus
'''

import listing
import messages
import os
import urllib
import tarfile

class RequiredPackageNotAvailable(Exception):
    pass

def get_listing_filename():
    return 'juggler_listing.xml'

class DependencyManager:
    def __init__(self, local_repository, remote_repositories):
        # download/read listings
        self.__local_listing = listing.load_listing_from_file(os.path.join(local_repository, get_listing_filename()))
        self.__remote_listing = []
        for repo in remote_repositories:
            try:
                self.__remote_listing.append(listing.load_listing_from_url('/'.join([repo, get_listing_filename()])))
            except listing.FileNotFound as error:
                messages.UnableToAccessRemoteRepository(repo, error)
    
    def deploy(self, required_packages, target_directory, ignore_local_builds):
        for package in required_packages:
            source_info = self.find_best_source(package, ignore_local_builds)
            if source_info is None:
                raise RequiredPackageNotAvailable('None of the repositories known to me contain the required package %s with version %s' % (package['name'], package['version']))
            if source_info['source_type'] == 'local':
                full_path = source_info['package'].get_path()
                touched_file = open(full_path, 'wb')
                touched_file.close()
            else:
                source_url = source_info['package'].get_path()
                filename = source_info['package'].get_filename()
                target_file = os.path.join(self.__local_listing.get_root(), filename)
                messages.DownloadingPackage(source_url)
                urllib.urlretrieve(source_url, target_file)
            # TODO only extract packages that are newer than the dependency in the build
            with tarfile.open(target_file, 'r') as archive:
                archive.extractall(target_directory)
        # TODO create a file with include directives (for CMake)
        # TODO remove unused dependencies from project dep folder
        pass
    
    def find_best_source(self, package, ignore_local_builds):
        best = {'package': self.__local_listing.get_package(package['name'], package['version'], ignore_local_builds),
                'source': self.__local_listing,
                'source_type:': 'local'}
        for remote in self.__remote_listing:
            candidate_package = remote.get_package(package['name'], package['version'], ignore_local_builds)
            if best['package'] < candidate_package:
                best['package'] = candidate_package
                best['source'] = remote
                best['source_type'] = 'remote'
        if best['package'] is None:
            return None
        return best
        