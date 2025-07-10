from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from utils.config_loader import ConfigLoader


class WebDriverInitializer:
    def __init__(self):
        """Initializes the WebDriverInitializer by loading the browser configuration."""
        self.config = ConfigLoader()
        self.browser = self.config.get_specified_browser().lower()

    def _get_browser_options(self):
        """Creates and returns browser-specific options based on the specified browser in the config.json file."""
        try:
            browser_options = self.config.get_browser_options()[self.browser]
            if self.browser == "chrome":
                options = ChromeOptions()
            elif self.browser == "firefox":
                options = FirefoxOptions()
            elif self.browser == "edge":
                options = EdgeOptions()
            elif self.browser == "chromium":
                options = ChromeOptions()
            elif self.browser == "brave":
                options = ChromeOptions()
            else:
                raise KeyError(f"The browser {self.browser} is not supported.")
            for option in browser_options:
                options.add_argument(option)
            return options
        except KeyError as e:
            raise KeyError(f"The browser_options option wasn't found in the config.json file. Error: {e}")

    def initialize_webdriver(self):
        """Initializes and returns a WebDriver instance for the specified browser."""
        try:
            options = self._get_browser_options()
            if self.browser == "chrome":
                web_driver = webdriver.Chrome(service=ChromeService(), options=options)
            elif self.browser == "firefox":
                web_driver = webdriver.Firefox(service=FirefoxService(), options=options)
            elif self.browser == "edge":
                web_driver = webdriver.Edge(service=EdgeService(), options=options)
            else:
                raise KeyError(f"The browser {self.browser} is not supported.")
            return web_driver
        except WebDriverException as e:
            raise WebDriverException(f"An error occurred while trying to initialize the WebDriver. Error: {e}")
