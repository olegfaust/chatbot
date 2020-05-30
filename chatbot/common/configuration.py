import logging

from pathlib import Path
from configparser import ConfigParser


class Configuration:
    # Default path to configs
    DEFAULT_CONFIG_FOLDER_PATH = "../../config"

    # Names of specific ChatBot components' configurations
    RETRIEVER_CONFIG_NAME = "retriever.ini"
    READER_CONFIG_NAME = "reader.ini"

    class __Configuration:
        __slots__ = \
            "retriever_config", \
            "reader_config"

        def __init__(self, config_path=None):
            logger = logging.getLogger(__name__)
            logger.info("Initializing Configuration")
            if config_path:
                logger.info("reading configuration from provided path: %s" % config_path)
                folder_path = Path(config_path)
            else:
                logger.info("no configuration configuration path provided, using default path")
                logger.info("using default configuration path: %s" % Configuration.DEFAULT_CONFIG_FOLDER_PATH)
                folder_path = Path(Path(__file__).parent, Configuration.DEFAULT_CONFIG_FOLDER_PATH)
            # check folder path exists
            if not folder_path.exists():
                logger.error("path to config files '%s' doesn't exist", folder_path)
                raise FileNotFoundError
            # create and read Retriever configuration
            self.retriever_config = ConfigParser()
            retriever_path = folder_path.joinpath(Configuration.RETRIEVER_CONFIG_NAME)
            if not retriever_path.exists():
                logger.error("path to config files '%s' doesn't exist", retriever_path)
                raise FileNotFoundError
            self.retriever_config.read(retriever_path)
            # create and read Reader configuration
            self.reader_config = ConfigParser()
            self.reader_config.read(folder_path.joinpath(Configuration.READER_CONFIG_NAME))

    __instance = None

    def __new__(cls):
        """ Virtually private constructor. """
        if not Configuration.__instance:
            Configuration.__instance = Configuration.__Configuration()
        return Configuration.__instance

    def __getattr__(self, name):
        return getattr(self.instance, name)
