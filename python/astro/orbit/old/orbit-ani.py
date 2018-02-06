#!/usr/bin/env python3

import math
import numpy as np
#from turtle import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# The gravitational constant G
G = 6.67428e-11

# Assumed scale: 100 pixels = 1AU.
EARTH_RADII = 6378.1 * 1000.0 # 6.3781E6 meters
AU = (149.6e6 * 1000)     # 149.6 million km, in meters.
SCALE = 1.0 / AU
timestep = 24*3600  # One day
px = []
py = []

ext = 2

fig = plt.figure()
ax = fig.add_axes([-2,-2,2,2])
#plt.axis('equal')
#plt.axis([-ext, ext, -ext, ext])

class Body:
    """
    name 
    mass : mass in kg
    vx, vy: x, y velocities in m/s
    px, py: x, y positions in m
    radius
    """
    
    name = 'Body'
    mass = None
    vx = vy = 0.0
    px = py = 0.0
    radius = 1
    color = 'black'
    
    def attraction(self, other):
        """(Body): (fx, fy)

        Returns the force exerted upon this body by the other body.
        """
        # Report an error if the other object is the same as this one.
        if self is other:
            raise ValueError("Attraction of object %r to itself requested"
                             % self.name)

        # Compute the distance of the other body.
        sx, sy = self.px, self.py
        ox, oy = other.px, other.py
        dx = (ox-sx)
        dy = (oy-sy)
        d = math.sqrt(dx**2 + dy**2)

        # Report an error if the distance is zero; otherwise we'll
        # get a ZeroDivisionError exception further down.
        if d == 0:
            s = '{:<8}  Pos.={:>6.2f} {:>6.2f} Vel.={:>10.3f} {:>10.3f}'.format(
                    self.name, self.px, self.py, self.vx, self.vy)
            print(s)
            s = '{:<8}  Pos.={:>6.2f} {:>6.2f} Vel.={:>10.3f} {:>10.3f}'.format(
                    other.name, other.px, other.py, other.vx, other.vy)
            print(s)
            s = 'Radius self={:>6.2f} Radius other={:>6.2f} Distance={:>6.2f} Diff={:>6.2f}'.format(self.radius,other.radius,d,(d-other.radius-self.radius))
            print(s)

            raise ValueError("Collision between objects %r and %r"
                             % (self.name, other.name))

        # Compute the force of attraction
        f = G * self.mass * other.mass / (d**2)

        # Compute the direction of the force.
        theta = math.atan2(dy, dx)
        fx = math.cos(theta) * f
        fy = math.sin(theta) * f
        return fx, fy

    def x(self):
        return self.px / AU

    def y(self):
        return self.py / AU
    
    def size(self):
        return self.radius / AU

    def plot(self):
        s = '{:<8}  Pos.={:>6.2f} {:>6.2f} Vel.={:>10.3f} {:>10.3f}'.format(
            self.name, self.px/AU, self.py/AU, self.vx, self.vy)
        print(s)
        #plt.plot(self.px*SCALE,self.py*SCALE,color=self.color,linestyle='none',marker='o')






def loop(bodies):
    """([Body])
    Never returns; loops through the simulation, updating the
    positions of all the provided bodies.
    """
    
    #Backstep velocity dt/2 with respect to position (Leapfrog method)
    for body in bodies:
        body.px += body.vx * timestep / 2
        body.py += body.vy * timestep / 2

    step = 1
    while step < 200:
        step += 1
        update(step)



class AnimatedScatter(object):
    """An animated scatter plot using matplotlib.animations.FuncAnimation."""
    def __init__(self, bodies):
        self.bodies = bodies	
        self.body_size = [body.size() for body in self.bodies]
        self.body_color = [body.color for body in self.bodies]
        self.numpoints = len(bodies)
        #self.stream = self.data_stream()
        
        # Setup the figure and axes...
        self.fig, self.ax = plt.subplots()
        # Then setup FuncAnimation.
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=5, 
	       init_func=self.setup_plot, blit=True)

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        x = [body.x() for body in self.bodies]	
        y = [body.y() for body in self.bodies]	
        self.scat = self.ax.scatter(x, y, c=self.body_color, s=self.body_size, animated=True)
        self.ax.axis([-10, 10, -10, 10])

        # For FuncAnimation's sake, we need to return the artist we'll be using
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,

    def integrate(self,step):
        force = {}
        for body in self.bodies:
            # Add up all of the forces exerted on 'body'.
            total_fx = total_fy = 0.0
            for other in self.bodies:
                # Don't calculate the body's attraction to itself
                if body is other:
                    continue
                fx, fy = body.attraction(other)
                total_fx += fx
                total_fy += fy

            # Record the total force exerted.
            force[body] = (total_fx, total_fy)

        # Update velocities based upon on the force.
        for body in self.bodies:
            fx, fy = force[body]
            body.vx += fx / body.mass * timestep
            body.vy += fy / body.mass * timestep

            # Update positions
            body.px += body.vx * timestep
            body.py += body.vy * timestep

        return [[body.x() for body in self.bodies],[body.y() for body in self.bodies]]

    def data_stream(self):
        """Generate a random walk (brownian motion). Data is scaled to produce
        a soft "flickering" effect."""
        data = np.random.random((4, self.numpoints))
        xy = data[:2, :]
        s, c = data[2:, :]
        while True:
            xy += 0.03 * (np.random.random((2, self.numpoints)) - 0.5)
            s += 0.05 * (np.random.random(self.numpoints) - 0.5)
            c += 0.02 * (np.random.random(self.numpoints) - 0.5)
            yield data


    def update(self, i):
        """Update the scatter plot."""
        #data = next(self.stream)
        xy = self.integrate(i)
        print(xy)
        # Set x and y data...
        self.scat.set_offsets(xy)
        # Set sizes...
        #self.scat._sizes = 300 * abs(data[2])**1.5 + 100
        # Set colors..
        #self.scat.set_array(data[3])

        # We need to return the updated artist for FuncAnimation to draw..
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,

    def show(self):
        plt.show()

if __name__ == '__main__':
    sun = Body()
    sun.name = 'Sun'
    sun.mass = 1.98892 * 10**30
    sun.radius = 100 * 110 * EARTH_RADII
    sun.color = 'yellow'

    earth = Body()
    earth.name = 'Earth'
    earth.mass = 5.9742 * 10**24
    earth.px = -1*AU
    earth.py = 0.0
    earth.vx = 0.0
    earth.vy = 29.783 * 1000            # 29.783 km/sec
    earth.radius = 20 * EARTH_RADII 
    earth.color = 'blue'

    moon = Body()
    moon.name = 'Moon'
    moon.mass = 7.342 * 10**22
    moon.px = -1 * AU - 384000000.0
    moon.vy = 29.783 * 1000 + 1022
    moon.radius = 0.25 * EARTH_RADII 
    moon.color = 'black'

    rocket = Body()
    rocket.name = 'Rocket'
    rocket.mass = 10**3
    rocket.py = -1 * AU
    rocket.vx = -0.7 * 29.783 * 1000
    rocket.vy = 0.0
    rocket.radius = 10 * EARTH_RADII 
    rocket.color = 'green'

    # Venus parameters taken from
    # http://nssdc.gsfc.nasa.gov/planetary/factsheet/venusfact.html
    venus = Body()
    venus.name = 'Venus'
    venus.mass = 4.8685 * 10**24
    venus.px = 0.723 * AU
    venus.vy = -35.02 * 1000
    venus.radius = 0.9 * EARTH_RADII 
    venus.color = 'red'

    a = AnimatedScatter([sun,earth])
    a.show()
    main()
