import json

from litellm import completion

from radio_listener import RadioListener


class ListenerGenerator:
    """
    LLMを使用してランダムなリスナー情報を生成するクラス。
    """

    def __init__(self, model: str = "ollama/gemma4:e4b"):
        self.model = model

    def generate(self) -> RadioListener:
        """
        ランダムなリスナーを1人生成します。

        Returns:
            RadioListener: 生成されたリスナー情報
        """
        prompt = """
        ラジオ番組のリスナー情報を1人分、ランダムに生成してください。
        以下のJSON形式で出力してください。余計な解説は不要です。

        {
            "radio_name": "ラジオネーム",
            "occupation": "職業",
            "gender": "性別",
            "age": 20,
            "personality": "性格の説明",
            "listener_type": "熱心なリスナー or 最近聞き始めた or 10年越しの復活組 など"
        }
        """

        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        return RadioListener(
            radio_name=data["radio_name"],
            occupation=data["occupation"],
            gender=data["gender"],
            age=data["age"],
            personality=data["personality"],
            listener_type=data["listener_type"],
        )

