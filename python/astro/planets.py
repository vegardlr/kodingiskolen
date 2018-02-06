import ephem
import matplotlib.pyplot as plt

date = ephem.date('2015/02/21')
mars = ephem.Mars()

ra = []
dec = []

for i in range(700):
	mars.compute(date)
	ra.append(mars.ra)
	dec.append(mars.dec)
	date = date+1

plt.plot(ra,dec)
plt.title('Mars')
plt.ylabel('Dec.')
plt.xlabel('R.A.')
plt.show()
