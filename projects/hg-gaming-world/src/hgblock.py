"""HG Block — display lettering built from the mark's two blocks.
Straight letters = the h-block (grip corner top-left, everything else sharp, slots with sharp corners).
Round letters    = the g-block (soft top corners, grip corner bottom-right, sharp bottom-left, circular counters).
Grid: cap height C = 100 (y up is negative: baseline y=0, cap line y=-100)."""
import sys, math; sys.path.insert(0, '.')
from geo import rrect, circle, RES, svg
from shapely.geometry import box, Polygon
from shapely.ops import unary_union
from shapely import affinity

C = 100          # cap height
S = 30           # vertical stem
B = 22           # horizontal bar (optically thinner)
K = 26           # counter / slot width
GRIP_H = 0.55    # h-block grip radius, x letter width  (mark: 220/380 = 0.58)
SOFT_G = 0.20    # g-block soft top corners              (mark: 80/380 = 0.21)
GRIP_G = 0.55    # g-block grip bottom-right
SP = 6           # sidebearing each side -> 18 between letters (mark channel 24/600 of height ~ 4%; type needs more)

def hblock(w, top=-C, bot=0):
    return rrect(0, top, w, bot, tl=min(GRIP_H * w, 0.5 * (bot - top)))
def gblock(w, top=-C, bot=0, sw_sharp=True):
    return rrect(0, top, w, bot, tl=SOFT_G * w, tr=SOFT_G * w, br=min(GRIP_G * w, 0.5 * (bot - top)))
def slot(x0, y0, x1, y1): return box(x0, y0, x1, y1)
def bowl(cx, cy, r): return circle(cx, cy, r)
def tri(*pts): return Polygon(pts)

G = {}
# ---- straight family (h-block) ----
w = 2*S + K
G["H"] = (hblock(w).difference(slot(S, -C-1, S+K, -C/2 - B/2)).difference(slot(S, -C/2 + B/2, S+K, 1)), w)
G["I"] = (hblock(S), S)
w = S + 50
G["L"] = (hblock(w).difference(slot(S, -C-1, w+1, -B)), w)
w = 2*S + K
G["N"] = (hblock(w).difference(tri((S, -C-1), (S+K, -C-1), (S+K, -C+52))).difference(tri((S, 1), (S+K, 1), (S, -52))), w)
w = 2*S + K + 4
G["A"] = (hblock(w).difference(slot(S+2, -C+B, S+K+2, -C/2 + 2)).difference(slot(S+2, -C/2 + 2 + B, S+K+2, 1)), w)
w = 2*S + K + 2
# P / R: h-block with a circular bowl (the g's bowl) and the stem dropping to the baseline
def p_shape(w, leg=False):
    top_h = 70
    body = hblock(w, -C, 0)
    r = (top_h - 2*18) / 2
    cx, cy = S + r + 1, -C + top_h/2
    g = body.difference(bowl(cx, cy, r))
    if leg:
        g = g.difference(slot(S, -C + top_h, S + K - 4, 1))                   # slot between stem and leg
        g = g.difference(tri((w+1, -C + top_h - 12), (w+1, -C + top_h + 12), (w - 12, -C + top_h)))  # 45-degree notch
    else:
        g = g.difference(slot(S, -C + top_h, w + 1, 1))
    return g
G["P"] = (p_shape(w), w)
G["R"] = (p_shape(w, leg=True), w)
w = 2*S + K
yv = -C * 0.42
G["Y"] = (hblock(w).difference(tri((S, -C-1), (S+K, -C-1), (S+K, yv - K/2), (S + K/2, yv), (S, yv - K/2)))
          .difference(tri((-1, 1), (S*0.5, 1), (S*0.5, -C*0.30), (-1, -C*0.30 - S*0.5 - 1)))
          .difference(tri((w+1, 1), (w - S*0.5, 1), (w - S*0.5, -C*0.30), (w+1, -C*0.30 - S*0.5 - 1))), w)
# M / W: three stems, 45-degree notch (the depth angle; W's notch = the W in the mark's depth)
s3, k2 = 26, 22
w = 3*s3 + 2*k2
n = 26
mid = w / 2
G["M"] = (hblock(w).difference(slot(s3, -C*0.62, s3+k2, 1)).difference(slot(2*s3+k2, -C*0.62, 2*s3+2*k2, 1))
          .difference(tri((mid - n, -C-1), (mid + n, -C-1), (mid, -C + n))), w)
G["W"] = (hblock(w).difference(slot(s3, -C-1, s3+k2, -C*0.38)).difference(slot(2*s3+k2, -C-1, 2*s3+2*k2, -C*0.38))
          .difference(tri((mid - n, 1), (mid + n, 1), (mid, -n))), w)
# ---- round family (g-block) ----
w = 2*S + K + 10
r = (w - 2*S) / 2 + 3
G["O"] = (rrect(0, -C, w, 0, tl=0.44*w, tr=0.44*w, br=0.55*w, bl=0.14*w).difference(bowl(w/2, -C/2, r)), w)
G["D"] = (rrect(0, -C, w, 0, tr=0.44*w, br=0.55*w).difference(bowl(w/2 - 2, -C/2, r)), w)
w = 2*S + K + 12
r = 25
cx, cy = w/2 - 2, -C/2
hole = bowl(cx, cy, r).union(slot(cx, cy - r, w + 1, cy - 3))          # bowl + aperture opening to the right edge
spur = slot(cx + 2, cy - 3, w + 1, cy + 11).intersection(bowl(cx, cy, r).union(slot(cx, cy - 3, w + 1, cy + 11)))
G["G"] = (rrect(0, -C, w, 0, tl=0.44*w, tr=0.22*w, br=0.55*w, bl=0.14*w).difference(hole).union(spur), w)
G[" "] = (None, 34)

def setword(text, x0=0, y0=0, space=None):
    out = []; x = x0
    for ch in text:
        g, w = G[ch]
        if g is not None: out.append(affinity.translate(g, x + SP, y0))
        x += w + 2*SP if ch != " " else (space or w)
    return unary_union(out), x

if __name__ == "__main__":
    OUT = sys.argv[1]
    rows = ["HAPPY GAMING WORLD", "HG WORLD", "HGW", "HAPPY", "GAMING", "WORLD"]
    for i, t in enumerate(rows):
        g, _ = setword(t)
        x0, y0, x1, y1 = g.bounds
        open(f"{OUT}/hgblock-{i}.svg", "w").write(svg([("t", g, "#0A0A10")], (x0 - 6, y0 - 6, x1 - x0 + 12, y1 - y0 + 12), t))
    print("ok")
