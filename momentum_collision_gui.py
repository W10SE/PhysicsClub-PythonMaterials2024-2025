"""
MOMENTUM & COLLISIONS -- INTERACTIVE GUI SIMULATION
-----------------------------------------------------
Two balls slide toward each other on a track and collide. You can set
each ball's mass and starting velocity with sliders, then hit Play to
watch the collision happen and see momentum get conserved live.

Physics recap:
    momentum (p) = mass (m) * velocity (v)
    Total momentum before collision = Total momentum after collision (always true)

    Elastic collision formulas (used here -- no energy lost, like billiard balls):
        v1' = ((m1 - m2)*v1 + 2*m2*v2) / (m1 + m2)
        v2' = ((m2 - m1)*v2 + 2*m1*v1) / (m1 + m2)

Run this file directly. Everything happens in one window:
    - Sliders: mass and velocity for each ball
    - Play/Pause button: start or stop the animation
    - Reset button: put both balls back at their starting positions/velocities
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# ---------------- DEFAULT STARTING VALUES ----------------
DEFAULTS = dict(m1=2.0, v1=3.0, m2=3.0, v2=-1.5)
TRACK_LEFT, TRACK_RIGHT = -10, 10
DT = 0.03  # seconds simulated per animation frame

# ---------------- FIGURE LAYOUT ----------------
fig, ax = plt.subplots(figsize=(9, 6))
plt.subplots_adjust(left=0.1, bottom=0.42, top=0.9)  # leave room for sliders/buttons

ax.set_xlim(TRACK_LEFT, TRACK_RIGHT)
ax.set_ylim(-1, 1)
ax.set_yticks([])
ax.set_xlabel("Position (m)")
ax.set_title("Momentum & Collisions")
ax.axhline(0, color="gray", linewidth=1)

# Ball 1 (blue, starts on the left moving right)
ball1, = ax.plot([], [], 'o', color='royalblue', markersize=20)
# Ball 2 (red, starts on the right moving left)
ball2, = ax.plot([], [], 'o', color='crimson', markersize=20)

info_text = ax.text(0.02, 0.85, "", transform=ax.transAxes, fontsize=10,
                     verticalalignment='top', family='monospace')

# ---------------- SIMULATION STATE ----------------
state = {}

def reset_state():
    """Reset ball positions/velocities to starting conditions from sliders."""
    state['m1'] = s_m1.val
    state['v1'] = s_v1.val
    state['m2'] = s_m2.val
    state['v2'] = s_v2.val
    state['x1'] = TRACK_LEFT + 2       # ball 1 starts near the left
    state['x2'] = TRACK_RIGHT - 2      # ball 2 starts near the right
    state['collided'] = False
    state['running'] = False

def radius_from_mass(m):
    """Bigger mass -> bigger-looking ball (just for visuals)."""
    return 0.3 + 0.05 * m

# ---------------- SLIDERS ----------------
axcolor = 'lightgoldenrodyellow'
ax_m1 = plt.axes([0.15, 0.30, 0.3, 0.03], facecolor=axcolor)
ax_v1 = plt.axes([0.15, 0.25, 0.3, 0.03], facecolor=axcolor)
ax_m2 = plt.axes([0.55, 0.30, 0.3, 0.03], facecolor=axcolor)
ax_v2 = plt.axes([0.55, 0.25, 0.3, 0.03], facecolor=axcolor)

s_m1 = Slider(ax_m1, 'Mass 1 (kg)', 0.5, 10.0, valinit=DEFAULTS['m1'])
s_v1 = Slider(ax_v1, 'Vel 1 (m/s)', -8.0, 8.0, valinit=DEFAULTS['v1'])
s_m2 = Slider(ax_m2, 'Mass 2 (kg)', 0.5, 10.0, valinit=DEFAULTS['m2'])
s_v2 = Slider(ax_v2, 'Vel 2 (m/s)', -8.0, 8.0, valinit=DEFAULTS['v2'])

# Resest the simulation whenever a slider is changed
def on_slider_change(val):
    reset_state()
    draw_balls()
    fig.canvas.draw_idle()

for s in (s_m1, s_v1, s_m2, s_v2):
    s.on_changed(on_slider_change)

# ---------------- BUTTONS ----------------
ax_play = plt.axes([0.15, 0.12, 0.15, 0.06])
ax_reset = plt.axes([0.35, 0.12, 0.15, 0.06])
btn_play = Button(ax_play, 'Play / Pause')
btn_reset = Button(ax_reset, 'Reset')

def on_play(event):
    state['running'] = not state['running']

def on_reset(event):
    reset_state()
    draw_balls()
    fig.canvas.draw_idle()

btn_play.on_clicked(on_play)
btn_reset.on_clicked(on_reset)

# ---------------- DRAWING ----------------
def draw_balls():
    ball1.set_data([state['x1']], [0])
    ball2.set_data([state['x2']], [0])
    ball1.set_markersize(radius_from_mass(state['m1']) * 40)
    ball2.set_markersize(radius_from_mass(state['m2']) * 40)

    p1 = state['m1'] * state['v1']
    p2 = state['m2'] * state['v2']
    info_text.set_text(
        f"Ball 1: m={state['m1']:.1f} kg  v={state['v1']:.2f} m/s  p={p1:.2f} kg*m/s\n"
        f"Ball 2: m={state['m2']:.1f} kg  v={state['v2']:.2f} m/s  p={p2:.2f} kg*m/s\n"
        f"Total momentum = {p1 + p2:.2f} kg*m/s\n"
        f"{'*** COLLISION HAPPENED ***' if state['collided'] else ''}"
    )

# ---------------- ANIMATION LOOP ----------------
def update(frame):
    if state['running']:
        r1 = radius_from_mass(state['m1'])
        r2 = radius_from_mass(state['m2'])

        # Move both balls
        state['x1'] += state['v1'] * DT
        state['x2'] += state['v2'] * DT

        # Check for collision (balls touching)
        if (not state['collided']) and (state['x2'] - state['x1'] <= r1 + r2) and state['v1'] > state['v2']:
            m1, m2, v1, v2 = state['m1'], state['m2'], state['v1'], state['v2']
            new_v1 = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
            new_v2 = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
            state['v1'], state['v2'] = new_v1, new_v2
            state['collided'] = True

        # Check for wall collisions (balls bounce off the track edges)
        if state['x1'] < TRACK_LEFT or state['x1'] > TRACK_RIGHT:
            state['v1'] *= -1
        if state['x2'] < TRACK_LEFT or state['x2'] > TRACK_RIGHT:
            state['v2'] *= -1

        draw_balls()

    return ball1, ball2, info_text

reset_state()
draw_balls()

from matplotlib.animation import FuncAnimation
anim = FuncAnimation(fig, update, interval=30, blit=False, cache_frame_data=False)

plt.show()
