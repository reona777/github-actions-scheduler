"""GAS Webアプリ エンドポイントへのトリガースクリプト"""
import argparse
import json
import os
import sys
import urllib.request


def trigger_gas(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        body = res.read().decode("utf-8")
        return {"status": res.status, "body": body}


def main() -> None:
    parser = argparse.ArgumentParser(description="GAS Webアプリ エンドポイントを呼び出します")
    parser.add_argument(
        "--url",
        default=os.getenv("GAS_WEBHOOK_URL"),
        help="GAS WebアプリのURL（環境変数 GAS_WEBHOOK_URL でも可）",
    )
    parser.add_argument(
        "--payload",
        default="{}",
        help='送信するJSONペイロード（例: \'{"action": "weeklyReport"}\'）',
    )
    args = parser.parse_args()

    if not args.url:
        print("エラー: --url または環境変数 GAS_WEBHOOK_URL を指定してください", file=sys.stderr)
        sys.exit(1)

    try:
        payload = json.loads(args.payload)
    except json.JSONDecodeError as e:
        print(f"エラー: ペイロードのJSON形式が不正です: {e}", file=sys.stderr)
        sys.exit(1)

    result = trigger_gas(args.url, payload)
    print(f"GASトリガー完了: HTTP {result['status']}")
    print(f"レスポンス: {result['body']}")


if __name__ == "__main__":
    main()
