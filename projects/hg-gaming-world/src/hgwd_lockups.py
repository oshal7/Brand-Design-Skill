"""Lockups: the mark (always with depth) + HGW Display, outlined."""
import sys; sys.path.insert(0, '.')
from typo import glyph_shapes
from logo import face as LF, body as LB
from geo import svg
from shapely import affinity
from shapely.ops import unary_union
FONT = sys.argv[2]; OUT = sys.argv[1]
C, LEAD, TRACK = 100, 1.12, -0.01
LAYOUTS = {"stack3": ["HAPPY", "GAMING", "WORLD"], "stack2": ["HAPPY", "GAMING WORLD"], "line": ["HAPPY GAMING WORLD"], "hg-world": ["HG WORLD"], "hgw": ["HGW"]}
def word(t):
    gl, _ = glyph_shapes(FONT, t, C, TRACK)
    return unary_union([g for ch, g, x in gl if g is not None])
def build(key):
    lines = LAYOUTS[key]
    t = unary_union([affinity.translate(word(s), 0, i * C * LEAD) for i, s in enumerate(lines)])
    tx0, ty0, tx1, ty1 = t.bounds; fx0, fy0, fx1, fy1 = LF.bounds
    if key == "hgw":
        s = (tx1 - tx0) / (fx1 - fx0); f = affinity.scale(LF, s, s, origin=(0, 0)); b = affinity.scale(LB, s, s, origin=(0, 0))
        dx = tx0 - f.bounds[0]; dy = ty0 - C * 0.45 - b.bounds[3]
        return affinity.translate(f, dx, dy), affinity.translate(b, dx, dy), t
    h = (ty1 - ty0) if len(lines) > 1 else C * 1.9
    s = h / (fy1 - fy0); f = affinity.scale(LF, s, s, origin=(0, 0)); b = affinity.scale(LB, s, s, origin=(0, 0))
    dx = -f.bounds[0]; dy = (ty0 + ty1) / 2 - (f.bounds[1] + f.bounds[3]) / 2
    f = affinity.translate(f, dx, dy); b = affinity.translate(b, dx, dy)
    return f, b, affinity.translate(t, b.bounds[2] + C * 0.36 - tx0, 0)
for key in LAYOUTS:
    f, b, t = build(key); x0, y0, x1, y1 = unary_union([b, t]).bounds; p = 24
    vb = (x0 - p, y0 - p, x1 - x0 + 2*p, y1 - y0 + 2*p); solo = b.difference(f)
    for mode, layers in {"black": [("mark", solo, "#0A0A10"), ("type", t, "#0A0A10")],
                         "white": [("mark", solo, "#FFFFFF"), ("type", t, "#FFFFFF")],
                         "on-dark": [("depth", b, "#2E1FF5"), ("face", f, "#FFFFFF"), ("type", t, "#FFFFFF")],
                         "on-light": [("depth", b, "#2E1FF5"), ("face", f, "#FFFFFF"), ("type", t, "#0A0A10")]}.items():
        open(f"{OUT}/hgw-{key}-{mode}.svg", "w").write(svg(layers, vb, f"Happy Gaming World — {key}"))
print("ok")
