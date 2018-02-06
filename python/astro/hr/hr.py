import csv
import string
import matplotlib.pyplot as plt
#stars.csv: http://stars.astro.illinois.edu/sow/bright.html


rem = ['D','I','V','pHgMn','pSi','op','ae','pe','b','a','e','p','m','-','.5']
classes = 'OBAFGKM'
def class2float(c):
		for s in rem:
			c = c.replace(s,'')
		if len(c) == 2:
			c = str(classes.find(c[0]))+"."+c[1]
		else:
			c = str(classes.find(c[0]))+".0"
		return float(c)

constellation_list = {}
with open('constellations.csv','rb') as constellationscsv:
	next(constellationscsv,None)
	reader = csv.reader(constellationscsv,delimiter=',', quotechar='"')
	for row in reader:
		constellation_list[row[2]] = row[1]
constellation_list["-"] = "Ukjent"

def constellation(abbr):
	abbr = abbr.split(' ')
	if len(abbr) > 1: 
		abbr.pop(0)
	while len(abbr) > 1:
		abbr.pop(-1)
	name = constellation_list[''.join(abbr)]
	return name







star_class = []
star_mag = []

with open('stars.csv','rb') as starscsv:
	next(starscsv,None)
	reader = csv.reader(starscsv,delimiter=',', quotechar='"')
	for row in reader:
		#print row
		c = row[3]
		m = row[6]
		if c.find('+')>-1 or m == '...': 
			continue
		print row[1],",", constellation(row[2]), row[3], row[6]
		#print row[3], row[6]
		star_class.append(class2float(c))
		star_mag.append(float(m))

x = [0.5,1.5,2.5,3.5,4.5,5.5,6.5]
clarr = ['O','B','A','F','G','K','M']
#plt.plot(star_class,star_mag,'+')
plt.scatter(star_class,star_mag)
plt.xticks(x,clarr)
plt.xlabel('Spectral class')
plt.ylabel('Absolute magnitude')
ax = plt.gca()
x = plt.gca()
ax.set_ylim(ax.get_ylim()[::-1])
plt.show()


