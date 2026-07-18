"""
Quipu メインプログラム

Streaming APIへ接続し、
Bot宛てのメンションを受信してOllamaへ渡す。
"""

from mastodon import StreamListener

from mastodon_client import get_client
from ollama_client import ask
from text_utils import clean_post_text


class QuipuListener(StreamListener):
    """
    Streaming APIのイベントを受け取るクラス
    """

    def on_notification(self, notification):
        """
        通知を受信した時に呼ばれる。
        """

        # メンション以外の通知（お気に入り、フォローなど）は無視する
        if notification.type != "mention":
            return

        # メンションされた投稿を取得
        status = notification.status

        # 投稿本文をLLMへ渡せる形に整形する
        prompt = clean_post_text(status.content)

        print("===== Mention =====")
        print(f"User     : @{status.account.acct}")
        print(f"Prompt   : {prompt}")
        print("===================")

        # Ollamaへ問い合わせる
        reply = ask(prompt)

        print("===== Reply =====")
        print(reply)
        print("=================")


def main():
    """
    Botのメイン処理
    """

    # Mastodon APIクライアントを取得
    mastodon = get_client()

    print("Quipu started.")
    print("Waiting for mentions...")

    # Streaming APIのイベント受信クラス
    listener = QuipuListener()

    # ユーザーストリームへ接続
    mastodon.stream_user(listener)


if __name__ == "__main__":
    main()
