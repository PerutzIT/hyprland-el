"""Procedural wallpapers for the hyprland-el themes (original artwork, MIT).

Every theme names a motif and three colours; the SVG is rendered with
rsvg-convert in the resolution of the screen and cached.
"""
import math
import os
import random
import subprocess

MOTIFS = ("aurora", "waves", "hills", "orbs", "dunes")


def _defs(t, c):
    return f"""
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0" stop-color="{t['base']}"/>
      <stop offset="1" stop-color="{t['bg']}"/>
    </linearGradient>
    <radialGradient id="glowA" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{c[0]}" stop-opacity="0.35"/>
      <stop offset="1" stop-color="{c[0]}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glowB" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{c[1]}" stop-opacity="0.30"/>
      <stop offset="1" stop-color="{c[1]}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="vignette" cx="0.5" cy="0.5" r="0.78">
      <stop offset="0.6" stop-color="#000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000" stop-opacity="{0.45 if t['dark'] else 0.12}"/>
    </radialGradient>
    <linearGradient id="ribA" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{c[0]}" stop-opacity="0"/>
      <stop offset="0.4" stop-color="{c[0]}" stop-opacity="0.8"/>
      <stop offset="0.75" stop-color="{c[2]}" stop-opacity="0.7"/>
      <stop offset="1" stop-color="{c[2]}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="ribB" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{c[1]}" stop-opacity="0"/>
      <stop offset="0.45" stop-color="{c[1]}" stop-opacity="0.7"/>
      <stop offset="1" stop-color="{c[1]}" stop-opacity="0"/>
    </linearGradient>
    <filter id="b1" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="140"/></filter>
    <filter id="b2" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="55"/></filter>
    <filter id="b3" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
    <filter id="b4" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="90"/></filter>
  </defs>"""


def _stars(rng, n, dark):
    if not dark:
        return ""
    s = []
    for _ in range(n):
        s.append(f'<circle cx="{rng.uniform(0, 3840):.0f}" cy="{rng.uniform(0, 1100):.0f}" '
                 f'r="{rng.uniform(1.0, 2.6):.1f}" fill="#fff" opacity="{rng.uniform(0.15, 0.55):.2f}"/>')
    return "\n  ".join(s)


def _aurora(t, c, rng):
    p1 = "M -200 1500 C 700 900, 1500 1700, 2300 1100 S 3600 700, 4100 1000"
    p2 = "M -200 1760 C 900 1300, 1700 2000, 2600 1450 S 3700 1150, 4100 1350"
    return f"""
  <ellipse cx="900" cy="700" rx="1300" ry="800" fill="url(#glowA)"/>
  <ellipse cx="3050" cy="1500" rx="1400" ry="900" fill="url(#glowB)"/>
  {_stars(rng, 40, t['dark'])}
  <path d="{p1}" stroke="url(#ribA)" stroke-width="260" fill="none" filter="url(#b1)"/>
  <path d="{p1}" stroke="url(#ribA)" stroke-width="70" fill="none" filter="url(#b2)"/>
  <path d="{p1}" stroke="url(#ribA)" stroke-width="5" fill="none" filter="url(#b3)" opacity="0.9"/>
  <path d="{p2}" stroke="url(#ribB)" stroke-width="220" fill="none" filter="url(#b1)"/>
  <path d="{p2}" stroke="url(#ribB)" stroke-width="45" fill="none" filter="url(#b2)"/>
  <path d="{p2}" stroke="url(#ribB)" stroke-width="4" fill="none" filter="url(#b3)" opacity="0.8"/>"""


def _wave_path(y, amp, phase, freq, rng):
    pts = []
    for i in range(0, 41):
        x = -100 + i * 101
        yy = y + amp * math.sin(i / 40 * freq * math.pi * 2 + phase) + amp * 0.35 * math.sin(i / 40 * freq * 5.1 + phase * 1.7)
        pts.append((x, yy))
    d = f"M {pts[0][0]} {pts[0][1]:.0f} " + " ".join(f"L {x} {yy:.0f}" for x, yy in pts[1:])
    return d + " L 4000 2300 L -100 2300 Z"


def _waves(t, c, rng):
    layers = []
    cols = [c[0], c[1], c[2], t['accent'], t['surface']]
    for i in range(5):
        y = 1050 + i * 190
        op = 0.55 - i * 0.07 if t['dark'] else 0.45 - i * 0.05
        d = _wave_path(y, 90 - i * 8, rng.uniform(0, 6.3), rng.uniform(1.2, 2.2), rng)
        layers.append(f'<path d="{d}" fill="{cols[i % len(cols)]}" opacity="{op:.2f}"/>')
        layers.append(f'<path d="{d}" fill="none" stroke="{cols[i % len(cols)]}" stroke-width="3" opacity="0.7" filter="url(#b3)"/>')
    return f"""
  <ellipse cx="2700" cy="650" rx="1500" ry="900" fill="url(#glowA)"/>
  <ellipse cx="700" cy="1200" rx="1300" ry="800" fill="url(#glowB)"/>
  {_stars(rng, 30, t['dark'])}
  <g>{''.join(layers)}</g>"""


def _ridge(y, rough, rng):
    x, pts = -100, []
    yy = y
    while x <= 4000:
        pts.append((x, yy))
        x += rng.uniform(120, 260)
        yy = y + rng.uniform(-rough, rough)
    d = f"M -100 2300 L {pts[0][0]:.0f} {pts[0][1]:.0f} "
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        mx = (x0 + x1) / 2
        d += f"Q {x0:.0f} {y0:.0f} {mx:.0f} {(y0 + y1) / 2:.0f} "
    return d + f"L {pts[-1][0]:.0f} {pts[-1][1]:.0f} L 4000 2300 Z"


def _mix(a, b, f):
    a = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * f):02x}" for x, y in zip(a, b))


def _hills(t, c, rng):
    layers = []
    for i in range(5):
        y = 1150 + i * 200
        col = _mix(_mix(t['surface'], c[i % 3], 0.35), t['bg'], i / 5)
        layers.append(f'<path d="{_ridge(y, 220 - i * 30, rng)}" fill="{col}" opacity="0.96"/>')
    return f"""
  <ellipse cx="2850" cy="760" rx="1600" ry="1000" fill="url(#glowA)"/>
  <circle cx="2850" cy="700" r="170" fill="{c[2]}" opacity="0.85" filter="url(#b3)"/>
  <circle cx="2850" cy="700" r="380" fill="{c[2]}" opacity="0.18" filter="url(#b4)"/>
  {_stars(rng, 60, t['dark'])}
  <g>{''.join(layers)}</g>"""


def _orbs(t, c, rng):
    s = []
    for i in range(16):
        r = rng.uniform(120, 520)
        s.append(f'<circle cx="{rng.uniform(0, 3840):.0f}" cy="{rng.uniform(0, 2160):.0f}" r="{r:.0f}" '
                 f'fill="{c[i % 3]}" opacity="{rng.uniform(0.18, 0.45):.2f}" filter="url(#b4)"/>')
    for i in range(10):
        r = rng.uniform(20, 70)
        s.append(f'<circle cx="{rng.uniform(0, 3840):.0f}" cy="{rng.uniform(0, 2160):.0f}" r="{r:.0f}" '
                 f'fill="{c[i % 3]}" opacity="{rng.uniform(0.25, 0.5):.2f}" filter="url(#b3)"/>')
    return f"""
  <ellipse cx="1900" cy="1080" rx="2000" ry="1100" fill="url(#glowB)"/>
  {''.join(s)}"""


def _dunes(t, c, rng):
    layers = []
    for i in range(6):
        y = 900 + i * 230
        col = _mix(c[i % 3], t['bg'], 0.35 + i * 0.1)
        d = _wave_path(y, 160 - i * 15, rng.uniform(0, 6.3), 0.8, rng)
        layers.append(f'<path d="{d}" fill="{col}" opacity="0.95"/>')
    return f"""
  <ellipse cx="1300" cy="600" rx="1700" ry="900" fill="url(#glowA)"/>
  <circle cx="1300" cy="640" r="230" fill="{c[1]}" opacity="0.9" filter="url(#b3)"/>
  <circle cx="1300" cy="640" r="520" fill="{c[1]}" opacity="0.18" filter="url(#b4)"/>
  <g>{''.join(layers)}</g>"""


_GEN = {"aurora": _aurora, "waves": _waves, "hills": _hills, "orbs": _orbs, "dunes": _dunes}


def svg(theme):
    wp = theme.get("wallpaper", {})
    motif = wp.get("motif", "aurora")
    cols = wp.get("colors") or [theme["accent"], theme["accent2"], theme["magenta"]]
    rng = random.Random(theme["id"])          # deterministic per theme
    body = _GEN.get(motif, _aurora)(theme, cols, rng)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="3840" height="2160" viewBox="0 0 3840 2160">
  <!-- hyprland-el wallpaper "{theme['name']}" ({motif}), MIT -->{_defs(theme, cols)}
  <rect width="3840" height="2160" fill="url(#bg)"/>{body}
  <rect width="3840" height="2160" fill="url(#vignette)"/>
</svg>
"""


def render(theme, width, height, cache_dir):
    """Render the theme wallpaper as PNG (cover crop to width x height)."""
    os.makedirs(cache_dir, exist_ok=True)
    png = os.path.join(cache_dir, f"{theme['id']}-{width}x{height}.png")
    if os.path.exists(png):
        return png
    src = os.path.join(cache_dir, f"{theme['id']}.svg")
    with open(src, "w") as f:
        f.write(svg(theme))
    # scale to cover, the SVG is 16:9
    scale = max(width / 3840, height / 2160)
    w, h = max(1, round(3840 * scale)), max(1, round(2160 * scale))
    tmp = png + ".tmp"
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h), "-o", tmp, src], check=True)
    os.replace(tmp, png)
    return png
