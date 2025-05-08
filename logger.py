import logging
import sys

def get_logger(name=__name__):

    """
    Returns a logger with the given name. If the logger has no handlers, adds
    console and file handlers with a DEBUG level and a format of
    "%(asctime)s - %(levelname)s - %(message)s".

    Parameters
    ----------
    name : str
        The name of the logger to return

    Returns
    -------
    logging.Logger
        The logger with the given name
    """


    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))


        # File handler
        file_handler = logging.FileHandler('test.log', mode='a')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
