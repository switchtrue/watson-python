from watson import debug_print, get_current_method_signature
import sys

BOLD      = "\033[01m"
UNDERLINE = "\033[4m"
RESET     = "\033[00m"

GRAY      = "\033[38;5;0m"
RED       = "\033[38;5;1m"
GREEN     = "\033[38;5;2m"
YELLOW    = "\033[38;5;3m"
BLUE      = "\033[38;5;4m"
MAGENTA   = "\033[38;5;5m"
CYAN      = "\033[38;5;6m"
WHITE     = "\033[38;5;7m"

class Printer:
    debug = False

    @staticmethod
    def cprint (msg="", color=""):
        """
        Custom color print for static call (only writes to STDOUT)
        """
        # Identify method entry
        debug_print(get_current_method_signature())

        if isinstance(color, str):
            debug_print('Custom color specified for cprint')
            sys.stdout.write(color)
        elif (256 <= color <= 0):
            debug_print('No or Default color specified for cprint')
            sys.stdout.write('\033[38;5;%sm' % color)

        sys.stdout.write(msg)

    @staticmethod
    def print_header():
        """
        Standard header print for static call (uses static cprint)
        """
        # Identify method entry
        debug_print(get_current_method_signature())

        # Header
        Printer.cprint('%s------------------------------%s\n' % (BOLD, RESET))
        Printer.cprint('%swatson%s' % (BOLD, RESET))
        Printer.cprint(' - %s%sinline issue manager%s\n' % (BOLD, YELLOW, RESET))
        Printer.cprint('%s------------------------------%s\n\n' % (BOLD, RESET))

    @staticmethod
    def print_status(msg, color):
        """
        Status printer for static call (uses static cprint)
        Print status block in standard format
        """
        Printer.cprint('%s%s%s[ ' % (RESET, BOLD, WHITE))
        Printer.cprint('%s ' % msg, color)
        Printer.cprint('%s] %s' % (WHITE, RESET))
