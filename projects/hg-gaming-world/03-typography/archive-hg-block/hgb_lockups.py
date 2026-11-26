import sys; sys.path.insert(0, '.')
from hgblock import G, setword, C, SP
from logo import face as LF, body as LB, L_blk, R_blk
from geo import svg
from shapely import affinity
from shapely.ops import unary_union
OUT = sys.argv[1]
LEAD = 1.2
LAYOUTS = {"stack3": ["HAPPY", "GAMING", "WORLD"], "stack2": ["HAPPY", "GAMING WORLD"], "line": ["HAPPY GAMING WORLD"], "hg-world": ["HG WORLD"], "hgw": ["HGW"]}
def lines_geom(lines):
    return unary_union([affinity.translate(setword(t)[0], 0, i * C * LEAD) for i, t in enumerate(lines)])
def build(key):
    t = lines_geom(LAYOUTS[key]); tx0, ty0, tx1, ty1 = t.bounds
    fx0, fy0, fx1, fy1 = LF.bounds
    if key == "hgw":
        s = (tx1 - tx0) / (fx1 - fx0); f = affinity.scale(LF, s, s, origin=(0, 0)); b = affinity.scale(LB, s, s, origin=(0, 0))
        dx = tx0 - f.bounds[0]; dy = ty0 - C * 0.5 - b.bounds[3]
        return affinity.translate(f, dx, dy), affinity.translate(b, dx, dy), t
    h = (ty1 - ty0) if len(LAYOUTS[key]) > 1 else C * 1.9
    s = h / (fy1 - fy0); f = affinity.scale(LF, s, s, origin=(0, 0)); b = affinity.scale(LB, s, s, origin=(0, 0))
    dx = -f.bounds[0]; dy = (ty0 + ty1) / 2 - (f.bounds[1] + f.bounds[3]) / 2
    f = affinity.translate(f, dx, dy); b = affinity.translate(b, dx, dy)
    t = affinity.translate(t, b.bounds[2] + C * 0.38 - tx0, 0)
    return f, b, t
for key in LAYOUTS:
    f, b, t = build(key); a = unary_union([b, t]); x0, y0, x1, y1 = a.bounds; p = 24
    vb = (x0 - p, y0 - p, x1 - x0 + 2*p, y1 - y0 + 2*p)
    open(f"{OUT}/hgw-{key}-black.svg", "w").write(svg([("mark", b.difference(f), "#0A0A10"), ("type", t, "#0A0A10")], vb, f"Happy Gaming World — {key}"))
    open(f"{OUT}/hgw-{key}-white.svg", "w").write(svg([("mark", b.difference(f), "#FFFFFF"), ("type", t, "#FFFFFF")], vb, f"Happy Gaming World — {key}"))
    open(f"{OUT}/hgw-{key}-on-dark.svg", "w").write(svg([("depth", b, "#2E1FF5"), ("face", f, "#FFFFFF"), ("type", t, "#FFFFFF")], vb, f"Happy Gaming World — {key}"))
    open(f"{OUT}/hgw-{key}-on-light.svg", "w").write(svg([("depth", b, "#2E1FF5"), ("face", f, "#FFFFFF"), ("type", t, "#0A0A10")], vb, f"Happy Gaming World — {key}"))
# individual letters + the two logo blocks for the construction sheet
for ch in "HAPYGMINWORLD":
    g, w = G[ch]; x0, y0, x1, y1 = g.bounds
    open(f"{OUT}/../construction/letter-{ch}.svg", "w").write(svg([("t", g, "#0A0A10")], (-6, -C - 6, w + 12, C + 12), ch))
for name, blk in [("h-block", L_blk), ("g-block", R_blk)]:
    blk2 = blk.intersection(LF.buffer(0.01)).union(blk.difference(blk))  # face of that block
    part = LF.intersection(blk.buffer(1)); x0, y0, x1, y1 = part.bounds
    open(f"{OUT}/../construction/{name}.svg", "w").write(svg([("t", part, "#0A0A10")], (x0 - 10, y0 - 10, x1 - x0 + 20, y1 - y0 + 20), name))
print("ok")
