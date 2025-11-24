from logging import config
from pathlib import Path

LEVEL = "INFO"

LOGGING_FORMATTERS = {
    "color": {
        "()": "colorlog.ColoredFormatter",
        "format": (
            "%(log_color)s%(levelname)-8s%(reset)s "
            "%(asctime)s "
            "%(blue)s[%(name)s]%(reset)s "
            "%(message_log_color)s%(message)s%(reset)s"
        ),
        "datefmt": "%Y-%m-%d %H:%M:%S",
        "log_colors": {
            "DEBUG": "green",
            "INFO": "cyan",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
        "secondary_log_colors": {
            "message": {
                "DEBUG": "green",
                "INFO": "cyan",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            }
        },
    },
}

LOGGER_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": LOGGING_FORMATTERS,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "color",
            "level": f"{LEVEL}",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "color",
            "level": f"{LEVEL}",
            "filename": "<REPLACE_WITH_ACTUAL_FILE_NAME>",
        },
    },
    "loggers": {
        "": {"handlers": ["console", "file"], "level": f"{LEVEL}"},
        "uvicorn.error": {"level": f"{LEVEL}", "propagate": True},
        "uvicorn.access": {
            "handlers": ["console"],
            "level": f"{LEVEL}",
            "propagate": False,
        },
    },
}


def setup_logging(log_file_name: str, log_path: Path) -> None:
    log_path.mkdir(parents=True, exist_ok=True)
    LOGGER_CONFIG["handlers"]["file"]["filename"] = str(
        (log_path / log_file_name).with_suffix(".log")
    )
    config.dictConfig(LOGGER_CONFIG)
