import os
import logging.handlers


def get_logger(name='main', dir_='logs', show_logs=True, encoding='utf-8', is_debug=True):
    """Настройки логгера"""

    if not os.path.exists(dir_):
        os.mkdir(dir_)

    logger = logging.getLogger(name)
    if is_debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '[%(filename)s] [LINE:%(lineno)03d] [%(levelname)s] [%(asctime)s]: %(message)s'
    )

    filename = os.path.join(dir_, 'general.log')
    file_handler = logging.handlers.RotatingFileHandler(filename,
                                                        maxBytes=50 * 1048576,
                                                        backupCount=3,
                                                        encoding=encoding,)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    filename_error = os.path.join(dir_, 'error.log')
    error_handler = logging.FileHandler(filename_error, encoding=encoding)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    if show_logs is True:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        cons_formatter = logging.Formatter(
            '[%(levelname)s] [%(asctime)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(cons_formatter)
        logger.addHandler(console_handler)

    return logger