from dotenv import load_dotenv
import os

from langchain_anthropic import ChatAnthropic

load_dotenv()

print("MODEL =", os.getenv("MODEL"))  # Temporary debug line

llm = ChatAnthropic(
    model=os.getenv("MODEL"),
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url=os.getenv("ANTHROPIC_BASE_URL"),
    temperature=0,
)