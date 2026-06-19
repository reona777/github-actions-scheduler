# github-actions-scheduler

> 業務自動化でよく使うGitHub Actionsスケジューラーのパターン集

「毎日9時にPythonスクリプトを実行」「週次でGAS Webアプリを呼び出す」「月次レポートを自動送信」など、実務でそのまま使えるワークフローをテンプレートとして整備しています。

## 収録ワークフロー

| ファイル | 実行タイミング | 処理内容 |
|---|---|---|
| `daily-python.yml` | 毎日 9:00 JST | Playwright スクレイピング → スプレッドシート同期 |
| `weekly-gas-trigger.yml` | 毎週月曜 9:00 JST | GAS Webアプリ エンドポイントを呼び出す |
| `monthly-report.yml` | 毎月1日 10:00 JST | 月次集計レポートを生成・Slack送信 |
| `slack-notify.yml` | push / PR / 手動 | 各イベントに応じたSlack通知 |
| `scraping-to-sheets.yml` | 平日 9:00 JST | スクレイピング → スプレッドシート同期（平日のみ） |

全ワークフローに `workflow_dispatch` が設定されており、スケジュール実行と手動実行の両方に対応しています。

## 背景・導入経緯

業務自動化で Python スクリプトや GAS を定期実行したい場面が繰り返し発生していた。GitHub Actions は無料枠で使えてコードと同じリポジトリで管理できる点が扱いやすいが、cron の UTC 変換・土日スキップ・dry_run 設計など、毎回同じ設定を一から書き直すのが手間だった。

よく使うスケジューラーパターンをテンプレートとして一箇所にまとめることで、新しい自動化タスクの立ち上げコストを下げることを目的に整備した。

## 技術スタック

![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=github-actions&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Slack](https://img.shields.io/badge/Slack-4A154B?style=flat&logo=slack&logoColor=white)
![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=flat&logo=google-sheets&logoColor=white)

- **GitHub Actions** — スケジュール実行・イベントトリガー
- **Python 3.x** — スクレイピング・レポート生成スクリプト
- **Slack Incoming Webhook** — 通知・アラート
- **Google Sheets API** — レポート出力・データ蓄積

## 設計上のポイント

- cron は UTC 基準のため、JST 変換を全ワークフローでコメント付きで明記
- 認証情報はすべて GitHub Secrets で管理し、コードへの直書きを排除
- `dry_run` 入力で本番送信せずに動作確認できるワークフロー設計
- 土日スキップ（`0 0 * * 1-5`）など実務でよく使うパターンを網羅

## セットアップ

```bash
pip install -r requirements.txt
```

リポジトリの **Settings → Secrets and variables → Actions** に以下を登録:

| Secret名 | 説明 |
|---|---|
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL |
| `SPREADSHEET_ID` | 同期先スプレッドシートID |
| `GOOGLE_CREDENTIALS_JSON` | サービスアカウントJSON（テキスト全体） |
| `GAS_WEBHOOK_URL` | GAS WebアプリのデプロイURL |

## ファイル構成

```
github-actions-scheduler/
├── .github/workflows/
│   ├── daily-python.yml         # 毎日 Python スクリプト実行
│   ├── weekly-gas-trigger.yml   # 週次 GAS トリガー
│   ├── monthly-report.yml       # 月次レポート生成
│   ├── slack-notify.yml         # Slack 通知（push/PR/手動）
│   └── scraping-to-sheets.yml   # 平日スクレイピング同期
├── scripts/
│   ├── notify_slack.py          # Slack Incoming Webhook 通知
│   └── trigger_gas.py           # GAS Webアプリ呼び出し
└── requirements.txt
```

## ライセンス

MIT License
