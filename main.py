from telebot import TeleBot, apihelper
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
import time
import config
import threading

import steam.__main__ as steam
import authentificator.__main__ as auth

from config import config

apihelper.API_URL = 'https://api.telegram.org/bot{0}/test/{1}'
bot = TeleBot(config.TELEGRAM_BOT_API)

def terminateMessage(chat_id, messages, terminationTime):
    try:
        while int(time.time()) < terminationTime:
            pass
        for message in messages:
            bot.delete_message(chat_id=chat_id, message_id=message)
    except:
        pass

def send(chat_id, message: str, reply_markup=None):
    msg: Message = bot.send_message(chat_id, message, reply_markup=reply_markup)
    threading.Thread(target=terminateMessage, args=(msg.chat.id, [msg.message_id, msg.message_id], time.time() + config.DELETE_TIME)).start()

def gen_markup(userId):
    userId = str(userId)
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if userId in config.users:
        if config.users[userId]['steamGuard']:
            markup.add(InlineKeyboardButton("Steam Guard", callback_data="steam_guard"))
        if config.users[userId]['authentificator']:
            markup.add(InlineKeyboardButton("Auth Codes", callback_data="auth_codes"))
    else:
        # TODO Not in whitelist
        pass

    return markup

@bot.message_handler(commands=['start', 'menu'])
def start(message: Message):
    # if message.chat.id not in config.WHITELIST:
    #     send(message.chat.id, "You are not in whitelist")
    send(message.chat.id, "Select:", reply_markup=gen_markup(message.from_user.id))

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery):
    if call.data == "steam_guard":
        send(call.from_user.id, "Select Steam account:", reply_markup=steam.generateOptions(call.from_user.id))
    elif call.data == "auth_codes":
        send(call.from_user.id, "Authentification accounts:", reply_markup=auth.generateOptions())
    elif call.data.startswith('steam_account_'):
        steam.processCallbackQuery(send, call)
    elif call.data.startswith('auth_account_'):
        auth.processCallbackQuery(send, call)

bot.infinity_polling()