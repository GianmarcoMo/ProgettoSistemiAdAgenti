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

data = json.loads(x)


risultati = {}
for malattia in data:
    probabilita = 1;
    denominatore = 0;
    sintomimatchati = 0
    
    for sintomo in malattia["symptoms"]:  
        for sintomoutente in listaSintomiUtente:
            if (sintomoutente == sintomo["name"]):
                probabilita = probabilita * sintomo["probability"] /100 
                denominatore += probabilita
                sintomimatchati += 1
                
    if (denominatore != 0):
        probabilita += sintomimatchati
        risultati[malattia["name"]] = probabilita/(denominatore + contatoresintomi)
        


maxProbability = max(risultati, key=risultati.get)  # Just use 'min' instead of 'max' for minimum.

print(maxProbability)




#print(sorted(risultati.items(), key=lambda x: x[1]))


