import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import scipy
from scipy.integrate import odeint
from scipy.integrate import solve_ivp
from IPython.display import HTML
from matplotlib.animation import FuncAnimation, FFMpegWriter
print(FFMpegWriter.isAvailable())


#initial conditions given 
#gravitational constant
G = 1 

#masses of the two bodies
m1 = 1
m2 = 1

#stand in for a small drag term/force (until gravitational wave energy loss is implemented)
c = 0.01 


#implement the equations of motion for a two body system in 2D
def two_body_eq(t, y):
    #planet 1 
    x1 = y[0]
    y1 = y[1]
    vx1 = y[2]
    vy1 = y[3]

    #planet 2 
    x2 = y[4]
    y2 = y[5]
    vx2 = y[6]
    vy2 = y[7]

    #calculate the distance between the two bodies
    r = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    #newton's law of gravitation, x and y 
    ax1 = G * m2 * (x2 - x1) / r**3
    ay1 = G * m2 * (y2 - y1) / r**3
    ax2 = G * m1 * (x1 - x2) / r**3
    ay2 = G * m1 * (y1 - y2) / r**3

    #drag force opposing the velocity of each body 
    ax1 = ax1 - c * vx1
    ay1 = ay1 - c * vy1
    ax2 = ax2 - c * vx2
    ay2 = ay2 - c * vy2

#return [xvelocity, y velocity, x acc, y acc] 
    return [vx1, vy1, ax1, ay1, vx2, vy2, ax2, ay2]


#set up the initial conditions for the two bodies

N = 5000 #how many steps or points it takes

#setting up the initial conditions for the two bodies, including their positions and velocities 
y0 = np.array([-1, 0, 0, -0.4,
               1, 0, 0, 0.4]) # initial condition for both, opposing velocities and positions

time_span = (0, 60) #time span for the simulation, from 0 to 60 seconds
t = np.linspace(time_span[0], time_span[1], N) #start at 0 seconds and end at 60 seconds

solv = solve_ivp(two_body_eq, time_span, y0, t_eval=t, method="RK45") # RK45 = numerical method, taking small steps through time  


# getting the positions 
x1_dat = solv.y[0] 
y1_dat = solv.y[1]
x2_dat = solv.y[4]
y2_dat = solv.y[5]

#getting the velocities 
vx1_dat = solv.y[2]
vy1_dat = solv.y[3]
vx2_dat = solv.y[6]
vy2_dat = solv.y[7]


#resolutions of ani
skip = 10 

x1_ani = x1_dat[::skip]
y1_ani = y1_dat[::skip]

x2_ani = x2_dat[::skip]
y2_ani = y2_dat[::skip]

t_ani = t[::skip]

# making the figures for the plots 
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

#orbital plot
padding = 1.2 

xmin = min(x1_ani.min(), x2_ani.min()) * padding
xmax = max(x1_ani.max(), x2_ani.max()) * padding
ymin = min(y1_ani.min(), y2_ani.min()) * padding
ymax = max(y1_ani.max(), y2_ani.max()) * padding

ax1.set_xlim(xmin, xmax)
ax1.set_ylim(ymin, ymax)

ax1.set_aspect('equal', adjustable='box')

ax1.set_title('Two-Body Inspiral')
ax1.set_xlabel('X Position')
ax1.set_ylabel('Y Position')

planet1, = ax1.plot([], [], 'ro', markersize=8, label='Body 1')
planet2, = ax1.plot([], [], 'bo', markersize=8, label='Body 2')

trail1, = ax1.plot([], [], 'r-', alpha=0.5, label='Trail 1')
trail2, = ax1.plot([], [], 'b-', alpha=0.5, label='Trail 2')

ax1.legend()

#position v time graph 
ax2.set_xlim(t_ani[0], t_ani[-1])

xmin2= min(x1_ani.min(), x2_ani.min())
xmax2= max(x1_ani.max(), x2_ani.max())

ax2.set_ylim(xmin2-0.5, xmax2+0.5)
ax2.set_xlabel("Time")
ax2.set_ylabel("x Position")

ax2.set_title("Position vs Time")

ax2.grid(True)

position1, = ax2.plot([], [], 'b-', label="Planet 1")
position2, = ax2.plot([], [], 'r-', label="Planet 2")

point1, = ax2.plot([], [], 'bo')
point2, = ax2.plot([], [], 'ro')

ax2.legend()

#initialize the animation
def init():

    planet1.set_data([], [])
    planet2.set_data([], [])

    trail1.set_data([], [])
    trail2.set_data([], [])

    position1.set_data([], [])
    position2.set_data([], [])

    point1.set_data([], [])
    point2.set_data([], [])

    return (planet1, planet2, trail1, trail2, position1, position2, point1, point2)

# update the animation for each frame
def animate(i):

    trail = 50
    start = max(0, i-trail)

# orbital plot
    planet1.set_data([x1_ani[i]], [y1_ani[i]])
    planet2.set_data([x2_ani[i]], [y2_ani[i]])

    trail1.set_data(x1_ani[start:i+1], y1_ani[start:i+1])
    trail2.set_data(x2_ani[start:i+1], y2_ani[start:i+1])

# position vs time plot
    position1.set_data(t_ani[:i+1], x1_ani[:i+1])
    position2.set_data(t_ani[:i+1], x2_ani[:i+1])

    point1.set_data([t_ani[i]], [x1_ani[i]])
    point2.set_data([t_ani[i]], [x2_ani[i]])

    return (planet1, planet2, trail1, trail2, position1, position2, point1, point2)

# create the animation
anim = FuncAnimation(fig, animate, frames=len(t_ani), init_func=init, interval=20, blit=True)
anim.save("/Users/alyanajusino/pn_trajectories_26/two_bodies.mp4", writer="ffmpeg", fps=240)

plt.tight_layout()
plt.show()
