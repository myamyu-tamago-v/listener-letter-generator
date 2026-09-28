import argparse
import asyncio
import traceback

import polars as pl

from letter_generator import LetterGenerator
from listener_generator import ListenerGenerator


def _write_to_letter_file(txt: str, append: bool = True):
    flg = "a" if append else "w"
    with open("letter.txt", flg, encoding="utf-8") as f:
        f.write(f"{txt} \n")


async def main():
    parser = argparse.ArgumentParser(
        description="ラジオ番組のリスナーとおたよりを生成します。"
    )
    parser.add_argument("-n", type=int, default=5, help="生成する数 (デフォルト: 5)")
    parser.add_argument("--theme", type=str, default=None, help="おたよりのテーマ")
    parser.add_argument("--description", type=str, default=None, help="テーマの説明")
    parser.add_argument(
        "--ai-degree",
        type=int,
        choices=[0, 1, 2],
        default=None,
        help="AIっぽさの度合い (0:なし, 1:ささいな違和感, 2:半々)",
    )
    args = parser.parse_args()

    listener_gen = ListenerGenerator()
    letter_gen = LetterGenerator(theme=args.theme, theme_description=args.description)

    results = []

    _write_to_letter_file(
        f"""================
theme: {args.theme or "フリー"}
description:
{args.description}
================

""",
        append=False,
    )

    for i in range(args.n):
        print(f"[{i + 1}/{args.n}] 生成中...")
        # ai_degreeが指定されている場合はそれを使用し、
        # 指定されていない場合は順番に割り当てることで偏りを防ぐ
        target_ai_degree = args.ai_degree if args.ai_degree is not None else i % 3

        try:
            listener = await listener_gen.generate_listener(ai_degree=target_ai_degree)
            letter = await letter_gen.generate_letter(
                listener=listener,
            )

            print(f"\n--- テーマ: {args.theme or 'フリー'} ---")
            print(f"\n--- 生成されたリスナー ---\n{listener}")
            print(f"\n--- 生成されたおたより ---\n{letter}\n")

            results.append(
                {
                    "letter": letter.strip(),
                    "theme": args.theme or "フリー",
                    "radio_name": listener.nickname,
                    "age": listener.age,
                    "gender": listener.gender,
                    "occupation": listener.occupation,
                    "personality": listener.personality,
                    "listener_type": listener.listener_type,
                    "ai_degree": listener.ai_degree.name,
                }
            )
            print(
                f"完了: {listener.nickname} (AI度: {listener.ai_degree.name})\n"
                + "=" * 40
            )
            _write_to_letter_file(f"""No. {i + 1}

--- 生成されたリスナー ---
{listener}

--- 生成されたおたより ---
{letter}

{"=" * 40}
""")
        except Exception as e:
            print(f"エラーが発生しました ({i + 1}): {e}")
            traceback.print_exc()

    if results:
        df = pl.DataFrame(results)
        df.write_csv("letter.tsv", separator="\t")
        print(f"\n{len(results)}件のデータを letter.tsv に保存しました。")


if __name__ == "__main__":
    asyncio.run(main())
