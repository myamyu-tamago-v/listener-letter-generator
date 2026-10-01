from typing import Generic, TypeVar, cast, overload

from agents import (
    Agent,
    Runner,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel as Model_
from openai import AsyncOpenAI
from pydantic import BaseModel

from .llm_conf import LLMConf, get_llm_conf

llm_conf: LLMConf = get_llm_conf()

# 初期設定
client = AsyncOpenAI(
    base_url=llm_conf.base_url,
    api_key=llm_conf.api_key,
)
# set_default_openai_client(client=client)
# set_default_openai_api("chat_completions")
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
        self.name = name
        self.instructions = instructions
        self.tools = tools

    def _agent(self):
        client = AsyncOpenAI(
            base_url=llm_conf.base_url,
            api_key=llm_conf.api_key,
        )
        model = Model_(model=llm_conf.model_name, openai_client=client)
        agent = Agent(
            name=self.name,
            instructions=self.instructions,
            tools=self.tools or [],
            output_type=self.schema,
            model=model,
        )
        return agent

    @overload
    async def generate(self, prompt: str) -> T: ...
    @overload
    async def generate(self, prompt: str) -> str: ...

    async def generate(self, prompt: str) -> T | str:
        agent = self._agent()
        res = await Runner.run(
            agent,
            input=prompt,
        )
        content = res.final_output
        if self.schema is None:
            return cast(str, content)
        return cast(T, content)
