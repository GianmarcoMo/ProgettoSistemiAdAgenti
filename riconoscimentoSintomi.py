# -*- coding: utf-8 -*-

import json
from nltk.tokenize import word_tokenize

class classeSintomo:
    def __init__(self, url, sinonimiInput, nomeIt, descInput):
        self.url = url
        self.sinonimi = sinonimiInput
        self.nomeIT = nomeIt
        self.descrizione = descInput
        
    def setUrl(self, url):
        self.url = url
    def setSinonimi(self, listaSinonimi):
        self.sinonimi = listaSinonimi
    def setNomeIT(self, nomeItaliano):
        self.nomeIT = nomeItaliano
    def setDescrizione(self, descInput):
        self.descrizione = descInput
    
    def getNome(self):
        return self.nomeIT
    def getUrl(self):
        return self.url
    def getSinonimi(self):
        return self.sinonimi
    def getDescrizione(self):
        return self.descrizione
 
sw_list = {"ho","mi","sento","oggi","stamattina","prima","avevo","avuto"}

f=open("res/datasetSymptomsIT.json")
y =f.read()

datasint = json.loads(y)

sintomi = {}
contatoresintomi = 0;

for sintomo in datasint:
    sintomi[sintomo["url"]] = classeSintomo(sintomo["url"], sintomo['senses'], sintomo['name'], sintomo['descriptions'])
    contatoresintomi += 1;
f.close()


def riconoscimentoSintomo(inputSintomo,update, context):
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
    
    for sintomo in sintomi: # per ogni sintomo in malattia
        trovato = False

        if(inputSintomo in sintomi[sintomo].getNome().lower()): # Se l'input è nel nome, segnamo il trovato su true.
            trovato = True
        else:
            for sinonimo in sintomi[sintomo].getSinonimi(): # Se l'input non è nel nome, cerchiamo nei sinonimi
                if(inputSintomo in sinonimo.lower()):
                    trovato = True
                    break
            # Se l'input non è nei sinonimi, cerchiamo nella descrizione
            if(trovato == False and inputSintomo in sintomi[sintomo].getDescrizione()):
                trovato = True
            
        # Se il sintomo è stato trovato, inseriamo il vero nome del sintomo in una lista.
        if(trovato):
            listaSintomiDefinitiva.append(sintomi[sintomo])
        
    if(len(listaSintomiDefinitiva) > 1):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Ho trovato diversi sintomi: ')
        for sintomo in listaSintomiDefinitiva:
            context.bot.send_message(chat_id=update.effective_chat.id, text='- ' + sintomi[sintomo].getNome())
        context.bot.send_message(chat_id=update.effective_chat.id, text='Potresti specificarmi uno tra questi?')
        return '0'
    else:
        if (len(listaSintomiDefinitiva) == 0):
            #print('Non ho trovato nessun sintomo corrispondente alla tua descrizione. \nPotresti essere più preciso?')
            context.bot.send_message(chat_id=update.effective_chat.id, text='Non ho trovato nessun sintomo corrispondente alla tua descrizione. \nPotresti essere più preciso?')
            return '0'
    
    #Quando la lista è formata da solo un sintomo
    context.bot.send_message(chat_id=update.effective_chat.id, text=listaSintomiDefinitiva[0].getNome())
    return listaSintomiDefinitiva[0]
    

def predizioneMalattia(listaSintomiUtente):   
    f=open("res/datasetConditionsIT.json")
    
    x =f.read()
    
    data = json.loads(x)
    f.close()

    risultati = {}
    for malattia in data:
        probabilita = 1;
        denominatore = 0;
        sintomimatchati = 0
        
        for sintomoMalattia in malattia["symptoms"]:  
            for sintomoutente in listaSintomiUtente:
                if (sintomoutente.getUrl() == sintomoMalattia["name"]):
                    probabilita = probabilita * sintomoMalattia["probability"] /100 
                    denominatore += probabilita
                    sintomimatchati += 1
                    
        if (denominatore != 0):
            probabilita += sintomimatchati
            risultati[malattia["name"]] = probabilita/(denominatore + contatoresintomi)
            
    maxProbability = max(risultati, key=risultati.get) # Just use 'min' instead of 'max' for minimum.
    print(maxProbability)
    return maxProbability
