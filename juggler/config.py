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

from exceptions import Exception
import os
import version
from xml.etree import ElementTree
from version import InvalidString

class ConfigurationError(Exception):
    pass

'''
example project configuration
<Project>
    <Name>NameOfThisProject</Name>
    <Version>0.0</Version>
    <Requires>
        <Package>
            <Name>RequiredPackage</Name>
            </Version> <!-- optional -->
        </Package>
    </Requires>
    <Content>
        <BinaryPath target=lib>build/libProject.a</Path>
        <SourcePath target=script>script/myscript.sh</Path>
        <Headers target=include/myproject>thisproject/mypublicheaders</Headers>
    </Content>
</Project>
'''
class ProjectConfig:
    def __init__(self):
        self.name = None
        self.version = None
        self.required_packages = []
        self.content_node = None
    
    def load(self, filename):
        xmltree = ElementTree.ElementTree();
        try:
            xmltree.parse(filename)
        except IOError as e:
            raise ConfigurationError("Could not load juggle.xml from source directory, I expect it to be in '%s'" % filename)
        
        root = xmltree.getroot()
        if root.tag != "Project":
            raise ConfigurationError("The root element in your project configuration is '%s' instead of 'Project'" % root.tag)
        
        self.name = root.find('Name').text
        if self.name is None or self.name == "":
            raise ConfigurationError("The name given in your project configuration (%s) is not valid." % self.local_repository)
        try:
            self.version = version.parse_version(root.find('Version').text)
        except InvalidString as e:
            raise ConfigurationError("My parser complained (%s) when processing the version given in your project configuration." % e)
        
        if self.version.getMajor() is None or self.version.getMinor() is None:
            raise ConfigurationError("The version given for your project must specify major and minor revision, you specified %s." % self.version)
        
        for element in root.findall('Requires/Package'):
            pack = {}
            pack['name'] = element.find('Name').text
            pack_version_element = element.find('Version')
            pack_version = None
            if pack_version_element is None:
                pack_version = ''
            else:
                pack_version = pack_version.text 
            pack['version'] = version.parse_version(pack_version)
            self.required_packages.append(pack)

        self.content_node = root.find('Content')
    
    def get_publishing_version(self, build_number):
        return version.VersionInfo( self.version.getMajor(), self.version.getMinor(), build_number)

'''
example juggler configuration
<Repositories>
    <Local>
        /writable/absolute/path/to/repository
    </Local>
    <Remote>
        http://readonly.url.to.server/somewhere
    </Remote>
    <Remote>
        http://readonly.url.to.server/somewhereelse
    </Remote>
</Repositories>
'''
class JugglerConfig:
    def __init__(self):
        self.local_repository = None
        self.remote_repositories = []

    def load(self, filename):
        if not os.path.isfile(filename):
            raise ConfigurationError("I can not find my configuration: '%s' does not appear to be an existing file." % filename)
        
        xmltree = ElementTree.ElementTree();
        xmltree.parse(filename)
        
        root = xmltree.getroot()
        if root.tag != "Repositories":
            raise ConfigurationError("The root element in my configuration is '%s' instead of 'Repositories'" % root.tag)
        
        self.local_repository = os.path.expanduser(root.find('Local').text.strip())
        if os.path.exists(self.local_repository):
            if not os.path.isdir(self.local_repository):
                raise ConfigurationError("The path to the local repository I was given (%s) exists and is not a directory." % self.local_repository)
        else:
            os.mkdir(self.local_repository)
        
        for item in root.findall('Remote'):
            self.remote_repositories.append(item.text.strip())
