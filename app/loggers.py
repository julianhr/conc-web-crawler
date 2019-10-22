import logging


FORMAT = "%(asctime)s [%(threadName)s] %(filename)s:%(lineno)d %(message)s"

class Loggers:

    def __init__(self):
        self.level = None
        self.formatter = logging.Formatter(FORMAT)
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.formatter)

    def setup(self, level):
        self.level = level
        self.set_logger('main', True)
        self.set_logger('rejected_urls', False)
        self.set_logger('enqueued_urls', False)
        self.set_logger('visited_urls', False)

    def main(self):
        self.set_logger('main', True)

    def set_logger(self, name, will_stream):
        filename = f'./logs/{name}.log'
        file_handler = logging.FileHandler(filename, mode='w')
        file_handler.setFormatter(self.formatter)
        logger = logging.getLogger(name)
        logger.setLevel(self.level)
        logger.addHandler(file_handler)

        if will_stream:
            logger.addHandler(self.stream_handler)
