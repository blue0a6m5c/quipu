from mastodon import Mastodon

from config import config

mastodon = Mastodon(
    access_token=config["mastodon"]["access_token"],
    api_base_url=config["mastodon"]["base_url"],
)


def verify_connection():
    """Mastodonへの接続を確認する"""
    me = mastodon.account_verify_credentials()

    print("Connected!")
    print(f"Display name : {me.display_name}")
    print(f"Username     : @{me.acct}")
    print(f"ID           : {me.id}")


if __name__ == "__main__":
    verify_connection()

def test_post():
    mastodon.status_post(
        "Hello from Quipu! 🤖"
    )

if __name__ == "__main__":
    test_post()
