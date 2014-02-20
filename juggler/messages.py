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

indent_level = 0
verbose = False

def Indent():
    global indent_level
    indent_level += 1

def Unindent():
    global indent_level
    indent_level -= 1

def GetIndent():
    global indent_level
    indent = ''
    i = 0
    while i < indent_level:
        indent += '  '
        i += 1
    return indent

def VERBOSE(msg):
    global verbose
    if verbose and not msg is None:
        print '%s%s' % (GetIndent(), msg)

def INFO(msg, verbose=None):
    print '%s%s' % (GetIndent(), msg) 
    Indent()
    VERBOSE(verbose)
    Unindent()

def WARNING(msg, verbose=None):
    print '%sWarning: %s' % (GetIndent(), msg) 
    Indent()
    VERBOSE(verbose)
    Unindent()

def ERROR(msg, verbose=None):
    print '%sERROR %s' % (GetIndent(), msg) 
    Indent()
    INFO(verbose)
    Unindent()

def UnableToAccessRemoteRepository(url, reason):
    WARNING('Could not access remote repository %s' % url, reason)

def VerboseException(error):
    VERBOSE(error)

def ConfigurationErrorDetected(e):
    ERROR('juggler was unable to load your project configuration', '%s' % e)

def FetchingRequiredPackages(local_repo, remote_repos):
    INFO('Fetching required packages')
    Indent()
    VERBOSE('Repositories queried:')
    Indent()
    VERBOSE('Local - %s' % local_repo)
    for repo in remote_repos:
        VERBOSE('Remote - %s' % repo)
    Unindent()
    Unindent()

def FetchingFailed(exception):
    ERROR('Failed to fetch dependencies', '%s' % exception)

def PublishingProject(name, version, flavor, local_repo):
    INFO('Publishing project')
    Indent()
    INFO('Name - %s' % name)
    INFO('Version - %s' % version)
    INFO('Flavor - %s' % flavor)
    VERBOSE('Publishing to %s' % local_repo)
    Unindent()

def PublishingFailed(exception):
    ERROR('Failed to publish project', '%s' % exception)

def ResolvedPackage(requested_package_info, flavor, resolved_package, source_type):
    INFO('Resolved %s (%s) %s - using version %s' % (requested_package_info['name'], flavor, requested_package_info['version'], resolved_package.get_version()))
    Indent()
    VERBOSE('Using artifact from %s (%s)' % (resolved_package.get_path(), source_type))
    Unindent()

def DownloadingPackage(url):
    INFO('Downloading %s' % url)
