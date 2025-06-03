import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv
import logfire
from pydantic_ai import Agent

# We expect OPENAI_API_KEY to be set in your .env file
load_dotenv()
logfire.configure(send_to_logfire=True)
logfire.instrument_pydantic_ai()
logfire.instrument_httpx(capture_all=True)

agent = Agent(model='gpt-3.5-turbo')


@agent.tool_plain()
def get_today() -> str:
    """Get the current date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


async def main():
    result = await agent.run("What is the current date?", output_type=str)

    if result.output is not None:
        print(f"The agent responded that the current date is: {result.output}")
    else:
        print("Error: Agent did not produce a valid output or an error occurred.")
        print(f"Raw output from LLM: {result.raw_output}")


if __name__ == "__main__":
    asyncio.run(main())
