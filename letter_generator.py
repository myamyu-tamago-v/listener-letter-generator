from litellm import completion

from radio_listener import RadioListener


class LetterGenerator:
    """
    リスナー情報に基づいてラジオへのおたよりを生成するクラス。
    """

    def __init__(self, model: str = "ollama/gemma4:e4b"):
        self.model = model
        self.personality_name = "みゃみゅ玉子"
        self.program_name = "殿の寝静まるそのあとに、家来はちょいと語りに入る"

    def generate(self, listener: RadioListener) -> str:
        """
        指定されたリスナーの属性に沿ったおたよりの内容を生成します。

        Args:
            listener (RadioListener): リスナー情報

        Returns:
            str: 生成されたおたよりの内容
        """
        prompt = f"""
        あなたはラジオ番組『{self.program_name}』の熱心なリスナーです。
        パーソナリティの「{self.personality_name}」さんにおたより（メール）を書いてください。

        以下の【リスナー情報】を参考に、その人の年齢、職業、性格が伝わるような内容にしてください。
        日々の悩みや、共感してほしいちょっとした出来事を1つ含めてください。

        【重要：生成の味付け】
        ・件名は含まず、本文のみを出力してください。
        ・全体的には自然ですが、一つだけ「AIが生成したような微妙な違和感」や「あれ？と思うような、事実に即していないかもしれない不思議なポイント」をあえて混ぜてください（例：実在しない奇妙な習慣や、少しズレた比喩など）。
        ・文章は短めで、200文字程度にまとめてください。

        【リスナー情報】
        ラジオネーム: {listener.radio_name}
        年齢: {listener.age}
        性別: {listener.gender}
        職業: {listener.occupation}
        性格: {listener.personality}
        リスナー歴: {listener.listener_type}
        """



        response = completion(
            model=self.model, messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
