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

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
from data import id
import logging
import random
from telegram.emoji import Emoji

# timers in different chats
timers = dict()
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
evil_em = Emoji.SMILING_FACE_WITH_HORNS
start_em = Emoji.SMILING_FACE_WITH_OPEN_MOUTH
help_em = Emoji.SMILING_FACE_WITH_SMILING_EYES


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def alarm(bot, job):
    """Function to send the alarm message"""
    bot.sendMessage(job.context, text='Бип-бип! Таймер сработал!')


def set(bot, update, args, job_queue):
    """Adds a job to the queue"""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            bot.sendMessage(chat_id, text='Мы пока что не можем лететь в прошлое!')
            return

        # Add job to queue
        job = Job(alarm, due, repeat=False, context=chat_id)
        timers[chat_id] = job
        job_queue.put(job)

        bot.sendMessage(chat_id, text='Таймер установлен!')

    except (IndexError, ValueError):
        bot.sendMessage(chat_id, text='Используй формат: /set <seconds>')


def unset(bot, update, job_queue):
    """Removes the job if the user changed their mind"""
    chat_id = update.message.chat_id

    if chat_id not in timers:
        bot.sendMessage(chat_id, text='У вас нет активных таймеров')
        return

    job = timers[chat_id]
    job.schedule_removal()
    del timers[chat_id]

    bot.sendMessage(chat_id, text='Таймер остановлен!')



def start(bot, update):
    chat_id = update.message.chat_id
    txt = "" + "Hey, " + update.message.from_user.first_name + "! " + start_em + " " + "".join(dsc)
    bot.sendMessage(chat_id,
                    text=txt)


def help(bot, update):
    chat_id = update.message.chat_id
    bot.sendMessage(update.message.chat_id, "".join([cmd[0][:-1]] + [" " + help_em] + ["\n"] + cmd[1:]))


def get_timetable(bot, update, args):
    chat_id = update.message.from_user.id
    if not args:
        bot.sendMessage(chat_id, text='<strong>Расписание уроков класса 8-1:</strong>', parse_mode="HTML")
        for day in range(len(days)):
            bot.sendMessage(chat_id, text='<b>' + days[day] + ':</b>', parse_mode="HTML")
            bot.sendMessage(chat_id,
                            "\n".join([str(i + 1) + ". " + timetable[day][i] for i in range(len(timetable[day]))]))
    else:
        try:
            day = int(args[0])
            if day > len(days) or day < 1:
                bot.sendMessage(chat_id, text="Используй формат: /timet <?day at 1 to 6>")
                return
            day -= 1
            right_day = days[day].lower()
            if right_day[-1] == "а":
                right_day = right_day[:-1] + "у"
            bot.sendMessage(chat_id, text='<b>Расписание на ' + right_day + ':</b>', parse_mode="HTML")
            bot.sendMessage(chat_id,
                            "\n".join([str(i + 1) + ". " + timetable[day][i] for i in range(len(timetable[day]))]))
        except (ValueError, KeyError, IndexError):
            bot.sendMessage(chat_id, text="Используй формат: /timet <?day at 1 to 6>")


def get_mates(bot, update):
    chat_id = update.message.from_user.id
    ans = ""
    for mate in range(len(mates)):
        ans += str(mate + 1) + ". " + mates[mate] + "\n"
    bot.sendMessage(chat_id, text='<strong>Состав класса 8-1:</strong>', parse_mode="HTML")
    bot.sendMessage(chat_id, text=ans)


def text_echo(bot, update):
    chat_id = update.message.chat_id
    mess = update.message.text
    for hi in greetings:
        if len(mess) >= len(hi) and mess.lower()[:len(hi)] == hi:
            if update.message.from_user.id == id.MY_ID:
                sticker = el_stickers[random.randint(0, len(el_stickers) - 1)]
                bot.sendMessage(chat_id, text='Здравствуй, создатель ' + evil_em)
                bot.sendSticker(chat_id, sticker)

            else:
                sticker = stickers[random.randint(0, len(stickers) - 1)]
                bot.sendMessage(chat_id, text='Рад видеть, ' + update.message.from_user.first_name)
                bot.sendSticker(chat_id, sticker)
            break


def sticker_echo(bot, update):
    chat_id = update.message.chat_id
    if update.message.chat.id == id.MY_ID:
        bot.sendMessage(chat_id, text="Айдишник этого стикера:")
        bot.sendMessage(chat_id, text=update.message.sticker.file_id)


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
    dp.add_handler(CommandHandler("timet", get_timetable, pass_args=True))
    dp.add_handler(CommandHandler("set", set, pass_args=True, pass_job_queue=True))
    dp.add_handler(CommandHandler("unset", unset, pass_job_queue=True))
    dp.add_handler(CommandHandler("mates", get_mates))

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
    hello_stickers = open("data/stickers/hello_stickers.txt", "r")
    elite_stickers = open("data/stickers/elite_stickers.txt", "r")
    stickers = [s[:-1] for s in hello_stickers.readlines()]
    el_stickers = [s[:-1] for s in elite_stickers.readlines()]
    hello_stickers.close()
    elite_stickers.close()

    timeT = open("data/timetable.txt", "r")
    timetable = {}
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    for day in range(len(days)):
        read_line = timeT.readline()
        timetable[day] = []
        while read_line != "D\n":
            timetable[day].append(read_line[:-1])
            read_line = timeT.readline()

    cm = open("data/classmates.txt", "r")
    mates = [s[:-1] for s in cm.readlines()]

    commands = open("data/help_command.txt", "r")
    cmd = commands.readlines()
    commands.close()

    description = open("data/bot_description", "r")
    dsc = description.readlines()
    description.close()

    hellowrds = open("data/hello_words.txt", "r")
    greetings = [s[:-1] for s in hellowrds.readlines()]
    hellowrds.close()

    main()
