"""
LIGHT REFRACTION -- INTERACTIVE GUI SIMULATION (Snell's Law)
----------------------------------------------------------------
A dot of light travels down toward a boundary between two materials,
bends according to Snell's Law, and continues into the second material.
Sliders let you change the incidence angle and both materials' index
of refraction; watch the ray (and the bend) update live.

Physics recap:
    n1 * sin(theta1) = n2 * sin(theta2)
    n1, n2 = index of refraction of medium 1 (top) and medium 2 (bottom)
    theta1 = angle of incidence (from the normal, the dashed vertical line)
    theta2 = angle of refraction

    Typical index of refraction values:
        Air ~ 1.00   Water ~ 1.33   Glass ~ 1.50   Diamond ~ 2.42

Run this file directly. Everything happens in one window:
    - Sliders: incidence angle, n1, n2
    - Play/Pause button: animate the light dot traveling along the ray
    - Reset button: restore default slider values and restart the animation
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

DEFAULTS = dict(theta1=40.0, n1=1.00, n2=1.33)
DOT_SPEED = 1.2  # how fast the light dot travels along the ray, per frame-unit

fig, ax = plt.subplots(figsize=(7, 8))
plt.subplots_adjust(left=0.15, bottom=0.42, top=0.92)

ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title("Refraction of Light (Snell's Law)")

# Boundary line between the two media
ax.axhline(0, color='black', linewidth=1.5)
# Normal line (dashed)
ax.plot([0, 0], [-1.5, 1.5], 'k--', linewidth=1)

label_top = ax.text(1.0, 0.08, "", fontsize=10)
label_bottom = ax.text(1.0, -0.15, "", fontsize=10)

incident_line, = ax.plot([], [], color='orange', linewidth=2.5)
refracted_line, = ax.plot([], [], color='red', linewidth=2.5)
reflected_line, = ax.plot([], [], color='purple', linewidth=2.5)
light_dot, = ax.plot([], [], 'o', color='yellow', markeredgecolor='black', markersize=12)

info_text = ax.text(-1.55, -1.3, "", fontsize=10, family='monospace')

state = {}

def compute_geometry():
    theta1_deg = s_theta1.val
    n1 = s_n1.val
    n2 = s_n2.val
    theta1 = np.radians(theta1_deg)
    sin_theta2 = (n1 / n2) * np.sin(theta1)

    state['n1'] = n1
    state['n2'] = n2
    state['theta1_deg'] = theta1_deg
    state['theta1'] = theta1

    # Points: incident ray goes from top down to origin
    state['incident_start'] = (-np.sin(theta1), np.cos(theta1))
    state['incident_end'] = (0.0, 0.0)

    if abs(sin_theta2) > 1:
        # Total internal reflection: no refracted ray, only reflection
        state['tir'] = True
        state['theta2_deg'] = None
        reflected_end = (np.sin(theta1), np.cos(theta1))
        state['reflected_end'] = reflected_end
        state['path'] = [state['incident_start'], state['incident_end'], reflected_end]
    else:
        theta2 = np.arcsin(sin_theta2)
        state['tir'] = False
        state['theta2_deg'] = np.degrees(theta2)
        refracted_end = (np.sin(theta2), -np.cos(theta2))
        state['refracted_end'] = refracted_end
        state['path'] = [state['incident_start'], state['incident_end'], refracted_end]

    state['dot_progress'] = 0.0  # 0 = start of path, grows as it animates
    state['running'] = False

def reset_state():
    compute_geometry()

axcolor = 'lightgoldenrodyellow'
ax_theta1 = plt.axes([0.2, 0.30, 0.6, 0.03], facecolor=axcolor)
ax_n1 = plt.axes([0.2, 0.25, 0.6, 0.03], facecolor=axcolor)
ax_n2 = plt.axes([0.2, 0.20, 0.6, 0.03], facecolor=axcolor)

s_theta1 = Slider(ax_theta1, 'Incidence angle (deg)', 0.0, 85.0, valinit=DEFAULTS['theta1'])
s_n1 = Slider(ax_n1, 'n1 (top medium)', 1.00, 2.50, valinit=DEFAULTS['n1'])
s_n2 = Slider(ax_n2, 'n2 (bottom medium)', 1.00, 2.50, valinit=DEFAULTS['n2'])

def on_slider_change(val):
    reset_state()
    draw_scene()
    fig.canvas.draw_idle()

for s in (s_theta1, s_n1, s_n2):
    s.on_changed(on_slider_change)

ax_play = plt.axes([0.25, 0.08, 0.2, 0.06])
ax_reset = plt.axes([0.5, 0.08, 0.2, 0.06])
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
    x0, y0 = state['incident_start']
    incident_line.set_data([x0, 0], [y0, 0])

    label_top.set_text(f"Medium 1  (n1 = {state['n1']:.2f})")
    label_bottom.set_text(f"Medium 2  (n2 = {state['n2']:.2f})")

    if state['tir']:
        refracted_line.set_data([], [])
        xr, yr = state['reflected_end']
        reflected_line.set_data([0, xr], [0, yr])
        info_text.set_text(
            f"Incidence angle: {state['theta1_deg']:.1f} deg\n"
            f"TOTAL INTERNAL REFLECTION -- no light enters medium 2"
        )
    else:
        reflected_line.set_data([], [])
        xf, yf = state['refracted_end']
        refracted_line.set_data([0, xf], [0, yf])
        bend = "toward" if state['n2'] > state['n1'] else "away from"
        info_text.set_text(
            f"Incidence angle: {state['theta1_deg']:.1f} deg\n"
            f"Refraction angle: {state['theta2_deg']:.1f} deg\n"
            f"Light bends {bend} the normal (n2 {'>' if state['n2']>state['n1'] else '<'} n1)"
        )

    place_dot()

def place_dot():
    """Move the light dot along the path according to dot_progress (0 to 1 per segment)."""
    path = state['path']
    progress = state['dot_progress']
    n_segments = len(path) - 1
    seg_progress = progress * n_segments
    seg_index = min(int(seg_progress), n_segments - 1)
    local_t = seg_progress - seg_index

    x_a, y_a = path[seg_index]
    x_b, y_b = path[seg_index + 1]
    x = x_a + (x_b - x_a) * local_t
    y = y_a + (y_b - y_a) * local_t
    light_dot.set_data([x], [y])

def update(frame):
    if state['running']:
        state['dot_progress'] += 0.01 * DOT_SPEED
        if state['dot_progress'] > 1.0:
            state['dot_progress'] = 0.0  # loop the animation
        place_dot()
    return incident_line, refracted_line, reflected_line, light_dot, info_text

reset_state()
draw_scene()

from matplotlib.animation import FuncAnimation
anim = FuncAnimation(fig, update, interval=30, blit=False, cache_frame_data=False)

plt.show()
