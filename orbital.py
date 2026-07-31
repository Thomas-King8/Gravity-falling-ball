import numpy as np
import matplotlib.pyplot as plt

G = 6.674e-11
M = 5.972e24
R_earth = 6.371e6

thrust     = 110000.0
burn_time  = 300.0               
fuel_mass  = 7000.0
dry_mass   = 1000.0
burn_rate  = fuel_mass / burn_time

TARGET_ALT     = 300000.0
PITCH_END_TIME = 235.0 

x, y   = 0.0, R_earth
vx, vy = 0.0, 0.0
fuel   = fuel_mass
phase  = "ascent"
dt     = 0.1

x_pos, y_pos = [], []
apoapsis = periapsis = 0.0

for step in range(200000):
    time = step * dt
    r        = np.sqrt(x**2 + y**2)
    altitude = r - R_earth
    v        = np.sqrt(vx**2 + vy**2)

    energy = v**2 / 2 - G*M/r
    h      = x*vy - y*vx
    if energy < 0:
        a_orbit   = -G*M / (2*energy)
        e         = np.sqrt(max(0.0, 1 + 2*energy*h**2 / (G*M)**2))
        apoapsis  = a_orbit*(1+e) - R_earth
        periapsis = a_orbit*(1-e) - R_earth
    else:
        apoapsis = periapsis = float('inf')
    v_radial = (x*vx + y*vy) / r

    thrusting = False
    tx, ty = 0.0, 0.0

    if phase == "ascent":
        thrusting = True
        if time < 10:
            angle = np.arctan2(x, y)                     
        else:
            frac  = (time - 10) / (PITCH_END_TIME - 10)
            pitch = np.radians(min(90, 90 * frac))
            angle = np.arctan2(x, y) + pitch
        tx = np.sin(angle)
        ty = np.cos(angle)
        if apoapsis >= TARGET_ALT:
            phase = "coast"     
            print(f"MECO        t={time:.0f}s  alt={altitude/1000:.0f} km  fuel={fuel:.0f} kg")

                                      
    elif phase == "coast":
        if v_radial <= 0: 
            phase = "circualize"
            print(f"Apoapsis    t={time:.0f}s  alt={altitude/1000:.0f} km  v={v:.0f} m/s")
    
    elif phase == "circualize":
        thrusting = True
        if v > 0:
            tx = vx / v
            ty = vy / v
        if v >= np.sqrt(G*M/r):
            phase = "done"
            print(f"Circularized t={time:.0f}s  fuel left={fuel:.0f} kg")
            

    if thrusting and fuel > 0:
        thrust_force = thrust
        fuel -= burn_rate * dt
    else:
        thrust_force = 0.0
    current_mass = dry_mass + max(fuel, 0.0)

    grav_ax = -(G*M) / r**2 * (x / r)
    grav_ay = -(G*M) / r**2 * (y / r)
    thrust_ax = (thrust_force / current_mass) * tx
    thrust_ay = (thrust_force / current_mass) * ty

    ax = grav_ax + thrust_ax
    ay = grav_ay + thrust_ay

    vx += ax * dt
    vy += ay * dt
    x  += vx * dt
    y  += vy * dt

    if r < R_earth:
        print(f"Crashed at t={time:.0f}s")
        break

    x_pos.append(x)
    y_pos.append(y)

print(f"Final phase: {phase}")
print(f"Periapsis: {periapsis/1000:.0f} km   Apoapsis: {apoapsis/1000:.0f} km")

theta = np.linspace(0, 2*np.pi, 200)
plt.plot(R_earth*np.cos(theta), R_earth*np.sin(theta), 'b')
plt.plot(x_pos, y_pos, 'r')
plt.axis('equal')
plt.title('Ascent + MECO only')
plt.show()