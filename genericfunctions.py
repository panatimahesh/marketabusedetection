
from configparser import ConfigParser
from os import environ, getcwd, path
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)

def get_config(config_file_path):
    '''
        Reads the configuration and returns a dict object with all the configs
    :param config_file_path: config file full path
    :return: dict
    '''

    if not path.isfile(config_file_path):
        raise ValueError(f"Config file not found: {config_file_path}" )
    parser = ConfigParser()
    parser.read(config_file_path)
    print("Configuration file has been found and read successfully")
    return parser