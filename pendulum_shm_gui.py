"""
PENDULUM / SIMPLE HARMONIC MOTION -- INTERACTIVE GUI SIMULATION
---------------------------------------------------------------------
Watch a pendulum swing back and forth in real time, plus a live graph
of its angle over time. Sliders control the string length and starting
swing angle.

Physics recap (small-angle approximation, valid under ~20 degrees):
    theta(t) = theta_max * cos(omega * t)
    omega = sqrt(g / L)        (angular frequency, rad/s)
    T     = 2*pi / omega       (period -- time for one full swing, s)
    L     = pendulum length (m)
    g     = 9.8 m/s^2

Run this file directly. Everything happens in one window:
    - Sliders: pendulum length, starting angle
    - Play/Pause button: start or stop the swinging
    - Reset button: put the pendulum back at its starting angle, t = 0
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

DEFAULTS = dict(L=1.0, theta_max=20.0)
G = 9.8
DT = 0.02

fig = plt.figure(figsize=(10, 6))
plt.subplots_adjust(left=0.08, right=0.95, bottom=0.35, top=0.9, wspace=0.3)

ax_pend = fig.add_subplot(1, 2, 1)
ax_graph = fig.add_subplot(1, 2, 2)

# --- Pendulum view (left) ---
ax_pend.set_xlim(-1.5, 1.5)
ax_pend.set_ylim(-1.6, 0.3)
ax_pend.set_aspect('equal')
ax_pend.set_title("Pendulum")
ax_pend.plot([0], [0], 'k^', markersize=10)  # pivot point
string_line, = ax_pend.plot([], [], 'k-', linewidth=1.5)
bob, = ax_pend.plot([], [], 'o', color='darkorange', markersize=18)

# --- Angle vs time graph (right) ---
ax_graph.set_xlabel("Time (s)")
ax_graph.set_ylabel("Angle (deg)")
ax_graph.set_title("Angle vs Time")
ax_graph.grid(True)
angle_line, = ax_graph.plot([], [], 'b-')

info_text = ax_pend.text(-1.45, 0.15, "", fontsize=9, family='monospace')

state = {}

def reset_state():
    L = s_L.val
    theta_max_deg = s_theta.val
    theta_max = np.radians(theta_max_deg)
    omega = np.sqrt(G / L)
    T = 2 * np.pi / omega

    state['L'] = L
    state['theta_max'] = theta_max
    state['theta_max_deg'] = theta_max_deg
    state['omega'] = omega
    state['T'] = T
    state['t'] = 0.0
    state['t_history'] = []
    state['theta_history'] = []
    state['running'] = False

    ax_pend.set_xlim(-L * 1.3, L * 1.3)
    ax_pend.set_ylim(-L * 1.3, 0.3)
    ax_graph.set_xlim(0, 3 * T)
    ax_graph.set_ylim(-theta_max_deg * 1.3, theta_max_deg * 1.3)

axcolor = 'lightgoldenrodyellow'
ax_L = plt.axes([0.2, 0.20, 0.6, 0.03], facecolor=axcolor)
ax_theta = plt.axes([0.2, 0.15, 0.6, 0.03], facecolor=axcolor)

s_L = Slider(ax_L, 'Length (m)', 0.2, 3.0, valinit=DEFAULTS['L'])
s_theta = Slider(ax_theta, 'Start angle (deg)', 1.0, 45.0, valinit=DEFAULTS['theta_max'])

def on_slider_change(val):
    reset_state()
    draw_scene()
    fig.canvas.draw_idle()

for s in (s_L, s_theta):
    s.on_changed(on_slider_change)

ax_play = plt.axes([0.3, 0.05, 0.18, 0.06])
ax_reset = plt.axes([0.52, 0.05, 0.18, 0.06])
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
    theta = state['theta_max'] * np.cos(state['omega'] * state['t'])
    x = state['L'] * np.sin(theta)
    y = -state['L'] * np.cos(theta)

    string_line.set_data([0, x], [0, y])
    bob.set_data([x], [y])

    angle_line.set_data(state['t_history'], np.degrees(state['theta_history']) if state['theta_history'] else [])

    info_text.set_text(
        f"L = {state['L']:.2f} m\n"
        f"period T = {state['T']:.2f} s\n"
        f"t = {state['t']:.2f} s"
    )

def update(frame):
    if state['running']:
        theta = state['theta_max'] * np.cos(state['omega'] * state['t'])
        state['t_history'].append(state['t'])
        state['theta_history'].append(theta)
        state['t'] += DT

        # keep history to a reasonable length (last 3 periods worth)
        max_points = int((3 * state['T']) / DT) + 5
        if len(state['t_history']) > max_points:
            state['t_history'] = state['t_history'][-max_points:]
            state['theta_history'] = state['theta_history'][-max_points:]

        draw_scene()

    return string_line, bob, angle_line, info_text

reset_state()
draw_scene()

from matplotlib.animation import FuncAnimation
anim = FuncAnimation(fig, update, interval=20, blit=False, cache_frame_data=False)

plt.show()
