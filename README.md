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

### Searching for People with `search_fourdigits_people.py`

The `search_fourdigits_people.py` script showcases a more advanced agent capability: using web browsing to gather information. This script attempts to find employees working at "fourdigits.nl" and extract their names and job titles.

**Key Features:**

-   **`pydantic-ai` Agent:** Leverages the `Agent` class from `pydantic-ai`.
-   **Web Search:** Integrates the `tavily_search_tool` for initial web searches.
-   **Browser Automation:** Utilizes a Playwright MCP (Media Control Protocol) server (`@playwright/mcp@latest`) which allows the agent to directly interact with web pages to enrich information. The agent is instructed to "Use the browser to enrich the information."
-   **Structured Output:** Aims to output a list of `Employee` objects, each containing a `name` and `job_title`.
-   **Local Observability:** Configured with Logfire for local tracing (`send_to_logfire=False`).

**Prerequisites:**

-   Besides the general project setup, ensure you have a Tavily API key. Add it to your `.env` file:
    ```dotenv
    TAVILY_API_KEY="YOUR_TAVILY_API_KEY_HERE"
    ```
    The script will assert that this key is present.

**Running the Script:**

Navigate to the project root and run:

```bash
python src/pydantic_ai_demo/search_fourdigits_people.py
```

**Expected Output:**

The script will print a list of dictionaries, where each dictionary represents an employee with their name and job title. For example:

```
{'name': 'Jane Doe', 'job_title': 'Software Engineer'}
{'name': 'John Smith', 'job_title': 'Project Manager'}
...
```
(The actual output will depend on the information found by the agent.)


## Project Structure

-   `pyproject.toml`: Project metadata and dependencies, configured for `uv`.
-   `README.md`: This file.
-   `src/`:
    -   `pydantic_ai_demo/`:
        -   `__init__.py`: Makes `pydantic_ai_demo` a Python package.
        -   `main.py`: Contains the Pydantic model, Logfire setup, OpenAI client, and Typer CLI application.
