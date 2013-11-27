from watson import debug_print, get_current_method_signature
from watson.fs import FS
import sys
import os
import re

class Config:
    """
    Configuration container class
    Contains all configuration options and state variables that are accessed
    throughout watson
    """
    # [todo] - Add config options (rc file) for default max depth and context lines

    # List of all files/folders to ignore when parsing
    ignore_list = []
    # List of directories to parse
    dir_list = []
    # List of all files to parse
    file_list = []
    # List of tags to look for when parsing
    tag_list = []
    # Number of directories to parse recursively
    parse_depth = 0
    # Number of lines of issue context to grab
    context_depth = 15

    # Flag for command line setting of file/dir to parse
    cl_entry_set = False
    # Flag for command line setting of file/dir to ignore
    cl_ignore_set = False
    # Flag for command line setting of tag to parse for
    cl_tag_set = False

    # Entries that watson should show
    show_type = 'all'

    # Flag for whether less is avaliable to print results
    use_less = False
    #Flag for where the config file is located
    rc_file = '.watsonrc'
    # Flag for where the temp file for printing is located
    tmp_file = '.watsonresults'

    # Flag for whether remote access is avaliable
    remote_vaild = False

    # Flag for whether GitHub access is avaliable
    github_valid = False
    # GitHub API key generated from Remote::GitHub setup
    github_api = ''
    # GitHub repo associated with current directory + watson config
    github_repo = ''
    # Hash to hold list of all GitHub issues associated with repo
    github_issues = None

    # Flag for whether Bitbucket access is avaliable
    bitbucket_valid = False
    # Bitbucket API key generated from Remote::Bitbucket setup (username for now)
    bitbucket_api = ''
    # Bitbucket password for access until OAuth is implemented for Bitbucket
    bitbucket_pw = ''
    # Bitbucket repo associated with current directory + watson config
    bitbucket_repo = ''
    # Hash to hold list of all Bitbucket issues associated with repo
    bitbucket_issues = None

    def __init__(self):
        """
        Config initialization method to setup necessary parameters, states, and
        vars
        """
        # Identify method entry
        debug_print(get_current_method_signature())

    def run(self):
        """
        Parse through configuration and obtain remote info if necessary
        """
        # Identify method entry
        debug_print(get_current_method_signature())

        # check_conf should create if no conf found, exit entirely if can't do either
        if self.check_conf() == False:
            sys.exit(1)

        self.read_conf()

        # [todo] - Need to implement the github/bitbucket stuff from the Ruby source here.

    def check_conf(self):
        """
        Check for config file in directory of execution
        Should have individual .rc for each dir that watson is used in
        This allows you to keep different preferences for different projects
        Create conf (with #create_conf) if not found
        """
        # Identify method entry
        debug_print(get_current_method_signature())

        # Check for .rc
        # If one doesn't exist, create default one with create_conf method
        if os.path.exists(self.rc_file):
            debug_print("%s found" % self.rc_file)
            return True
        else:
            debug_print("%s not found" % self.rc_file)
            debug_print("Creating default %s" % self.rc_file)

            # Create default .rc and return create_conf (True if created, False
            # if not)
            return self.create_conf()            

    def create_conf(self):
        """
        Watson config creater
        Copies default config from /assets/defaultConf to the current directory
        """
        # Identify method entry
        debug_print(get_current_method_signature())

        # Get the absolute path to the directory this source is in.
        s = os.path.abspath(sys.modules[Config.__module__].__file__)
        # [review] - regex uses (.?)+ to grab anything after lib (optional), better regex?
        full_path = re.sub(r'/lib/watson(.?)+', '', s) + "/assets/defaultConf"

        # Check to make sure we can access the default file
        if not FS.check_file(full_path):
            print "Unable to open %s" % full_path
            print "Cannot create default, exiting..."
            return False
        else:
            # Open default config file in read mode and read into temp
            input_file = open(full_path, 'r')
            default = input_file.read()

            # Open rc file in current directory in write mode and write default
            output_file = open(self.rc_file, 'w')
            output_file.write(default)

            # Close both default and new rc files
            input_file.close()
            output_file.close()

            debug_print("Successfully wrote defaultConf to current directory")
            return True


           