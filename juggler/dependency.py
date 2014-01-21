'''
Created on 10.01.2014

@author: Konfuzzyus
'''

import listing
import messages
import os

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
            source = self.find_best_source(package, ignore_local_builds)
            if source is None:
                raise RequiredPackageNotAvailable('None of the repositories known to me contain the required package %s with version %s' % (package['name'], package['version']))
            # - if not found in local repo, download from remote repo
            # - if found in local repo, touch
            # - unpack from local repo to project dependency folder
            pass
        # create a file with include directives for gcc
        # remove unused dependencies from project dep folder
        pass
    
    def find_best_source(self, package, flavor, ignore_local_builds):
        best = {'version': self.__local_listing.get_package(package['name'], package['version'], ignore_local_builds),
                'source': self.__local_listing}
        for remote in self.__remote_listing:
            candidate_version = remote.get_package(package['name'], package['version'], ignore_local_builds)
            if best['version'] < candidate_version:
                best['version'] = candidate_version
                best['source'] = remote
        if best['version'] is None:
            return None
        return best['source']
        