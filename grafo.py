# Coda con priorita' per creare la frontiera 
from queue import PriorityQueue
# put per inserire
# get per prendere

class StrutturaMappa():
    def __init__(self):
        self.mappa = dict()
    
    def aggiungiVia(self, viaInput):
        # inserisce nodo senza collegamento e senza peso
        self.mappa.update({viaInput : list()})
    
    # Aggiorna il nodo con il valore uguale a viaPartenza
    # se non esiste, ne crea uno nuovo
    def aggiungiCollegamento(self, viaPartenza, viaArrivo, pesoArco):
        # Peso espresso in metri
        self.mappa[viaPartenza].append({viaArrivo : pesoArco})
        
    
    def visualizzaStrade(self):
        for strade in self.mappa:
            print(strade)
    
    def visualizzaCollegamenti(self):
        for strade in self.mappa.keys():
            print('Strada: ', strade)
            print('Collegata con: ')
            
            for collegamento in self.mappa.get(strade):
                chiavi = list(collegamento.keys())
                for chiave in chiavi:
                    print('\t',chiave,' distanza:',collegamento.get(chiave),'metri')
            print('\n')
    
    def getVicini(self, viaPartenza):
        return self.mappa.get(viaPartenza)
    
    # Restituisci il costo dato un elemento preso dall'insieme dei vicini
    def getCosto(self, elementoInsiemeVicini):
        # Trasformo l'elemento in lista, e prendo l'unico elemento in posizione 0 (unico)
        chiave = list(elementoInsiemeVicini.keys())[0]
        # Restituisco il valore della chiave, ovvero il costo
        return elementoInsiemeVicini.get(chiave)
           
        
        
        
        
        
        
            

# Oggetto 
mappa = StrutturaMappa()

# Inserimento delle strade senza archi
mappa.aggiungiVia("Via Capruzzi")
mappa.aggiungiVia("Via Policlinico")
mappa.aggiungiVia("Viale Aviatori")
mappa.aggiungiVia("Via Marcuzzi")
mappa.aggiungiVia("Via Napoli")
mappa.aggiungiVia("Corso Roma")
mappa.aggiungiVia("Via Lattea")
mappa.aggiungiVia("Via degli Dei")
mappa.aggiungiVia("Via delle querce")
mappa.aggiungiVia("Viale del Todis")
mappa.aggiungiVia("Corso Umberto Primo")

# Inserimento degli archi con peso (metri)
mappa.aggiungiCollegamento('Via Capruzzi','Via Marcuzzi', 200)

mappa.aggiungiCollegamento('Via Policlinico','Viale Aviatori', 100)

mappa.aggiungiCollegamento('Viale Aviatori','Via Policlinico', 100)
mappa.aggiungiCollegamento('Viale Aviatori','Via Marcuzzi', 100)
mappa.aggiungiCollegamento('Viale Aviatori','Via Napoli', 100)

mappa.aggiungiCollegamento('Via Marcuzzi','Via Capruzzi', 200)
mappa.aggiungiCollegamento('Via Marcuzzi','Viale Aviatori', 200)

mappa.aggiungiCollegamento('Via Napoli','Viale Aviatori', 100)

mappa.aggiungiCollegamento('Corso Roma','Corso Giannone', 100)

mappa.aggiungiCollegamento('Via Lattea','Via degli Dei', 200)
mappa.aggiungiCollegamento('Via Lattea','Via delle querce', 400)

mappa.aggiungiCollegamento('Via degli Dei','Via Lattea', 200)
mappa.aggiungiCollegamento('Via degli Dei','Viale del Todis', 200)

mappa.aggiungiCollegamento('Via delle querce','Via Lattea', 400)
mappa.aggiungiCollegamento('Via delle querce','Corso Umberto Primo', 200)

mappa.aggiungiCollegamento('Viale del Todis','Via degli Dei', 200)

mappa.aggiungiCollegamento('Corso Umberto Primo','Via delle querce', 200)
#----------------------------------------------------------------------

#vicino = mappa.getVicini('Viale Aviatori')[0]
#print(mappa.getCosto(vicino))

