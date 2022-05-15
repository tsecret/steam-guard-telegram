import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import config
import threading

import steam.__main__ as steam
import authentificator.__main__ as auth

API_TOKEN = '812906647:AAHGW74HYpmj-gZBgyZ9Ph9XdPyXSRMIXk8'
bot = telebot.TeleBot(API_TOKEN)

def terminateMessage(chat_id, messages, terminationTime):
    try:
        while int(time.time()) < terminationTime:
            pass
        for message in messages:
            bot.delete_message(chat_id=chat_id, message_id=message)
    except:
        pass

def send(chat_id, message, reply_markup=None):
    msg = bot.send_message(chat_id, message, reply_markup=reply_markup)
    threading.Thread(target=terminateMessage, args=(msg.chat.id, [msg.message_id, msg.message_id], time.time() + config.DELETE_TIME)).start()

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Steam Guard", callback_data="steam_guard"),
        InlineKeyboardButton("Auth Codes", callback_data="auth_codes")
    )
    return markup

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    if message.chat.id not in config.WHITELIST:
        send(message.chat.id, "You are not in whitelist")
    send(message.chat.id, "Select:", reply_markup=gen_markup())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "steam_guard":
        send(call.from_user.id, "Select Steam account:", reply_markup=steam.generateOptions())
    elif call.data == "auth_codes":
        send(call.from_user.id, "Authentification accounts:", reply_markup=auth.generateOptions())
    elif call.data.startswith('steam_account_'):
        steam.processCallbackQuery(send, call)
    elif call.data.startswith('auth_account_'):
        auth.processCallbackQuery(send, call)

bot.infinity_polling()