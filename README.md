# Thinker

LLM chat helper with function calling.

This project runs on prem. Use it in data pipelines, as part of CI/CD, or for your own chats. Write custom functions for the LLM to call. The on-prem system calls functions on behalf of the LLM. Currently using OpenAI.

### Getting started

Docker and make needs to be installed.

- Create custom functions in the udf/ directory and import them in cli.py. A sample function file is already being imported.
- Update or create a new configuration file in configs/.
- Make sure the configuration file describes your custom functions in `assistants.tools`.
- `make run`
- Use files/input.md to send messages.
- Use files/output.md to receive messages.
- CTRL + C to quit out of the container and clean up orphans.

### Configuration file

If both (input_file, output_file) are ommited, then the default terminal will be used.
Using the input and output files to converse with an LLM is easier than using the terminal.

- **input_file**: specify a file for user input
- **output_file**: specify a file for LLM response
- **assistants**:
    - **type**: Assistant type, currently only OpenAI.
    - **assistant_name**: Assistant name.
    - **assistant_description**: Assistant description which OpenAI will use for assistant context.
    - **api_key**: OpenAI API key.
    - **model**: OpenAI model.
    - **tools**: Function definitions. For now, in addition to creating functions, functions must be also defined in a format which OpenAI API can understand. Functions take one object argument which must be unpacked to extract arguments within each function. Hopefully this changes in the future.

The image used for running this code has some common tools installed which I use daily in my custom functions:

- awscli
- cloudquery
- numpy
- pandas
- psycopg2-binary
- SQLAlchemy

Build and use your own image with additional tools for whatever your functions need.

## Need help?

I help organizations build data pipelines with AI integrations. If your organization needs help building or exploring solutions, feel free to reach me at artem at outermeasure.com. The general workflow is:

1. **Fine tune** a curated model with proprietary data to perform tasks specific to your pipeline.
2. **Deploy** the model in your cloud environment.
3. **Connect your pipeline** to the deployment via an API.
4. **Iterate and improve** the model.
