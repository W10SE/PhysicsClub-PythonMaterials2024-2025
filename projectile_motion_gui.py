"""
PROJECTILE MOTION -- INTERACTIVE GUI SIMULATION
----------------------------------------------------
Launch a ball at an angle and watch it fly along its parabolic path.
Sliders control the launch speed and angle; a trail shows the path
it has already traveled.

Physics recap:
    x(t) = v0 * cos(theta) * t
    y(t) = v0 * sin(theta) * t - 0.5 * g * t^2

    v0    = initial speed (m/s)
    theta = launch angle (degrees, from horizontal)
    g     = 9.8 m/s^2 (gravity)

    Time of flight = 2 * v0 * sin(theta) / g
    Max height     = (v0 * sin(theta))^2 / (2*g)
    Range          = v0^2 * sin(2*theta) / g

Run this file directly. Everything happens in one window:
    - Sliders: launch speed, launch angle
    - Play/Pause button: launch (or pause) the ball
    - Reset button: send the ball back to the launch point
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

DEFAULTS = dict(v0=20.0, theta=45.0)
G = 9.8
TIME_SCALE = 1.0   # simulated seconds per real second (change to speed up/slow down)
DT = 0.02

fig, ax = plt.subplots(figsize=(9, 6))
plt.subplots_adjust(left=0.1, bottom=0.35, top=0.9)

ax.set_xlabel("Horizontal distance (m)")
ax.set_ylabel("Height (m)")
ax.set_title("Projectile Motion")
ax.grid(True)

trail_line, = ax.plot([], [], 'b--', linewidth=1, alpha=0.6)
ball, = ax.plot([], [], 'o', color='crimson', markersize=14)
peak_marker, = ax.plot([], [], 'g^', markersize=10)
info_text = ax.text(0.02, 0.95, "", transform=ax.transAxes, fontsize=10,
                     verticalalignment='top', family='monospace')

state = {}

def compute_launch():
    v0 = s_v0.val
    theta_deg = s_theta.val
    theta = np.radians(theta_deg)

    t_flight = 2 * v0 * np.sin(theta) / G
    h_max = (v0 * np.sin(theta))**2 / (2 * G)
    R = v0**2 * np.sin(2 * theta) / G

    state['v0'] = v0
    state['theta_deg'] = theta_deg
    state['theta'] = theta
    state['t_flight'] = t_flight
    state['h_max'] = h_max
    state['range'] = R
    state['t'] = 0.0
    state['xs'] = []
    state['ys'] = []
    state['running'] = False

    # Resize axes to comfortably fit this trajectory
    ax.set_xlim(-1, max(R * 1.15, 5))
    ax.set_ylim(-1, max(h_max * 1.4, 5))

def reset_state():
    compute_launch()

axcolor = 'lightgoldenrodyellow'
ax_v0 = plt.axes([0.2, 0.22, 0.6, 0.03], facecolor=axcolor)
ax_theta = plt.axes([0.2, 0.17, 0.6, 0.03], facecolor=axcolor)

s_v0 = Slider(ax_v0, 'Launch speed (m/s)', 1.0, 40.0, valinit=DEFAULTS['v0'])
s_theta = Slider(ax_theta, 'Launch angle (deg)', 1.0, 89.0, valinit=DEFAULTS['theta'])

def on_slider_change(val):
    reset_state()
    draw_scene()
    fig.canvas.draw_idle()

for s in (s_v0, s_theta):
    s.on_changed(on_slider_change)

ax_play = plt.axes([0.3, 0.06, 0.18, 0.06])
ax_reset = plt.axes([0.52, 0.06, 0.18, 0.06])
btn_play = Button(ax_play, 'Play / Pause')
btn_reset = Button(ax_reset, 'Reset')

def on_play(event):
    state['running'] = not state['running']

def on_reset(event):
    reset_state()
    draw_scene()
    fig.canvas.draw_idle()

btn_play.on_clicked(on_play)
btn_reset.on_clicked(on_reset)

def draw_scene():
    peak_marker.set_data([state['range'] / 2], [state['h_max']])
    trail_line.set_data(state['xs'], state['ys'])
    if state['xs']:
        ball.set_data([state['xs'][-1]], [state['ys'][-1]])
    else:
        ball.set_data([0], [0])
    info_text.set_text(
        f"v0 = {state['v0']:.1f} m/s   angle = {state['theta_deg']:.1f} deg\n"
        f"time of flight = {state['t_flight']:.2f} s\n"
        f"max height = {state['h_max']:.2f} m\n"
        f"range = {state['range']:.2f} m\n"
        f"t = {state['t']:.2f} s"
    )

def update(frame):
    if state['running'] and state['t'] <= state['t_flight']:
        x = state['v0'] * np.cos(state['theta']) * state['t']
        y = state['v0'] * np.sin(state['theta']) * state['t'] - 0.5 * G * state['t']**2
        state['xs'].append(x)
        state['ys'].append(y)
        state['t'] += DT * TIME_SCALE

        if state['t'] > state['t_flight']:
            state['running'] = False  # stop once it lands

        draw_scene()

    return trail_line, ball, peak_marker, info_text

reset_state()
draw_scene()

from matplotlib.animation import FuncAnimation
anim = FuncAnimation(fig, update, interval=20, blit=False, cache_frame_data=False)

plt.show()
