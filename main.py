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
    args = parser.parse_args()

    listener_gen = ListenerGenerator()
    letter_gen = LetterGenerator()

    results = []

    for i in range(args.n):
        print(f"[{i + 1}/{args.n}] 生成中...")
        try:
            listener = listener_gen.generate()
            letter = letter_gen.generate(listener, theme=args.theme, theme_description=args.description)

            print(f"\n--- 生成されたリスナー ---\n{listener}")
            print(f"\n--- 生成されたおたより ---\n{letter}\n")

            results.append(
                {
                    "letter": letter.strip(),
                    "radio_name": listener.radio_name,
                    "age": listener.age,
                    "gender": listener.gender,
                    "occupation": listener.occupation,
                    "personality": listener.personality,
                    "listener_type": listener.listener_type,
                }
            )
            print(f"完了: {listener.radio_name}\n" + "=" * 40)

        except Exception as e:
            print(f"エラーが発生しました ({i + 1}): {e}")

    if results:
        df = pl.DataFrame(results)
        df.write_csv("letter.tsv", separator="\t")
        print(f"\n{len(results)}件のデータを letter.tsv に保存しました。")


if __name__ == "__main__":
    main()
