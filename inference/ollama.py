from ollama import chat
from config.loader import load_config

config = load_config("config/config.yaml")

def get_llm_response(input_text: str) -> str | None:

    response = chat(
        model=config["model"],
        think=False,
        messages=[{'role': 'user', 'content': f"""Continue the following text with the next word or short phrase only.
Do not explain. Do not repeat what is already written. Just continue naturally.

Text so far:
{input_text}

Continuation:
"""}],
    )

    return response.message.content
