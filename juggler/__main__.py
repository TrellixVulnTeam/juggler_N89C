#!/usr/bin/env/python

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

import argparse
import config
import dependency
import publisher
import os
import sys
import messages

def create_argparser():
    parser = argparse.ArgumentParser(prog='juggler',
                                     version='v0.2',
                                     description="""Juggler - Dirty dependency management and packaging for compiled code
                                                    Copyright (C) 2014  Christian Meyer
                                                    This program comes with ABSOLUTELY NO WARRANTY. This is free software,
                                                    and you are welcome to redistribute it under certain conditions.""")
    
    parser.add_argument('COMMAND', action='store', choices=['fetch', 'publish'])
    parser.add_argument('SOURCE_PATH', action='store', help='Path to the project to be juggled. Must be a directory containing a juggle.xml')
    parser.add_argument('BINARY_PATH', action='store', help='Path to the directory where the binary files will be built, can be the same as SOURCE_PATH.')
    parser.add_argument('--build_number', action='store', default='local', help='Specify the build number to use when publishing, defaults to local')
    parser.add_argument('--user_config', action='store', default='~/.juggler/global.xml', help='Specify a juggler configuration explicitly. Defaults to ~/.juggler/global.xml')
    parser.add_argument('--flavor', action='store', default='vanilla', help='Specify the flavor of the build. Only packages of this flavor will be fetched and only the package of this flavor will be published. Defaults to vanilla.')
    parser.add_argument('--do_not_use_local_builds', action='store_true', default=False, help='Prevents juggler from pulling local builds from repositories. Only regular builds will be considered.')

    return parser

def main(argv):
    parser = create_argparser()
    args = parser.parse_args(argv)
    
    deployment_path = os.path.join(args.BINARY_PATH, '.juggler')
    try:
        global_config = config.JugglerConfig()
        global_config.load(os.path.expanduser(args.user_config))
        
        project_config = config.ProjectConfig()
        project_config.load(os.path.expanduser(os.path.join(args.SOURCE_PATH, 'juggle.xml')))
    except config.ConfigurationError as e:
        messages.ConfigurationErrorDetected(e)
        return -1
        
    if args.COMMAND == 'fetch':
        try:
            messages.FetchingRequiredPackages(global_config.local_repository, global_config.remote_repositories)
            dep_manager = dependency.DependencyManager(global_config.local_repository, global_config.remote_repositories)
            dep_manager.deploy(project_config.required_packages, deployment_path, args.do_not_use_local_builds, args.flavor)
        except dependency.RequiredPackageNotAvailable as e:
            messages.FetchingFailed(e)
            return -1
    elif args.COMMAND == 'publish':
        try:
            name = project_config.name
            version = project_config.get_publishing_version(args.build_number)
            flavor = args.flavor
            repo = global_config.local_repository
            messages.PublishingProject(name, version, flavor, repo)
            distributer = publisher.Publisher(project_config.content_node, args.SOURCE_PATH, args.BINARY_PATH)
            distributer.publish(repo, name, version, flavor)
        except publisher.PackedPathNotFound as e:
            messages.PublishingFailed(e)
            return -1
    else:
        pass
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))