# Red-Log

Helpful classes, functions, & utilities for the stdlib `logging` module. No external dependencies.

## Why?

I wanted to learn the stdlib `logging` module, and found I liked configuring my logger(s) with `logging.config.dictConfig()`. However, I did not want to have to continually check reference pages, copy/paste code, and do all the logging setup by hand each time.

`red-log` does not import any 3rd party modules, only Python's stdlib modules are used. This package does not necessarily aim to simplify configuring logging, but the [config classes](./src/red_logging/config_classes) help by exposing configuration options for the `logging` module's formatters, handlers, and loggers.

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