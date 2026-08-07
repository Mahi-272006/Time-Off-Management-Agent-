from dotenv import load_dotenv
from pathlib import Path
import os

from langchain_anthropic import ChatAnthropic

ENV_PATH = Path(__file__).resolve().parent / ".env"
print("Loading .env from:", ENV_PATH)

load_dotenv(dotenv_path=ENV_PATH)

print("MODEL =", os.getenv("MODEL"))  # Temporary debug line

llm = ChatAnthropic(
    model=os.getenv("MODEL"),
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url=os.getenv("ANTHROPIC_BASE_URL"),
    temperature=0,
)