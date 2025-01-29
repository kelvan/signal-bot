# Quickstart Guide

## Prerequisites

- Python 3.12 or higher
- `signal-cli-rest-api`
- `ollama`

## Setup

1. **Clone the Repository**

    ```sh
    git clone https://gitlab.com/intheflow/signal-bot.git
    cd signal-bot
    ```

3. **Set Up `signal-cli-rest-api`**

    Follow the instructions in the [signal-cli-rest-api repository](https://github.com/bbernhard/signal-cli-rest-api) to set up the API.

4. **Set Up `ollama`**

    Follow the instructions in the [ollama repository](https://github.com/ollama/ollama) to set up the service.

5. **Configure the `.env` File**

    Create a `.env` file in the root directory of the project and add the necessary configuration variables.

    ```env
    SIGNAL_NUMBER=<your phone number>
    # optional
    OLLAMA_MODEL=<defaults to llama3.2>
    SIGNAL_SERVICE=<defaults to localhost:8080>
    OLLAMA_HOST=<defaults to 127.0.0.1:11434>
    OLLAMA_CONTEXT=<some custom instruction on how the bot should behave>
    BOT_WAKE_WORD=<some wake words the bot should listen to>
    ```

## Running the Bot

1. **Quick Test**

    To run a quick test:

    ```sh
    uv run python -m signal_bot.chat
    ```

2. **Run the Signal Bot**

    To run the Signal bot:

    ```sh
    uv run python -m signal_bot.bot
    ```
