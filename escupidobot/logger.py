import logging


class BotLogger:

    @staticmethod
    def get_logger(filename):
        logger = logging.getLogger("escupidobot")
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler = logging.FileHandler(filename)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger