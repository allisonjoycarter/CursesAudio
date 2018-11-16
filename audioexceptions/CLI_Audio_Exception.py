#not sure exactly what these are supposed to do
class CLI_Audio_Exception(Exception):
    def __init__(self):
        """a general exception that inherits exception"""
        Exception.__init__(self)

class CLI_Audio_Screen_Size_Exception(CLI_Audio_Exception):
    def __init__(self, arg):
        """a screen size exception"""
        CLI_Audio_Exception.__init__(self)

class CLI_Audio_File_Exception(CLI_Audio_Exception):
    def __init__(self, arg):
        """a file exception"""
        CLI_Audio_Exception.__init__(self)
