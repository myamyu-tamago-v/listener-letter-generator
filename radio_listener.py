from dataclasses import dataclass
from enum import IntEnum


class AiDegree(IntEnum):
    """
    リスナーの「AIっぽさ（違和感）」の度合いを表す列挙型。
    """

    HUMAN = 0  # 違和感なし
    SUBTLE = 1  # 1〜2つのささいな違和感
    MIXED = 2  # 人間とAIが半々
    FULL_AI = 3  # 完全にAI（違和感しかない）


@dataclass
class RadioListener:
    """
    ラジオ番組のリスナー情報を表すクラス。

    Attributes:
        radio_name (str): ラジオネーム
        occupation (str): 職業
        gender (str): 性別
        age (int): 年齢
        personality (str): 性格・パーソナリティ
        listener_type (str): リスナーのタイプ
            （例：熱心なリスナー、最近聞き始めた、など）
        ai_degree (AiDegree): AIっぽさの度合い
    """

    radio_name: str
    occupation: str
    gender: str
    age: int
    personality: str
    listener_type: str
    ai_degree: AiDegree = AiDegree.SUBTLE

    def __str__(self):
        return (
            f"{self.radio_name} "
            f"({self.age}歳 {self.gender} / {self.occupation}) "
            f"[{self.listener_type}] (AI度: {self.ai_degree.name}) - 性格: {self.personality}"
        )
