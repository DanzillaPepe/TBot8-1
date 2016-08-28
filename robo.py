#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json
import random

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    txt = "<em>" + "Hey, " + update.message.from_user.first_name + "! " + "".join(
        description.readlines()) + "</em>"
    bot.sendMessage(update.message.chat_id,
                    text=txt,
                    parse_mode="HTML")


def help(bot, update):
    bot.sendMessage(update.message.chat_id, "".join(commands))


def schedule(bot, update):
    bot.sendMessage(update.message.chat_id, text='Расписание уроков:')


def text_echo(bot, update):
    mess = update.message.text
    for hi in greetings:
        if len(mess) >= len(hi) and mess.lower()[:len(hi)] == hi:

            if update.message.from_user.id == 211754983:
                sticker = el_stickers[random.randint(0, len(el_stickers) - 1)]
                bot.sendMessage(update.message.chat_id, text='Здравствуй, создатель')
                bot.sendSticker(update.message.chat_id, sticker)
            else:
                sticker = stickers[random.randint(0, len(stickers) - 1)]
                bot.sendMessage(update.message.chat_id, text='Рад видеть, ' + update.message.from_user.first_name)
                bot.sendSticker(update.message.chat_id, sticker)
            break


def sticker_echo(bot, update):
    if update.message.chat.id == 211754983:
        bot.sendMessage(update.message.chat_id, text="Айдишник этого стикера:")
        bot.sendMessage(update.message.chat_id, text=update.message.sticker.file_id)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    token = open("token.txt", "r")
    token_name = token.readline()
    token.close()
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token_name)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("timetable", schedule))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler([Filters.text], text_echo))
    dp.add_handler(MessageHandler([Filters.sticker], sticker_echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    hello_stickers = open("hello_stickers.txt", "r")
    elite_stickers = open("elite_stickers.txt", "r")
    stickers = [s[:-1] for s in hello_stickers.readlines()]
    el_stickers = [s[:-1] for s in elite_stickers.readlines()]

    commands = open("help_command.txt", "r")
    description = open("bot_description", "r")
    greetings = ["hello", "привет", "драсьте", "дравствуйте", "hi", "дарова", "здравствуйте"]
    main()
    commands.close()
    hello_stickers.close()
