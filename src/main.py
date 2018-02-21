#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.
"""
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from messages import emojidb as emo
from messages import info
from messages import buttons as btn

from nearest import get_nearest_location

import telegram
from dbhelper import DBHelper

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)
logger = logging.getLogger(__name__)

# DB settings
db = DBHelper()
db.setup()

def str_to_keyboard(lst):
	return [[KeyboardButton(j) for j in i] for i in lst]

def create_main_keyboard():
	keyboard_main = str_to_keyboard(btn.keyboard_main_layout)
	reply_markup_main = ReplyKeyboardMarkup(keyboard_main, resize_keyboard=1)
	return reply_markup_main


def start(bot, update):
	update.message.reply_text(info.helping_info, reply_markup=create_main_keyboard(), parse_mode='HTML')

# Create main keyboard
def cansel(bot, update):
	update.message.reply_text(info.cansel, reply_markup=create_main_keyboard(), parse_mode='HTML')

def button(bot, update):
	query = update.callback_query

	bot.edit_message_text(text="Selected option: {}".format(query.data),
						  chat_id=query.message.chat_id,
						  message_id=query.message.message_id)

def help(bot, update):
	update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, error)

def keyboard_handler_phonebtn(bot, update):
	logger.info('Phone clicked')
	update.message.reply_text(info.starting_message, parse_mode='HTML')

def create_location_send_keyboard():
	keyboard_office = str_to_keyboard(btn.keyboard_offices_layout)
	keyboard_office[0][0] = KeyboardButton(text=keyboard_office[0][0].text, request_location=True)
	reply_markup_main = ReplyKeyboardMarkup(keyboard_office, resize_keyboard=True, selective=False)
	return reply_markup_main

def keyboard_handler_officebtn(bot, update):
	logger.info('Office clicked')
	chat_id = update.message.chat_id
	text    = update.message.text

	db.add_item(item_text=text, chat_id=chat_id)
	update.message.reply_text(info.share_location_office, reply_markup=create_location_send_keyboard(), parse_mode='HTML')

def keyboard_handler_atmbtn(bot, update):
	logger.info('Atm clicked')
	chat_id = update.message.chat_id
	text    = update.message.text

	db.add_item(item_text=text, chat_id=chat_id)
	update.message.reply_text(info.share_location_atm, reply_markup=create_location_send_keyboard(), parse_mode='HTML')

def get_currency(bot, update):
	logger.info('currancy_rate clicked')
	print(info.currancy_rate)
	update.message.reply_text(str(info.currancy_rate), parse_mode='HTML')

def keyboard_handler(bot, update):
	user = update.message.from_user
	text = update.message.text

	if btn.btn_phone == text: keyboard_handler_phonebtn(bot, update)
	elif btn.btn_offices == text: keyboard_handler_officebtn(bot, update)
	elif btn.btn_atm == text: keyboard_handler_atmbtn(bot, update)
	elif btn.btn_offices_cansel == text: cansel(bot,update)
	elif btn.btn_cash == text: get_currency(bot, update)
	else:
		logger.info(text)
		db_add(bot, update)
		update.message.reply_text((text), parse_mode='HTML')

def location_handler(bot, update):
	chat_id = update.message.chat_id
	latitude = update.message.location['latitude']
	longitude = update.message.location['longitude']

	bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

	if btn.btn_offices.strip() == db.get_last_element(chat_id=chat_id).strip():
		nearest_latitude, nearest_longitude = get_nearest_location(latitude=latitude, longitude=longitude, bank_or_atm='bank')
		bot.sendLocation(chat_id=chat_id, latitude=nearest_latitude, longitude=nearest_longitude)
		logger.info('information sended')

	elif btn.btn_atm.strip() == db.get_last_element(chat_id=chat_id).strip():
		nearest_latitude, nearest_longitude = get_nearest_location(latitude=latitude, longitude=longitude, bank_or_atm='atm')
		bot.sendLocation(chat_id=chat_id, latitude=nearest_latitude, longitude=nearest_longitude)
	
	update.message.reply_text("Ближайшее место", reply_markup=create_main_keyboard(), parse_mode='HTML')

def db_add(bot, update):
	chat_id = update.message.chat_id
	text    = update.message.text.lstrip('/add ')
	db.add_item(item_text=text, chat_id=chat_id)
	# output_string = "Object stored text = {} with chat_id = {}".format(text, chat_id)
	output_string = 'Сохранил';
	update.message.reply_text(output_string, parse_mode='HTML')

def db_get_all(bot, update):
	chat_id = update.message.chat_id
	results = db.get_items(chat_id=chat_id)
	results = "\n".join(results)
	update.message.reply_text(results, parse_mode='HTML')

def db_get_last_element(bot, update):
	chat_id = update.message.chat_id
	results = db.get_last_element(chat_id=chat_id)
	update.message.reply_text(results, parse_mode='HTML')
	return results

def main():
	logger.info('Bot started')
	from settings import TOKEN
	# Create the Updater and pass it your bot's token.
	updater = Updater(TOKEN)

	logger.info('Updater started')
	updater.dispatcher.add_handler(CommandHandler('start', start))
	updater.dispatcher.add_handler(CommandHandler('add', db_add))
	updater.dispatcher.add_handler(CommandHandler('get_all', db_get_all))
	updater.dispatcher.add_handler(CommandHandler('get_last_element', db_get_last_element))

	#main_keyboard_handler
	updater.dispatcher.add_handler(MessageHandler(Filters.text, keyboard_handler))

	updater.dispatcher.add_handler(MessageHandler(Filters.location, location_handler))

	updater.dispatcher.add_handler(CallbackQueryHandler(button))
	updater.dispatcher.add_handler(CommandHandler('help', help))
	updater.dispatcher.add_error_handler(error)

	# Start the Bot
	logger.info('Pooling started')
	updater.start_polling()

	# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT
	updater.idle()


if __name__ == '__main__':
	main()
