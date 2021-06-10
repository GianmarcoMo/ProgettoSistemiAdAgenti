# -*- coding: utf-8 -*-

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import connDialog as diagFlow
import main as 

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao sono il bot Campa100anni! \nCome posso aiutarti?")


def echo(update, context):
    messaggioBot = diagFlow.invioMessaggioAgente(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=messaggioBot)

def inputSintomiUtente(inputUtente):
    

updater = Updater(token='1624193679:AAEllin0OJLmKcU5c0rDfzL99yKi9QudgSA', use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

    
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

