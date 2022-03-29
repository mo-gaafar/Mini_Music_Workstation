'''Should contain printdebug and logging functionality '''
import logging

# utility globals
DEBUG_MODE = True
LOGGING_MODE = True


logging.basicConfig(filename="logs.txt",
                    format='%(asctime)s %(message)s', filemode='w')

logger = logging.getLogger()

# set the threshold to debug
logger.setLevel(logging.INFO)

logger.debug("Logger Initialized")


def print_debug(string):
    '''This prints and logs based on preset variables in util'''
    if DEBUG_MODE:
        print(string)
    if LOGGING_MODE:
        logger.info(string)
