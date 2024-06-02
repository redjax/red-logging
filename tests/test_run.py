from __future__ import annotations

import logging

log = logging.getLogger("red-log_tests")

logging.basicConfig(level=logging.DEBUG)

log.info("Running validation tests, expect passes")

from .test_suites.validation_tests.expect_pass import (
    test_return_valid_formatter_class,
    test_return_valid_formatter_dict,
    test_valid_formatter_class,
    test_valid_formatter_dict,
)

log.info("Running validation tests, expect fails")
