import logging


def log_it(text, log_type='info'):
    if log_type == 'exception':
        logging.exception(text)
    else:
        logging.info(text)
