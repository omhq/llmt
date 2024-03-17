import os
import json
import time
import jinja2

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.consts import ROOT_PATH, RESPONSE_TEMPLATE


class EventHandler(FileSystemEventHandler):
    """Event handler for the input file system events."""

    def __init__(self):
        super().__init__()

        self.contents = ""
        self.event_queue = []

    def read_file(self, file_path: str) -> str:
        with open(file_path, "r") as file:
            return file.read()

    def on_modified(self, event):
        if not event.is_directory:
            content_updates = self.read_file(event.src_path).strip()

            if content_updates != self.contents:
                self.contents = content_updates

                if self.contents != "":
                    self.event_queue.append(content_updates)

    def events_generator(self):
        while True:
            if self.event_queue:
                yield self.event_queue.pop(0)
            else:
                time.sleep(0.1)


class FileHandler:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = os.path.join(ROOT_PATH, "files", input_file)
        self.output_file = os.path.join(ROOT_PATH, "files", output_file)

        self.init()

        self.event_handler = EventHandler()
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.input_file, recursive=False)
        self.observer.start()
        self.env = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            loader=jinja2.FileSystemLoader(searchpath=os.path.join(ROOT_PATH, "src"))
        )

    def init(self):
        if not os.path.exists(self.input_file):
            with open(self.input_file, "w") as f:
                f.write("")

        if not os.path.exists(self.output_file):
            with open(self.output_file, "w") as f:
                f.write("")

    def write_to_output(self, data):
        template = self.env.get_template(RESPONSE_TEMPLATE)
        with open(self.output_file, "w") as f:
            f.write(template.render(**data))

    def events_generator(self):
        for event in self.event_handler.events_generator():
            yield event

        self.observer.join()

    def __del__(self):
        self.observer.stop()


class ChatManager:
    def __init__(self, path):
        self.path = f"{path}/chats"

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def init_chat(self, chat_name):
        self.chat_name = chat_name
        self.file_path = os.path.join(self.path, f"{self.chat_name}.json")

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def save_to_chat(self, message):
        chat_list = []

        with open(self.file_path) as f:
            chat_list = json.load(f)

        chat_list.append(message)

        with open(self.file_path, "w") as f:
            json.dump(chat_list, f, indent=4)

    def list_chats(self):
        return [x.split(".")[0] for x in os.listdir(self.path) if x.endswith(".json")]

    def list_messages(self):
        with open(os.path.join(self.path, f"{self.chat_name}.json")) as f:
            return len(json.load(f))
