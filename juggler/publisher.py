'''
Created on 23.01.2014

@author: Konfuzzyus
'''

class Publisher:
    def __init__(self, root_xml_element):
        self.__packers = []
        
        for bin_element in root_xml_element.findall('Binary'):
            # files go into bin
            pass
        for lib_element in root_xml_element.findall('Library'):
            # files go into lib
            pass
        for header_element in root_xml_element.findall('HeaderDirectory'):
            # files go into include
            pass
        for source_element in root_xml_element.findall('SourceDirectory'):
            # files go into src
            pass
        