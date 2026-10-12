# LLM Signal Bot

A chatbot for the Signal messenger. It answers messages with local LLMs served by [Ollama](https://github.com/ollama/ollama) and talks to Signal through `signal-cli-rest-api`. Each personality has its own trigger phrase, model and instructions. Send `hey bot` to get a help page.

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

## Running with Docker / Podman Compose

`compose.yml` starts `signal-cli-rest-api` and builds the bot from the `Containerfile`. Use `podman compose` instead of `docker compose` for Podman.

1. **Create the config file**

    ```sh
    cp config.yml.example config.yml
    ```

    Set the Signal service to the compose service name and add your ICD API credentials:

    ```yaml
    signal:
      number: "+<your phone number>"
      service: "signal-cli-rest-api:8080"

    icd:
      client_id: "<WHO ICD API client id>"
      client_secret: "<WHO ICD API client secret>"
    ```

2. **Start `signal-cli-rest-api`**

    ```sh
    docker compose up -d signal-cli-rest-api
    ```

    The REST API is published on `http://localhost:18080`. Signal state is stored in `./signal-cli-config`.

3. **Link your Signal account**

    Open `http://localhost:18080/v1/qrcodelink?device_name=signal-bot` in a browser. In the Signal app, go to *Settings → Linked devices* and scan the QR code.

4. **Set the Ollama host**

    The bot reads `OLLAMA_HOST`, which overrides `ollama.host` from `config.yml`. The default in `compose.yml` is `10.0.2.236:11434`.

    ```sh
    export OLLAMA_HOST=<ollama host>:11434
    ```

5. **Build and start the bot**

    ```sh
    docker compose up -d --build
    docker compose logs -f bot
    ```

    `config.yml` is mounted read-only. After editing it, restart the bot:

    ```sh
    docker compose restart bot
    ```

6. **Try it**

    Send `hey bot` to the linked number to get the help page.
