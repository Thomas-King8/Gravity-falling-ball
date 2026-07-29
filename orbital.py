import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation

# orbital velocity v = sqrt(GM/r)
# gravity F = GM*m / (r ** 2)
# altitude r = sqrt(x^2 + y^2)
# acceleration = a = F/m 

G = 6.674e-11 # Gravitational constant 
M = 5.972e24 # Mass of earth
R_earth = 6.371e6 # radius/altitude of earth 

x = 0 
y = R_earth + 0
vx = 0
vy = 0
dt = 1 

thrust = 110000
burn_time = 300
fuel_mass = 7000
dry_mass = 1000
burn_rate = fuel_mass / burn_time
fuel = fuel_mass

max_alt = 0
speed_at_apex = 0

x_pos = []
y_pos = []

for step in range(50000):
    time = step * dt 
    if time < burn_time:
        current_mass = dry_mass + fuel_mass * (1 - time/burn_time)
        thrust_force = thrust
    else:   
        current_mass = dry_mass
        thrust_force = 0 
    
    r = np.sqrt(x**2 + y**2)
    
    altitude = r - R_earth
    
    if time < 10:
        tx = x / r
        ty = y / r
    elif time < burn_time:
        frac = (time - 10) / (burn_time * 0.585 - 10)
        pitch = np.radians(min(90, 90 * frac))
        angle = np.arctan2(x, y) + pitch
        tx = np.sin(angle)
        ty = np.cos(angle)
    else:
        v_total = np.sqrt(vx**2 + vy**2)
        tx = vx / v_total
        ty = vy / v_total
        
    
    grav_ax = -(G * M) / (r**2) * (x / r)
    grav_ay = -(G * M) / (r**2) * (y / r)

    thrust_ax = (thrust_force / current_mass) * tx
    thrust_ay = (thrust_force / current_mass) * ty

    ax = grav_ax + thrust_ax
    ay = grav_ay + thrust_ay
        
    vx = vx + ax * dt
    vy = vy + ay * dt
    x = x + vx * dt
    y = y + vy * dt
    
    if r < R_earth:
        break 
    
    x_pos.append(x)
    y_pos.append(y)
    
    if altitude > max_alt:
        max_alt = altitude
        speed_at_apex = np.sqrt(vx**2 + vy**2)
    
theta = np.linspace(0, 2 * np.pi, 100)
plt.plot(R_earth * np.cos(theta), R_earth * np.sin(theta), 'b')

plt.plot(x_pos, y_pos, 'r')
plt.axis('equal')
plt.title('Falling from 200km')
plt.show()

v2 = vx**2 + vy**2
energy = v2/2 - G*M/r

if energy >= 0:
    print("Escape trajectory — too fast")
else:
    a_orbit = -G*M / (2*energy)
    h = x*vy - y*vx
    e = np.sqrt(1 + 2*energy*h**2 / (G*M)**2)
    periapsis = a_orbit*(1-e) - R_earth
    apoapsis = a_orbit*(1+e) - R_earth
    print(f"Periapsis: {periapsis/1000:.0f} km")
    print(f"Apoapsis: {apoapsis/1000:.0f} km")  
    