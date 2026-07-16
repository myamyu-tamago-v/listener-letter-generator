import os
from typing import Generic, TypeVar, cast, overload

from agents import (
    Agent,
    Runner,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)
from openai import AsyncOpenAI
from pydantic import BaseModel

_LLAMA_CPP_API_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:18080")
_LLAMA_CPP_API_KEY = os.getenv("LLM_API_KEY", "dummy_api_key")

# 初期設定
client = AsyncOpenAI(
    base_url=_LLAMA_CPP_API_BASE_URL,
    api_key=_LLAMA_CPP_API_KEY,
)
set_default_openai_client(client=client)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)

T = TypeVar("T", bound=BaseModel)


class LLMAgentBase(Generic[T]):
    def __init__(
        self,
        name: str,
        instructions: str,
        schema: type[T] | None = None,
        tools: list | None = None,
    ) -> None:
        self.schema = schema
        self.agent = Agent(
            name=name,
            instructions=instructions,
            tools=tools or [],
            output_type=self.schema,
        )

    @overload
    async def generate(self, prompt: str) -> T: ...
    @overload
    async def generate(self, prompt: str) -> str: ...

    async def generate(self, prompt: str) -> T | str:
        res = await Runner.run(
            self.agent,
            input=prompt,
        )
        content = res.final_output
        if self.schema is None:
            return cast(str, content)
        return cast(T, content)
