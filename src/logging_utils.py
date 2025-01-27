import os
import logging

def setup_logger(name, log_file, level=logging.INFO):
    """
    Function to setup logger.
    
    Args:
        name (str): Name of the logger.
        log_file (str): File path to log to.
        level (int): Logging level.
    
    Returns:
        logger: Configured logger object.
    """
    
    # Create the logs directory if it does not exist
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))

    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create file handler which logs even debug messages
    fh = logging.FileHandler(log_file)
    fh.setLevel(level)
    
    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    
    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger
