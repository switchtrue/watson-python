from watson import debug_print, get_current_method_signature
import os

class FS:
    """
    File system utility function class
    Contains all methods for file access in watson
    """
    debug = False

    @staticmethod
    def check_file(filename):
        """
        Check if file exists and can be opened
        """
        # Identify method entry
        debug_print(get_current_method_signature())

        # Error check for input
        if len(filename) == 0:
            debug_print("No file specified")
            return False

        # Check if file can be opened
        if os.access(filename, os.R_OK):
            debug_print("%s exists and opened successfully" % filename)
            return True
        else:
            debug_print("Could not open %s, skipping" % filename)
            return False            

    @staticmethod
    def check_dir(dirname):
        """
        Check if directory exists and can be opened
        """
        # Identify method entry
        debug_print(get_current_method_signature())

        # Error check for input
        if len(dirname) == 0:
            debug_print( "No directory specified")
            return False

        if os.path.isdir(dirname):
            debug_print("%s exists and opened succesfully" % dirname)
            return True
        else:
            debug_print("Could not open %s, skipping" % dirname)
            return False