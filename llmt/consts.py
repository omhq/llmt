import os


DEBUG = os.getenv("DEBUG", False)
RESPONSE_TEMPLATE = "response.txt.j2"
EXIT_CODES = ["quit", "q", "/q", "exit", "bye", "goodbye"]
