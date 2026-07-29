import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation

gravity = -9.81
radius = 0.01
A = np.pi * radius ** 2
rho = 1.225
Cd = 0.47
dt = 0.01
thrust = 500
burn_time = 10 
fuel_mass = 5
dry_mass = 5


initialSpeed = 0
initialAngle = np.radians(45)


rocket_x = 0
rocket_vx = initialSpeed * np.cos(initialAngle)
rocket_y = 0
rocket_vy = initialSpeed * np.sin(initialAngle)

x_positions = []
y_positions = []


for step in range(100000):
    time = step * dt 
    if time < burn_time:
        current_mass = dry_mass + fuel_mass * (1 - time/burn_time)
        thrust_force = thrust 
    else:   
        current_mass = dry_mass
        thrust_force = 0 
    
    thrust_x = thrust_force * np.cos(initialAngle)
    thrust_y = thrust_force * np.sin(initialAngle)
    
    speed = np.sqrt(rocket_vx ** 2 + rocket_vy ** 2)
    drag_y = -0.5 * rho * speed * rocket_vy * Cd * A
    drag_x = -0.5 * rho * speed * rocket_vx * Cd * A
    
    # Y 
    
    force_gravity = current_mass * gravity 
    
    force = force_gravity + drag_y + thrust_y
    ay = force/current_mass
    
    rocket_vy = rocket_vy + ay * dt
    rocket_y = rocket_y + rocket_vy * dt
    
    if rocket_y <= 0 and step > 0:
        break
    # X
    
    force = drag_x + thrust_x
    ax = force/current_mass
    rocket_vx = rocket_vx + ax * dt
    rocket_x = rocket_x + rocket_vx * dt
    
    y_positions.append(rocket_y)
    x_positions.append(rocket_x)
    
plt.plot(x_positions, y_positions)
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.show()

