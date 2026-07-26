import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation



# Globals 
gravity = -9.81
dt = 0.01
ball_y = 100
ball_vy = 0
mass = 10
rho = 1.225
Cd = 0.47
radius = 0.01
A = np.pi * radius ** 2

positions = []
for step in range(6000):
    #Grav
    force_gravity = mass * gravity 
    # Drag
    force_drag = 0.5 * rho * ball_vy ** 2 * Cd * A
    
    if ball_vy > 0:
        force_drag = -force_drag
    
    force = force_gravity + force_drag
    acceleration = force/mass
    
    ball_vy = ball_vy + acceleration * dt
    ball_y = ball_y + ball_vy * dt
    
    if ball_y <= 0:
        ball_y = 0 
        ball_vy = -ball_vy * 0.9

    positions.append(ball_y)
    
plt.plot(positions)
plt.xlabel('Time')
plt.ylabel('Height (m)')
plt.show()

