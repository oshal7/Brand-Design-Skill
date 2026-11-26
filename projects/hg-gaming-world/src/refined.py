"""Faithful refinement of the original HG mark (two controller-half blocks, 180° rotational pair)."""
import sys, math; sys.path.insert(0, '.')
from geo import *
from shapely import affinity
from shapely.geometry import box

# ---- grid (unit = 8) -------------------------------------------------------
W, H   = 384, 600        # each block
GAP    = 24              # channel between the blocks
R, r   = 224, 40         # grip corner (outer) / standard corner
SLIT   = 36              # one cut width: hook, smile
FLARE  = 100             # radius where the slit opens to the edge
# hook: horizontal from the inner edge, then an arc down-left to a round terminal
Y0, ARC_C, ARC_R, A_END = 96, (300, 266), 170, 228
ICON   = (192, 416)      # D-pad centre (left) == bowl centre (right, rotated)

def block_with_slit():
    blk = rrect(0, 0, W, H, tl=R, tr=r, br=r, bl=r)
    path = [(W + 60, Y0), (ARC_C[0], Y0)] + arcpts(*ARC_C, ARC_R, 270, A_END, 48)
    cut = stroke(path, SLIT)
    # flare: round off the body's corner under the slit so the cut opens to the edge
    top = Y0 + SLIT / 2
    corner = box(W - FLARE, top, W + 1, top + FLARE).difference(
             rrect(W - 2 * FLARE, top, W, top + 2 * FLARE, tr=FLARE))
    return blk, blk.difference(cut).difference(corner)

def dpad(cx, cy, L=216, arm=72, x_gap=12):
    plus = unary_union([box(cx - L/2, cy - arm/2, cx + L/2, cy + arm/2),
                        box(cx - arm/2, cy - L/2, cx + arm/2, cy + L/2)])
    plus = fillet(plus, 4)
    e = arm / 2
    xcut = unary_union([stroke([(cx - e, cy - e), (cx + e, cy + e)], x_gap, cap="flat"),
                        stroke([(cx - e, cy + e), (cx + e, cy - e)], x_gap, cap="flat")])
    return plus.difference(xcut)            # the 4 arrows (cut from the block)

def buttons(cx, cy, off=64, rad=30):
    return unary_union([circle(cx + dx, cy + dy, rad) for dx, dy in [(0,-off),(off,0),(0,off),(-off,0)]])

L_blk, L_face = block_with_slit()
L_face = L_face.difference(dpad(*ICON))

# right block = left block rotated 180° (exact rotational pair), but with the bowl + buttons
R_blk0, R_face0 = block_with_slit()
rot = lambda g: affinity.translate(affinity.rotate(g, 180, origin=(W/2, H/2)), W + GAP, 0)
R_blk = rot(R_blk0)
R_face = rot(R_face0)
bc = (W + GAP + W - ICON[0], H - ICON[1])
R_face = R_face.difference(circle(*bc, 116)).union(buttons(*bc))

face  = unary_union([L_face, R_face])
blocks = unary_union([L_blk, R_blk])

if __name__ == "__main__":
    OUT = sys.argv[1]
    BLUE, INK, WHITE, BLACK = "#2E1FF5", "#1C1C1E", "#FFFFFF", "#111111"
    D, O = 80, 16
    body = sweep(blocks, D, D).buffer(O, quad_segs=RES)
    minx, miny, maxx, maxy = body.bounds
    pad = 64
    vb = (minx - pad, miny - pad, maxx - minx + 2*pad, maxy - miny + 2*pad)
    open(f"{OUT}/hg-depth-on-dark.svg","w").write(svg([("depth", body, BLUE), ("face", face, WHITE)], vb, "HG Gaming World logo — depth", bg=INK, size=1024))
    open(f"{OUT}/hg-depth-on-light.svg","w").write(svg([("depth", body, BLUE), ("face", face, WHITE)], vb, "HG Gaming World logo — depth on light", bg="#F2F2F5", size=1024))
    open(f"{OUT}/hg-depth-transparent.svg","w").write(svg([("depth", body, BLUE), ("face", face, WHITE)], vb, "HG Gaming World logo — depth", size=1024))
    # flat versions: cropped to the blocks only
    fx0, fy0, fx1, fy1 = blocks.bounds
    p2 = 48
    vbf = (fx0 - p2, fy0 - p2, fx1 - fx0 + 2*p2, fy1 - fy0 + 2*p2)
    open(f"{OUT}/hg-flat-black.svg","w").write(svg([("symbol", face, BLACK)], vbf, "HG Gaming World logo — flat", size=1024))
    open(f"{OUT}/hg-flat-white-on-dark.svg","w").write(svg([("symbol", face, WHITE)], vbf, "HG Gaming World logo — flat reversed", bg=INK, size=1024))
    open(f"{OUT}/hg-flat-white.svg","w").write(svg([("symbol", face, WHITE)], vbf, "HG Gaming World logo — flat white", size=1024))
    open(f"{OUT}/hg-flat-blue.svg","w").write(svg([("symbol", face, BLUE)], vbf, "HG Gaming World logo — flat blue", size=1024))
    print("viewBox depth", vb)
