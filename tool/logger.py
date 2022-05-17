import logging

import coloredlogs


def setup_logging(log_level=logging.DEBUG):
    """Setup root logger and quiet some levels."""
    logger = logging.getLogger()

    # Set log format to display the logger name to hunt down verbose logging modules
    fmt = "%(name)-25s %(levelname)-8s %(message)s"

    # Use colored logging output for console with the coloredlogs package
    # https://pypi.org/project/coloredlogs/
    coloredlogs.install(level=log_level, fmt=fmt, logger=logger)

    # Disable logging of JSON-RPC requests and replies
    logging.getLogger("web3.RequestManager").setLevel(logging.WARNING)
    logging.getLogger("web3.providers.HTTPProvider").setLevel(logging.WARNING)
    # logging.getLogger("web3.RequestManager").propagate = False

    # Disable all internal debug logging of requests and urllib3
    # E.g. HTTP traffic
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    return logger
