import traceback

# Global flag to turn ON debugging across all files
GLOBAL_DEBUG_ON = True
# Global flag to turn OFF debugging across all files
GLOBAL_DEBUG_OFF = False

def debug_print(msg):
    """
    Global debug print that prints based on local file DEBUG flag as well as GLOBAL debug flag
    """
    # [todo] - If input msg is a Hash, use pp to dump it

    # Print only if DEBUG flag of calling class is true OR
    # GLOBAL_DEBUG_ON of Watson module (defined above) is true
    # AND GLOBAL_DEBUG_OFF of Watson module (Defined above) is false

    # Sometimes we call debug_print from a static method (class << self)
    # and other times from a class method, and ::DEBUG is accessed differently
    # from a class vs object, so lets take care of that
    #_DEBUG = (self.is_a? Class) ? self::DEBUG : self.class::DEBUG

    _DEBUG = False

    if (_DEBUG == True or GLOBAL_DEBUG_ON == True) and GLOBAL_DEBUG_OFF == False:
        print '=> %s' % msg



def get_current_method_signature():
    """
    Returns the name of the method that is currently running (prior to calling 
    this method).
    """
    (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
    return 'watson.%s : %s' % (filename.split('/')[-1][:-3], function_name)