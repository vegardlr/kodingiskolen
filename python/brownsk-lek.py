#LEK MED BROWNSK GANGE
#
#Programmet lager en enkel lek av brownsk (tilfeldig) 
#bevegelse. En blaa strek vil starte fra origo
#i et aksekors. Fra origo vil den bevege seg med 
#tilfeldig steglengde (0-1) og i tilfeldig retning
#(0-360 grader) hvert tidsteg.
#
#Hvis streken treffer firkanten (maal/target), vinner spilleren
#Hvis streken treffer sirkelen, taper spilleren. 



#Vi trenger aa importere noen python-biblioteker
from math import sin,cos,pi,sqrt
from random import uniform
import matplotlib.pyplot as plt

#Beskriv maal (target) og sirkel med koordinater 
#som vi skal tegne etterpaa
#Maal (target): Et rektangel
xmin,xmax = 5,7
ymin,ymax = -2,2
targetx = [xmin,xmax,xmax,xmin,xmin]
targety = [ymax,ymax,ymin,ymin,ymax]
#Spillets yttergrense: En stor sirkel
rmax = 10.0
circlex = [rmax*cos(2.0*pi*i/100.) for i in range(0,101)]
circley = [rmax*sin(2.0*pi*i/100.) for i in range(0,101)]

#Naa skal vi aapne og definere et vindu hvor vi skal 
#tegne streken, yttergrensen og maal.
#Bestem vinduets yttergrenser
plt.axis([-rmax,rmax,-rmax,rmax])
#Gjoer vinduet kvadratisk
plt.axis('equal')
#Merk aksene med en 'x' og 'y'
plt.ylabel('y')
plt.xlabel('x')
#Aapne et vindu som kan tegnes paa flere ganger
#uten at vinduet skrives over eller toemmes
plt.ion()
#Tegn firkanten (target)
plt.plot(targetx,targety,'green')
#Tegn yttergrensen r=rmax (sirkel)
plt.plot(circlex,circley,'red')
#Vi maa lagre en python-ting som heter 'Axis'
#som vi skal bruke til aa endre bakgrunnsfargen
ax = plt.gca()
#Sett bakgrunnsfargen foer start
ax.set_facecolor("yellow")

#Startposisjon (origo)
x = 0.0
y = 0.0
r = 0.0

#Her starter moroa!
#Vi starter en loekke som aldri stopper av seg selv (while True), 
#men vi vil legge inn 'break' kommandoer lenger ned som 
#stopper den slik vi oensker det lengre ned. 
while True:
	#Her regner vi ut hvor streken skal gaa (tilfeldige tall)
	dr = uniform(0,1)		#Steglengde
	vinkel = uniform(0,2*pi)#Stegretning
	dx = dr*cos(vinkel)		#Finn x-komponent av steget
	dy = dr*sin(vinkel)		#Finn y-komponenten av steget
	#dx = uniform(-1,1)
	#dy = uniform(-1,1)
	
	#Tegn en strek som viser det siste steget
	#fra forrige (x,y) til ny (x+dx,y+dy) oppdatert posisjon
	plt.plot([x,x+dx],[y,y+dy],'blue')

	#Lagre den nye posisjonen
	x += dx
	y += dy
	r = sqrt(x**2 + y**2)
	
	#Sjekk om streken har truffet maal (target)
	if x > xmin and x < xmax and y > ymin and y < ymax:
		#Hvis ja, sett groenn bakgrunnsfarge
		ax.set_facecolor("green")
		#Stopp programmet
		break

	#Sjekk om streken har truffet yttergrensen (sirkelen)
	if r > rmax:
		#Hvis ja, sett roed bakgrunnsfarge
		ax.set_facecolor("red")
		#Stopp programmet
		break

	#Vent litt foer vi regner ut og tegner neste steg
	plt.pause(0.01)

#Denne loekkken holder vinduet aapent og synlig
#fram til noen avbryter programmet manuelt
while True:
	plt.pause(0.05)


