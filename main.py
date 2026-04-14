from letter_generator import LetterGenerator
from listener_generator import ListenerGenerator


def main():
    listener_gen = ListenerGenerator()
    letter_gen = LetterGenerator()

    print("リスナー情報を生成中...")
    try:
        listener = listener_gen.generate()
        print(f"生成されたリスナー情報: {listener}")
        print("\n" + "=" * 30 + "\n")

        print("おたよりを生成中...")
        letter = letter_gen.generate(listener)
        print("【生成されたおたより】")
        print(letter)

    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
