#!/usr/bin/python

import hmac, base64, struct, hashlib, time, json, os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sys

sys.path.append('.')
import config


def get_hotp_token(secret, intervals_no):
	"""This is where the magic happens."""
	key = base64.b32decode(normalize(secret), True) # True is to fold lower into uppercase
	msg = struct.pack(">Q", intervals_no)
	h = bytearray(hmac.new(key, msg, hashlib.sha1).digest())
	o = h[19] & 15
	h = str((struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000)
	return prefix0(h)

def get_totp_token(secret):
	"""The TOTP token is just a HOTP token seeded with every 30 seconds."""
	return get_hotp_token(secret, intervals_no=int(time.time())//30)

def normalize(key):
	"""Normalizes secret by removing spaces and padding with = to a multiple of 8"""
	k2 = key.strip().replace(' ','')
	# k2 = k2.upper()	# skipped b/c b32decode has a foldcase argument
	if len(k2)%8 != 0:
		k2 += '='*(8-len(k2)%8)
	return k2

def prefix0(h):
	"""Prefixes code with leading zeros if missing."""
	if len(h) < 6:
		h = '0'*(6-len(h)) + h
	return h

def loadAccounts() -> list:
    try:
        with open(f"./authentificator/{config.ACCOUNTS_FILE_NAME}", 'r') as file:
            return json.load(file)
    except Exception as err:
        print("loadAccounts() error: ", err)
        return []

def generateOptions():
	markup = InlineKeyboardMarkup()
	markup.row_width = 2
	accounts = loadAccounts()
	for i, account in enumerate(accounts):
		if account['secret']:
			markup.add(InlineKeyboardButton(f"{account['issuer']} {account['name']}", callback_data=f"auth_account_{i}"))
	return markup

def processCallbackQuery(send, call):
	number = call.data[13:]
	send(call.from_user.id, generateCode(int(number)))

def generateCode(i: int):
	rel = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	with open(os.path.join(rel, 'accounts.json'), 'r') as f:
		secrets = json.load(f)

	return get_totp_token(secrets[i]['secret'])
    
