# Utility functions (e.g., logging setup)
import logging

# Function to set up a logger
def setup_logger(log_file):
    """
    Sets up a logger to log messages to a file.

    Args:
        log_file (str): Path to the log file.

    Returns:
        Logger: Configured logger instance.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
    )
    return logging.getLogger()
