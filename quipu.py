"""
Quipu メインプログラム

Streaming APIへ接続し、
Bot宛てのメンションを受信してOllamaへ渡す。
"""

from mastodon import StreamListener

from mastodon_client import (
    get_client,
    get_my_account,
    reply_to_status,
)
from ollama_client import ask
from text_utils import clean_post_text
from logger import logger

class QuipuListener(StreamListener):
    """
    Streaming APIのイベントを受け取るクラス
    """

    def __init__(self, my_account_id):
        """
        Bot自身のアカウントIDを保持する。
        """
        super().__init__()
        self.my_account_id = my_account_id

    def on_notification(self, notification):
        """
        通知を受信した時に呼ばれる。
        """

        # メンション以外の通知（お気に入り、フォローなど）は無視する
        if notification.type != "mention":
            return

        # メンションされた投稿を取得
        status = notification.status

        # Bot自身の投稿には返信しない（無限ループ防止）
        if status.account.id == self.my_account_id:
            return

        # 投稿本文をLLMへ渡せる形に整形する
        prompt = clean_post_text(status.content)

        # メンションだけで本文が空なら返信しない
        if not prompt:
            return

        logger.info("===== Mention =====")
        logger.info(f"User     : @{status.account.acct}")
        logger.info(f"Prompt   : {prompt}")
        logger.info("===================")

        # Ollamaへ問い合わせる
        reply = ask(prompt)

        logger.info("===== Reply =====")
        logger.info(reply)
        logger.info("=================")

        # AIの返答をMastodonへ返信する
        reply_to_status(status, reply)


def main():
    """
    Botのメイン処理
    """

    # Mastodon APIクライアントを取得
    mastodon = get_client()

    # Bot自身のアカウント情報を取得
    me = get_my_account()

    logger.info("Quipu started.")
    logger.info("Waiting for mentions...")

    # Streaming APIのイベント受信クラス
    listener = QuipuListener(me.id)

    # ユーザーストリームへ接続
    mastodon.stream_user(listener)


if __name__ == "__main__":
    main()
