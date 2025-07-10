import json

from utils.logger_instance import logger


class ConfigLoader:
    def __init__(self, config_path="config/config.json"):
        """Initializes the ConfigLoader with the path to the configuration file."""
        self.config_path = config_path
        self.logger = logger
        self.config = self._load_config_file()

    def _load_config_file(self):
        """Loads the configuration file and returns its content as a dictionary."""
        self.logger.log_method_entry(self._load_config_file.__name__)
        try:
            self.logger.info(f"Loading configuration file from {self.config_path}")
            with open(self.config_path) as config_file:
                config_data = json.load(config_file)
                self.logger.info(f"The configuration file has been loaded from {self.config_path} successfully.")
                return config_data
        except FileNotFoundError as e:
            self.logger.error("The configuration file wasn't found.")
            raise FileNotFoundError(f"The configuration file {self.config_path} was not found. Error: {e}")

    def get_specified_browser(self):
        """Retrieves the specified browser from the configuration file."""
        self.logger.log_method_entry(self.get_specified_browser.__name__)
        try:
            self.logger.info("Retrieving the specified browser from the configuration file")
            specified_browser = self.config["browser"]
            self.logger.info(
                f"The specified browser which is : {specified_browser} has been retrieved from "
                f"{self.config_path} successfully."
            )
            return specified_browser
        except KeyError as e:
            self.logger.error('No "browser" key in the configuration file.')
            raise KeyError(f'The "browser" key is missing in the configuration file. Error: {e}')

    def get_browser_options(self):
        """Retrieves the browser options from the configuration file."""
        self.logger.log_method_entry(self.get_browser_options.__name__)
        try:
            self.logger.info("Retrieving the browser options from the configuration file")
            browser_options = self.config["browser_options"]
            self.logger.info(
                "Successfully retrieved the browser options from the configuration file. "
                f"The browser options are : {browser_options}"
            )
            return browser_options
        except KeyError as e:
            self.logger.error('No "browser_options" key in the configuration file.')
            raise KeyError(f'The "browser_options" key is missing in the configuration file. Error: {e}')
