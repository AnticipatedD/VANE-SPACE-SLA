#!/usr/bin/env python3
"""
VANE-SPACE-SLA - Centralized Logging Configuration
Author: MD ABUL HOSSAIN
Description: Single source of truth for structured logging across all modules
"""

import logging
import sys
from typing import Optional


def configure_logging(
    name: str = "vane_space",
    level: int = logging.INFO,
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    Configure and return a structured logger instance.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (default: INFO)
        log_format: Custom log format string
    
    Returns:
        Configured logger instance
    """
    if log_format is None:
        log_format = "%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s"
    
    formatter = logging.Formatter(
        log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers = []
    
    # Stream handler (console output)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    return logger


# Root logger for VANE-SPACE-SLA
root_logger = configure_logging("vane_space", logging.INFO)
