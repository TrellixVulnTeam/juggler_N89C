'''
Created on 06.01.2014

@author: Konfuzzyus
'''

from exceptions import Exception
import os
import version
from xml.etree import ElementTree
from juggler.version import InvalidString

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
    <PackageStructure>
        <Library>libProject.a</Library>
        <Header>project.h</Header>
    </PackageStructure>
</Project>
'''
class ProjectConfig:
    def __init__(self):
        self.name = None
        self.version = None
        self.required_packages = []
        self.package_structure = None
    
    def load(self, filename):
        xmltree = ElementTree.ElementTree();
        xmltree.parse(filename)
        
        root = xmltree.getroot()
        if root.tag != "Project":
            raise ConfigurationError("The root element in your project configuration is '%s' instead of 'Project'" % root.tag)
        
        self.name = root.find('Name')
        if self.name is None or self.name == "":
            raise ConfigurationError("The name given in your project configuration (%s) is not valid." % self.local_repository)
        try:
            self.version = version.parse_version(root.find('Version').text)
        except InvalidString as e:
            raise ConfigurationError("My parser complained (%s) when processing the version given in your project configuration." % e)
        
        for element in root.findall('Requires/Package'):
            pack = {}
            pack['name'] = element.find('Name').text
            pack_version = element.find('Version').text
            if pack_version is None:
                pack_version = ''
            pack['version'] = version.parse_version(pack_version)
            self.required_packages.append(pack)

        # parse packaging information

'''
example juggler configuration
<Repositories>
    <Local>
        /writable/absolute/path/to/repository
    </Local>
    <Remote>
        http://readonly.url.to.server/somewhere
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
        
        self.local_repository = os.path.expanduser(root.find('Local').text)
        if os.path.exists(self.local_repository):
            if not os.path.isdir(self.local_repository):
                raise ConfigurationError("The path to the local repository I was given (%s) exists and is not a directory." % self.local_repository)
        else:
            os.mkdir(self.local_repository)
        
        for item in root.findall('Remote'):
            self.__remote_repositories.append(item.text)
