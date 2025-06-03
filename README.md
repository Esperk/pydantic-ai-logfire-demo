# Pydantic AI Demo with Instructor and Logfire

This project demonstrates a simple command-line agent built using `instructor` (for Pydantic model integration with LLMs), `logfire` for observability, and `openai` for interacting with an LLM. The project uses `uv` for package management.

## Prerequisites

- Python 3.8+
- `uv` installed (see [UV installation guide](https://github.com/astral-sh/uv#installation))
- An OpenAI API key.
- A Logfire token (optional, but recommended for full observability).

## Setup

1.  **Clone the repository (if you haven't already):**
    ```bash
    # git clone <your-repo-url>
    # cd pydantic-ai-demo
    ```

2.  **Create a virtual environment and install dependencies using UV:**
    ```bash
    uv venv
    uv pip install -e . 
    ```
    This command installs the project in editable mode (`-e .`) along with all dependencies specified in `pyproject.toml`.

3.  **Activate the virtual environment:**
    On macOS/Linux:
    ```bash
    source .venv/bin/activate
    ```
    On Windows:
    ```bash
    .venv\Scripts\activate
    ```

4.  **Configure API Keys:**
    This project uses a `.env` file to manage API keys. 
    Copy the example file:
    ```bash
    cp .env.example .env
    ```
    Then, open the `.env` file and add your actual `OPENAI_API_KEY`. If you're using Logfire for cloud logging, also add your `LOGFIRE_TOKEN`.
    ```dotenv
    # .env
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
    LOGFIRE_TOKEN="YOUR_LOGFIRE_TOKEN_HERE_OR_LEAVE_BLANK_FOR_CONSOLE_LOGGING"
    ```
    **Important:** The `.env` file is included in `.gitignore` and should not be committed to your repository.

## Running the Demo

Once the setup is complete, you can run the CLI application:

```bash
pydantic-agent-demo process-text "Extract user info from: John Doe is 30 years old and lives in New York."
```

This will call the agent, which will attempt to extract user information from the provided text and return it as a Pydantic model. Logfire will capture traces of the execution.

### Example Output (Conceptual)

```
UserInfo(name='John Doe', age=30, city='New York')
```
(The actual output will be the Pydantic model representation)

## Project Structure

-   `pyproject.toml`: Project metadata and dependencies, configured for `uv`.
-   `README.md`: This file.
-   `src/`:
    -   `pydantic_ai_demo/`:
        -   `__init__.py`: Makes `pydantic_ai_demo` a Python package.
        -   `main.py`: Contains the Pydantic model, Logfire setup, OpenAI client, and Typer CLI application.
