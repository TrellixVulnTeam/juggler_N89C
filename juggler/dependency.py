'''
Created on 10.01.2014

@author: Konfuzzyus
'''

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