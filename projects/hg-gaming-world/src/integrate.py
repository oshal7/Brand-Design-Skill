"""Lockups where the type is built on the mark's own geometry (straight + tilted), variant A."""
import sys, math; sys.path.insert(0, '.')
import logo2
from logo2 import layers, one_colour, TILT, vbox, parts, WL, WR, GAP, H, DROP, D, O
from typo import glyph_shapes
from geo import svg
from shapely import affinity
from shapely.ops import unary_union
from shapely.geometry import Point
FONT = "/home/user/Brand-Design-Skill/projects/hg-gaming-world/03-typography/font/HGWDisplay-ExtraBold.ttf"
LINES = ("Happy", "Gaming", "World"); LEAD = 1.18

def text_block(cap):
    """Three lines; origin at top-left of the cap line of line 1; returns geom, block height (cap top -> last baseline)."""
    geoms = []
    for i, s in enumerate(LINES):
        gl, _ = glyph_shapes(FONT, s, cap, -0.015)
        g = unary_union([g for ch, g, x in gl if g is not None])
        geoms.append(affinity.translate(g, 0, cap + i * cap * LEAD))
    t = unary_union(geoms); x0 = t.bounds[0]
    return affinity.translate(t, -x0, 0), cap + 2 * cap * LEAD

def g_frame(tilt):
    """Key points of the g block (face) after tilt: top-right corner, bottom-right corner, top-left."""
    Lb, Lf, Rb, Rf = parts()
    c = unary_union([Lb, Rb]).centroid
    X0 = WL + GAP
    pts = {"tr": (X0 + WR, DROP), "br": (X0 + WR, DROP + H), "tl": (X0, DROP)}
    return {k: affinity.rotate(Point(p), tilt, origin=c).coords[0] for k, p in pts.items()}

def build(rule, tilt):
    L = layers(tilt); mark = unary_union([g for _, g, _ in L])
    fr = g_frame(tilt)
    gh = H                                     # g block height
    cap = gh / (1 + 2 * LEAD)                  # text block exactly as tall as the g block
    t, th = text_block(cap)
    gap = D + O + 0.45 * cap                   # clear the depth, then one consistent gap
    a = math.radians(tilt)
    ux, uy = math.cos(a), math.sin(a)          # direction of the g block's top edge
    vx, vy = -math.sin(a), math.cos(a)         # direction of its right edge (down)
    if rule == "centred":                      # what we had: straight block, centred on the whole mark
        mx0, my0, mx1, my1 = mark.bounds; s = 0.78 * (my1 - my0) / th
        t = affinity.scale(t, s, s, origin=(0, 0)); x0, y0, x1, y1 = t.bounds
        t = affinity.translate(t, mx1 + 0.1 * (mx1 - mx0) - x0, (my0 + my1) / 2 - (y0 + y1) / 2)
    elif rule == "aligned":                    # straight lines; cap line = g top, block height = g height
        tx, ty = fr["tr"]; t = affinity.translate(t, tx + gap, ty)
    elif rule == "rotated":                    # whole block on the mark's axis
        t = affinity.rotate(t, tilt, origin=(0, 0))
        tx, ty = fr["tr"]; t = affinity.translate(t, tx + ux * gap, ty + uy * gap)
    elif rule == "stepped":                    # level lines, each starting on the slanted right edge
        parts_ = []
        for i, s in enumerate(LINES):
            gl, _ = glyph_shapes(FONT, s, cap, -0.015)
            g = unary_union([g for ch, g, x in gl if g is not None]); g = affinity.translate(g, -g.bounds[0], 0)
            down = cap * 0.5 + i * cap * LEAD                     # line centre, measured down the right edge
            px, py = fr["tr"][0] + vx * down, fr["tr"][1] + vy * down
            parts_.append(affinity.translate(g, px + gap, py + cap * 0.5))
        t = unary_union(parts_)
    elif rule == "slanted":                    # letters lean with the mark (shear = tilt)
        t = affinity.skew(t, xs=-tilt, origin=(0, 0))
        tx, ty = fr["tr"]; t = affinity.translate(t, tx + gap, ty)
    vb = vbox([mark, t], 40)
    return L, t, vb

if __name__ == "__main__":
    OUT = sys.argv[1]
    combos = [("straight", 0, "centred"), ("straight", 0, "aligned"), ("tilted", TILT, "centred"), ("tilted", TILT, "rotated"), ("tilted", TILT, "stepped"), ("tilted", TILT, "slanted")]
    for name, tilt, rule in combos:
        L, t, vb = build(rule, tilt)
        open(f"{OUT}/hgw-a-{name}-{rule}-black.svg", "w").write(svg([("mark", one_colour(tilt), "#0A0A10"), ("type", t, "#0A0A10")], vb, "Happy Gaming World"))
        open(f"{OUT}/hgw-a-{name}-{rule}-on-dark.svg", "w").write(svg(L + [("type", t, "#FFFFFF")], vb, "Happy Gaming World"))
    print("ok")
