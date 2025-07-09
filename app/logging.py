import logging
from logging.handlers import RotatingFileHandler
import os

# Create the logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Define the log file path
log_file = "logs/app.log"

# Create a logger
logger = logging.getLogger(__name__)

# Set the logging level
logger.setLevel(logging.DEBUG)  # Capture all levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Define a formatter that will add timestamp, log level, and the actual message
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Console Handler for logging to the terminal
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File Handler for logging to a file, with log rotation after 1MB
file_handler = RotatingFileHandler(log_file, maxBytes=1e6, backupCount=3)  # 1 MB, 3 backup files
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Optional: Log to a second file for error logs
error_log_file = "logs/error.log"
error_file_handler = RotatingFileHandler(error_log_file, maxBytes=1e6, backupCount=3)
error_file_handler.setLevel(logging.ERROR)  # Log only ERROR and CRITICAL to this file
error_file_handler.setFormatter(formatter)
logger.addHandler(error_file_handler)

# A sample log message to verify
logger.debug("Logging setup complete.")

# Sample utility functions
def log_debug(message: str):
    logger.debug(message)

def log_info(message: str):
    logger.info(message)

def log_warning(message: str):
    logger.warning(message)

def log_error(message: str):
    logger.error(message)

def log_critical(message: str):
    logger.critical(message)
