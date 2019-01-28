RECV_BUF_SIZE = 4096
DATA_PACKET_SIZE = 22

SERVER = {
    "HOST" : "xxx.xxx.xxx.xxx",
    "PORT" : 8090,
    "MAX_LISTENER" : 10
}

DATABASE = {
    "HOST": "localhost",
    "PORT": 27018,
    "DB_NAME": "Database Test",
}

SAVE_DATA_PACKING = False

LOGGER= {
    "formatters": {
        "simple": {
            "format": '[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s'
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "infoFileHandler": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filename": "info.log"
        }
    },
    "root": {
        "level" : "DEBUG",
        "handlers": ["console", "infoFileHandler"]
    }
}

LOG_DIR = './log'

LOG_FILE = {
    "PATH": "./log/server.log",
    "MAX_FILE_SIZE": 10 * 1024 * 1024
}