"""
Lists all Gemini models available to your API key, and flags which ones
support generateContent (needed for chat + tool calling).

Usage:
    pip install google-generativeai --break-system-packages
    export GOOGLE_API_KEY="your-key-here"
    python list_gemini_models.py
"""

import os
import google.generativeai as genai

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise SystemExit("Set GOOGLE_API_KEY in your environment first.")

genai.configure(api_key=api_key)

print(f"{'Model name':45} {'Supports generateContent':28} Input tokens / Output tokens")
print("-" * 100)

for m in genai.list_models():
    supports_chat = "generateContent" in m.supported_generation_methods
    marker = "YES" if supports_chat else "no"
    print(f"{m.name:45} {marker:28} {m.input_token_limit} / {m.output_token_limit}")