from loguru import logger


def setup_logging():
    logger.remove()
    logger.add(lambda m: print(m, end=""), level="INFO")
    return logger
