import logging
import os
from datetime import datetime
from pathlib import Path

# Global variables to maintain configuration
log_file = None
logger_initialized = False
app_logger = None


def setup_logger(script_file=None, logger_name="app_logger"):
    """
    Configures the main application logger.
    Should only be called once from main.py
    """
    global log_file, logger_initialized, app_logger
    log_level = os.getenv("APP_LOG_LEVEL", "DEBUG").upper()

    if logger_initialized and app_logger:
        return app_logger

    if script_file is None:
        return logging.getLogger(logger_name)

    current_dir = Path(script_file).resolve().parent
    log_file = current_dir / "app.log"

    # Use a fixed name for the logger
    app_logger = logging.getLogger(logger_name)

    if not app_logger.hasHandlers():
        app_logger.setLevel(log_level)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        app_logger.addHandler(console_handler)
        app_logger.addHandler(file_handler)

        date_time = datetime.now()
        app_logger.info(
            "************************************************************************************************")
        app_logger.info(f"Executing {os.path.basename(script_file)} at {date_time.strftime('%Y-%m-%d %H:%M:%S')}")
        app_logger.info(
            "************************************************************************************************")

    logger_initialized = True
    return app_logger


def get_logger(logger_name="app_logger"):
    """
    Gets the already configured logger.
    Use this function in services, repositories, etc.
    """
    global app_logger, logger_initialized

    if not logger_initialized or app_logger is None:
        # If not initialized, return a basic logger
        return logging.getLogger(logger_name)

    return app_logger


def get_log_file_path():
    """
    Returns the path of the current log file
    """
    global log_file
    return log_file