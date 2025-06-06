import instructor
import logfire
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
import typer
from openai import OpenAI
from pydantic import BaseModel, Field


logfire.configure(send_to_logfire=True)
logfire.instrument_pydantic()
logfire.instrument_openai(OpenAI)
logfire.instrument_httpx(capture_all=True)

class UserInfo(BaseModel):
    name: str = Field(..., description="The name of the user.")
    age: int = Field(..., description="The age of the user.")
    city: str = Field(..., description="The city where the user lives.")
    reasoning: str = Field(..., description="The reasoning per field behind the extracted information.")

    def __str__(self):
        return f"UserInfo(name='{self.name}', age={self.age}, city='{self.city}', reasoning='{self.reasoning}')"

client = instructor.patch(OpenAI())

app = typer.Typer(
    help="A simple CLI agent to extract user information using Instructor and Logfire."
)

@app.command()
@logfire.instrument("process_text_command", extract_args=True)
def process_text(text: str = typer.Argument(..., help="The text to process for user information.")):
    """
    Processes the input text to extract user information and returns it as a UserInfo object.
    """
    logfire.info(f"Received text for processing: {text}")
    try:
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
        logfire.info(f"Successfully extracted user info: {user_info}")
    except Exception as e:
        logfire.error(f"Error processing text: {e}")
        print(f"Error: Could not process text. {e}")

if __name__ == "__main__":
    app()
