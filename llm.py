import json

from litellm import completion

_LLAMA_CPP_API_BASE_URL = "http://localhost:18080"
_LLAMA_CPP_API_KEY = "dummy_api_key"


def _generate(messages: list[dict], opts: dict = {}) -> str:
    response = completion(
        model="openai/local-model",
        messages=messages,
        api_base=_LLAMA_CPP_API_BASE_URL,
        api_key=_LLAMA_CPP_API_KEY,
        **opts,
    )

    return response.choices[0].message.content


def generate_text(messages: list[dict]) -> str:
    return _generate(messages=messages)


def generate_json(messages: list[dict]) -> dict:
    res = _generate(
        messages=messages,
        opts={"response_format": {"type": "json_object"}},
    )
    return json.loads(res)
