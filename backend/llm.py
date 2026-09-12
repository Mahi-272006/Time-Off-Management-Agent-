from dotenv import load_dotenv
from pathlib import Path
import os
import warnings

from langchain_google_genai import ChatGoogleGenerativeAI

ENV_PATH = Path(__file__).resolve().parent / ".env"
print("Loading .env from:", ENV_PATH)

load_dotenv(dotenv_path=ENV_PATH)

print("MODEL =", os.getenv("MODEL"))  # Temporary debug line

_api_key = os.getenv("GOOGLE_API_KEY")

if not _api_key:
    warnings.warn(
        "GOOGLE_API_KEY is not set. LLM calls will fail at runtime until a valid key is configured."
    )
    _api_key = "placeholder-key"

llm = ChatGoogleGenerativeAI(
    model=os.getenv("MODEL"),
    api_key=_api_key,
    temperature=0,
)