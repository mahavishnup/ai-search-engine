"""Logging configuration for the application."""

import logging
import logging.handlers
import sys
from pathlib import Path

# Create logs directory at project root if it doesn't exist
LOGS_DIR = Path("src/storage/logs")
LOGS_DIR.mkdir(exist_ok=True)


class StdoutWrapper:
    """Wrapper to redirect stdout to logging."""

    def __init__(self, logger: logging.Logger, level: int = logging.INFO):
        self.logger = logger
        self.level = level

    def write(self, message: str) -> None:
        if message.strip():
            self.logger.log(self.level, message)

    def flush(self) -> None:
        pass


class StderrWrapper:
    """Wrapper to redirect stderr to logging."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def write(self, message: str) -> None:
        if message.strip():
            self.logger.error(message)

    def flush(self) -> None:
        pass


def setup_logging(log_level: str = "INFO") -> None:
    """Configure robust, daily timed rotating file and stream logging.

    Args:
        log_level: Console logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    root_logger = logging.getLogger()
    # If root logger is already configured with handlers, skip re-configuration
    if root_logger.handlers:
        return

    # Convert string to logging level
    level = getattr(logging, log_level.upper(), logging.INFO)

    # Detailed formatter for production auditing
    detailed_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console stream handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(detailed_formatter)

    # Rotating file handler (rotates daily at midnight, stores 30 days backup)
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=LOGS_DIR / "app.log",
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)  # Always capture full DEBUG logs in file
    file_handler.setFormatter(detailed_formatter)
    file_handler.suffix = "%Y-%m-%d.log"

    # Set root logger level and wire handlers
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Reduce noise from standard libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine.Engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("python_multipart").setLevel(logging.WARNING)

    # Redirect stdout/stderr to capture all unhandled outputs
    sys.stdout = StdoutWrapper(logging.getLogger("stdout"), logging.INFO)
    sys.stderr = StderrWrapper(logging.getLogger("stderr"))

    logging.info(
        f"Logging system initialized - Level: {log_level}, File: {LOGS_DIR / 'app.log'}"
    )


def setup_logger(name: str = "backend") -> logging.Logger:
    """Get or configure a logger instance by name.

    Args:
        name: Logger module/component name.

    Returns:
        logging.Logger: The configured Logger instance.
    """
    setup_logging()
    return logging.getLogger(name)
