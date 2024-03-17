import os


DEBUG = os.getenv("DEBUG", False)
ROOT_PATH = os.getenv("ROOT_PATH", os.getcwd())
RESPONSE_TEMPLATE = "response.txt.j2"
EXIT_CODES = ["quit", "q", "/q", "exit", "bye", "goodbye"]
