"""Variant B: staggered + the h block gets a true h arch (cut opening from the bottom), so it can't read as a 6."""
import sys, math; sys.path.insert(0, '.')
import logo2
from logo2 import *
from shapely.geometry import Polygon, LineString, box

def h_arch(W=WL, Hh=H):
    """h counter: opens from the bottom edge; round top-right (inside of the shoulder), sharp top-left (stem join)."""
    x0, x1, yt = 0.52 * W, 0.52 * W + 76, 0.42 * Hh
    return rrect(x0, yt, x1, Hh + 2, tr=60)

from shapely.geometry import Point
ORIG_PARTS = logo2.parts
def parts_b(drop=DROP):
    L_blk = rrect(0, 0, WL, H, tl=R_GRIP)
    small_dpad = affinity.translate(affinity.scale(dpad(0, 0), 0.72, 0.72, origin=(0, 0)), 100, 430)
    L_face = L_blk.difference(h_arch()).difference(small_dpad)
    _, _, Rb, Rf = ORIG_PARTS(drop)
    mit = dict(quad_segs=RES, join_style="mitre")
    Lb = unary_union([L_blk.buffer(O, **mit), sweep(L_blk, D, D).buffer(O, **mit)])
    return Lb, L_face, Rb, Rf

def use_b():
    logo2.parts = parts_b

if __name__ == "__main__":
    OUT = sys.argv[1]
    use_b()
    for name, tilt in [("straight", 0), ("tilted", TILT)]:
        L = layers(tilt); vb = vbox([g for _, g, _ in L])
        open(f"{OUT}/hg-b-{name}-primary.svg", "w").write(svg(L, vb, f"HG logo variant B {name}", size=1024))
        open(f"{OUT}/hg-b-{name}-primary-on-dark.svg", "w").write(svg(L, vb, f"HG logo variant B {name}", bg="#0A0A10", size=1024))
        for c, hexv in [("black", "#0A0A10"), ("white", "#FFFFFF"), ("blue", "#2E1FF5")]:
            open(f"{OUT}/hg-b-{name}-one-colour-{c}.svg", "w").write(svg([("mark", one_colour(tilt), hexv)], vb, "HG logo variant B", size=1024))
    print("ok")
