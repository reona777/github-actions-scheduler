# GitHub Actions スケジューラー サンプル集

GitHub Actions の `schedule` トリガーを使った定期実行ワークフローのサンプル集です。
GASトリガー・Pythonスクリプト実行・Slack通知など、業務自動化でよく使うパターンを網羅しています。

---

## ワークフロー一覧

| ファイル | 実行タイミング | 処理内容 |
|---|---|---|
| `daily-python.yml` | 毎日 9:00 JST | Playwright スクレイピング → スプレッドシート同期 |
| `weekly-gas-trigger.yml` | 毎週月曜 9:00 JST | GAS Webアプリ エンドポイントを呼び出す |
| `monthly-report.yml` | 毎月1日 10:00 JST | 月次集計レポートを生成・Slack送信 |
| `slack-notify.yml` | push / PR / 手動 | 各イベントに応じたSlack通知 |
| `scraping-to-sheets.yml` | 平日 9:00 JST | スクレイピング → スプレッドシート同期（平日のみ） |

全ワークフローに `workflow_dispatch` が設定されており、GitHub UIから手動実行できます。

---

## ファイル構成

```
github-actions-scheduler/
├── .github/
│   └── workflows/
│       ├── daily-python.yml           # 毎日Pythonスクリプト実行
│       ├── weekly-gas-trigger.yml     # 週次GASトリガー
│       ├── monthly-report.yml         # 月次レポート生成
│       ├── slack-notify.yml           # Slack通知（push/PR/手動）
│       └── scraping-to-sheets.yml     # 平日スクレイピング同期
├── scripts/
│   ├── notify_slack.py                # Slack Incoming Webhook 通知
│   └── trigger_gas.py                 # GAS Webアプリ呼び出し
└── requirements.txt
```

---

## 共通セットアップ

### GitHub Secrets の設定

リポジトリの「Settings → Secrets and variables → Actions」で以下を登録してください。

| Secret名 | 説明 | 使用ワークフロー |
|---|---|---|
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL | 全ワークフロー |
| `SPREADSHEET_ID` | 同期先スプレッドシートID | daily / monthly / scraping |
| `GOOGLE_CREDENTIALS_JSON` | サービスアカウントJSONの内容（テキスト全体） | daily / monthly / scraping |
| `GAS_WEBHOOK_URL` | GAS WebアプリのデプロイURL | weekly-gas-trigger |

### GOOGLE_CREDENTIALS_JSON の登録方法

```bash
# JSONファイルの内容をそのままSecretに貼り付ける
cat credentials.json
```

ワークフロー内で `echo "$GOOGLE_CREDENTIALS_JSON" > credentials.json` として復元します。

---

## ワークフロー詳細

### daily-python.yml — 毎日 Python スクリプト実行

```
毎日 9:00 JST
  → Playwright でスクレイピング
  → Google Sheets へ差分同期
  → 成功/失敗を Slack 通知
```

手動実行時はダミーデータ（`--dummy`）の使用も可能です。

---

### weekly-gas-trigger.yml — 週次 GAS トリガー

```
毎週月曜 9:00 JST
  → scripts/trigger_gas.py が GAS Webアプリへ POST
  → GAS 側で週次レポート生成などの処理を実行
  → 結果を Slack 通知
```

GAS Webアプリ側では `doPost(e)` でリクエストを受け取ります。

```javascript
// GAS 側の受信例
function doPost(e) {
  var payload = JSON.parse(e.postData.contents);
  if (payload.action === "weeklyReport") {
    sendWeeklyReport();
  }
  return ContentService.createTextOutput("OK");
}
```

---

### monthly-report.yml — 月次レポート生成

```
毎月1日 10:00 JST
  → 前月分のデータを集計
  → スプレッドシートへ出力
  → 完了を Slack 通知
  → エラー時は緊急通知
```

---

### slack-notify.yml — イベント連動 Slack 通知

`push`・`pull_request`・手動実行の3パターンに対応しています。

```yaml
# 手動実行時にメッセージを指定
workflow_dispatch:
  inputs:
    message:
      description: "Slack に送信するメッセージ"
```

---

### scraping-to-sheets.yml — 平日スクレイピング同期

```
平日（月〜金）9:00 JST のみ実行
  → 手動実行時は use_dummy: true でダミーデータ使用可能
```

土日は実行されないため、無駄なAPI呼び出しを防げます。

---

## scripts/ の使い方

### notify_slack.py — Slack 通知

```bash
python scripts/notify_slack.py \
  --message "デプロイが完了しました。" \
  --webhook-url "https://hooks.slack.com/services/..."
```

環境変数 `SLACK_WEBHOOK_URL` が設定されていれば `--webhook-url` は省略可能です。

### trigger_gas.py — GAS Webアプリ呼び出し

```bash
python scripts/trigger_gas.py \
  --url "https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec" \
  --payload '{"action": "weeklyReport"}'
```

---

## cron 式チートシート

| cron式 | 実行タイミング |
|---|---|
| `0 0 * * *` | 毎日 9:00 JST（UTC 0:00） |
| `0 0 * * 1` | 毎週月曜 9:00 JST |
| `0 1 1 * *` | 毎月1日 10:00 JST |
| `0 0 * * 1-5` | 平日（月〜金）9:00 JST |
| `0 23 * * 0` | 毎週日曜 8:00 JST（UTC 23:00） |

GitHub Actions の `schedule` は UTC 基準です。JST = UTC + 9時間で計算してください。

---

## ライセンス

MIT License
