import instructor
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
import typer
from openai import OpenAI
from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    name: str = Field(..., description="The name of the user.")
    age: int = Field(..., description="The age of the user.")
    city: str = Field(..., description="The city where the user lives.")
    reasoning: str = Field(..., description="The reasoning per field behind the extracted information.")

client = instructor.patch(OpenAI())

app = typer.Typer()

@app.command()
def process_text(text):
    """
    Processes the input text to extract user information and returns it as a UserInfo object.
    """
    user_info: UserInfo = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=UserInfo,
        messages=[
            {
                "role": "user",
                "content": f"Extract user information from the following text: {text}. Also, provide a brief reasoning for how you determined each piece of information.",
            }
        ],
    )
    print(user_info)


if __name__ == "__main__":
    app()
