from watson import debug_print, get_current_method_signature
from watson.printer import Printer, RED
from watson.fs import FS
import os
import re

class Parser:
    """
    Dir/File parser class.
    Contains all necessary methods to parse through files and directories for
    specified tags and generate data structure containing found issues.
    """

    # [review] - Not sure if passing config here is best way to access it.
    def __init__(self, config):
        """
        Initialize the parse with the current watson config.
        """
        # Identify method entry.
        debug_print(get_current_method_signature())
        self.config = config

    def run(self):
        """
        Begins parsing of files / dirs specified in the initial dir/file lists.
        """
        # Identify method entry.
        debug_print(get_current_method_signature())

        # Go through all files added for CL (sort them first).
        # If empty, sort and each will do nothing, no errors.
        completed_dirs = []
        completed_files = []
        if self.config.cl_entry_set:
            for f in self.config.file_list.sort():
                completed_files.append(parse_file(f))

    def parse_dir(self, dir, depth):
        """
        Parse through specified directory and find all subdirs and files.
        """
        # Identify method entry.
        debug_print(get_current_method_signature())
        return NotImplemented

    def parse_file(self, filename):
        """
        Parse through individual files looking for issue tags, then generate
        formatted issue hash.
        """
        # Identify method entry.
        debug_print(get_current_method_signature())

        relative_path = filename
        absolute_path = os.path.abspath(filename)

        # Error check on input, use input filename to make sure relative path is
        # correct.
        if FS.check_file(relative_path):
            debug_print("Opened %s for parsing." % absolute_path)
            debug_print("Short path: %s" % relative_path)
        else:
            print "Unable to open %s, exiting" % relative_path
            # [review] - do I really want to return None here? what consumes this?
            return None 

        # Get file extension and set corresponding comment type.
        comment_type = self.get_comment_type(relative_path)
        if not comment_type:
            debug_print("Using default (#) comment type.")
            comment_type = '#'

        # Open file and read in entire thing into an array.
        # Use an array so we can look ahead when creating issues later.
        # [review] - Not sure if explicit file close is required here.
        data = []
        file_to_parse = open(absolute_path, 'r')
        for line in file_to_parse:
            data.append(line.strip())

        # Initialize issue list hash
        issue_list = {}
        issue_list['relative_path'] = relative_path
        issue_list['absolute_path'] = absolute_path
        issue_list['has_issues'] = False
        for tag in self.config.tag_list:
            debug_print("Create array named %s" % tag)
            issue_list[tag] = []

        
        # For each comment type allowed for the file type convert it into a
        # string that can be used in a regex.
        comment_type_re_str = '|'.join('(' + re.escape(ext) + ')' for ext in comment_type)
        issue_re = re.compile(r'^(%s)+?\s+\[(?P<tag_name>\w+)\]\s+-\s+(?P<title_text>.+)' % comment_type_re_str)
        # Loop through all array elements (lines in file) and look for issues
        for i, line in enumerate(data):
            # Find any comment line with [tag] - text (any combination of space
            # and # acceptable).
            # Using if match to stay consistent (with config.py) see there for 
            # explanation of why I do this (not a good good one persay...)
            mtch = issue_re.match(line.strip())
            if not mtch:
                debug_print("No valid tag found in line, skipping")
                continue

            tag = mtch.group('tag_name')

            if tag not in self.config.tag_list:
                Printer.print_status('!', RED)
                print "Unknown tag [%s] found, ignoring" % tag
                print "      You might want to include it in you RC or with the -t/--tags flag"
                continue

            # Found a valid match (with recognized tag).
            # Set flag for this issue_list (for_file) to indicate that.
            issue_list['hase_issues'] = True

            title = mtch.group('title_text')
            debug_print("Issue found")
            debug_print("Tag: %s" % tag)
            debug_print("Issue: %s" % title)

            # Create dict for each issue found.
            issue = {}
            issue['line_number'] = i + 1
            issue['title'] = title

            # Grab context of issue specified by Config param (+1 to include issue iteself.)
            issue['context'] = data[i:i + self.config.context_depth + 1]





    def get_comment_type(self, filename):
        """
        Get comment syntax for given file.
        """
        # Identify method entry
        debug_print(get_current_method_signature())

        ext = {
            'cpp'    : ['//', '/*'],        # C++
            'cc'     : ['//', '/*'],
            'hpp'    : ['//', '/*'],
            'c'      : ['//', '/*'],        # C
            'h'      : ['//', '/*'],
            'java'   : ['//', '/*', '/**'], # Java
            'class'  : ['//', '/*', '/**'],
            'cs'     : ['//', '/*'],        # C#
            'js'     : ['//', '/*'],        # JavaScript
            'php'    : ['//', '/*', '#'],   # PHP
            'm'      : ['//', '/*'],        # ObjectiveC
            'mm'     : ['//', '/*'],
            'go'     : ['//', '/*'],        # Go(lang)
            'scala'  : ['//', '/*'],        # Scala
            'erl'    : ['%%', '%'],         # Erlang
            'f'      : ['!'],               # Fortran
            'f90'    : ['!'],               # Fortran
            'F'      : ['!'],               # Fortran
            'F90'    : ['!'],               # Fortran
            'hs'     : ['--'],              # Haskell
            'sh'     : ['#'],               # Bash
            'rb'     : ['#'],               # Ruby
            'pl'     : ['#'],               # Perl
            'pm'     : ['#'],
            't'      : ['#'],
            'py'     : ['#'],               # Python
            'coffee' : ['#'],               # CoffeeScript
            'zsh'    : ['#'],               # Zsh
            'clj'    : [';;'],              # Clojure
            'sql'    : ['---', '//', '#' ], # SQL and PL types
        }

        # Grab the file extension (.something).
        # Check to see whether it is recognized and set comment type.
        # If unrecognized, try to grab the next .something extension.
        # This is to account for file.cpp.1 or file.cpp.bak, ect.

        filename_part_list = filename.split('.')
        for filename_part in reversed(filename_part_list):
            debug_print("Extension .%s" % filename_part)

            if filename_part in ext:
                return ext[filename_part]

        # We didn't find any matches from the filename, return None
        # Deal with what default to use in calling method
        debug_print("Couldn't find any recognized extension type")
        return None

