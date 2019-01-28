import logging, logging.config, os, config, datetime, time
import logging.handlers

from SingletonCreator import SingletonCreater

class Logger( SingletonCreater):
    logWriter = None
    # logging.config.dictConfig(config=config.LOGGER)

    logWriter = logging.getLogger('ServerLogger')
    logWriter.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s|%(filename)s] %(asctime)s > %(message)s')

    if not os.path.isdir(config.LOG_DIR):
        os.mkdir(config.LOG_DIR)

    fileHandler = logging.handlers.RotatingFileHandler( filename= config.LOG_FILE['PATH'],
                                                        maxBytes= config.LOG_FILE['MAX_FILE_SIZE'],
                                                        backupCount=3)
    streamHandler = logging.StreamHandler()

    fileHandler.setLevel( logging.INFO)
    fileHandler.setFormatter(formatter)
    streamHandler.setFormatter(formatter)

    logWriter.addHandler(fileHandler)
    logWriter.addHandler(streamHandler)