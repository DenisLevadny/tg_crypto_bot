import os
from flask import Flask, request, Response
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

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
      if (webhook_id == os.environ['ALCHEMY_KEY_MUMBAI'] or webhook_id == os.environ['ALCHEMY_KEY_GOERLI']) and category == 'token':
        # get the network name
        network = logs['event']['network']
        
        # create a dictionary to map the network names to the domain names
        domains = {
        'ETH_GOERLI': 'goerli.etherscan.io',
        'ETH_MAINNET': 'etherscan.io',
        'POLYGON_MAINNET': 'polygonscan.com',
        'BSC_MAINNET': 'bscscan.com',
        'MATIC_MUMBAI': 'mumbai.polygonscan.com'
        }

       # check if the network is in the dictionary
       if network in domains:
          # get the domain name from the dictionary
          domain = domains[network]

       # iterate over the logs array and process each log item
       for log in logs:
          # extract the necessary information
          txhash = log['event']['activity'][0]['hash']
          from_address = log['event']['activity'][0]['fromAddress']
          to_address = log['event']['activity'][0]['toAddress']
          token_symbol = log['event']['activity'][0]['asset']
          token_address = log['event']['activity'][0]['rawContract']['address']
          value = str(round(log['event']['activity'][0]['value']))

       # create the text string using f-strings
       message = f'*Token transfer:*\n[{txhash}](https://{domain}/tx/{txhash})\nfrom [{from_address}](https://{domain}/address/{from_address}#tokentxns) \nto [{to_address}](https://{domain}/address/{to_address}#tokentxns): \nvalue: {value} *{token_symbol}* [{token_address}](https://{domain}/address/{token_address})'
 
       # try to send the message to the bot and handle any errors
       try:
          bot.send_message(chat_id=user_chat_id, text=message, parse_mode='MarkdownV2')
       except Exception as e:
          print(f"Error sending message: {e}")      
      
  return Response(status=200)

updater = Updater(TELEGRAM_API_TOKEN)
# Start the bot
updater.start_polling()

if __name__ == '__main__':
    app.run()
