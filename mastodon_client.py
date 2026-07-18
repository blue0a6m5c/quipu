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

    正常に認証できれば、自分のアカウント情報を表示する。
    """

    # 自分自身のアカウント情報を取得
    me = mastodon.account_verify_credentials()

    print("Connected!")
    print(f"Display name : {me.display_name}")
    print(f"Username     : @{me.acct}")
    print(f"ID           : {me.id}")


def get_client():
    """
    Mastodonクライアントを返す。

    quipu.pyなど他のモジュールから利用するための関数。
    """
    return mastodon


# このファイル単体で実行された場合だけ接続確認を行う
if __name__ == "__main__":
    verify_connection()
