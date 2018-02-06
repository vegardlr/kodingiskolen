import sys
import time
import math
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import animation


class Orbit():
	def __init__(self,dt=0.005,L=10.0):
		self.dt = dt
		self.n = 0
		self.L = L
		self.interval=10
		self.origo = np.array([L/2.,L/2.])


	def addObject(self,pos,vel,size):
		datatype = np.dtype([('pos', np.float64 , 2),('vel', np.float64 , 2),
			('force', np.float64 , 2),('mass', np.float64 , 1),('size', np.float64 , 1)])
		mass = size**2
		force = np.zeros(2)
		new=np.zeros(1,dtype=datatype) 
		#new = np.array([('pos',pos),('vel',vel),('force',force),('mass',mass),("size",size)],dtype=datatype)
		new["pos"] = pos
		new["vel"] = vel
		new["mass"] = mass
		new["size"] = size
		if self.n > 0:
			self.obj = np.append(self.obj,new)
		else:
			self.obj = new 
		self.n = len(self.obj)


	def loadExample(self,example="cloud",n=1):
		L = self.L
		print("Loading example: "+example)
		if example == "cloud":
			self.addObject(self.origo,[0,0],200.)
			for i in range(n):
				r = np.random.uniform(0.1*L,0.2*L)
				v = 2.0/r
				theta = np.random.uniform(0.0,2.0*np.pi)
				pos = np.array([r*np.cos(theta),r*np.sin(theta)])+self.origo
				vel = np.array([v*np.sin(theta),-v*np.cos(theta)])
				size = np.random.uniform(1.0,1.5)
				self.addObject(pos,vel,size)
		elif example == "double-planet":
			self.addObject(self.origo,[0.,0.],100.0)
			self.addObject(self.origo+[0.5,0.],[0.,-1.],1.0)
			self.addObject(self.origo-[0.5,0.],[0.,+1.],1.0)
		else:
			raise ValueError('Invalid example.')


	def initLeapfrog(self):
		self.forces('init')
		self.obj["vel"]=self.obj["vel"]-self.obj["force"]*self.dt/2.


	def forces(self,mode='std'):
		G = 0.00005
		size_factor = 0.000002
		ones = np.ones(self.n)
		m = self.obj["mass"][:]
		s = self.obj["size"][:]
		x = self.obj["pos"][:,0]
		y = self.obj["pos"][:,1]
		dx = np.outer(ones,x) - np.outer(x,ones)
		dy = np.outer(ones,y) - np.outer(y,ones)
		s2 = size_factor * (np.outer(ones,s) + np.outer(s,ones))**2
		m2 = np.outer(ones,m) * np.outer(m,ones)
		d2 = dx**2 + dy**2
		np.fill_diagonal(d2,np.inf)
		f  = G*m2/d2
		theta = np.arctan2(dy, dx)
		fx = np.sum(f * np.cos(theta),1)
		fy = np.sum(f * np.sin(theta),1)
		self.obj["force"] = np.transpose(np.vstack((fx,fy)))
		#self.obj["force"][self.obj["stat"]] = np.zeros(self.nstat,2)

		collisions = np.tril(d2 <= s2)
		if np.sum(collisions) > 0 and not mode == "init": 
			indices = np.column_stack(np.where(collisions))
			for ind in indices:
				self.collide(ind)
			self.n = len(self.obj)
	

	def collide(self,i):
		msum = np.sum(self.obj["mass"][i])
		psum = np.sum(self.obj["vel"][i]*self.obj["mass"][i],0)
		if self.obj["mass"][i[0]] > self.obj["mass"][i[1]]:
			i = np.flip(i,0)
		self.obj["mass"][i[0]] = msum
		self.obj["size"][i[0]] = np.sqrt(np.sum(self.obj["size"][i]**2))
		self.obj["vel"][i[0],:] =  psum / msum
		self.obj["force"][i[0],:] = np.zeros(2)
		self.obj = np.delete(self.obj,i[1])


	def integrate(self):
		if self.n == 0:
			raise ValueError('No more obj.')

		self.obj["vel"]=self.obj["vel"]+self.obj["force"]*self.dt
		self.obj["pos"]=self.obj["pos"]+self.obj["vel"]*self.dt
		#msum = np.sum(self.obj["mass"])
		#x=np.sum(self.obj["pos"][:,0]*self.obj["mass"])/msum
		#y=np.sum(self.obj["pos"][:,1]*self.obj["mass"])/msum
		#self.obj["pos"] += (self.origo - np.array(x,y))

			
		#Periodic boundaries
		#self.obj["pos"] = self.obj["pos"]%self.L

		#Save to scatter object type
		self.scatter.set_offsets(self.obj["pos"])
		self.scatter.set_sizes(self.obj["size"])
	

	def update(self,frame_number):
		sys.stdout.write('\rObjects: %4d' % self.n)
		sys.stdout.flush()
		self.forces()
		self.integrate()
		#self.cirle = plt.Circle(self.origo,radius=0.5,fc='y')
		#self.ax.add_patch(self.circle)
		return self.scatter, 
		#return [self.scatter,]
		#return self.circle, 
		#return tuple(self.scatter)+(self.circle,)
		#return self.scatter,self.circle,
		

	def run(self):
		self.fig = plt.figure(figsize=(7,7))
		self.ax = plt.axes(xlim=(0,self.L),ylim=(0,self.L))
		#self.cirle = plt.Circle(self.origo,radius=0.5,fc='y')
		#self.ax.add_patch(self.circle)
		self.scatter = self.ax.scatter(self.obj["pos"][:,0], 
				self.obj["pos"][:,1], s=self.obj["size"])
		anim = animation.FuncAnimation(self.fig, self.update, 
				interval=self.interval)
		plt.show() 


if __name__ == "__main__":
	orbits = Orbit()
	#orbits.loadExample("double-planet")
	orbits.loadExample("cloud",100)
	orbits.initLeapfrog()
	orbits.run()
