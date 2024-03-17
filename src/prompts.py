import inquirer

from typing import List
from halo import Halo
from openai.types import CompletionChoice, CompletionUsage
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessage,
    ChatCompletionMessageToolCall,
)

from src.assistants import OpenAIAssistant
from src.consts import EXIT_CODES


class Style:
    GREEN = "\033[32m"
    RESET = "\033[0m"
    YELLOW = "\033[33m"


def prompt_create_chat():
    """Prompt the user to create a new chat thread.

    Returns:
        str: Chat name.
    """
    questions = [inquirer.Text("chat_name", message="Enter a chat name")]
    answers = inquirer.prompt(questions)
    return answers["chat_name"]


def prompt_init(assistants, chats):
    """Prompt the user to select an assistant and chats.

    Args:
        assistants (list): The list of assistants.
        chats (list): The list of chats.

    Returns:
        dict: The user's selections.
    """
    questions = [
        inquirer.List(
            "assistant",
            message="Select an assistant to use",
            choices=[x["name"] for x in assistants],
        ),
        inquirer.List(
            "chat_name",
            message="Select an existing chat",
            choices=chats,
        ),
    ]

    return inquirer.prompt(questions)


def converse(chat_manager, file_handler, assistant: OpenAIAssistant, functions):
    """Chat with the assistant.

    Args:
        chat_manager (ChatManager): The chat manager.
        file_handler (InputFileHandler or None): The input file handler object or None.
        assistant (OpenAIAssistant): The assistant.

    Returns:
        None
    """
    response = ""
    capture_user_input = True
    messages = [{"role": "system", "content": assistant.description}]
    spinner = Halo(text="Working...", spinner="dots")
    input_text = ""
    function_calls = []

    while True:
        if capture_user_input:
            if file_handler:
                print(
                    f"{Style.GREEN}You{Style.RESET}: using {file_handler.input_file} to ask questions."
                )

                for event in file_handler.events_generator():
                    input_text = event
                    break
            else:
                input_text = input(f"{Style.GREEN}You{Style.RESET}: ").strip()

            message = {"role": "user", "content": input_text}
            messages.append(message)
            chat_manager.save_to_chat(message)

        if input_text.lower() in EXIT_CODES:
            break

        spinner.start()

        chat_completion: ChatCompletion = assistant.generate_response(messages)
        chat_completion_choice: CompletionChoice = chat_completion.choices[0]
        chat_completion_message: ChatCompletionMessage = chat_completion_choice.message
        usage: CompletionUsage = chat_completion.usage
        response: str = chat_completion_message.content

        if chat_completion_choice.finish_reason == "tool_calls":
            capture_user_input = False
            tool_calls: List[ChatCompletionMessageToolCall] = (
                chat_completion_message.tool_calls
            )
            message = {"role": "assistant", "tool_calls": tool_calls}

            messages.append(message)

            for tool_call in tool_calls:
                fn_name = tool_call.function.name
                arguments = tool_call.function.arguments
                function = getattr(functions, fn_name)
                result = function(arguments)
                message = {
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool_call.id,
                    "name": fn_name,
                }
                template_message = {
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool_call.id,
                    "name": fn_name,
                    "arguments": arguments,
                }

                messages.append(message)
                chat_manager.save_to_chat(message)
                function_calls.append(template_message)

            continue

        if chat_completion_choice.finish_reason == "stop":
            capture_user_input = True

        spinner.stop()

        info = ", ".join(
            [
                f"completion tokens: {usage.completion_tokens}",
                f"prompt tokens: {usage.prompt_tokens}",
                f"total tokens: {usage.total_tokens}",
            ]
        )

        message = {"role": "assistant", "content": response}
        messages.append(message)
        chat_manager.save_to_chat(message)

        if file_handler:
            file_handler.write_to_output(
                {
                    "assistant": assistant,
                    "response": response,
                    "function_calls": function_calls,
                    "info": info,
                }
            )
        
        function_calls = []

        if not file_handler:
            yield f"{Style.GREEN}{assistant.name}{Style.RESET}: {response}\n\n{Style.YELLOW}usage{Style.RESET}: {info}"
