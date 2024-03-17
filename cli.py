import argparse

from src.managers import ChatManager, FileHandler
from src.utils import load_config
from src.consts import ROOT_PATH
from src.assistants import OpenAIAssistant
from src.prompts import (
    prompt_create_chat,
    prompt_init,
    converse,
)

# import all custom functions here
import udfs.udfs as functions


def parse_args() -> argparse.Namespace:
    """Parse the command line arguments.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="Data Assistant")
    parser.add_argument(
        "-f" "--config-file",
        type=str,
        dest="config_file",
        required=True,
        help="The path to the configuration file.",
    )
    parser.add_argument(
        "--create-chat",
        action="store_true",
        dest="create_chat",
        help="Create chat.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args: argparse.Namespace = parse_args()
    config_file = args.config_file
    configs = load_config(config_file)
    chat_manager = ChatManager(ROOT_PATH)
    file_handler = None

    create_chat = args.create_chat
    chats = [x for x in chat_manager.list_chats()]

    if create_chat:
        chat_name = prompt_create_chat()
        chat_manager.init_chat(chat_name)
        exit(0)

    if len(chats) == 0:
        chat_name = prompt_create_chat()
        chat_manager.init_chat(chat_name)
        chats = [x for x in chat_manager.list_chats()]

    init_answers = prompt_init(configs["assistants"], chats)

    selected_assistant = next(
        (x for x in configs["assistants"] if x["name"] == init_answers["assistant"]),
        None,
    )

    openai_key = selected_assistant["api_key"]
    tools = selected_assistant.get("tools", [])

    assistant = OpenAIAssistant(
        openai_key,
        selected_assistant["model"],
        selected_assistant["assistant_name"],
        selected_assistant["assistant_description"],
        tools,
    )

    selected_chat = init_answers["chat_name"]

    chat_manager.init_chat(selected_chat)

    if chat_manager.list_messages() == 0:
        chat_manager.save_to_chat(
            {"role": "system", "content": selected_assistant["assistant_description"]}
        )

    if configs["input_file"] and configs["output_file"]:
        file_handler = FileHandler(configs["input_file"], configs["output_file"])

    for response in converse(chat_manager, file_handler, assistant, functions):
        print(f"\n{response}\n")
