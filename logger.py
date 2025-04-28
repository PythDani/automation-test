import logging
import sys

def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers
    if not logger.handlers:

        # Handler de consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        # Handler de archivo
        file_handler = logging.FileHandler('test.log', mode='a')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
