import os
import logging
import sys

basedir = os.path.abspath(os.path.dirname(__file__))
FORMATTER = logging.Formatter("%(asctime)s - %(filename)s:%(lineno)s - %(funcName)2s() ] %(message)s")
LOG_FILE = "WMO_logs/WMO.log"


class MyLogger:

    @staticmethod
    def get_console_handler():
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(FORMATTER)
        return console_handler

    # @staticmethod
    # def get_file_handler():
    #     file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    #     file_handler.setFormatter(FORMATTER)
    #     return file_handler

    def get_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.get_console_handler())
        # logger.addHandler(self.get_file_handler())
        logger.propagate = False
        return logger


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'secret-key'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    # SECRET_KEY = 'soft-testing-dev'
    SERVER_NAME = 'localhost.localdomain:9898'


class TestingConfig(Config):
    TESTING = True
