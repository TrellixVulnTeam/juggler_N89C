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
import os
import sys

def create_argparser():
    parser = argparse.ArgumentParser(prog='juggler',
                                     version='v1.0',
                                     description="""Juggler - Dirty dependency management and packaging for compiled code
                                                    Copyright (C) 2014  Christian Meyer
                                                    This program comes with ABSOLUTELY NO WARRANTY. This is free software,
                                                    and you are welcome to redistribute it under certain conditions.""")
    
    parser.add_argument('COMMAND', action='store', choices=['fetch', 'publish'])
    parser.add_argument('PATH', action='store', help='Path to the project to be juggled. Must be a directory containing a juggle.xml')
    parser.add_argument('--build_number', action='store', default='local', help='Specify the build number to use when publishing, defaults to local')
    parser.add_argument('--user_config', action='store', default='~/.juggler/global.xml', help='Specify a juggler configuration explicitly. Defaults to ~/.juggler/global.xml')
    parser.add_argument('--flavor', action='store', default='vanilla', help='Specify the flavor of the build. Only packages of this flavor will be fetched and only the package of this flavor will be published. Defaults to vanilla.')
    parser.add_argument('--do_not_use_local_builds', action='store_true', default=False, help='Prevents juggler from pulling local builds from repositories. Only regular builds will be considered.')

    return parser

def main():
    parser = create_argparser()
    args = parser.parse_args()
    
    deployment_path = os.path.join(args.PATH, '.juggler')
    
    global_config = config.JugglerConfig()
    global_config.load(os.path.expanduser(args.user_config))
    
    project_config = config.ProjectConfig()
    project_config.load(os.path.expanduser(os.path.join(args.PATH, 'juggle.xml')))
    
    if args.COMMAND == 'fetch':
        dep_manager = dependency.DependencyManager(global_config.local_repository, global_config.remote_repositories)
        dep_manager.deploy(project_config.required_packages, deployment_path, args.do_not_use_local_builds)
        return 0
    elif args.COMMAND == 'publish':
        project_config.publisher.publish(global_config.local_repository,
                                         project_config.name,
                                         project_config.get_publishing_version(args.build_number),
                                         args.flavor)
        return 0
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())