import datetime
import requests
import os

def get_garbage_type():
    # 日本時間（JST）を取得
    tz = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(tz)
    
    weekday = now.weekday() # 0:月, 1:火, 2:水, 3:木, 4:金, 5:土, 6:日
    day = now.day

    # その月の「第何週目」かを計算 (1〜7日は第1週、8〜14日は第2週...)
    nth_week = (day - 1) // 7 + 1

    # ゴミの種類の判定
    if weekday == 1 or weekday == 4:
        return "燃えるゴミ"
    elif weekday == 3:
        if nth_week == 2:
            return "ペットボトル"
        elif nth_week == 4:
            return "燃えないゴミ"
            
    return None # ゴミの日ではない

def main():
    garbage_type = get_garbage_type()
    
    # ゴミの日であればDiscordに通知
    if garbage_type:
        webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
        if not webhook_url:
            print("Webhook URLが設定されていません。")
            return

        # ここを夜用のメッセージに変更！
        content = f"今日は **{garbage_type}** の日です、あなたが出しましょう"
        
        payload = {"content": content}
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code == 204:
            print("通知を送信しました。")
        else:
            print(f"送信に失敗しました: {response.status_code}")
    else:
        print("本日はゴミ収集日ではありません。")

if __name__ == "__main__":
    main()
