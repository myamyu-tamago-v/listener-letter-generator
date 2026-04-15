import json

from litellm import completion

from radio_listener import AiDegree, RadioListener


class ListenerGenerator:
    """
    LLMを使用してランダムなリスナー情報を生成するクラス。
    """

    def __init__(self, model: str = "ollama/gemma4:e4b"):
        self.model = model

    def generate(self, ai_degree: int = None) -> RadioListener:
        """
        ランダムなリスナーを1人生成します。

        Args:
            ai_degree (int, optional): AIっぽさの度合い (0-3).
                指定されない場合はLLMがランダムに選択します.

        Returns:
            RadioListener: 生成されたリスナー情報
        """
        ai_degree_instruction = ""
        if ai_degree is not None:
            ai_degree_instruction = (
                f"今回は ai_degree を必ず {ai_degree} に設定してください。"
            )

        prompt = f"""
        ラジオ番組のリスナー情報を1人分、ランダムに生成してください。
        以下のJSON形式で出力してください。余計な解説は不要です。

        {{
            "radio_name": "ラジオネーム",
            "occupation": "職業",
            "gender": "性別",
            "age": 20,
            "personality": "性格の説明",
            "listener_type": "熱心なリスナー or 最近聞き始めた or 10年越しの復活組 など",
            "ai_degree": 0
        }}

        ※ai_degreeは「AIっぽさ（違和感）」の度合いを0〜3の整数で指定してください：
        0: 違和感なし（人間らしい）
        1: ささいな違和感が1〜2つ（よく考えると変）
        2: 半々（人間味とAIっぽさが混ざっている）
        3: 完全にAI（違和感の塊）

        {ai_degree_instruction}
        """

        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        # AI度合いをEnumに変換（数値で返ってくるため）
        raw_degree = data.get("ai_degree", ai_degree if ai_degree is not None else 1)
        try:
            enum_degree = AiDegree(int(raw_degree))
        except ValueError, TypeError:
            enum_degree = AiDegree.SUBTLE

        return RadioListener(
            radio_name=data["radio_name"],
            occupation=data["occupation"],
            gender=data["gender"],
            age=data["age"],
            personality=data["personality"],
            listener_type=data["listener_type"],
            ai_degree=enum_degree,
        )
