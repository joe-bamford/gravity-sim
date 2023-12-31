# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 15:24:16 2023

@author: bamjo
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import keyboard as kb

#%%

G = 10

class Simulation:
    def __init__(self, dt):
        self.time = 0.
        self.dt = dt
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-100, 100)
        self.ax.set_ylim(-100, 100)
        self.ax.set_aspect('equal')
        self.ax.grid(True)
        self.ax.set_xlabel('x', fontsize=20)
        self.ax.set_ylabel('y', fontsize=20)
        plt.get_current_fig_manager().full_screen_toggle()
        
    def animate(self, particle_list):
        while True:
            if kb.is_pressed('esc'):
                print('\nExiting')
                plt.close('all')
                break
            for p in particle_list:
                p.update(particle_list)
                p.sctr.set_offsets(p.position)
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            plt.show()
        

class Particle:
    def __init__(self, _id, mass, position, velocity):
        self._id = _id
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.sctr = sim.ax.scatter(self.position[0], self.position[1], s=50)
        
    def compute_acceleration(self, particle_list):
        # Drop concerned particle from list to iterate over
        other_particles = particle_list[:self._id] + particle_list[self._id+1:]
        # A somewhat arbitrary parameter to soften the potential. Reduces extreme scattering effects on close approach of particles
        softening_length = self.mass**(1/3)
        accel_contributions = np.array([(-G * o.mass * (self.position - o.position) / ((np.linalg.norm(self.position - o.position)**2
                                           + softening_length**2) * np.linalg.norm(self.position - o.position))) for o in other_particles])
        acceleration = np.sum(accel_contributions, axis=0)
        return acceleration
        
    def update(self, particle_list):
        self.acceleration = self.compute_acceleration(particle_list)
        self.velocity += self.acceleration * sim.dt
        self.position += self.velocity * sim.dt
        sim.time += sim.dt
        particle_list[self._id] = self
                        
#%% INITIALISE SIM

sim = Simulation(dt=0.03)

#%% SET UP PARTICLES INDIVIDUALLY

# # Potential source
# p0 = Particle(0, 10000., np.array([0., 0.]), np.array([0., 0.]))
# # Test mass
# p1 = Particle(1, 2., np.array([10., 10.]), np.array([-15., 15.]))
# # Another one
# p2 = Particle(2, 1., np.array([-10., -10.]), np.array([12., -12.]))
# # Another one
# p3 = Particle(3, 1., np.array([-20., 20.]), np.array([5., -10.]))
# # # Another one
# # p4 = Particle(4, 1., np.array([10., -10.]), np.array([0., 0.]))
# # Collect
# particle_list = [p0, p1,  p2,  p3]

#%% RANDOM PARTICLE DISTRIBUTION

# No. of particles
N = 10
# Draw initial conditions from a distribution
np.random.seed(5678)
positions = np.random.normal(loc=0, scale=20, size=(N,2))
velocities = np.random.normal(loc=0, scale=7, size=(N,2))

# Test masses
particle_list = np.empty(shape=N).tolist()
for i in range(0,N-1):
    particle_list[i] = Particle(i, 10, positions[i], velocities[i])

# Potential source
particle_list[N-1] = Particle(N-1, 1000., np.array([0., 0.]), np.array([0., 0.]))

#%% ANIMATE

# Animate particles
sim.animate(particle_list)


