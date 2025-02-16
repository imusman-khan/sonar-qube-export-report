import logging


def setup_logger():
    """
    Sets up and configures a logger for the SonarQube report generation.

    This function initializes a logger named 'sonar_qube_report' with the DEBUG level. It adds a file handler to the logger
    that writes log messages to 'sonar_qube_report.log'. The log messages include the timestamp, logger name, log level,
    and the message itself.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("sonar_qube_report")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler("sonar_qube_report.log")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = setup_logger()
