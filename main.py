'''
Simple Telegram Bot
which making screenshots and sending messages to user
created on telebot module


functions:
get_text_messages(message) - getting commands from user
available:
     /start      -   Message for choosing language (RU or ENG) with user choice buttons
                     after choosing write hello message in chosen lang(the next messages will be too
     /screenshot -  Message for choosing screenshot format (available formats: png,jpg,pdf)
                     After choosing user should write url with /site command
     /site url   -   Making screenshot, writing message for user "Checking"
                     After making screenshot - message changing,
                                               it have available button "More" to get more information of url
                                               with WHOIS module
                     Then screenshot in needed data format sending to user

     /help       -   All available commands

callback_worker(message) - handler for buttons

Working with files:
screenshot.py - make screenshot and check url
language_handler.py - handler for languages (work dir languages/eng.py and rus.py to add a lang)
search_whois.py - WHOIS checker

Also working with logging:
log.conf - file for configuration of logging
app.log - output of logging
(also logging going in console)

'''
import telebot
from telebot import types
from screenshot import screenshotmaker
from language_handler import Translate
from search_whois import search_info
from screenshot import findurl
import logging
import logging.config
from datetime import datetime
from pathlib import Path
import time
import os
import lxml.html
#from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
from database_add import add_new_row

load_dotenv()
user = ''
format = ''
url = ''
name=''
TOKEN = os.getenv('TOKEN')

logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logger.debug('Debug message')


print('Telegram Bot screenshot website starting . . .')

'''
Simple realization of Bot
'''
bot = telebot.TeleBot(TOKEN)

'''
Asynchronous TeleBot
to use add async for bot functions
also add commands:
 - import asyncio
 - tb = AsyncTeleBot(TOKEN)
 - asyncio.run(bot.polling()) 
'''


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global url
    if message.text =="/start":
        keyboard_lang = types.InlineKeyboardMarkup(row_width=2)
        key_eng = types.InlineKeyboardButton(text="English", callback_data='eng')
        key_ru = types.InlineKeyboardButton(text="Russian", callback_data='rus')
        keyboard_lang.row(key_eng,key_ru)
        bot.send_message(message.from_user.id, "Choose your language", reply_markup=keyboard_lang)
    if message.text =="/screenshot":
        keyboard_format = types.InlineKeyboardMarkup(row_width=3)
        key_png = types.InlineKeyboardButton(text="png", callback_data='png')
        key_jpg = types.InlineKeyboardButton(text="jpg", callback_data='jpg')
        key_pdf = types.InlineKeyboardButton(text="pdf", callback_data='pdf')
        keyboard_format.row(key_png, key_jpg, key_pdf)
        bot.send_message(message.from_user.id, user.message_answer("format"), reply_markup=keyboard_format)
    if "/site" in message.text:
        url = findurl(message.text)
        message = bot.send_message(message.from_user.id, user.message_answer("check"))
        if len(url) != 0:
            now = datetime.now()
            current_time = now.strftime("%m%d")
            url_formatted = url[0]
            replacement_strings = ['.', 'https', 'http', ':', '//', '/', '-']
            for string in replacement_strings:
                if string in url_formatted:
                    url_formatted = url_formatted.replace(string,'')
            filename = current_time + name + url_formatted
            start_time = time.time()
            a = screenshotmaker(url[0], format, filename)
            time_screenshot = time.time() - start_time
            print(f"Working time of sreenshotmaker {time_screenshot}")
            try:
                t = lxml.html.parse(url[0])
                title = t.find(".//title").text
            except OSError:
                print("Error in parsing")
                logger.exception("Exception occurred in parser - OSError")
                title = url_formatted
            key = telebot.types.InlineKeyboardMarkup()
            but = telebot.types.InlineKeyboardButton(text=user.message_answer("more"), callback_data=user.message_answer("more"))
            key.add(but)
            bot.edit_message_text(chat_id=message.chat.id,
                                  text = (user.message_answer("result") +
                                          title + "\n" +
                                          url[0] + "\n" +user.message_answer("time") +
                                          str(time_screenshot)[:5] + "s"),
                                  message_id=message.message_id,
                                  reply_markup=key)
            #if Path('screens/' + filename+'.'+format, 'rb').is_file():
            image = open('screens/' + filename+'.'+format, 'rb')
            bot.send_document(message.chat.id, image)
        else:
            bot.send_message(message.from_user.id, user.message_answer("wrong"))
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Commands:\n"
                                               "/start \n"
                                               "/screenshot\n"
                                               "/site url\n"
                                               "For start write /start and choose language\n")


@bot.callback_query_handler(func = lambda call: True)
def callback_worker(message):
    global user
    global format
    global name
    if message.data == "eng" or message.data =="rus":
        print(f"Choosed language {message.data}")
        name = message.from_user.username
        user = Translate(message.data)
        bot.send_message(message.from_user.id, user.message_answer("hello"))
        #add_new_row(name,'start'+',lang:'+ message.data)  --- for the statistics in db
    elif message.data == "png" or message.data =="jpg" or message.data == "pdf":
        print(f"Choosed data format {message.data}")
        format = message.data
        bot.send_message(message.from_user.id, user.message_answer("site"))
    elif message.data == "More" or message.data =="Подробнее":
        print(f"Choosed button {message.data}")
        print(f"Checking url: {url}")
        bot.send_message(message.from_user.id, search_info(url[0]))

bot.polling(none_stop=True, interval=0)
