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

    def generate(
        self, listener: RadioListener, theme: str = None, theme_description: str = None
    ) -> str:
        """
        指定されたリスナーの属性に沿ったおたよりの内容を生成します。

        Args:
            listener (RadioListener): リスナー情報
            theme (str, optional): おたよりのテーマ. Defaults to None.
            theme_description (str, optional): テーマの説明. Defaults to None.

        Returns:
            str: 生成されたおたよりの内容
        """
        if theme:
            theme_section = f"【募集テーマ：{theme}】\n{theme_description or ''}"
            theme_instruction = f"""
今回は「{theme}」というテーマでおたよりを募集しています。
このテーマに沿った内容にしてください。
"""
        else:
            theme_section = "【募集テーマ：フリー】\n現在は特定のテーマはありません。"
            theme_instruction = """
現在はフリートークを募集しています。
パーソナリティへの質問、日常の出来事、共感してほしいこと、番組の感想など
自由に書いてください。
"""

        # AI度合いに応じた味付けの指示
        ai_instructions = {
            0: "・違和感のない、人間として自然な文章を書いてください。",
            1: "・全体的には自然ですが、1つか2つ、よく考えると少しおかしい程度のささいな違和感（例：実在しない地名や、少しズレた比喩など）を混ぜてください。",
            2: "・人間らしさと、AI特有の支離滅裂な違和感が半々くらいに混ざった、どこか奇妙な文章にしてください。",
            3: "・全体が違和感の塊で、完全にAIが生成したような、意味が通じそうで通じない不可思議な文章にしてください。",
        }
        ai_style = ai_instructions.get(int(listener.ai_degree), ai_instructions[1])

        prompt = f"""
        あなたはラジオ番組『{self.program_name}』のリスナーです。
        パーソナリティの「{self.personality_name}」さんにおたより（メール）を書いてください。

        {theme_section}

        以下の【リスナー情報】を参考に、その人の年齢、職業、性格が伝わるような内容にしてください。
        {theme_instruction}
        日々の悩みや、共感してほしいちょっとした出来事を1つ含めてください。

        【重要：生成の味付け】
        ・件名は含まず、本文のみを出力してください。
        {ai_style}
        ・「AIっぽい違和感」を出す際は、毎回同じパターン（例：存在しない地名ばかり出す等）にならないよう、比喩、習慣、知識の欠落、文体の急な変化など、バリエーション豊かな違和感を持たせてください。
        ・文章は短めで、200文字程度にまとめてください。

        【リスナー情報】
        ラジオネーム: {listener.radio_name}
        年齢: {listener.age}
        性別: {listener.gender}
        職業: {listener.occupation}
        性格: {listener.personality}
        リスナー歴: {listener.listener_type}
        AI度設定: {listener.ai_degree.name}
        """

        response = completion(
            model=self.model, messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
