# -*- coding: utf-8 -*-

import json
from nltk.tokenize import word_tokenize
sw_list = {"ho","mi","sento","oggi","stamattina","prima","avevo","avuto"}


f=open("res/datasetSymptomsIT.json")
y =f.read()

datasint = json.loads(y)


sintomi = {}
contatoresintomi = 0;

for sintomo in datasint:
    sintomi[sintomo["url"]] = sintomo["name"]
    contatoresintomi += 1;
f.close()


def riconoscimentoSintomo(inputSintomo,update, context):
    #inputSintomo = input().lower()
    inputSintomo = inputSintomo.lower()
    #Tokenize input
    text_tokens = word_tokenize(inputSintomo)
    #Tokenize input ed eliminazione stopwords
    tokens_without_sw = [word for word in text_tokens if not word in sw_list]
    inputSintomo = ''
    #Ricompongo stringa utente stenza sw
    for token in tokens_without_sw:
        inputSintomo += token + ' '
    #elimino spazio finale del for
    inputSintomo = inputSintomo[:-1]
    if (inputSintomo == ''):
         context.bot.send_message(chat_id=update.effective_chat.id, text='Non ho trovato nessun sintomo corrispondente alla tua descrizione. \nPotresti essere più preciso?')
         return '0'
    listaSintomiDefinitiva = list()
    
    for sintomo in datasint: # per ogni sintomo in malattia
        trovato = False
        if(inputSintomo in sintomo["name"].lower()): # Se l'input è nel nome, segnamo il trovato su true.
            trovato = True
        else:
            for sinonimo in sintomo["senses"]: # Se l'input non è nel nome, cerchiamo nei sinonimi
                if(inputSintomo in sinonimo.lower()):
                    trovato = True
                    break
            # Se l'input non è nei sinonimi, cerchiamo nella descrizione
            if(trovato == False and inputSintomo in sintomo["descriptions"]):
                trovato = True
            
        # Se il sintomo è stato trovato, inseriamo il vero nome del sintomo in una lista.
        if(trovato):
            listaSintomiDefinitiva.append(sintomo["name"])
        
    if(len(listaSintomiDefinitiva) > 1):
        #print('Ho trovato diversi sintomi: ')
        context.bot.send_message(chat_id=update.effective_chat.id, text='Ho trovato diversi sintomi: ')
        for sintomo in listaSintomiDefinitiva:
            #print('-',sintomo)
            context.bot.send_message(chat_id=update.effective_chat.id, text='- ' + sintomo)
        #print('\nPotresti specificarmi uno tra questi?')
        context.bot.send_message(chat_id=update.effective_chat.id, text='Potresti specificarmi uno tra questi?')
        return '0'
    else:
        if (len(listaSintomiDefinitiva) == 0):
            #print('Non ho trovato nessun sintomo corrispondente alla tua descrizione. \nPotresti essere più preciso?')
            context.bot.send_message(chat_id=update.effective_chat.id, text='Non ho trovato nessun sintomo corrispondente alla tua descrizione. \nPotresti essere più preciso?')
            return '0'
    
    #Quando la lista è formata da solo un sintomo
    context.bot.send_message(chat_id=update.effective_chat.id, text=listaSintomiDefinitiva[0])
    return listaSintomiDefinitiva[0]
    

#print('Che sintomo hai?')
#risultato = riconoscimentoSintomo()
#while(risultato != 1):
#    risultato = riconoscimentoSintomo()
