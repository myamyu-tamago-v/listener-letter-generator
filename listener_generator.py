from llm import LLMAgentBase
from radio_listener import RadioListener


class ListenerGenerator(LLMAgentBase[RadioListener]):
    def __init__(self) -> None:
        instructions = """
ラジオ番組のリスナー情報を1人分、ランダムに生成してください。
"""
        super().__init__(
            name="listener_generator",
            instructions=instructions,
            schema=RadioListener,
        )

    async def generate_listener(self, ai_degree: int | None = None) -> RadioListener:
        ai_degree_instruction = ""
        if ai_degree is not None:
            ai_degree_instruction = (
                f"今回は ai_degree を必ず {ai_degree} に設定してください。"
            )

        prompt = f"""リスナー情報を生成してください。
{ai_degree_instruction}
"""
        res = await self.generate(prompt)
        return res
