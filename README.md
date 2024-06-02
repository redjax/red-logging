# red-log

## Logger Configuration

### With dictConfig()

Base config dict:

```python
{
    "version": 1,
    "disable_existing_loggers": False,
    "propagate": True,
    "root": {},
    "formatters": {},
    "handlers": {},
    "loggers": {}
}
```

```python
from logging.config import dictConfig

logging_configdict: dict = {
    "version": 1,
    "disable_existing_loggers": false,
    "propagate": true,
    "root": {
        "": {
            "handlers": [
                "console"
            ],
            "level": "NOTSET"
        }
    },
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s] > [%(filename)s:%(lineno)d] [%(funcName)s]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "": {
            "handlers": [
                "console"
            ],
            "level": "NOTSET"
        }
    }
}

dictConfig(logging_configdict)
log = logging.getLogger(__name__)

log.info("Logger configured")

```

## Links

- [python-guide.org: Logging in a library](https://docs.python-guide.org/writing/logging/#logging-in-a-library)
- [docs.python.org: Configuring logging for a library](https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library)
- [RealPython: Logging in Python](https://realpython.com/python-logging/)
- [dev.to: Using the logger class in Python](https://dev.to/luca1iu/using-the-logger-class-in-python-for-effective-logging-4ghc)
- [machinelearningplus.com: Python logging guide](https://www.machinelearningplus.com/python/python-logging-guide/)
- [askpython.com: Configure logging in Python](https://www.askpython.com/python-modules/configure-logging-in-python)
- [betterprogramming.pub: How to implement logging in your Python application](https://betterprogramming.pub/how-to-implement-logging-in-your-python-application-1730315003c4)
- [Medium.com: Create a reusable logger factory](https://medium.com/geekculture/create-a-reusable-logger-factory-for-python-projects-419ad408665d)