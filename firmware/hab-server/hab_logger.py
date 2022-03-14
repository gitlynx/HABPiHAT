'''
Experimental logging module
'''
import logging
logging.basicConfig(level=logging.NOTSET)

class BaseLogger:
    ''' Base Logger class '''
    def __init__(self, module):
        self.filename = 'example.log'
        self._logger = logging.getLogger(module)

        # Create Handlers
        f_handler = logging.FileHandler(self.filename)
        f_handler.setLevel('INFO')

        # Create Formatter and add it to handler
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        self._logger.addHandler(f_handler)

    def log_debug(self, msg):
        ''' Log debug level message '''
        self._logger.debug(msg)

    def log_info(self, msg):
        ''' Log info level message '''
        self._logger.info(msg)

    def log_warning(self, msg):
        ''' Log warning level message '''
        self._logger.warning(msg)

    def log_error(self, msg):
        ''' Log error level message '''
        self._logger.error(msg)
