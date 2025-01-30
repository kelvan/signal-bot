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

5. **Create config file**

    ```sh
    cp config.yml.example config.yml
    ```

    Edit `config.yml` to configure your bot settings, such as personalities, Signal service details, and Ollama configuration.

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
