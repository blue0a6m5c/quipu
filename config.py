from pathlib import Path

import yaml

CONFIG_FILE = Path("config.yaml")
PERSONALITY_FILE = Path("personality.txt")

if not CONFIG_FILE.exists():
    raise FileNotFoundError(
        "config.yaml が見つかりません。config.yaml.example をコピーして作成してください。"
    )

if not PERSONALITY_FILE.exists():
    raise FileNotFoundError(
        "personality.txt が見つかりません。"
    )

with CONFIG_FILE.open("r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

with PERSONALITY_FILE.open("r", encoding="utf-8") as f:
    personality = f.read().strip()
