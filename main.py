import argparse

import polars as pl

from letter_generator import LetterGenerator
from listener_generator import ListenerGenerator


def main():
    parser = argparse.ArgumentParser(
        description="ラジオ番組のリスナーとおたよりを生成します。"
    )
    parser.add_argument("-n", type=int, default=5, help="生成する数 (デフォルト: 5)")
    parser.add_argument("--theme", type=str, default=None, help="おたよりのテーマ")
    parser.add_argument("--description", type=str, default=None, help="テーマの説明")
    parser.add_argument(
        "--ai-degree",
        type=int,
        choices=[0, 1, 2, 3],
        default=None,
        help="AIっぽさの度合い (0:なし, 1:ささいな違和感, 2:半々, 3:完全にAI)",
    )
    args = parser.parse_args()

    listener_gen = ListenerGenerator()
    letter_gen = LetterGenerator()

    results = []

    for i in range(args.n):
        print(f"[{i + 1}/{args.n}] 生成中...")
        # ai_degreeが指定されている場合はそれを使用し、
        # 指定されていない場合は順番に割り当てることで偏りを防ぐ
        target_ai_degree = args.ai_degree if args.ai_degree is not None else i % 4

        try:
            listener = listener_gen.generate(ai_degree=target_ai_degree)
            letter = letter_gen.generate(
                listener, theme=args.theme, theme_description=args.description
            )

            print(f"\n--- テーマ: {args.theme or 'フリー'} ---")
            print(f"\n--- 生成されたリスナー ---\n{listener}")
            print(f"\n--- 生成されたおたより ---\n{letter}\n")

            results.append(
                {
                    "letter": letter.strip(),
                    "theme": args.theme or "フリー",
                    "radio_name": listener.radio_name,
                    "age": listener.age,
                    "gender": listener.gender,
                    "occupation": listener.occupation,
                    "personality": listener.personality,
                    "listener_type": listener.listener_type,
                    "ai_degree": listener.ai_degree.name,
                }
            )
            print(
                f"完了: {listener.radio_name} (AI度: {listener.ai_degree.name})\n"
                + "=" * 40
            )

        except Exception as e:
            print(f"エラーが発生しました ({i + 1}): {e}")

    if results:
        df = pl.DataFrame(results)
        df.write_csv("letter.tsv", separator="\t")
        print(f"\n{len(results)}件のデータを letter.tsv に保存しました。")


if __name__ == "__main__":
    main()
