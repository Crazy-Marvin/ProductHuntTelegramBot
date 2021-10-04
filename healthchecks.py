import requests
import os
import time

API_KEY = os.getenv("HEALTH_BOT_API")
ID = os.getenv("GROUP_ID")
MSG = ""

url = 'https://api.telegram.org/bot' + API_KEY + \
    '/sendMessage?chat_id=' + ID + '&parse_mode=Markdown&text='

while True:

    # YogiBot Telegram Bot
    try:
        requests.get(
            "https://hc-ping.com/c0bc0baa-b74c-4cb3-bb4b-26c0743b6843", timeout=30)
        MSG += "🟢 YOGI BOT\n\n"
    except:
        MSG += "🔴 YOGI BOT\n\n"

    requests.get(url=(url+MSG))
    MSG = ""
    time.sleep(3600)
