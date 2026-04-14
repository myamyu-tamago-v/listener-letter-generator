from dataclasses import dataclass


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
        listener_type (str): リスナーのタイプ（例：熱心なリスナー、最近聞き始めた、など）
    """

    radio_name: str
    occupation: str
    gender: str
    age: int
    personality: str
    listener_type: str

    def __str__(self):
        return (
            f"{self.radio_name} ({self.age}歳 {self.gender} / {self.occupation}) "
            f"[{self.listener_type}] - 性格: {self.personality}"
        )


