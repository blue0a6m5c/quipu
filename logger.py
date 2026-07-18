"""
Quipu用のロガー設定

コンソールとログファイルの両方へ出力する。
"""

import logging
from pathlib import Path


# ログ保存ディレクトリ
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# ログファイル
LOG_FILE = LOG_DIR / "quipu.log"

# ロガー作成
logger = logging.getLogger("quipu")
logger.setLevel(logging.INFO)

# 既にハンドラが設定されている場合は追加しない
if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )

    # ファイル出力
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    # コンソール出力
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
