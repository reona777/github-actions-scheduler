"""Slack Incoming Webhook への通知スクリプト"""
import argparse
import json
import os
import sys
import urllib.request


def post_to_slack(webhook_url: str, message: str, username: str = "GitHub Actions Bot") -> None:
    payload = json.dumps({
        "username": username,
        "icon_emoji": ":robot_face:",
        "text": message,
    }).encode("utf-8")

    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as res:
        if res.status != 200:
            print(f"Slack通知失敗: HTTP {res.status}", file=sys.stderr)
            sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Slack へメッセージを送信します")
    parser.add_argument("--message", required=True, help="送信するメッセージ本文")
    parser.add_argument(
        "--webhook-url",
        default=os.getenv("SLACK_WEBHOOK_URL"),
        help="Slack Incoming Webhook URL（環境変数 SLACK_WEBHOOK_URL でも可）",
    )
    parser.add_argument("--username", default="GitHub Actions Bot", help="Bot の表示名")
    args = parser.parse_args()

    if not args.webhook_url:
        print("エラー: --webhook-url または環境変数 SLACK_WEBHOOK_URL を指定してください", file=sys.stderr)
        sys.exit(1)

    post_to_slack(args.webhook_url, args.message, args.username)
    print("Slack通知を送信しました")


if __name__ == "__main__":
    main()
