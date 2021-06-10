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


listaSintomiUtente = ["http://www.symcat.com/symptoms/abnormal-appearing-skin",
                      "http://www.symcat.com/symptoms/acne-or-pimples",
                      "http://www.symcat.com/symptoms/skin-rash"]


f=open("res/datasetConditionsIT.json")

x =f.read()

dataMalattie = json.loads(x)



listacopia = dataMalattie.copy()

for sintomo in listaSintomiUtente:
    for malattia in dataMalattie:
        trovato = False
        for sintomomalattia in malattia["symptoms"]:
            if sintomomalattia["name"] == sintomo:
                trovato = True
        if trovato == False:       
            listacopia.remove(malattia)
    dataMalattie = listacopia.copy()
          
dictMalattia = {}
    
for malattia in dataMalattie:
    risultato = 1
    for sintomo in malattia["symptoms"]:
        if sintomo["name"] in listaSintomiUtente:
            risultato *= sintomo["probability"]
    dictMalattia[malattia["name"]] = risultato
    
    
maxProbability = max(dictMalattia, key=dictMalattia.get)
print(maxProbability)
#print(sorted(dictMalattia.items(), key=lambda x: x[1]))