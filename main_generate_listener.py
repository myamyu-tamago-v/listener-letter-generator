import argparse
import asyncio
import traceback

from generator.listener_generator import ListenerGenerator


async def main():
    parser = argparse.ArgumentParser(
        description="ラジオ番組のリスナーを試しに生成します。"
    )
    parser.add_argument("-n", type=int, default=5, help="生成する数 (デフォルト: 5)")
    args = parser.parse_args()

    listener_gen = ListenerGenerator()

    for i in range(args.n):
        print(f"[{i + 1}/{args.n}] 生成中...")
        target_ai_degree = i % 3

        try:
            listener = await listener_gen.generate_listener(ai_degree=target_ai_degree)
            print(f"\n--- 生成されたリスナー ---\n{listener}")
            print(
                f"完了: {listener.nickname} (AI度: {listener.ai_degree.name})\n"
                + "=" * 40
            )

        except Exception as e:
            print(f"エラーが発生しました ({i + 1}): {e}")
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
