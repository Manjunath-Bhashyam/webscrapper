import logging


class Lg:

    def __init__(self, logname):
        self.logname = logname

    def getlog(self):
        """Creating a logger with a given name"""
        try:
            logger = logging.getLogger(self.logname)
            # Set Logging to the low Level
            logger.setLevel(logging.DEBUG)
            # Set Format for the log record
            formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
            # Set FileHandler
            file_handler = logging.FileHandler('log files/scrap.log',mode='w')
            # Adding formatter
            file_handler.setFormatter(formatter)
            # Adding handlers to logger
            logger.addHandler(file_handler)
            return logger
        except Exception as e:
            raise Exception(f"(getlog): Issue in lg class \n" + str(e))
