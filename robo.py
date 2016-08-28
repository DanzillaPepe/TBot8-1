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

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    txt = "".join(description.readlines())
    bot.sendMessage(update.message.chat_id, text="<b>" + txt + "</b>", parse_mode="HTML")


def help(bot, update):
    bot.sendMessage(update.message.chat_id, "".join(commands))

def schedule(bot, update):
    bot.sendMessage(update.message.chat_id, text='Расписание уроков: бла-бла-бла')


def text_echo(bot, update):
    mess = update.message.text
    for hi in greetings:
        if hi in mess.lower():
            bot.sendMessage(update.message.chat_id, text='Рад видеть, ' + update.message.from_user.first_name)
            bot.sendSticker(update.message.chat_id, "BQADAgADBwADW__yCiAy3DULmbfPAg")


# def sticker_echo(bot, update):
#     # bot.sendMessage(update.message.chat_id, text="Айдишник этого стикера:")
#     # bot.sendMessage(update.message.chat_id, text=update.message.sticker.file_id)


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
    # dp.add_handler(MessageHandler([Filters.sticker], sticker_echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    commands = open("help_command.txt", "r")
    description = open("bot_description", "r")
    greetings = ["hello", "привет", "ку", "драсьте", "дравствуйте", "hi"]
    main()
    commands.close()
