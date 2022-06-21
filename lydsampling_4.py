# Et program som tar opp lyd i tre sekunder og finner tid mellom to lydimpulser.
import pyaudio
import numpy as np

chunk = 1024  # Opptak i "klumper" med 1024 målinger
sample_format = pyaudio.paInt16  # 16 bits per måling
channels = 2 # Tar opp i to kanaler
fs = 44100  # Tar opp med 44100 målinger per sekund
seconds = 3

p = pyaudio.PyAudio()  # Lager et grensesnitt til PortAudio

print('Gjør opptak')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Klargjør og tømmer et array til å lagre bitene med opptak

# Lagrer data i klumper i tre sekunder.
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)

# Stopper og lukker datainnsamlingen 
stream.stop_stream()
stream.close()
# Avslutter grensesnittet til Pyaudio
p.terminate()

print('Opptak utført')

# Konverterer listen med dataene til et array
are=np.array(frames)
#Konverterer arrayet med data fra hexadesimale koder til heltall mellom -32 768 til 32767
signal_gm = np.frombuffer(are, dtype='int16')

#Funksjon som tar ei liste og en tallverdi som er avstand fra største verdi og returnerer ei liste med indekser til høye verdier 
def storsteVerdierIArray(liste, avstandFraStorste):
    maxIndexList = list() #Deklarerer liste for indekser
    verdierList = list() #Deklarerer liste før de høyeste verdiene. Kan sløyfes.
    index = 0 #definerer index
    storste=max(liste) #Finner største verdi i lista som er sendt inn
    #print('Største er ',storste)
    for j in liste: # Går gjennom lista med dataverdiene for å finne indeks til høyeste verdier.
        if j>=(storste-avstandFraStorste): #sjekker om verdi i lista er stor nok til å bli registrert.
            maxIndexList.append(index) #lagrer index til høye verdier
            verdierList.append(j) #lagrer høye målte verdier i form av tall. Kan sløyfes.
        index=index+1 #inkrementerer index
        
    print('Print av maxIndexList: ',maxIndexList) #Skriver ut lista med indekser til de høyeste verdiene. Kan sløyfes.
    print('Print av verdiList: ',verdierList) #Skriver ut lista med de høyeste verdiene. Kan sløyfes.
    return maxIndexList # Sender tilbake ei liste med indekser til de høyeste dataverdiene.
    

maxList = storsteVerdierIArray(signal_gm,500) # Finner liste med indekser for verdier som er inntil 500 fra største verdi.
maxList.sort() # Sorterer lista i stigende rekkefølge
listeLengde = len(maxList) # Finner antall listeverdier.
#print('Makslista: ',maxList)
# Hvis lista har mer enn to verdier skriver man ut tiden mellom de høye målingene.
if listeLengde>1:
    print('Tid: ',(maxList[listeLengde-1]-maxList[0])/(channels*fs)) # Skriver ut tid. Beregnet som differanse mellom indeks til to høye målinger i forhold til antall målinger per sekund.
    

