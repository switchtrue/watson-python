import argparse
from watson import debug_print, get_current_method_signature
from watson.version import VERSION

class Command:
    debug = False
    config = None

    @staticmethod
    def version():
        """
        Print version information about watson
        """
        # Identify method entry
        debug_print(get_current_method_signature())

        print 'watson v%s' % VERSION
        print 'Copyright (c) 2012-2013 goosecode labs'
        print 'Licensed under MIT, see LICENSE for details\n'
        print 'Written by mleonard87, see <http://goosecode.com/projects/watson>'

        return True

    @staticmethod
    def execute():
        """
        Command line controller.
        Manages program flow from given command line arguments
        """
        # Identify method entry
        debug_print(get_current_method_signature())
        
        parser = argparse.ArgumentParser(prog='',
            usage='\033[01mwatson [OPTION]...',
            description="""
                Running watson with no arguments will parse with settings in
                RC file If no RC file exists, default RC file will be created
                """,
            epilog="""
                Any number of files, tags, dirs, and ignores can be listed after flag
                Ignored files should be space separated
                To use *.filetype identifier, encapsulate in "" to avoid shell substitutions

                Report bugs to: watson@goosecode.com
                watson home page: <http://goosecode.com/projects/watson>
                [goosecode] labs | 2012-2013\033[00m
                """)

        parser.add_argument('-c', '--context-depth', dest='context_depth',
            help='number of lines of context to provide with posted issue')
        parser.add_argument('-d', '--dirs', dest='dirs',
            help='list of directories to search in')
        parser.add_argument('-f', '--files', dest='files',
            help='list of files to search in')
        parser.add_argument('-i', '--ignore', dest='ignore',
            help='list of files, directories, or types to ignore')
        parser.add_argument('-p', '--parse-depth', dest='parse_depth',
            help='depth to recursively parse directories')
        parser.add_argument('-r', '--remote', dest='remote',
            help='list / create tokens for Bitbucket/Github')
        parser.add_argument('-s', '--show', dest='show',
            help='whether to show [all, clean, dirty] files')
        parser.add_argument('-t', '--tags', dest='tags',
            help='list of tags to search for')
        parser.add_argument('-u', '--update', dest='update', action='store_const',
            const=True, help='update remote repos with current issues')
        parser.add_argument('-v', '--version', dest='version', action='store_const',
            const=True, help='print watson version and info')        

        args = parser.parse_args()
        
        # If we get the version flag, ignore all other flags. Just display the 
        # version information and exit.
        if args.version:
            return Command.version()

        from watson.config import Config
        Command.config = Config()

        if args.context_depth:
            debug_print('Found -c/--context-depth argument')
            set_context(args.context_depth)

        if args.dirs:
            debug_print('Found -d/--dirs argument')

        if args.files:
            debug_print('Found -f/--files argument')

        if args.ignore:
            debug_print('Found -i/--ignore argument')

        if args.parse_depth:
            debug_print('Found -p/--parse-depth argument')

        if args.remote:
            debug_print('Found -r/--remote argument')

        if args.show:
            debug_print('Found -s/--show argument')
        
        if args.tags:
            debug_print('Found -t/--tags argument')

        if args.update:
            debug_print('Found -u/--update argument')

    @staticmethod
    def set_context(args):
        """
        Set context_depth parameter in config
        """
        # Identify method entry
        debug_print(get_current_method_signature())
