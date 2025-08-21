import os
import logging
from datetime import datetime

def setup_logger(name, logFile, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s '
                                  '| %(message)s', datefmt='%m-%d-%Y.%H:%M:%S')
    handler = logging.FileHandler(logFile)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


current_date = datetime.now().strftime("%Y-%m-%d")
log_directory = os.path.dirname(os.path.realpath(__file__)) + '/logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
log_filename = f"{log_directory}/crewai_{current_date}.log"

# Configure logging
LOGGER = setup_logger(name='log', logFile=log_filename)
