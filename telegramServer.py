# -*- coding: utf-8 -*-

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import telegram


import logging
import connDialog as diagFlow
import riconoscimentoSintomi


class Persona:
    def __init__(self):
        self.statoSintomi = False
        self.nome = ''
        self.cognome = ''
        self.eta = 0
        self.sintomi = list()
        self.riconocimento = '0'
        
    def cambiaStatoSintomi(self):
        if(self.statoSintomi):
            # Si attiva l'acquisizione dei sintomi
            self.statoSintomi = False
        else: 
            # Si disattiva l'acquisizione dei sintomi
            self.statoSintomi = True

    def inserisciNome(self, nome):
        self.nome = nome

    def inserisciCognome(self, cognome):
        self.cognome = cognome
        
    def inserisciEta(self, eta):
        self.eta = eta
    
    def getStato(self):
        return self.statoSintomi

    def getSintomi(self):
        return self.sintomi
    
    def getRiconoscimento(self):
        return self.riconocimento
    
    def SetRiconoscimento(self,inpututente):
        self.riconocimento = inpututente
   
    

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao sono il bot Campa100anni!\nCome posso aiutarti?")

def echo(update, context):
    # Se l'utente è entrato nello stato per prendere i sintomi
    if(utente.getStato()):
        messaggioUtente = update.message.text
        
        
        if("mostra" in messaggioUtente.lower() and "sintomi" in messaggioUtente.lower()):
            if (len(utente.getSintomi())!=0):
                mostraChatSintomiAcquisiti(update, context)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Scusami, non ho ancora compreso nessun sintomo")

        
        
        elif(messaggioUtente.lower() == 'no' or messaggioUtente.lower() == 'stop' or messaggioUtente.lower()=="non ho altri sintomi"):
            #se abbiamo acquisito sintomi
            if (len(utente.getSintomi())!=0):
                utente.cambiaStatoSintomi()
                mostraChatSintomiAcquisiti(update, context)
                context.bot.send_message(chat_id=update.effective_chat.id, text="Ora controllo cosa hai...")
                # predizione malattia
                risultato = riconoscimentoSintomi.predizioneMalattia(utente.getSintomi())
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Secondo i dati che miei fornito potresti avere: *{risultato.getNome()}*", parse_mode=telegram.ParseMode.MARKDOWN)
                if (risultato.getLinkWiki()!=None):
                    context.bot.send_message(chat_id=update.effective_chat.id, text=risultato.getLinkWiki())
                else:
                     context.bot.send_message(chat_id=update.effective_chat.id, text=risultato.getDescrizione()[0])
            else:
                #se abbiamo acquisito sintomi
                context.bot.send_message(chat_id=update.effective_chat.id, text="Scusami, non ho ancora compreso nessun sintomo, non posso avviare la predizione della malattia. \nQuale sintomo credi di avere?")
                utente.SetRiconoscimento('0')

        else:
            if(messaggioUtente.lower() == 'si'):
                 context.bot.send_message(chat_id=update.effective_chat.id, text="Cos'altro credi di avere?")
                 utente.SetRiconoscimento('0')
            elif(messaggioUtente.lower() == 'conferma'):
                utente.getSintomi().append(riconoscimentoSintomi.conferma())
                context.bot.send_message(chat_id=update.effective_chat.id, text="Sintomo acquisito correttamente.\nHai altri sintomi?")
                utente.SetRiconoscimento('0')
            else:
                utente.SetRiconoscimento(riconoscimentoSintomi.riconoscimentoSintomo(messaggioUtente,update, context, dispatcher, updater))
                if (utente.getRiconoscimento() != '0'):
                    if(utente.getRiconoscimento() in utente.getSintomi()):
                         context.bot.send_message(chat_id=update.effective_chat.id, text="Sintomo già acquisito in precedenza, inserire un *nuovo sintomo* o digitare *stop*",parse_mode=telegram.ParseMode.MARKDOWN)
                    else:
                        utente.getSintomi().append(utente.getRiconoscimento())
                        context.bot.send_message(chat_id=update.effective_chat.id, text="Sintomo acquisito correttamente.\nHai altri sintomi?")
                    utente.SetRiconoscimento('0')
            
    else:
        messaggioBot = diagFlow.invioMessaggioAgente(update.message.text) 
        if("Mi dispiace" in messaggioBot):
            utente.cambiaStatoSintomi()
        context.bot.send_message(chat_id=update.effective_chat.id, text=messaggioBot)
        
def gestoreMessaggi():     
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)     

def mostraChatSintomiAcquisiti(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Per adesso i sintomi che ho inserito sono:")
    for sintomo in utente.getSintomi():
         context.bot.send_message(chat_id=update.effective_chat.id, text=f"- {sintomo.getNome()}")
# -------------------------------------------------------------
utente = Persona()

updater = Updater(token='1624193679:AAEllin0OJLmKcU5c0rDfzL99yKi9QudgSA', use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()

gestoreMessaggi()


