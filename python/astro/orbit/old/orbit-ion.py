#!/usr/bin/env python3

import math
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

ext = 2

fig = plt.figure()
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

    def position(self,*args):
        return self.px, self.py
    

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

        force = {}
        for body in bodies:
            # Add up all of the forces exerted on 'body'.
            total_fx = total_fy = 0.0
            for other in bodies:
                # Don't calculate the body's attraction to itself
                if body is other:
                    continue
                fx, fy = body.attraction(other)
                total_fx += fx
                total_fy += fy

            # Record the total force exerted.
            force[body] = (total_fx, total_fy)

        # Update velocities based upon on the force.
        for body in bodies:
            fx, fy = force[body]
            body.vx += fx / body.mass * timestep
            body.vy += fy / body.mass * timestep

            # Update positions
            body.px += body.vx * timestep
            body.py += body.vy * timestep
        
        print(bodies.px)


def main():
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

    loop([sun, earth])

if __name__ == '__main__':
    main()

