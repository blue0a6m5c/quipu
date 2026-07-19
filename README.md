# Quipu

Quipuは、Ollamaを利用してローカルLLMと会話できるMastodon Botです。

## 主な機能

- Mastodon Streaming APIによるリアルタイム応答
- メンションへの自動返信
- Ollamaを利用したローカルLLM応答
- HTML・メンション除去
- 自己返信防止
- 空メッセージの無視
- サーバーホワイトリスト
- レートリミット
- ログ出力
- タイムアウト・接続エラー時の例外処理

## ディレクトリ構成

```
quipu/
├── config.py
├── config.yaml
├── logger.py
├── mastodon_client.py
├── ollama_client.py
├── personality.txt
├── quipu.py
├── requirements.txt
└── logs/
```

## 必要環境

- Python 3.12+
- Ollama
- Mastodon Access Token

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`config.yaml`を編集し、以下を設定してください。

- Mastodon URL
- Access Token
- Ollama URL
- 使用するモデル

`personality.txt`を編集し、以下を設定してください。
- Ollamaとの対話の際に使うデフォルトプロンプト（人格設定など）

## 起動

```bash
python quipu.py
```

## 今後の予定

- 会話履歴対応
- 管理者コマンド
- Docker対応

## systemdによる常駐化

### サービスファイルの作成

`/etc/systemd/system/quipu.service`

```ini
[Unit]
Description=Quipu Mastodon Bot
After=network.target

[Service]
Type=simple
User=root ##環境によって変えてください
WorkingDirectory=/root/quipu ##環境によって変えてください
ExecStart=/root/quipu/.venv/bin/python3 /root/quipu/quipu.py ##環境によって変えてください
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### サービスを有効化

```bash
sudo systemctl daemon-reload
sudo systemctl enable quipu
sudo systemctl start quipu
```

### 状態確認

```bash
systemctl status quipu
```

### ログ確認

```bash
journalctl -u quipu -f
```

### サービス停止

```bash
sudo systemctl stop quipu
```

### サービス再起動

```bash
sudo systemctl restart quipu
```
