"""Patterns extracted from the HG mark. Each is built from the logo's own geometry."""
import sys, math, random; sys.path.insert(0, '.')
from logo import dpad, buttons, HOOK, R_GRIP, face as LF, body as LB, D
from small import s_face, s_body
from geo import *
from shapely import affinity
from shapely.geometry import box, Polygon

Wc, Hc = 1600, 1000
CANVAS = box(0, 0, Wc, Hc)

def place(g, x, y, s=1.0, r=0):
    g = affinity.scale(g, s, s, origin=(0, 0))
    if r: g = affinity.rotate(g, r, origin=(0, 0))
    return affinity.translate(g, x, y)

def grid(step_x, step_y, half_drop=False):
    for j in range(-1, int(Hc / step_y) + 2):
        for i in range(-1, int(Wc / step_x) + 2):
            yield i * step_x + (step_x / 2 if (half_drop and j % 2) else 0), j * step_y, i, j

def p_dpad():
    unit = dpad(0, 0)                                   # the arrow-key D-pad, centred
    return unary_union([place(unit, x, y, 0.42) for x, y, i, j in grid(150, 150, True)]).intersection(CANVAS)

def p_buttons():
    ring = circle(0, 0, 118).difference(buttons(0, 0))  # the button ring (bowl + 4 buttons)
    return unary_union([place(ring, x, y, 0.38) for x, y, i, j in grid(120, 104, True)]).intersection(CANVAS)

def p_blocks():
    solo = s_body.difference(s_face)                    # small-size mark, one colour, depth kept
    minx, miny, maxx, maxy = solo.bounds
    solo = affinity.translate(solo, -(minx + maxx) / 2, -(miny + maxy) / 2)
    return unary_union([place(solo, x, y, 0.19) for x, y, i, j in grid(230, 170, True)]).intersection(CANVAS)

def p_depth_lines():
    """45-degree extrusion lines: parallel bands at the depth angle, stepped like extruded block edges."""
    bands = []
    for k in range(-40, 60):
        off = k * 64
        bands.append(Polygon([(off, 0), (off + 22, 0), (off + 22 + Hc, Hc), (off + Hc, Hc)]))
    lines = unary_union(bands)
    # interrupt with block-shaped windows (the HG blocks, scaled) to show the "extruded" rhythm
    win = unary_union([place(box(0, 0, 380, 600), x, y, 0.28) for x, y, i, j in grid(260, 260, True)])
    return lines.difference(win).intersection(CANVAS)

def p_truchet(seed=7):
    """Grip-corner Truchet: each cell holds two quarter-rings built from the logo's big grip corner."""
    random.seed(seed); c = 100; t = 24; out = []
    for x, y, i, j in grid(c, c):
        r_mid = c / 2
        q1 = Point(x, y).buffer(r_mid + t/2, quad_segs=RES).difference(Point(x, y).buffer(r_mid - t/2, quad_segs=RES))
        q2 = Point(x + c, y + c).buffer(r_mid + t/2, quad_segs=RES).difference(Point(x + c, y + c).buffer(r_mid - t/2, quad_segs=RES))
        cell = box(x, y, x + c, y + c)
        g = unary_union([q1, q2]).intersection(cell)
        if random.random() < 0.5: g = affinity.rotate(g, 90, origin=(x + c/2, y + c/2))
        out.append(g)
    return unary_union(out).intersection(CANVAS)

def p_smile():
    """The hook/smile cut repeated as a happy wave."""
    h = HOOK.intersection(box(0, 0, 380, 400))
    minx, miny, maxx, maxy = h.bounds
    h = affinity.translate(h, -minx, -miny)
    rows = []
    for x, y, i, j in grid(150, 70, True):
        g = place(h, x, y, 0.55, 0 if j % 2 == 0 else 180)
        rows.append(g)
    return unary_union(rows).intersection(CANVAS)

from shapely.geometry import Point
PATTERNS = {"01-dpad-grid": p_dpad, "02-button-field": p_buttons, "03-hg-blocks": p_blocks,
            "04-depth-lines": p_depth_lines, "05-grip-truchet": p_truchet, "06-smile-wave": p_smile}
WAYS = {"subtle-dark": ("#0A0A10", "#1E1E29"), "indigo": ("#2E1FF5", "#4A3DFF"), "loud": ("#0A0A10", "#C6FF33"), "light": ("#F4F4F8", "#DCDAF5")}

if __name__ == "__main__":
    OUT = sys.argv[1]
    for name, fn in PATTERNS.items():
        g = fn()
        for way, (bg, fg) in WAYS.items():
            open(f"{OUT}/{name}-{way}.svg", "w").write(svg([("pattern", g, fg)], (0, 0, Wc, Hc), f"HG pattern {name} {way}", bg=bg, size=Wc))
        print(name, "ok")
