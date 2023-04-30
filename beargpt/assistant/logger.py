import logging
import logging.handlers
import os
from assistant import config

def configure_logger(app):
    log_level_str = config.config('log_level')
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)

    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log_directory = config.config('log_directory')
    log_filename = os.path.join(log_directory, "beargpt.log")
    file_handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_formatter)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)

    log_to_stdout = config.config('log_to_stdout')
    if log_to_stdout:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(log_formatter)
        app.logger.addHandler(stream_handler)

