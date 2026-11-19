# Simplified plot maps traced from the two satellite maps in the family dossier (§5).
# Shapes are approximate on purpose: they show where the orchards sit inside the land, not survey lines.

FIG = {
 "w": 792, "h": 261,
 "bound": [(18,88),(490,88),(490,126),(755,126),(755,170),(270,188),(20,232)],
 "plots": [
  [(20,90),(160,88),(155,110),(140,160),(125,150),(118,128),(20,106)],
  ("e",210,145,52,31), [(198,90),(238,90),(238,113),(198,113)], ("e",292,136,15,18),
  ("e",412,148,33,23), [(238,90),(268,92),(268,128),(236,121)], ("e",58,163,25,15), ("e",74,128,35,20),
 ],
}
NOG = {
 "w": 792, "h": 294,
 "bound": [(248,78),(728,66),(728,116),(622,118),(622,215),(445,224),(125,233),(125,180),(10,176),(10,133),(248,127)],
 "plots": [
  [(15,135),(205,128),(182,165),(60,178),(18,166)], [(308,150),(335,150),(335,175),(308,175)],
  [(340,122),(500,122),(490,160),(440,166),(345,156)], [(540,118),(612,118),(608,160),(530,158)],
  [(125,182),(440,175),(452,195),(432,214),(130,228)], [(445,216),(545,180),(580,214),(452,222)],
  [(585,168),(622,165),(624,214),(600,215)], [(315,81),(350,79),(352,115),(320,115)],
  [(352,76),(540,72),(570,95),(560,118),(352,118)], [(575,72),(605,70),(605,112),(578,112)],
  [(615,69),(725,67),(726,114),(620,116)],
 ],
}

import math, random

def _ellipse(cx, cy, rx, ry, seed):
    r = random.Random(seed); n = 14
    return [(cx + rx * math.cos(2*math.pi*i/n) * (1 + r.uniform(-.08, .08)),
             cy + ry * math.sin(2*math.pi*i/n) * (1 + r.uniform(-.08, .08))) for i in range(n)]

def _smooth(pts, t=.18):
    """Closed Catmull-Rom curve through the points, as an SVG path (soft, hand-drawn edges)."""
    n = len(pts); d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(n):
        p0, p1, p2, p3 = pts[i-1], pts[i], pts[(i+1) % n], pts[(i+2) % n]
        c1 = (p1[0] + (p2[0]-p0[0])*t, p1[1] + (p2[1]-p0[1])*t)
        c2 = (p2[0] - (p3[0]-p1[0])*t, p2[1] - (p3[1]-p1[1])*t)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d + "Z"

def _densify(pts, step=26):
    out = []
    for i, a in enumerate(pts):
        b = pts[(i+1) % len(pts)]; L = math.dist(a, b); k = max(1, int(L // step))
        out += [(a[0] + (b[0]-a[0])*j/k, a[1] + (b[1]-a[1])*j/k) for j in range(k)]
    return out

def _poly(pts): return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"

def _forest(uid, seed):
    r = random.Random(seed); dots = []
    for _ in range(34):
        x, y = r.uniform(0, 48), r.uniform(0, 48)
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r.uniform(.7, 1.6):.2f}"/>')
    return (f'<pattern id="fo{uid}" width="48" height="48" patternUnits="userSpaceOnUse">'
            f'<g fill="#3f5a34">{"".join(dots)}</g></pattern>')

def _rows(uid):
    # orchard rows: gold trees in lines, slightly tilted like the real planting
    return (f'<pattern id="or{uid}" width="5.5" height="5.5" patternUnits="userSpaceOnUse" patternTransform="rotate(-9)">'
            f'<rect width="5.5" height="5.5" fill="#26261a"/><circle cx="2.75" cy="2.75" r="1.45" fill="#c4a46a"/></pattern>')

def svg(m, uid, label):
    xs = [x for x, _ in m["bound"]]; ys = [y for _, y in m["bound"]]
    pad = 8
    vx, vy, w, h = min(xs)-pad, min(ys)-pad, max(xs)-min(xs)+2*pad, max(ys)-min(ys)+2*pad
    plots = []
    for i, p in enumerate(m["plots"]):
        pts = _ellipse(*p[1:], seed=i) if isinstance(p, tuple) else _densify(p)
        cx = sum(x for x, _ in pts) / len(pts)
        plots.append((cx, _smooth(pts)))
    plots.sort()  # reveal left to right
    b = _poly(m["bound"])
    g = "".join(f'<path d="{d}" style="--i:{i}"/>' for i, (_, d) in enumerate(plots))
    return (f'<svg class="map" viewBox="{vx} {vy} {w} {h}" role="img" aria-label="{label}">'
            f'<defs>{_forest(uid, len(uid))}{_rows(uid)}<clipPath id="c{uid}"><path d="{b}"/></clipPath></defs>'
            f'<path class="land" d="{b}" fill="#151b12"/><path d="{b}" fill="url(#fo{uid})"/>'
            f'<g class="plots" clip-path="url(#c{uid})" fill="url(#or{uid})" stroke="#c4a46a" stroke-width="1">{g}</g>'
            f'<path class="edge" d="{b}" pathLength="1" fill="none" stroke="#e9e9e4" stroke-opacity=".6" stroke-width=".9"/>'
            f'</svg>')
