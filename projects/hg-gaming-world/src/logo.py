"""HG mark v2 — faithful to the original: sharp h-block, rounded g-block, tapered hook/smile
with sharp angled terminals, pointed arrow-key D-pad. Measured from the original artwork."""
import sys, math; sys.path.insert(0, '.')
import numpy as np
from geo import *
from shapely import affinity
from shapely.geometry import Polygon, box

k = 600 / 587                      # original px -> grid units
H, GAP = 600, 24
R_GRIP = 220                       # the two big outer corners (h top-left, g bottom-right)
G_TL, G_TR = 80, 72                # the g's softer top corners

def P(x, y): return (x * k, y * k)  # original local px -> units

def fit_circle(pts):
    A = np.array([[2*x, 2*y, 1] for x, y in pts]); b = np.array([x*x + y*y for x, y in pts])
    cx, cy, c = np.linalg.lstsq(A, b, rcond=None)[0]
    return cx, cy, math.sqrt(c + cx*cx + cy*cy)

def fit_tangent_top(pts, ytop):
    """circle tangent to the horizontal line y=ytop from below: centre (xt, ytop+r)."""
    best = None
    for xt in np.linspace(200, 420, 441):
        # r from least squares on (x-xt)^2 + (y-ytop-r)^2 = r^2  ->  r = ((x-xt)^2+(y-ytop)^2) / (2(y-ytop))
        rs = [((x-xt)**2 + (y-ytop)**2) / (2*(y-ytop)) for x, y in pts]
        r = float(np.mean(rs)); err = float(np.var(rs))
        if best is None or err < best[0]: best = (err, xt, r)
    return best[1], ytop + best[2], best[2]

def ang(c, p): return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))

# ---- slits: measured in the original, each in a "hook frame" (opening on the right edge) ----
def make_slit(Wu, upper, ytop, u_end, lower, l_end):
    cu = fit_tangent_top([P(*p) for p in [u_end] + upper], ytop * k)
    c0 = fit_circle([P(*p) for p in [l_end] + lower])
    cl = (Wu - c0[2], c0[1], c0[2])                  # lobe meets the block edge tangentially
    U, L = P(*u_end), P(*l_end)
    up = arcpts(cu[0], cu[1], cu[2], ang(cu, U), -90, 96)
    a_end = ang(cl, L)
    if a_end > 0: a_end -= 360
    low = arcpts(cl[0], cl[1], cl[2], 0.0, a_end, 96)
    pts = up + [(Wu + 60, ytop * k), (Wu + 60, cl[1] + 60), (Wu, cl[1] + 60)] + low
    return Polygon(pts).buffer(0)

WL, WR = 380, 400                                  # original block widths (371 / 390 px)
HOOK = make_slit(WL, [(205,106), (265,81)], 73, (168,147),
                 [(221,124), (271,111), (315,117), (351,146), (368,182)], (193,153))
# smile points, rotated 180 deg inside the g block (390 x 589 px) into the same frame
f = lambda x, y: (390 - (x - 659), 589 - (y - 169))
SMILE_F = make_slit(WR, [f(865,634), f(845,654), f(795,676), f(745,686)], 589 - (689 - 169), f(875,617),
                    [f(835,624), f(805,645), f(765,655), f(725,648), f(685,620), f(665,588)], f(844,609))

def dpad(cx, cy, a=36, reach=108, tip=20):
    arrows = []
    for rot in (0, 90, 180, 270):
        p = Polygon([(-a, -reach), (a, -reach), (a, -(tip + a)), (0, -tip), (-a, -(tip + a))])
        arrows.append(affinity.translate(affinity.rotate(p, rot, origin=(0, 0)), cx, cy))
    return unary_union(arrows)

def buttons(cx, cy, off=64, r=30):
    return unary_union([circle(cx + dx, cy + dy, r) for dx, dy in [(0,-off),(off,0),(0,off),(-off,0)]])

L_blk = rrect(0, 0, WL, H, tl=R_GRIP)
L_face = L_blk.difference(HOOK).difference(dpad(*P(185.5, 409.5)))

X0 = WL + GAP
rot = lambda g: affinity.translate(affinity.rotate(g, 180, origin=(WR/2, H/2)), X0, 0)
R_blk = rrect(X0, 0, X0 + WR, H, tl=G_TL, tr=G_TR, br=R_GRIP)
bc = (X0 + 194 * k, 191 * k)
R_face = R_blk.difference(rot(SMILE_F)).difference(circle(*bc, 118)).union(buttons(*bc))

face = unary_union([L_face, R_face])
blocks = unary_union([L_blk, R_blk])

if __name__ == "__main__":
    OUT = sys.argv[1]
    BLUE, INK, LIGHT, WHITE, BLACK = "#2E1FF5", "#1C1C1E", "#F2F2F5", "#FFFFFF", "#111111"
    D, O = 80, 16
    body = sweep(blocks, D, D).buffer(O, quad_segs=RES, join_style="mitre")
    minx, miny, maxx, maxy = body.bounds; pad = 64
    vb = (minx - pad, miny - pad, maxx - minx + 2*pad, maxy - miny + 2*pad)
    lay = [("depth", body, BLUE), ("face", face, WHITE)]
    open(f"{OUT}/hg-primary.svg","w").write(svg(lay, vb, "HG Gaming World logo", size=1024))
    open(f"{OUT}/hg-primary-on-light.svg","w").write(svg(lay, vb, "HG Gaming World logo — on light", bg=LIGHT, size=1024))
    open(f"{OUT}/hg-primary-on-dark.svg","w").write(svg(lay, vb, "HG Gaming World logo — on dark", bg=INK, size=1024))
    fx0, fy0, fx1, fy1 = blocks.bounds; p2 = 48
    vbf = (fx0 - p2, fy0 - p2, fx1 - fx0 + 2*p2, fy1 - fy0 + 2*p2)
    for name, col, t in [("white", WHITE, "flat white"), ("blue", BLUE, "flat blue"), ("black", BLACK, "one colour")]:
        open(f"{OUT}/hg-flat-{name}.svg","w").write(svg([("symbol", face, col)], vbf, f"HG Gaming World logo — {t}", size=1024))
