import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation

gravity = -9.81
mass = 10
radius = 0.01
A = np.pi * radius ** 2
rho = 1.225
Cd = 0.47
dt = 0.01

initialSpeed = 50
initialAngle = np.radians(45)




ball_x = 0
ball_vx = initialSpeed * np.cos(initialAngle)
ball_y = 0
ball_vy = initialSpeed * np.sin(initialAngle)

x_positions = []
y_positions = []


for step in range(6000):
    speed = np.sqrt(ball_vx ** 2 + ball_vy ** 2)
    drag_y = -0.5 * rho * speed * ball_vy * Cd * A
    drag_x = -0.5 * rho * speed * ball_vx * Cd * A
    
    # Y 
    
    force_gravity = mass * gravity 
    
    force = force_gravity + drag_y
    ay = force/mass
    
    ball_vy = ball_vy + ay * dt
    ball_y = ball_y + ball_vy * dt
    
    if ball_y <= 0:
        ball_y = 0 
        ball_vy = -ball_vy * 0.9

    # X
    
    force = drag_x
    ax = force/mass
    ball_vx = ball_vx + ax * dt
    ball_x = ball_x + ball_vx * dt
    
    y_positions.append(ball_y)
    x_positions.append(ball_x)
    
plt.plot(x_positions, y_positions)
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.show()

