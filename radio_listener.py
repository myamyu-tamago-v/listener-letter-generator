from enum import IntEnum

from pydantic import BaseModel


class AiDegree(IntEnum):
    """
    リスナーの「AIっぽさ（違和感）」の度合いを表す列挙型。
    """

    HUMAN = 0  # 違和感なし
    SUBTLE = 1  # 1〜2つのささいな違和感
    MIXED = 2  # 人間とAIが半々


class RadioListener(BaseModel):
    """
    ラジオ番組のリスナー情報を表すクラス。
    """

    nickname: str
    occupation: str
    gender: str
    age: int
    personality: str
    listener_type: str
    ai_degree: AiDegree = AiDegree.SUBTLE

    def __str__(self):
        return (
            f"{self.nickname} "
            f"({self.age}歳 {self.gender} / {self.occupation}) "
            f"[{self.listener_type}] (AI度: {self.ai_degree.name})"
            f" - 性格: {self.personality}"
        )
