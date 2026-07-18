import requests

from config import config, personality

OLLAMA_URL = config["ollama"]["url"]
MODEL = config["ollama"]["model"]
CONNECT_TIMEOUT = config["ollama"]["connect_timeout"]
READ_TIMEOUT = config["ollama"]["read_timeout"]


def ask(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {
               "role": "system",
               "content": personality
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
    )

    response.raise_for_status()

    data = response.json()
    return data["message"]["content"]


if __name__ == "__main__":
    while True:
        prompt = input("> ")

        if prompt == "/bye":
            break

        print()
        print(ask(prompt))
        print()
