import logging
import os
from datetime import datetime

_logger = None

def get_logger() -> logging.Logger:
    global _logger
    if _logger is None:
        _logger = setup_logging()
    return _logger

def setup_logging() -> logging.Logger:
    logger = logging.getLogger("tmdb_mcp")
    logger.setLevel(logging.INFO)
    date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    #Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(console_handler)
    #File handler
    file_handler = logging.FileHandler(f"logs/tmdb-logs-{date_time}.log")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.info(f"Logging setup completed with console and file handlers")
    return logger

def setup_api_key_config() -> str:
    logger = get_logger()
    tmdb_api_key = os.getenv("TMDB_API_KEY", "")
    if not tmdb_api_key:
        logger.error(f"TMDB_API_KEY is not set, please set the TMDB_API_KEY environment variable")
        raise ValueError("TMDB_API_KEY is not set, please set the TMDB_API_KEY environment variable")
    
    omdb_api_key = os.getenv("OMDB_API_KEY", "")
    if not omdb_api_key:
        logger.error(f"OMDB_API_KEY is not set, please set the OMDB_API_KEY environment variable")
        raise ValueError("OMDB_API_KEY is not set, please set the OMDB_API_KEY environment variable")

    logger.info(f"API key config loaded successfully")
    return tmdb_api_key, omdb_api_key