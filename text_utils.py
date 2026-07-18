import re

from bs4 import BeautifulSoup


def strip_html(text: str) -> str:
    """
    HTMLタグを除去し、プレーンテキストを返す。
    """
    return BeautifulSoup(text, "html.parser").get_text()


def remove_mentions(text: str) -> str:
    """
    @user や @user@domain のメンションを除去する。
    """
    text = re.sub(r'@\S+', '', text)
    return text.strip()


def clean_post_text(text: str) -> str:
    """
    Mastodonの投稿本文をLLMへ渡せる形に整形する。

    処理内容
    --------
    1. HTMLタグを除去
    2. メンションを除去
    3. 前後の空白を削除
    """

    text = strip_html(text)
    text = remove_mentions(text)

    return text.strip()
