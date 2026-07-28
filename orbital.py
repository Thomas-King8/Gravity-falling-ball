import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation

# orbital velocity v = sqrt(GM/r)
# gravity F = GM*m / (r ** 2)
# altitude r = sqrt(x^2 + y^2)
# acceleration = a = F/m 

G = 6.674e-11 # Gravitational constant 
M = 5.972e24 # Mass of earth
m = 10 # Mass of ship
R_earth = 6.371e6 # radius/altitude of earth 

x = 0 
y = R_earth + 200000
vx = 11200
vy = 0
dt = 1 

x_pos = []
y_pos = []

for step in range(50000):
    r = np.sqrt(x**2 + y**2)
    grav_force = -(G * M * m) / (r**2)
    ax = grav_force * (x / r) / m
    ay = grav_force * (y / r) / m
    
    vx = vx + ax * dt
    vy = vy + ay * dt
    x = x + vx * dt
    y = y + vy * dt
    
    if r < R_earth:
        break 
    
    x_pos.append(x)
    y_pos.append(y)
    
theta = np.linspace(0, 2 * np.pi, 100)
plt.plot(R_earth * np.cos(theta), R_earth * np.sin(theta), 'b')

# Draw trajectory
plt.plot(x_pos, y_pos, 'r')
plt.axis('equal')
plt.title('Falling from 200km')
plt.show()
    
    
    