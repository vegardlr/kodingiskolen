import math
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation

dt = 0.005
n = 20
L = 1.0
particles=np.zeros(n,dtype=[("position", float , 2),
                            ("velocity", float ,2),
                            ("force", float ,2),
                            ("size", float , 1)])

particles["position"]=np.random.normal(L/2,L/10.0,(n,2));
#particles["velocity"]=np.random.normal(0,0.1,(n,2));
particles["velocity"][:,1]=-1.2*(particles["position"][:,0]-L/2)
particles["velocity"][:,0]=1.2*(particles["position"][:,1]-L/2)
particles["size"]=2.0*np.ones(n);
#particles["size"]=np.random.uniform(1,3,(n));
particles["position"][0,:] = [L/2,L/2]
particles["velocity"][0] = [0,0]
particles["size"][0] = 50.0

fig = plt.figure(figsize=(7,7))
ax = plt.axes(xlim=(0,L),ylim=(0,L))
scatter=ax.scatter(particles["position"][:,0], particles["position"][:,1], s=particles["size"])


def force():
    forces = np.zeros((n,2))
    for i in range(n):
	if np.isnan(particles["position"][i,0]):
            continue
        for o in range(1,n):
            if i==o:
                continue
	    if np.isnan(particles["position"][o,0]):
                continue
            dx = particles["position"][o,0]-particles["position"][i,0] 
            dy = particles["position"][o,1]-particles["position"][i,1] 
            d2 = (dx**2 + dy**2)
            if math.sqrt(d2) <= 0.0005*(particles["size"][i]+particles["size"][o]):
                mi,mo=particles["size"][i],particles["size"][o]
                vi,vo=particles["velocity"][i],particles["velocity"][o]
                particles["velocity"][i]=(mi*vi+mo*vo)/(mi*mo)
                particles["size"][i]+=particles["size"][o]
                particles["position"][o] = [np.nan,np.nan]
                continue
            theta = math.atan2(dy, dx)
            f = 0.0001 * particles["size"][o]/d2
            fx = math.cos(theta) * f
            fy = math.sin(theta) * f
            forces[i,:] += [fx,fy]
    return forces



def update(frame_number):
    particles["force"]=force()
    particles["velocity"] = particles["velocity"] + particles["force"]*dt
    particles["velocity"][0,:] = [0,0]
    particles["position"] = particles["position"] + particles["velocity"]*dt
    #Check collisions:
        
    #Periodic boundaries
    particles["position"] = particles["position"]%L
    scatter.set_offsets(particles["position"])
    scatter.set_sizes(particles["size"])
    return scatter, 

anim = FuncAnimation(fig, update, interval=10)
plt.show() 
