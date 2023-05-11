import os
from flask import Flask, request
from flask_restful import Api, Resource
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

app = Flask(__name__)
api = Api(app)

# Set up Telegram bot API
TELEGRAM_API_TOKEN = os.environ['BOT_TOKEN']
bot = Bot(TELEGRAM_API_TOKEN)
user_chat_id = os.environ['CHANNEL_ID']

class Notify(Resource):
 def post(self):
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
 
 if logs['webhookId']==os.environ['ALCHEMY_KEY'] and category == 'token':
 # extract the necessary information
 txhash = from_address = "["+str(logs['event']['activity'][0]['hash'])+"](https://etherscan.io/tx/"+str(logs['event']['activity'][0]['hash'])+")"
 
 from_address = "["+str(logs['event']['activity'][0]['fromAddress'])+"](https://etherscan.io/address/"+str(logs['event']['activity'][0]['fromAddress'])+"#tokentxns)"
 to_address = "["+str(logs['event']['activity'][0]['toAddress'])+"](https://etherscan.io/address/"+str(logs['event']['activity'][0]['toAddress'])+"#tokentxns)"
 
 token_symbol = logs['event']['activity'][0]['asset']
 token_address = "["+str(logs['event']['activity'][0]['rawContract']['address'])+"](https://etherscan.io/address/"+str(logs['event']['activity'][0]['rawContract']['address'])+")"
 
 value = str(round(logs['event']['activity'][0]['value']))

 # create the text string
 message = f'*Token transfer:*\n{txhash}\nfrom {from_address} \nto {to_address}: \nvalue: {value} *{token_symbol}* {token_address}'
 bot.send_message(chat_id=user_chat_id, text=message, parse_mode='MarkdownV2')
 
 return 200

api.add_resource(Notify, '/notify')

updater = Updater(TELEGRAM_API_TOKEN)
# Start the bot
updater.start_polling()

if __name__ == '__main__':
 app.run()
