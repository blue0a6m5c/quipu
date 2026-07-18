"""
Quipu メインプログラム

Streaming APIへ接続し、
Bot宛てのメンションを受信してOllamaへ渡す。
"""
import time
import requests
from mastodon import StreamListener

from mastodon_client import (
    get_client,
    get_my_account,
    reply_to_status,
)
from ollama_client import ask
from text_utils import clean_post_text
from logger import logger
from config import config

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

        # リモートユーザーの場合は所属サーバーを取得する。
        # ローカルユーザーの場合はサーバー名を取得できないため許可する。
        server = None
        if "@" in status.account.acct:
            server = status.account.acct.split("@")[-1]

        # 許可されていないサーバーからのメンションは無視する
        if (
            server is not None
            and server not in config["mastodon"]["allowed_servers"]
        ):
            logger.info(
                f"Ignored mention from unauthorized server: {server}"
            )
            return


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

                # Ollamaへ問い合わせる処理時間を計測するため、開始時刻を記録する
        start_time = time.perf_counter()

        try:
            # Ollamaへ問い合わせを開始する
            logger.info("Sending prompt to Ollama...")

            # Ollamaへプロンプトを送り、応答を取得する
            reply = ask(prompt)

            # Ollamaから応答が返るまでにかかった時間を計算する
            elapsed = time.perf_counter() - start_time

            logger.info(f"Ollama replied in {elapsed:.2f} sec")

            logger.info("===== Reply =====")
            logger.info(reply)
            logger.info("===================")

            # AIの返答をMastodonへ返信する
            reply_to_status(status, reply)

        except requests.exceptions.Timeout:
            # Ollamaが一定時間応答しなかった場合
            elapsed = time.perf_counter() - start_time

            logger.warning(
                f"Ollama timed out after {elapsed:.2f} sec"
            )

            reply_to_status(status, "zzz...")

        except requests.exceptions.ConnectionError:
            # Ollamaサーバーへ接続できなかった場合
            elapsed = time.perf_counter() - start_time

            logger.warning(
                f"Could not connect to Ollama after {elapsed:.2f} sec"
            )

            reply_to_status(status, "……まだ寝ています。")

        except Exception:
            # 想定外のエラーが発生した場合
            elapsed = time.perf_counter() - start_time

            # スタックトレースを含めてログへ記録する
            logger.exception(
                f"Failed to process mention after {elapsed:.2f} sec"
            )


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
