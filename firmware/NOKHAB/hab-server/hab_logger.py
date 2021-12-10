'''
Experimental logging module
'''
import logging
logging.basicConfig(level=logging.NOTSET)

class LoggerBase:
    ''' Base Logger class '''
    def __init__(self, module):
        self.filename = 'example.log'
        self.logger = logging.getLogger(module)

        # Create Handlers
        f_handler = logging.FileHandler(self.filename)
        f_handler.setLevel('INFO')

        # Create Formatter and add it to handler
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        self.logger.addHandler(f_handler)

    def debug(self, msg):
        ''' Log debug level message '''
        self.logger.debug(msg)

    def info(self, msg):
        ''' Log info level message '''
        self.logger.info(msg)

    def warning(self, msg):
        ''' Log warning level message '''
        self.logger.warning(msg)

    def error(self, msg):
        ''' Log error level message '''
        self.logger.error(msg)
