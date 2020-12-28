import logging


def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')

    file_handler = logging.FileHandler('./log/api.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
