from watson import debug_print, get_current_method_signature, check_less
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
    def __init__(self):
        """
        Config initialization method to setup necessary parameters, states, and
        vars
        """
        # Identify method entry
        debug_print(get_current_method_signature())

        # [todo] - Add config options (rc file) for default max depth and context lines

        # List of all files/folders to ignore when parsing
        self.ignore_list = []
        # List of directories to parse
        self.dir_list = []
        # List of all files to parse
        self.file_list = []
        # List of tags to look for when parsing
        self.tag_list = []
        # Number of directories to parse recursively
        self.parse_depth = 0
        # Number of lines of issue context to grab
        self.context_depth = 15

        # Flag for command line setting of file/dir to parse
        self.cl_entry_set = False
        # Flag for command line setting of file/dir to ignore
        self.cl_ignore_set = False
        # Flag for command line setting of tag to parse for
        self.cl_tag_set = False

        # Entries that watson should show
        self.show_type = 'all'

        # Flag for whether less is avaliable to print results
        self.use_less = False
        #Flag for where the config file is located
        self.rc_file = '.watsonrc'
        # Flag for where the temp file for printing is located
        self.tmp_file = '.watsonresults'

        # Flag for whether remote access is avaliable
        self.remote_vaild = False

        # Flag for whether GitHub access is avaliable
        self.github_valid = False
        # GitHub API key generated from Remote::GitHub setup
        self.github_api = ''
        # GitHub repo associated with current directory + watson config
        self.github_repo = ''
        # Hash to hold list of all GitHub issues associated with repo
        # [todo] - What data structure for github_issues is best?
        self.github_issues = None

        # Flag for whether Bitbucket access is avaliable
        self.bitbucket_valid = False
        # Bitbucket API key generated from Remote::Bitbucket setup (username for now)
        self.bitbucket_api = ''
        # Bitbucket password for access until OAuth is implemented for Bitbucket
        self.bitbucket_pw = ''
        # Bitbucket repo associated with current directory + watson config
        self.bitbucket_repo = ''
        # Hash to hold list of all Bitbucket issues associated with repo
        # [todo] - What data structure for bitbucket_issues is best?
        self.bitbucket_issues = None

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
        # [review] - regex uses (.?)+ to grab anything after watson (optional), better regex?
        full_path = re.sub(r'/watson(.?)+', '', s) + "/assets/defaultConf"

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

    def read_conf(self):
        """
        Read configuration file and populate Config container class
        """
        # Identify method entry
        debug_print(get_current_method_signature())


        debug_print("Reading %s" % self.rc_file)
        if not FS.check_file(self.rc_file):
            print ("Unable to open %s, exiting" % self.rc_file)
            return False
        else:
            debug_print("Opened %s for reading" % self.rc_file)

        # Check if system has less for output
        self.use_less = check_less()

        # Add all the standard items to ignorelist
        # This gets added regardless of ignore list specified
        # [review] - Keep *.swp in there?
        # [todo] - Add conditional to @rc_file such that if passed by -f we accept it
        # [todo] - Add current file (watson) to avoid accidentally printing app tags
        self.ignore_list.append("..")
        self.ignore_list.append(self.rc_file)
        self.ignore_list.append(self.tmp_file)

        # Open and read rc
        # [review] - Not sure if explicit file close is required here
        rc = open(self.rc_file, 'r').read()

        debug_print('\n')

        # Create temp section var to keep track of what we are populating in config
        section = ""

        # Keep index to print what line we are on
        i = 0;

        # Fix line endings so we can support Windows/Linux edited rc files
        rc = re.sub(r'\r\n?', '\n', rc)
        for line in rc.splitlines():
            debug_print("%d: %s" % (i, line))
            i += 1

            # Ignore full line comments or newlines
            mtch = re.match(r'(^#)|(^\n)|(^ *$)', line)
            if mtch:
                debug_print("Full line comment or newline found, skipping")
                continue

            # Regex on line to find out if we are in a new [section] of
            # config parameters. If so, store it into section var and move
            # to next line
            mtch = re.match(r'\[(\w+)\]', line)
            if mtch:
                debug_print("Found section %s" % mtch.group(1))
                section = mtch.group(1)
                continue

            if section == 'context_depth':
                # No need for regex on context value, command should read this in only as a #
                # strip to get rid of any nonsense
                self.context_depth = line.strip()

            elif section == 'parse_depth':
                # No need for regex on parse value, command should read this in only as a #
                # strip to get rid of any nonsense
                self.parse_depth = line.strip()

            elif section == 'dirs':
                # If self.dir_list or self.file_list wasn't populated by CL args
                # then populate from rc
                # [review] - Populate @dirs/files_list first, then check size instead
                if self.cl_entry_set:
                    debug_print("Directories or files set from command line ignoring rc [dirs]")
                    continue

                # Regex to grab directory
                # Substitute trailing / (necessary for later formatting)
                # and push to self.dir_list
                mtch = re.match(r'^(([\w*]+)?\.?\/?)+', line)
                if mtch:
                    dir_path = mtch.group(0).rstrip('/')
                    self.dir_list.append(dir_path)
                    debug_print("%s added to self.dir_list" % dir_path)

                debug_print("self.dir_list --> %s" % self.dir_list.__str__())

            elif section == 'tags':
                # Same as previous for tags
                # [review] - Populate @tag_list, then check size instead
                if self.cl_tag_set:
                    debug_print("Tags set from command line, ignoring rc [tags]")
                    continue

                # Same as previous for tags
                # [review] - Need to think about what kind of tags this supports
                # Check compatibility with GitHub + Bitbucket and what makes sense
                # Only supports single word+number tags
                mtch = re.match(r'(\S+)', line)
                if mtch:
                    tag = mtch.group(0)
                    self.tag_list.append(tag)
                    debug_print("%s added to @tag_list" % tag)

                debug_print("self.tag_list --> %s" % self.tag_list.__str__())

            elif section == 'ignore':
                # Same as previous for ignores
                # [review] - Populate @tag_list, then check size instead
                if self.cl_ignore_set:
                    debug_print("Ignores set from command line, ignoring rc [ignores]")
                    continue

                # Same as previous for ignores (regex same as dirs)
                # Don't eliminate trailing / because not sure if dir can have
                # same name as file (Linux it can't, but not sure about Win/Mac)
                # [review] - Can Win/Mac have dir + file with same name in same dir?
                mtch = re.match(r'^(([\w*]+)?\.?\/?)+', line)
                if mtch:
                    dir_path = mtch.group(0)
                    self.ignore_list.append(dir_path)
                    debug_print("%s added to self.ignore_list" % dir_path)

                debug_print("self.ignore_list --> %s" % self.ignore_list.__str__())

            elif section == 'github_api':
                # No need for regex on API key, GitHub setup should do this properly
                # strip to get rid of any nonsense
                self.github_api = line.string()
                debug_print("GitHub API: %s" % self.github_api)

            elif section == 'github_repo':
                # Same as above
                self.github_repo = line.strip()
                debug_print("GitHub Repo: %s" % self.github_repo)

            elif section == 'bitbucket_api':
                # Same as GitHub parse above
                self.bitbucket_api = line.strip()
                debug_print("Bitbucket API: %s" % self.bitbucket_api)

            elif section == 'bitbucket_repo':
                # Same as GitHub repo parse above
                self.bitbucket_repo = line.strip()
                debug_print("Bitbucket Repo: %s" % self.bitbucket_repo)

            else:
                debug_print("Unknown tag found %s" % section)

        return True



    def update_conf(self, **kwargs):
        """
        Update config file with specified parameters
        Accepts input parameters that should be updated and writes to file
        Selective updating to make bookkeeping easier
        """
        # Identify method entry
        debug_print(get_current_method_signature())

        # Check if RC exists, if not create one.
        if not FS.check_file(self.rc_file):
            print "Unable to open %s, exiting" % self.rc_file
            self.create_conf()
        else:
            debug_print("Opened %s for reading" % self.rc_file)

        # Go through all given params and make sure they are actually config vars
        for param in kwargs:
            if not hasattr(self, param):
                debug_print("%s does not exist in Config" % param)
                debug_print("Check your input(s) to update_conf")

        # Read in currently saved RC and go through it line by line
        # Only update params that were passed to update_conf
        # This allows us to clean up the config file at the same time

        # Open and read rc
        # [review] - Not sure if explicit file close is required here
        rc = open(self.rc_file, 'r').read()
        rc_update_file = open(self.rc_file, 'w')

        # Keep index to print what line we are on
        i = 0;

        # Keep track of newlines for prettying up the conf
        nlc = 0
        section = ""

        # Fix line endings so we can support Windows/Linux edited rc files
        rc = re.sub(r'\r\n?', '\n', rc)
        for line in rc.splitlines():
            # Print line for debug purposes
            debug_print("%d: %s" % (i, line))
            i += 1

            # Look for sections and set section var
            mtch = re.match(r'\[(\w+)\]', line)
            if mtch:
                debug_print("Found section %s" % mtch.group(1))
                section = mtch.group(1)

            # Check for newlines
            # If we already have 2 newlines before any actual content, skip
            # This is just to make the RC file output nicer looking
            if line == '\n':
                debug_print("Newline found")
                nlc += 1
                if nlc < 3:
                    debug_print("Less than 3 newlines so far, let it print")
                    rc_update_file.write('%s\n' % line)
            # If the section we are in doesn't match the params passed to update_conf
            # it is safe to write the line over to the new config
            elif not section in kwargs:
                debug_print("Current section NOT a param to update")
                debug_print("Writing to new rc")
                rc_update_file.write('%s\n' % line)

                # Reset newline
                nlc = 0

            debug_print("line: %s" % line)
            debug_print("nlc: %d" % nlc)

        # Make sure there is at least 3 newlines between last section before writing new params
        rc_update_file.write('\n' * (2 - nlc))

        # Now that we have skipped all the things that need to be update, write them in
        for key, value in kwargs.iteritems():
            rc_update_file.write('[%s]\n' % key)
            rc_update_file.write(getattr(self, key))
            rc_update_file.write('\n\n\n')
            
        rc_update_file.close()
