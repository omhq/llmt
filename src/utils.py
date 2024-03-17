import logging
import yaml
import pprint

from src.consts import DEBUG


pp = pprint.PrettyPrinter(indent=4)
default_log_args = {
    "level": (logging.DEBUG if DEBUG else logging.WARN),
    "format": "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    "datefmt": "%d-%b-%y %H:%M",
    "force": True,
}

if logging.getLogger().hasHandlers():
    logging.getLogger().setLevel(default_log_args["level"])
else:
    logging.basicConfig(**default_log_args)

logger = logging.getLogger()


def load_config(config_file):
    """Load the configuration file.

    Args:
        config_file (str): The path to the configuration file.

    Returns:
        dict: The configuration file as a dictionary.
    """
    objects = {}

    with open(config_file, "r") as file:
        objects = yaml.safe_load(file)

    return objects
