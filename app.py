import os
from flask import Flask, request, Response
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
import time

app = Flask(__name__)

# Set up Telegram bot API
TELEGRAM_API_TOKEN = os.environ['BOT_TOKEN']
bot = Bot(TELEGRAM_API_TOKEN)
user_chat_id = os.environ['CHANNEL_ID']

@app.route('/')
def hello():
    return 'Service for sending notifications to a telegram channel '

@app.route('/notify', methods=['POST','GET'])
def notify():
  logs = request.json
  if (len(logs) == 0):
    print("Empty logs array received, skipping")
  else:    
      
      print(logs)
      
      category = ""
      try:
         category = logs['event']['activity'][0]['category']
      except:
         print("category not defined")
            
      webhook_id = logs['webhookId']
      if (webhook_id == os.environ['ALCHEMY_KEY_MUMBAI'] or webhook_id == os.environ['ALCHEMY_KEY_GOERLI'] or webhook_id == os.environ['ALCHEMY_KEY_ETH'] or webhook_id == os.environ['ALCHEMY_KEY_POLYGON'] or webhook_id == os.environ['ALCHEMY_KEY_OPTIMISM'] or webhook_id == os.environ['ALCHEMY_KEY_ARBITRUM']) and category == 'token':
        # get the network name
        network = logs['event']['network']

        # check the network and set the domain accordingly
        if network == 'MATIC_MUMBAI':
          domain = 'mumbai.polygonscan.com'
        elif network == 'ETH_GOERLI':
          domain = 'goerli.etherscan.io'
        elif network == 'ETH_MAINNET':
          domain = 'etherscan.io'
        elif network == 'POLYGON_MAINNET':
          domain = 'polygonscan.com'
        elif network == 'OPTIMISM_MAINNET':
          domain = 'optimistic.etherscan.io'
        elif network == 'ARBITRUM_MAINNET':
          domain = 'arbiscan.io'
        else:
          # unknown network, skip the processing
          return Response(status=200)
        
        # extract the necessary information
        txhash = "["+str(logs['event']['activity'][0]['hash'])+"](https://"+domain+"/tx/"+str(logs['event']['activity'][0]['hash'])+")"
           
        from_address = "["+str(logs['event']['activity'][0]['fromAddress'])+"](https://"+domain+"/address/"+str(logs['event']['activity'][0]['fromAddress'])+"#tokentxns)"
        to_address = "["+str(logs['event']['activity'][0]['toAddress'])+"](https://"+domain+"/address/"+str(logs['event']['activity'][0]['toAddress'])+"#tokentxns)"
          
        token_symbol = logs['event']['activity'][0]['asset']
        token_address = "["+str(logs['event']['activity'][0]['rawContract']['address'])+"](https://"+domain+"/address/"+str(logs['event']['activity'][0]['rawContract']['address'])+")"
          
        value = str(round(logs['event']['activity'][0]['value']))

        # create the text string
        message = f'*Token transfer:*\n{txhash}\nfrom {from_address} \nto {to_address}: \nvalue: {value} *{token_symbol}* {token_address}'
        bot.send_message(chat_id=user_chat_id, text=message, parse_mode='MarkdownV2')
      
  return Response(status=200)

updater = Updater(TELEGRAM_API_TOKEN)
# Start the bot
updater.start_polling()

while True:
    try:
        requests.get('https://test-crypto-notify-2.onrender.com/notify')
        print('Сайт работает нормально') # вставьте код, который выполняется, когда сайт работает
    except:
        print('Сайт не работает!') # вставьте код, который выполняется, когда сайт не работает
        # можно добавить дополнительные действия, например отправить уведомление или перезапустить сайт
    time.sleep(600) # 600 секунд = 10 минут

if __name__ == '__main__':
    app.run()
