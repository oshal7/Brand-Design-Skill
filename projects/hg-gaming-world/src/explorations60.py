"""60 iterations of the HG mark (no D-pad): h opening x hook x proportion x composition. g, smile, buttons, 45-degree depth constant."""
import sys, math, itertools; sys.path.insert(0, '.')
import refined2 as M
from geo import rrect, circle, sweep, svg, RES
from shapely.geometry import box, Polygon, Point, LineString
from shapely.ops import unary_union
from shapely import affinity
WL, WR, H, GAP, k = M.WL, M.WR, M.H, M.GAP, M.k
R_GRIP, G_TL, G_TR = M.R_GRIP, M.G_TL, M.G_TR
SLIT = 36 * k; D, O = 80, 16; DROP = 192; TILT = -8

# ---------- h openings (block coords, block = 0..WL x 0..H) ----------
def arch(xc, w, top, r=None):
    r = w / 2 if r is None else r
    return rrect(xc - w/2, top, xc + w/2, H + 2, tl=r, tr=r)
def flare(xc, w, R=44):
    return box(xc - w/2 - R, H - R, xc + w/2 + R, H + 2).difference(
        unary_union([Point(xc - w/2 - R, H - R).buffer(R, quad_segs=RES), Point(xc + w/2 + R, H - R).buffer(R, quad_segs=RES)]))
def sharp_line(xc, w, top, ang=35):
    dy = w * math.tan(math.radians(ang)); return Polygon([(xc - w/2, H + 2), (xc - w/2, top + dy), (xc + w/2, top), (xc + w/2, H + 2)])
def crescent():
    """curved cut rising from the bottom and bending left - the smile's vocabulary turned into an h counter."""
    pts = [(0.62 * WL, H + 30)] + [(0.62 * WL - 70 + 70 * math.cos(math.radians(a)), 0.60 * H + 70 * math.sin(math.radians(-a))) for a in range(0, 181, 6)]
    return LineString(pts).buffer(SLIT / 2 + 6, quad_segs=RES, cap_style="flat")
OPEN = {
  "A": ("narrow arch",        lambda: arch(0.48 * WL, 84, 0.66 * H)),
  "B": ("wide arch",          lambda: arch(0.50 * WL, 116, 0.55 * H)),
  "C": ("tall arch",          lambda: arch(0.50 * WL, 72, 0.45 * H)),
  "D": ("square slot",        lambda: rrect(0.50 * WL - 46, 0.58 * H, 0.50 * WL + 46, H + 2)),
  "E": ("flared arch",        lambda: arch(0.50 * WL, 84, 0.62 * H).union(flare(0.50 * WL, 84))),
  "F": ("line, round end",    lambda: arch(0.50 * WL, SLIT, 0.48 * H)),
  "G": ("line, sharp end",    lambda: sharp_line(0.50 * WL, SLIT, 0.46 * H)),
  "H": ("offset arch",        lambda: arch(0.60 * WL, 92, 0.56 * H)),
  "I": ("shoulder arch",      lambda: rrect(0.47 * WL - 44, 0.57 * H, 0.47 * WL + 44, H + 2, tr=60)),
  "J": ("crescent cut",       lambda: crescent()),
}
# ---------- hooks ----------
HOOK = M.HOOK
def hook_short():
    return HOOK.intersection(box(235, -50, WL + 80, H))
def hook_round():
    h = HOOK.intersection(box(205, -50, WL + 80, H))
    seg = HOOK.boundary.intersection(LineString([(205, -50), (205, 400)]))
    ys = sorted(p.y for p in getattr(seg, "geoms", [seg]) if hasattr(p, "y"))
    if len(ys) >= 2:
        r = (ys[-1] - ys[0]) / 2; h = h.union(Point(205, (ys[0] + ys[-1]) / 2).buffer(r, quad_segs=RES))
    return h
HOOKS = {"m": ("master hook", lambda: HOOK), "s": ("short hook", hook_short), "r": ("round-end hook", hook_round)}

def g_local():
    rot = lambda g: affinity.rotate(g, 180, origin=(WR/2, H/2))
    blk = rrect(0, 0, WR, H, tl=G_TL, tr=G_TR, br=R_GRIP)
    bc = (194 * k, 191 * k)
    return blk, blk.difference(rot(M.SMILE_F)).difference(circle(*bc, 118)).union(M.buttons(*bc))

def build(op, hk, comp, sx=1.0):
    hb = rrect(0, 0, WL, H, tl=R_GRIP)
    hf = hb.difference(HOOKS[hk][1]()).difference(OPEN[op][1]())
    gb, gf = g_local()
    sc = lambda g: affinity.scale(g, sx, 1, origin=(0, 0))
    hb, hf, gb, gf = sc(hb), sc(hf), sc(gb), sc(gf)
    drop = DROP if comp in ("stag", "tilt") else 0
    x0 = WL * sx + GAP
    gb, gf = affinity.translate(gb, x0, drop), affinity.translate(gf, x0, drop)
    mit = dict(quad_segs=RES, join_style="mitre")
    Lb = unary_union([hb.buffer(O, **mit), sweep(hb, D, D).buffer(O, **mit)])
    Rb = unary_union([gb.buffer(O, **mit), sweep(gb, D, D).buffer(O, **mit)])
    geoms = [Lb, hf, Rb, gf]
    if comp == "tilt":
        c = unary_union([Lb, Rb]).centroid; geoms = [affinity.rotate(g, TILT, origin=c) for g in geoms]
    Lb, hf, Rb, gf = geoms
    solo = Lb.difference(hf).difference(Rb).union(Rb.difference(gf))
    colour = [("h-depth", Lb, "#2E1FF5"), ("h-face", hf.difference(Rb), "#FFFFFF"), ("g-depth", Rb, "#2E1FF5"), ("g-face", gf, "#FFFFFF")]
    x0_, y0_, x1_, y1_ = unary_union([Lb, Rb]).bounds
    vb = (x0_ - 40, y0_ - 40, x1_ - x0_ + 80, y1_ - y0_ + 80)
    return solo, colour, vb

# curated set: every opening in all 3 compositions (30), hooks on 5 openings x 2 comps (20), compact on 5 openings (5), extra tilt-compact (5)
SET = []
for op in OPEN:
    for comp in ("align", "stag", "tilt"): SET.append((op, "m", comp, 1.0))
for op in ["A", "B", "E", "I", "J"]:
    for hk in ("s", "r"):
        SET.append((op, hk, "align", 1.0)); SET.append((op, hk, "stag", 1.0))
for op in ["A", "B", "E", "I", "J"]:
    SET.append((op, "r", "align", 0.82)); SET.append((op, "m", "tilt", 0.82))

if __name__ == "__main__":
    OUT = sys.argv[1]
    for n, (op, hk, comp, sx) in enumerate(SET, 1):
        solo, colour, vb = build(op, hk, comp, sx)
        name = f"{n:02d}-{op}{hk}-{comp}{'-compact' if sx < 1 else ''}"
        open(f"{OUT}/{name}-black.svg", "w").write(svg([("mark", solo, "#0A0A10")], vb, name))
        open(f"{OUT}/{name}-on-dark.svg", "w").write(svg(colour, vb, name, bg="#0A0A10"))
    print(len(SET), "iterations")
