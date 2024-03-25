from typing import List

from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessage


from llmt.utils import logger


class OpenAIAssistant:
    def __init__(
        self,
        api_key: str,
        model: str,
        assistant_name: str,
        assistant_description: str,
        tools: List[dict] = None,
    ) -> None:
        """Initialize the assistant.

        Args:
            api_key (str): The OpenAI API key.
            model (str): The model to use.
            assistant_name (str): The name of the assistant.
            assistant_description (str): The description of the assistant.
            tools (list): The list of tools.
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.assistant_name = assistant_name
        self.assistant_description = assistant_description
        self.tools = tools

    def chat_completions_create(
        self, messages: List[ChatCompletionMessage]
    ) -> ChatCompletion:
        """Create a chat completion.

        Args:
            messages (list): List of ChatCompletionMessage objects.

        Returns:
            ChatCompletion: The chat completion.
        """
        return self.client.chat.completions.create(
            messages=messages, model=self.model, tools=self.tools
        )

    def generate_response(
        self, messages: List[ChatCompletionMessage]
    ) -> ChatCompletion:
        """Generate a response from the assistant.

        Args:
            messages (list): List of ChatCompletionMessage objects.

        Returns:
            ChatCompletion: The chat completion.

        """
        logger.debug(f"Request: {messages}")
        return self.chat_completions_create(messages)

    @property
    def name(self):
        return self.assistant_name

    @property
    def description(self):
        return self.assistant_description
