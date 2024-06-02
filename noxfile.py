from __future__ import annotations

import logging
import logging.config
import logging.handlers
from pathlib import Path
import platform
import shutil

def setup_nox_logging() -> None:
    logging_config: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {"nox": {"level": "DEBUG", "handlers": ["console"], "propagate": False}},
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "nox",
                "level": "DEBUG",
                "stream": "ext://sys.stdout",
            }
        },
        "formatters": {
            "nox": {
                "format": "[NOX] [%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
                "datefmt": "%Y-%m-%D %H:%M:%S",
            }
        },
    }

    logging.config.dictConfig(config=logging_config)

setup_nox_logging()

log = logging.getLogger("nox")

import nox

nox.options.default_venv_backend = "venv"
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = False
nox.options.error_on_missing_interpreters = False
# nox.options.report = True

## Define sessions to run when no session is specified
nox.sessions = ["lint", "export", "tests"]

# INIT_COPY_FILES: list[dict[str, str]] = [
#     {"src": "config/.secrets.example.toml", "dest": "config/.secrets.toml"},
#     {"src": "config/settings.toml", "dest": "config/settings.local.toml"},
# ]
## Define versions to test
PY_VERSIONS: list[str] = ["3.12", "3.11"]
log.debug(f"Configured Python versions: {PY_VERSIONS}")
## Set PDM version to install throughout
PDM_VER: str = "2.15.4"
log.debug(f"PDM version: {PDM_VER}")
## Set paths to lint with the lint session
LINT_PATHS: list[str] = ["src", "tests", "./noxfile.py"]
log.debug(f"Lint paths: {LINT_PATHS}")

## Get tuple of Python ver ('maj', 'min', 'mic')
PY_VER_TUPLE = platform.python_version_tuple()
log.debug(f"Python version tuple: {PY_VER_TUPLE}")
## Dynamically set Python version
DEFAULT_PYTHON: str = f"{PY_VER_TUPLE[0]}.{PY_VER_TUPLE[1]}"
log.debug(f"Detected Python version: {DEFAULT_PYTHON}")

## Set directory for requirements.txt file output
REQUIREMENTS_OUTPUT_DIR: Path = Path("./requirements")
log.debug(f"Searching for requirements.txt file(s) in path: {REQUIREMENTS_OUTPUT_DIR}.")
## Ensure REQUIREMENTS_OUTPUT_DIR path exists
if not REQUIREMENTS_OUTPUT_DIR.exists():
    log.warning(
        f"Could not find path '{REQUIREMENTS_OUTPUT_DIR}'. Attempting to create directory."
    )
    try:
        REQUIREMENTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        msg = Exception(
            f"Unable to create requirements export directory: '{REQUIREMENTS_OUTPUT_DIR}'. Details: {exc}"
        )
        log.error(msg)

        log.warning(
            f"Failed creating path '{REQUIREMENTS_OUTPUT_DIR}'. Defaulting to path '.'"
        )
        REQUIREMENTS_OUTPUT_DIR: Path = Path(".")


@nox.session(python=DEFAULT_PYTHON, name="build-env")
@nox.parametrize("pdm_ver", [PDM_VER])
def setup_base_testenv(session: nox.Session, pdm_ver: str):
    log.info(
        f"Building Nox environment. PDM version: {pdm_ver}. Using Python: {DEFAULT_PYTHON}"
    )
    session.install(f"pdm>={pdm_ver}")

    log.info("Installing dependencies with PDM")
    session.run("pdm", "sync")
    session.run("pdm", "install")


@nox.session(python=[DEFAULT_PYTHON], name="lint")
def run_linter(session: nox.Session):
    log.info(f"Linting code. Python version(s): {DEFAULT_PYTHON}")
    session.install("ruff")

    for d in LINT_PATHS:
        if not Path(d).exists():
            log.warning(f"Skipping lint path '{d}', could not find path")
            pass
        else:
            lint_path: Path = Path(d)
            log.debug(f"Running ruff imports sort on '{d}'")
            session.run(
                "ruff",
                "--select",
                "I",
                "--fix",
                lint_path,
            )

            # print(f"Formatting '{d}' with Black")
            # session.run(
            #     "black",
            #     lint_path,
            # )

            log.debug(f"Running ruff checks on '{d}' with --fix")
            session.run(
                "ruff",
                "check",
                "--config",
                "ruff.toml",
                lint_path,
                "--fix",
            )


@nox.session(python=[DEFAULT_PYTHON], name="ci-lint")
def run_ci_linter(session: nox.Session):
    log.info(f"Linting code (CI pipeline). Python version(s): {DEFAULT_PYTHON}")

    session.install("ruff")

    for d in LINT_PATHS:
        if not Path(d).exists():
            log.warning(f"Skipping lint path '{d}', could not find path")
            pass
        else:
            lint_path: Path = Path(d)
            log.debug(f"Running ruff imports sort on '{d}'")
            session.run(
                "ruff",
                "--select",
                "I",
                "--fix",
                lint_path,
            )

            # print(f"Formatting '{d}' with Black")
            # session.run(
            #     "black",
            #     lint_path,
            # )

            log.debug(f"Running ruff checks on '{d}' with --fix")
            session.run(
                "ruff",
                "check",
                "--config",
                "ruff.ci.toml",
                lint_path,
                "--fix",
            )


@nox.session(python=[DEFAULT_PYTHON], name="export")
@nox.parametrize("pdm_ver", [PDM_VER])
def export_requirements(session: nox.Session, pdm_ver: str):
    log.info(
        f"Exporting requirements file(s). Python version(s): {DEFAULT_PYTHON}. PDM version: {pdm_ver}. Requirements output directory: {REQUIREMENTS_OUTPUT_DIR}"
    )
    session.install(f"pdm>={pdm_ver}")

    log.debug("Exporting production requirements")
    session.run(
        "pdm",
        "export",
        "--prod",
        "-o",
        f"{REQUIREMENTS_OUTPUT_DIR}/requirements.txt",
        "--without-hashes",
    )

    log.debug("Exporting development requirements")
    session.run(
        "pdm",
        "export",
        "-d",
        "-o",
        f"{REQUIREMENTS_OUTPUT_DIR}/requirements.dev.txt",
        "--without-hashes",
    )

    # log.debug("Exporting CI requirements")
    # session.run(
    #     "pdm",
    #     "export",
    #     "--group",
    #     "ci",
    #     "-o",
    #     f"{REQUIREMENTS_OUTPUT_DIR}/requirements.ci.txt",
    #     "--without-hashes",
    # )


@nox.session(python=PY_VERSIONS, name="tests")
@nox.parametrize("pdm_ver", [PDM_VER])
def run_tests(session: nox.Session, pdm_ver: str):
    log.info(f"Running tests. Python version(s): {PY_VERSIONS}")
    session.install(f"pdm>={pdm_ver}")
    session.run("pdm", "install")

    log.debug("Running Pytest tests")
    session.run(
        "pdm",
        "run",
        "pytest",
        "-n",
        "auto",
        "--tb=auto",
        "-v",
        "-rsXxfP",
    )


@nox.session(python=PY_VERSIONS, name="pre-commit-all")
def run_pre_commit_all(session: nox.Session):
    log.info(f"Running pre-commit. Python version(s): {PY_VERSIONS}")
    session.install("pre-commit")
    session.run("pre-commit")

    log.debug("Running all pre-commit hooks")
    session.run("pre-commit", "run")


@nox.session(python=PY_VERSIONS, name="pre-commit-update")
def run_pre_commit_autoupdate(session: nox.Session):
    log.info(f"Updating pre-commit hook(s). Python version(s): {PY_VERSIONS}")
    session.install(f"pre-commit")

    log.debug("Running pre-commit autoupdate")
    session.run("pre-commit", "autoupdate")


@nox.session(python=PY_VERSIONS, name="pre-commit-nbstripout")
def run_pre_commit_nbstripout(session: nox.Session):
    log.info(f"Running Jupyter notebook strip hook. Python version(s): {PY_VERSIONS}")
    session.install(f"pre-commit")

    log.debug("Running nbstripout pre-commit hook")
    session.run("pre-commit", "run", "nbstripout")


# @nox.session(python=[PY_VER_TUPLE], name="init-setup")
# def run_initial_setup(session: nox.Session):
#     if INIT_COPY_FILES is None:
#         print(f"INIT_COPY_FILES is empty. Skipping")
#         pass

#     else:

#         for pair_dict in INIT_COPY_FILES:
#             src = Path(pair_dict["src"])
#             dest = Path(pair_dict["dest"])
#             if not dest.exists():
#                 print(f"Copying {src} to {dest}")
#                 try:
#                     shutil.copy(src, dest)
#                 except Exception as exc:
#                     msg = Exception(
#                         f"Unhandled exception copying file from '{src}' to '{dest}'. Details: {exc}"
#                     )
#                     print(f"[ERROR] {msg}")
