import numpy as np
import matplotlib.pyplot as plt

#Toyota Avensis Verso
#aarsmodell, km-stand, pris 
avensisverso = [[2004,222000,57500,'Vikhammer OK'],
				[2004,255000,49500,'Mandal OK+'],
				[2004,201000,63000,'Oslo (ref)'],
				[2002,250000,46500,'Oslo -1'],
				[2004,283000,68500,'Heimdal --'],
				[2005,151000,74500,'Oslo (auksjon)'],
				[2002,207000,53500,'Vassoy'],
				[2004,231000,79900,'Trondheim']]

alder	= [2015-bil[0]  for bil in avensisverso]
km		= [bil[1]/1000. for bil in avensisverso]
pris	= [bil[2]/1000. for bil in avensisverso]

plt.plot(km,pris,'*')
for bil in avensisverso:
	plt.text(bil[1]/1000.0,bil[2]/1000.0,bil[3])

plt.ylabel("Pris (kkr)")
plt.xlabel("Km-stand (kkm)")
plt.ylim(0,100)
plt.xlim(0,350)
plt.grid()
plt.show()
