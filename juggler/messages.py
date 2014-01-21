'''
Created on 13.01.2014

@author: Konfuzzyus
'''

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

def WARNING(msg, verbose=None):
    print "%sWarning: %s" % (GetIndent(), msg) 
    Indent()
    VERBOSE(verbose)
    Unindent()

def UnableToAccessRemoteRepository(url, reason):
    WARNING("Could not access remote repository %s" % url, reason)

def VerboseException(error):
    VERBOSE(error)
