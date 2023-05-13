import requests
import time

while True:
    try:
        requests.get('https://your-app.render.com') # вставьте код, который выполняется, когда сайт работает
    except:
        # вставьте код, который выполняется, когда сайт не работает
    time.sleep(30) # 600 секунд = 10 минут
