#
#   Experimenting Logging
#
#
import logging
logging.basicConfig(level=logging.NOTSET)

LOG_FILE = 'base_station.log'

class loggerBase:
    def __init__(self, module):
        self.filename = LOG_FILE
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
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)


class loggerGPS(loggerBase):
    def __init__(self):
        loggerBase.__init__(self, "GPS")


class loggerRF(loggerBase):
    def __init__(self):
        loggerBase.__init__(self, 'RF')


if __name__ == "__main__":
    GPS = loggerGPS()
    RF = loggerRF()

    GPS.info("GPS Locked")
    GPS.warning("NO satellites")
    GPS.debug("Debug")
    GPS.error("Error")

    RF.error("Radio Not available")
    RF.info("Wat is er fout met info")
