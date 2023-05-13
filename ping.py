import requests
import time

while True:
    try:
        requests.get('https://test-crypto-notify-2.onrender.com/notify') # вставьте код, который выполняется, когда сайт работает
    except:
        # вставьте код, который выполняется, когда сайт не работает
    time.sleep(600) # 600 секунд = 10 минут
