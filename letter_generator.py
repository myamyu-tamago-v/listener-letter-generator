from llm import LLMAgentBase
from radio_listener import AiDegree, RadioListener

# AI度合いに応じた味付けの指示
_ai_instructions = {
    AiDegree.HUMAN: "・違和感のない、人間として自然な文章を書いてください。",
    AiDegree.SUBTLE: (
        "・全体的には自然ですが、1つか2つ、よく考えると少しおかしい程度の"
        "ささいな違和感（例：実在しない地名や、少しズレた比喩など）を混ぜてください。"
    ),
    AiDegree.MIXED: (
        "・人間らしさと、AI特有の支離滅裂な違和感が半々くらいに混ざった、"
        "どこか奇妙な文章にしてください。"
    ),
}


class LetterGenerator(LLMAgentBase):
    def __init__(
        self,
        theme: str | None = None,
        theme_description: str | None = None,
    ):
        self.personality_name = "みゃみゅ玉子"
        self.program_name = "殿の寝静まるそのあとに、家来はちょいと語りに入る"
        self.theme = theme or "フリートーク"
        self.theme_description = theme_description or (
            "パーソナリティへの質問、日々の悩み、日常の出来事、共感してほしいこと、"
            "番組の感想など自由に書いてください。"
        )

        instructions = f"""
あなたはラジオ番組『{self.program_name}』のリスナーです。
パーソナリティの「{self.personality_name}」さんにおたよりを書いてください。
与えられた【リスナー情報】を参考に、その人の年齢、職業、性格が伝わるような内容にしてください。

【重要：生成の味付け】
・件名は含まず、本文のみを出力してください。
・「AIっぽい違和感」を出す際は、毎回同じパターン（例：存在しない地名ばかり出す等）にならないよう、比喩、習慣、知識の欠落、文体の急な変化など、バリエーション豊かな違和感を持たせてください。
・文章は短めで、200文字程度にまとめてください。
・与えられた【生成についての指示】にも従ってください。

【今回のテーマ：{self.theme}】
・今回は「{self.theme}」というテーマでおたよりを募集しております。
・{self.theme_description}
"""
        super().__init__(name="ltter_generator", instructions=instructions)

    async def generate_letter(self, listener: RadioListener) -> str:
        """リスナーの情報に基づいてお便りを生成する。"""
        ai_style = _ai_instructions.get(
            int(listener.ai_degree), _ai_instructions[AiDegree.SUBTLE]
        )

        prompt = f"""次の情報をもとにおたよりを書いてください。

【リスナー情報】
ラジオネーム: {listener.nickname}
年齢: {listener.age}
性別: {listener.gender}
職業: {listener.occupation}
性格: {listener.personality}
リスナー歴: {listener.listener_type}
AI度設定: {listener.ai_degree.name}

【生成についての指示】
{ai_style}
"""
        res = await self.generate(prompt)
        return res or ""
