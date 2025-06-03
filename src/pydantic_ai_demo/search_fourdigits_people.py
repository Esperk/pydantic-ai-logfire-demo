import asyncio
from typing import Annotated
from pydantic import Field
from typing_extensions import TypedDict
from pydantic_ai.mcp import MCPServerStdio
import os
from dotenv import load_dotenv
import logfire
from pydantic_ai import Agent
from pydantic_ai.common_tools.tavily import tavily_search_tool

load_dotenv()  # Load environment variables from .env file

logfire.configure(send_to_logfire=True)
logfire.instrument_pydantic_ai()
logfire.instrument_httpx(capture_all=True)


mcp_server = MCPServerStdio(command="npx", args=["-y", "@playwright/mcp@latest"])


class Employee(TypedDict):
    name: str
    job_title: str


tavily_api_key = os.getenv("TAVILY_API_KEY")
assert tavily_api_key, "TAVILY_API_KEY is not set"


agent = Agent(
    'gpt-3.5-turbo',
    tools=[tavily_search_tool(api_key=tavily_api_key)],
    mcp_servers=[mcp_server],
    instructions="Use the browser to enrich the information.",
)


async def main():
    async with agent.run_mcp_servers():
        result = await agent.run("Find me all the people that work at fourdigits.nl.", output_type=list[Employee])
        for employee in result.output:
            print(str(employee))


asyncio.run(main())
