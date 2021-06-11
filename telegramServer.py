# -*- coding: utf-8 -*-

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import connDialog as diagFlow
import riconoscimentoSintomi
import bayesianMethod as bm

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
        if(messaggioUtente.lower() == 'stop'):
            utente.cambiaStatoSintomi()
            context.bot.send_message(chat_id=update.effective_chat.id, text="Ora controllo cosa hai...")
            # predizione malattia
            risultato = bm.prepredizioneMalattia(utente.getSintomi())
            context.bot.send_message(chat_id=update.effective_chat.id, text="Secondo i dati che miei fornito potresti avere: " + risultato)
        else:
            utente.SetRiconoscimento(riconoscimentoSintomi.riconoscimentoSintomo(messaggioUtente,update, context))
            if (utente.getRiconoscimento() != '0'):
                utente.getSintomi().append(utente.getRiconoscimento())
                utente.SetRiconoscimento('0')
            
            
    else:
        messaggioBot = diagFlow.invioMessaggioAgente(update.message.text) 
        if(messaggioBot == 'Dimmi che sintomi hai'
           or messaggioBot == 'Dimmi i tuoi dolori'):
            utente.cambiaStatoSintomi()
        context.bot.send_message(chat_id=update.effective_chat.id, text=messaggioBot)  
        
def gestoreMessaggi():     
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)     

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


