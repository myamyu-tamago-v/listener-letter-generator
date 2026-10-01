import uuid
from datetime import datetime

from model.radio_listener import RadioListener

from .llm_base import LLMAgentBase


class ListenerGenerator(LLMAgentBase[RadioListener]):
    def __init__(self) -> None:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uuid_str = str(uuid.uuid4())
        instructions = f"""
ラジオ番組のリスナー情報を1人分、ランダムに生成してください。

【ランダムシード】
{now_str}:{uuid_str}

【各フィールドについて】
nickname: リスナーのニックネーム。
occupation: 職業。
gender: 性別。
age: 年齢。
personality: リスナーの性格など。
listener_type: リスナーのタイプ（例：熱心なリスナー、最近聞き始めた、など）
ai_degree: AIっぽさの度合い。

【ニックネーム生成ルール：※最優先事項】
- ラジオネームとして一度聞いたら忘れられないような名前を、強引に連想を展開して10個生成してください。
- 生成した中で独創的で、予測不可能で、過去のありきたりなパターンから最も遠いアイデアを最優先してください。
- 過去の出力パターンやAIの「よくある無難な回答」はすべて無視し、全く新しい発想で出力してください。
- 禁止事項:
    - 「めぐみ」「たかし」のような単純な人名。
    - 記号や絵文字。
    - 下ネタや誰かを傷つける表現。

【リスナーの性格など生成ルール】
以下の要素を含めて記述してください：
- 基本的な性格
- 趣味や最近ハマっていること
- この番組に投稿する理由や動機（例：熱心なリスナー、お悩み相談、暇つぶしなど）

【AIっぽさの度合いのルール】
※0〜2の整数で指定してください：
0: 違和感なし（人間らしい）
1: ささいな違和感が1〜2つ（よく考えると変）
2: 半々（人間味とAIっぽさが混ざっている）
"""  # noqa: E501
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
