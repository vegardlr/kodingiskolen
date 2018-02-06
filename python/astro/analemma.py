import ephem
import matplotlib.pyplot as plt

#Definer foerst et sted hvor vi skal 
#observere solen fra.
#Tilpass variable sted.lat og sted.lon
#om dere oensker f.eks. Moss
sted = ephem.Observer()
sted.date = '2016/01/01 12:00:00'
sted.lat = '85.0'
sted.lon = '10.0'

#Biblioteket vet hva solen er, vi maa bare
#opprette en lenke fra vaar kode til Solen
#i PyEphem
sol = ephem.Sun()

#Tomme lister hvor vi skal lagre data
#Disse skal vi plotte siden
alt = []
az = []

#Vi vil ogsaa ha merkelapper i plottet 
#som sier hvor paa analemmaet vi finner
#utvalgte datoer
merker = []
malt = []
maz = []

#Saa en for-loekke hvor vi tar 365 steg. Verdien av
#for-variablen 'day' brukes ikke til noe
for day in range(0,365):

	#Beregner solens posisjon sett fra 'sted' 
	sol.compute(sted)

	#Legg til solens posisjon i datalistene
	alt.append(float(sol.alt)*180.0/ephem.pi)
	az.append(float(sol.az)*180.0/ephem.pi)

	#Lagre dato som en tuple (tuple = vektor)
	#d[2] = dag i maaneden
	#d[1] = maaned-nr
	d = sted.date.tuple()

	#Hvis det er den foerste dagen i en maaned 
	#eller datoen er 21/3, 21/6, 21/9 eller 21/12, 
	#("x%3==0" tester om x er delelig med 3)
	#lag en merkelapp i plottet med dato paa rett posisjon
	if d[2]==1 or (d[2]==21 and d[1]%3==0):

		#Legg til et tekst-element i merker-listen
		#med formatet 'dag/maaned'
		merker.append("%s/%s"%(d[2],d[1]))

		#Lagre solens posisjon denne dagen slik
		#at vi kan sette merkelappen paa samme 
		#plass som grafen i plottet
		maz.append(az[-1])
		malt.append(alt[-1])
	
	#Oek steget med 1 dag foer neste 
	#gjennomgang av for-loekken
	sted.date = ephem.Date(sted.date+1)

#Plott dataene
plt.plot(az,alt)

#Plott merkelappene 
for i in range(0,len(merker)):
	plt.plot(maz[i],malt[i],'+',color='blue')
	plt.text(maz[i],malt[i],merker[i])

#Tekst paa aksene
plt.ylabel('Altitude')
plt.xlabel('Azimuth')
plt.title('Analemma\nLat=%s Lon=%s ' % (sted.lat,sted.lon))

#Merk de spesielle solhoeydene
x = [min(az),max(az)]
y = 90.0 - float(sted.lat)*180/ephem.pi
plt.plot(x,[y,y])
plt.plot(x,[y-23.5,y-23.5])
plt.plot(x,[y+23.5,y+23.5])

#Vis bildet
plt.show()
