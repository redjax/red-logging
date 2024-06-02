import typing as t

import logging
from logging.config import dictConfig
from logging import StreamHandler, Formatter

tests_logging_config: dict[str, t.Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "propagate": True,
    "root": {},
    "formatters": {
        "tests": {
            "format": "[TESTS] [%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            "datefmt": "%Y-%m-%D %H:%M:%S",
        }
    },
    "handlers": {
        "tests_console": {
            "class": "logging.StreamHandler",
            "formatter": "tests",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "tests": {"level": "DEBUG", "handlers": ["tests_console"], "propagate": True}
    },
}


def setup_tests_logging(
    logging_config: dict[str, t.Any] = tests_logging_config
) -> None:
    assert logging_config, ValueError("Missing a logging config dict")
    assert isinstance(logging_config, dict), TypeError(
        f"logging_config must be a dict. Got type: ({type(tests_logging_config)})"
    )

    dictConfig(config=logging_config)
