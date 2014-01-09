#!/usr/bin/env/python

import argparse
import config
import os
import sys

def create_argparser():
    parser = argparse.ArgumentParser(prog='juggler',
                                     version='v1.0',
                                     description='')
    
    parser.add_argument('COMMAND', action='store', choices=['fetch', 'publish'])
    parser.add_argument('PATH', action='store', help='Path to the project to be juggled. Must be a directory containing a juggle.xml')
    parser.add_argument('--user_config', action='store', default='~/.juggler/global.xml', help='Specify a juggler configuration explicitly. Defaults to ~/.juggler/global.xml')
    
    return parser

def main():
    command = ''
    
    parser = create_argparser()
    args = parser.parse_args()
    
    global_config = config.JugglerConfig()
    global_config.load(os.path.expanduser(args.user_config))
    
    project_config = config.ProjectConfig()
    project_config.load(os.path.expanduser(os.path.join(args.PATH, 'juggle.xml')))
    
    if command == 'fetch':
        # for each dependency
        # - if not found in local repo, download from remote repo
        # - if found in local repo, touch
        # - unpack from local repo to project dependency folder
        # remove unused dependencies from project dep folder
        # delete packages in local repo that are older than a month
        # create a file with include directives for gcc
        # extract project version from code
        return 0;
    elif command == 'publish':
        # pack artifacts in tar file
        # upload tar file to remote repo
        return 0;
    else:
        return 0;
    return 0


if __name__ == "__main__":
    sys.exit(main())