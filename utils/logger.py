import os
import logging
from datetime import datetime


class Logger:
    def __init__(self, name, log_level=logging.INFO, log_file_path="logs"):
        """Logger class to log messages to console and file."""

        self.logger = logging.getLogger(name)

        self.logger.setLevel(log_level)
        self.logger.propagate = False

        log_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        if not os.path.exists(log_file_path):
            os.makedirs(log_file_path)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)

        log_file_name = os.path.join(log_file_path, f"app_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
        file_handler = logging.FileHandler(log_file_name)
        file_handler.setFormatter(log_format)

        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)


    def debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)

    def info(self, message):
        """Log an info message."""
        self.logger.info(message)

    def warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)

    def error(self, message):
        """Log an error message."""
        self.logger.error(message)

    def critical(self, message):
        """Log a critical message."""
        self.logger.critical(message)

    def log_method_entry(self, method_name, width=30):
        """Logs the entry into the current method with the method name centered."""
        centered_name = method_name.center(width, "-")
        self.logger.info(f"Method Name: {centered_name}")

    def log_action(self, action_name, width=92):
        """Logs the start of an action with the action name centered."""
        centered_name = action_name.center(width, "*")
        self.logger.info(f"Action: {centered_name}")
