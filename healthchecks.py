import requests
import os
import time

API_KEY = os.getenv("HEALTH_BOT_API")
ID = os.getenv("GROUP_ID")
MSG = ""

url = 'https://api.telegram.org/bot' + API_KEY + \
    '/sendMessage?chat_id=' + ID + '&parse_mode=Markdown&text='

while True:

    # Product Hunt Telegram Bot
    try:
        requests.get(
            "https://hc-ping.com/97c84712-e1e6-4d4e-a9b4-670b702f9c5b", timeout=30)
        MSG += "🟢 PRODUCT HUNT BOT\n\n"
    except:
        MSG += "🔴 PRODUCT HUNT BOT\n\n"

    requests.get(url=(url+MSG))
    MSG = ""
    time.sleep(3600)
