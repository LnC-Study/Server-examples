import platform
from multiprocessing import freeze_support

import config
from Server import Server
from Logger import Logger

if __name__ == '__main__':
    '''
        Initialize the server & start with config.py
        If the os platform is window, freeze_support() for multi processing (for test)
    '''
    # freeze_support()
    server = Server( _host= config.SERVER['HOST'],
                     _port= config.SERVER['PORT'])
    server.start()
    Logger.logWriter.info(f'Server Start: {config.SERVER["HOST"]}:{config.SERVER["PORT"]}')