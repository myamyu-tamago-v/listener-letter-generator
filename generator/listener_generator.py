from model.radio_listener import RadioListener

from .llm_base import LLMAgentBase


class ListenerGenerator(LLMAgentBase[RadioListener]):
    def __init__(self) -> None:
        instructions = """
ラジオ番組のリスナー情報を1人分、ランダムに生成してください。

【各フィールドについて】
nickname: リスナーのニックネーム。
occupation: 職業。
gender: 性別。
age: 年齢。
personality: リスナーの性格など。
listener_type: リスナーのタイプ（例：熱心なリスナー、最近聞き始めた、など）
ai_degree: AIっぽさの度合い。

【ニックネーム生成ルール：※最優先事項です】
- 「めぐみ」「たかし」のような単純な人名は絶対に使わないでください。
- ポッドキャストのラジオネームとして成立する、ユニークで記憶に残る名前を生成してください。
- 以下のパターンを必ず使用して、ひねりのある面白いラジオネームにしてください：
    1. 【形容詞/動詞】＋【名詞】（例：『徹夜明けのメロンパン』『鼻歌まじりのエンジニア』）
    2. 【意外な組み合わせ】（例：『冷蔵庫のプリン泥棒』『火曜日のタートルネック』）
    3. 【その人の属性＋エピソード】（例：『昨日フラれたばかりの課長』『3年待ったラーメンオタク』）
- 記号は不可。読みやすい日本語のみ。

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
