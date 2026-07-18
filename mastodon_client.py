# Mastodonライブラリを読み込む
from mastodon import Mastodon

# Quipuの設定ファイルを読み込む
from config import config


# Mastodon APIへ接続するクライアントを作成
mastodon = Mastodon(
    access_token=config["mastodon"]["access_token"],
    api_base_url=config["mastodon"]["base_url"],
)


def verify_connection():
    """
    Mastodon APIへの接続確認を行う。
    """

    me = mastodon.account_verify_credentials()

    print("Connected!")
    print(f"Display name : {me.display_name}")
    print(f"Username     : @{me.acct}")
    print(f"ID           : {me.id}")


def get_client():
    """
    Mastodonクライアントを返す。
    """
    return mastodon


def get_my_account():
    """
    Bot自身のアカウント情報を取得する。
    """
    return mastodon.account_verify_credentials()


def reply_to_status(status, text: str):
    """
    指定した投稿へ返信する。
    """

    mastodon.status_post(
        status=text,
        in_reply_to_id=status.id,
        visibility=status.visibility,
    )


# このファイル単体で実行された場合だけ接続確認を行う
if __name__ == "__main__":
    verify_connection()
