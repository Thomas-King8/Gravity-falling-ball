import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation



# Globals 
gravity = -9.81
dt = 0.001
ball_y = 100
ball_vy = 0
mass = 10


positions = []
for step in range(100000):
    force = mass * gravity 
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

