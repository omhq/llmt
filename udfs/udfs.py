import json
import time
import logging
from functools import wraps


default_log_args = {
    "level": logging.INFO,
    "format": "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    "datefmt": "%d-%b-%y %H:%M",
    "force": True,
}


logging.basicConfig(**default_log_args)
logger = logging.getLogger()


def timer(func):
    """Decorator for timing functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} completed in {end_time - start_time} seconds")
        return result
    return wrapper


@timer
def add_decimal_values(arguments):
    args = json.loads(arguments)
    value1 = args["value1"]
    value2 = args["value2"]
    return value1 + value2


@timer
def add_hexadecimal_values(arguments):
    args = json.loads(arguments)
    value1 = args["value1"]
    value2 = args["value2"]
    decimal1 = int(value1, 16)
    decimal2 = int(value2, 16)
    return hex(decimal1 + decimal2)[2:]

# load data into snowflake using cloudquery

# describe snowflake table by database + schema

# execute SELECT query