"""HG mark v3 — staggered: the h block rises, the g block drops (ascender / descender), straight and tilted.
Same geometry as the master (cuts, D-pad, buttons, corners); per-block 45-degree depth; g block sits in front."""
import sys; sys.path.insert(0, '.')
from logo import (HOOK, SMILE_F, dpad, buttons, P, k, WL, WR, GAP, H, R_GRIP, G_TL, G_TR, rrect, circle,
                      unary_union, affinity, sweep, svg, RES)
DROP = 192                         # 0.32 x block height: the g hangs below the h like a descender
D, O = 80, 16
TILT = -8                          # degrees for the tilted version (counter-clockwise)

def parts(drop=DROP):
    L_blk = rrect(0, 0, WL, H, tl=R_GRIP)
    L_face = L_blk.difference(HOOK).difference(dpad(*P(185.5, 409.5)))
    X0 = WL + GAP
    rot = lambda g: affinity.translate(affinity.rotate(g, 180, origin=(WR/2, H/2)), X0, drop)
    R_blk = affinity.translate(rrect(0, 0, WR, H, tl=G_TL, tr=G_TR, br=R_GRIP), X0, drop)
    bc = (X0 + 194 * k, 191 * k + drop)
    R_face = R_blk.difference(rot(SMILE_F)).difference(circle(*bc, 118)).union(buttons(*bc))
    mit = dict(quad_segs=RES, join_style="mitre")
    L_body = unary_union([L_blk.buffer(O, **mit), sweep(L_blk, D, D).buffer(O, **mit)])
    R_body = unary_union([R_blk.buffer(O, **mit), sweep(R_blk, D, D).buffer(O, **mit)])
    return L_body, L_face, R_body, R_face

def layers(tilt=0, face="#FFFFFF", depth="#2E1FF5"):
    """Painter's order: h (back) then g (front). Returns list of (id, geom, fill)."""
    Lb, Lf, Rb, Rf = parts()
    geoms = [Lb, Lf, Rb, Rf]
    if tilt:
        c = unary_union([Lb, Rb]).centroid
        geoms = [affinity.rotate(g, tilt, origin=c) for g in geoms]
    Lb, Lf, Rb, Rf = geoms
    return [("h-depth", Lb, depth), ("h-face", Lf.difference(Rb), face), ("g-depth", Rb, depth), ("g-face", Rf, face)]

def one_colour(tilt=0):
    Lb, Lf, Rb, Rf = [g for _, g, _ in layers(tilt)]
    return Lb.difference(Lf).difference(Rb).union(Rb.difference(Rf))

def vbox(geoms, pad=48):
    x0, y0, x1, y1 = unary_union(geoms).bounds
    return (x0 - pad, y0 - pad, x1 - x0 + 2*pad, y1 - y0 + 2*pad)

if __name__ == "__main__":
    OUT = sys.argv[1]
    for name, tilt in [("straight", 0), ("tilted", TILT)]:
        L = layers(tilt); vb = vbox([g for _, g, _ in L])
        open(f"{OUT}/hg-{name}-primary.svg", "w").write(svg(L, vb, f"HG Gaming World logo — {name}", size=1024))
        open(f"{OUT}/hg-{name}-primary-on-dark.svg", "w").write(svg(L, vb, f"HG Gaming World logo — {name}", bg="#0A0A10", size=1024))
        solo = one_colour(tilt)
        for c, hexv in [("black", "#0A0A10"), ("white", "#FFFFFF"), ("blue", "#2E1FF5")]:
            open(f"{OUT}/hg-{name}-one-colour-{c}.svg", "w").write(svg([("mark", solo, hexv)], vb, f"HG Gaming World logo — {name}, one colour", size=1024))
    print("ok")
