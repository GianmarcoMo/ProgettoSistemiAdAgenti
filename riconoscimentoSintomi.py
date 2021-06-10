# -*- coding: utf-8 -*-

import json
f=open("res/datasetSymptomsIT.json")
y =f.read()

datasint = json.loads(y)


sintomi = {}
contatoresintomi = 0;

for sintomo in datasint:
    sintomi[sintomo["url"]] = sintomo["name"]
    contatoresintomi += 1;
f.close()


def riconoscimentoSintomo():
    inputSintomo = input().lower()
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
        print('Ho trovato diversi sintomi: ')
        for sintomo in listaSintomiDefinitiva:
            print('-',sintomo)
        print('\nPotresti specificarmi uno tra questi?')
        return 0
    else:
        if (len(listaSintomiDefinitiva) == 0):
            print('Non ho trovato nessun sintomo corrispondente alla tua descrizione. \nPotresti essere più preciso?')
            return 0
    
    return 1
    

print('Che sintomo hai?')
risultato = riconoscimentoSintomo()
while(risultato != 1):
    risultato = riconoscimentoSintomo()
