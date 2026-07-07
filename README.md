# PhysicsClub-PythonMaterials2024-2025

This repository contains the curated collection of Python-based teaching materials and interactive scripts developed by me for Bangladesh International School and College's (BISC) Physics Club during the 2024-2025 academic year. While originally kept offline, a recent request for access after my relocation to Texas prompted me to make the collection publicly available here on GitHub.

These scripts are interactive GUI simulations covering core **Physics I** topics: momentum & collisions, refraction of light, projectile motion, and simple harmonic motion (pendulum). Each one opens in its own window with sliders, a Play/Pause button, and a Reset button — no separate GUI library needed, just Python + matplotlib.

## Requirements

```bash
pip install matplotlib numpy
```

Run any script with:

```bash
python3 filename.py
```

---

## The Scripts

### 1. `momentum_collision_gui.py` — Momentum & Collisions
Two balls slide toward each other on a track and collide elastically (no energy lost). Watch their velocities swap according to the conservation of momentum, with a live readout of each ball's momentum and the total.

**Key physics:** `p = m * v`, and total momentum before = total momentum after.

**Sliders:** Mass 1, Velocity 1, Mass 2, Velocity 2

### 2. `refraction_snell_gui.py` — Refraction of Light (Snell's Law)
A dot of light travels down to the boundary between two materials and bends according to Snell's Law. If the angle is steep enough going into a less-dense material, it shows total internal reflection instead.

**Key physics:** `n1 * sin(theta1) = n2 * sin(theta2)`

**Sliders:** Incidence angle, n1 (top medium), n2 (bottom medium)

### 3. `projectile_motion_gui.py` — Projectile Motion
Launches a ball at an angle and animates it flying along its parabolic path, leaving a trail behind it. Displays time of flight, max height, and range live as the ball flies.

**Key physics:** `x(t) = v0*cos(theta)*t`, `y(t) = v0*sin(theta)*t - 0.5*g*t^2`

**Sliders:** Launch speed, Launch angle

### 4. `pendulum_shm_gui.py` — Pendulum / Simple Harmonic Motion
A pendulum swings back and forth in real time, with a live angle-vs-time graph next to it showing the wave-like pattern of its motion.

**Key physics:** `theta(t) = theta_max * cos(omega*t)`, where `omega = sqrt(g/L)`

**Sliders:** Pendulum length, Starting swing angle

---

## Changing Parameters

There are two ways to change a simulation's parameters:

### A) While it's running (easiest)
Just drag the sliders at the bottom of the window. Moving a slider automatically resets the simulation to the new starting conditions (paused), so you can set everything up before pressing **Play**. Press **Reset** any time to go back to the current slider values.

### B) Changing the default starting values in the code
Near the top of every script there's a `DEFAULTS` dictionary. Editing these numbers changes what the sliders (and the simulation) start at when the script is first launched.

For example, in `momentum_collision_gui.py`:

```python
DEFAULTS = dict(m1=2.0, v1=3.0, m2=3.0, v2=-1.5)
```

To make ball 1 heavier and faster, just change the numbers:

```python
DEFAULTS = dict(m1=6.0, v1=5.0, m2=3.0, v2=-1.5)
```

Each script also lets you widen or narrow the *range* a slider can move across. Look for the `Slider(...)` lines — the second and third arguments are the minimum and maximum values. For example, in `projectile_motion_gui.py`:

```python
s_v0 = Slider(ax_v0, 'Launch speed (m/s)', 1.0, 40.0, valinit=DEFAULTS['v0'])
```

`1.0` and `40.0` are the slowest/fastest launch speeds allowed. Change them to, say, `1.0, 100.0` to allow much faster launches.

### Quick reference: what to edit and where

| Script | Edit this to change starting values | Edit this to change slider limits |
|---|---|---|
| `momentum_collision_gui.py` | `DEFAULTS` dict (m1, v1, m2, v2) | `s_m1`, `s_v1`, `s_m2`, `s_v2` lines |
| `refraction_snell_gui.py` | `DEFAULTS` dict (theta1, n1, n2) | `s_theta1`, `s_n1`, `s_n2` lines |
| `projectile_motion_gui.py` | `DEFAULTS` dict (v0, theta) | `s_v0`, `s_theta` lines |
| `pendulum_shm_gui.py` | `DEFAULTS` dict (L, theta_max) | `s_L`, `s_theta` lines |

Every script is also fully commented, with a short physics recap at the top explaining the formulas being simulated.

---

## Repository Structure

```
PhysicsClub-PythonMaterials2024-2025/
├── momentum_collision_gui.py
├── refraction_snell_gui.py
├── projectile_motion_gui.py
├── pendulum_shm_gui.py
└── README.md
```

---

Maintained for BISC Physics Club, 2024-2025.
