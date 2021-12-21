import telebot
import base64
import hmac
import json
import struct
import time
from hashlib import sha1
import config
import threading

bot = telebot.TeleBot(config.TELEGRAM_BOT_API)

activeMessages = []

# Simple function that generates steam codes by passing shared secret key
def getTwoFactorCode(shared_secret: str) -> str:
    timestamp = int(time.time())
    time_buffer = struct.pack('>Q', timestamp // 30)
    time_hmac = hmac.new(base64.b64decode(shared_secret), time_buffer, digestmod=sha1).digest()
    begin = ord(time_hmac[19:20]) & 0xf
    full_code = struct.unpack('>I', time_hmac[begin:begin + 4])[0] & 0x7fffffff
    chars = '23456789BCDFGHJKMNPQRTVWXY'
    code = ''
    for _ in range(5):
        full_code, i = divmod(full_code, len(chars))
        code += chars[i]
    return code

# Loading accounts from the list
def loadAccounts() -> list:
    try:
        with open(config.ACCOUNTS_FILE_NAME, 'r') as file:
            return json.load(file)
    except Exception as err:
        print("loadAccounts() error: ", err)
        return []

def generateCodes() -> str:
    try:
        accounts = loadAccounts()
        msg=""


        for username in accounts:
            if "shared_secret" in accounts[username]:
                msg = msg + f"{username}: {getTwoFactorCode(accounts[username]['shared_secret'])}\n"

        return msg
    except Exception as e:
        print("Error: ", e)
        return "Error using the bot"

def terminateMessage(chat_id, messages, terminationTime):
    while int(time.time()) < terminationTime:
        pass
    for message in messages:
        bot.delete_message(chat_id=chat_id, message_id=message)

# Handling the incoming telegram message
@bot.message_handler(commands=['start', 'menu'])
def start(message):
    if message.chat.id not in config.WHITELIST:
        bot.send_message(message.chat.id, "You are not in whitelist")

    msg = generateCodes()
    botmsg = bot.send_message(message.chat.id, msg)
    threading.Thread(target=terminateMessage, args=(message.chat.id, [botmsg.message_id, message.message_id], time.time() + config.DELETE_TIME)).start()

while True:
    try:
        print("Bot running")
        bot.polling(none_stop=True, timeout=15)
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        time.sleep(20)