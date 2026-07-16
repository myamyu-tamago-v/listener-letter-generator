from enum import IntEnum

from pydantic import BaseModel, Field


class AiDegree(IntEnum):
    """
    リスナーの「AIっぽさ（違和感）」の度合いを表す列挙型。
    """

    HUMAN = 0  # 違和感なし
    SUBTLE = 1  # 1〜2つのささいな違和感
    MIXED = 2  # 人間とAIが半々
    FULL_AI = 3  # 完全にAI（違和感しかない）


class RadioListener(BaseModel):
    """
    ラジオ番組のリスナー情報を表すクラス。
    """

    radio_name: str = Field(description="ラジオネーム")
    occupation: str = Field(description="職業")
    gender: str = Field(description="性別")
    age: int = Field(description="年齢")
    personality: str = Field(
        description="""リスナーの性格・パーソナリティ。
以下の要素を含めて記述してください：
- 基本的な性格
- 趣味や最近ハマっていること
- この番組に投稿する理由や動機（例：熱心なリスナー、お悩み相談、暇つぶしなど）
"""
    )
    listener_type: str = Field(
        description=("リスナーのタイプ（例：熱心なリスナー、最近聞き始めた、など）")
    )
    ai_degree: AiDegree = Field(
        description="""AIっぽさの度合い
※0〜3の整数で指定してください：
0: 違和感なし（人間らしい）
1: ささいな違和感が1〜2つ（よく考えると変）
2: 半々（人間味とAIっぽさが混ざっている）
3: 完全にAI（違和感の塊）
""",
        default=AiDegree.SUBTLE,
    )

    def __str__(self):
        return (
            f"{self.radio_name} "
            f"({self.age}歳 {self.gender} / {self.occupation}) "
            f"[{self.listener_type}] (AI度: {self.ai_degree.name})"
            f" - 性格: {self.personality}"
        )
