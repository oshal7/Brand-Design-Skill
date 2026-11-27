"""Tilted mark + LEVEL type: many lockup iterations. Text is never rotated."""
import sys, math; sys.path.insert(0, '.')
from logo2 import layers, one_colour, TILT, vbox, parts, WL, WR, GAP, H, DROP, D, O
from typo import glyph_shapes
from geo import svg
from shapely import affinity
from shapely.ops import unary_union
from shapely.geometry import Point, box
HGWD = "/home/user/Brand-Design-Skill/projects/hg-gaming-world/03-typography/font/HGWDisplay-ExtraBold.ttf"
GROT = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
TL = TILT
LEADV = 1.18
L = layers(TL); MARK = unary_union([g for _, g, _ in L]); SOLO = one_colour(TL)
mx0, my0, mx1, my1 = MARK.bounds
_, _, Rb, Rf = parts(); _c = unary_union([parts()[0], Rb]).centroid
def rp(p): return affinity.rotate(Point(p), TL, origin=_c).coords[0]
X0 = WL + GAP
G = {"tl": rp((X0, DROP)), "tr": rp((X0 + WR, DROP)), "br": rp((X0 + WR, DROP + H)), "bl": rp((X0, DROP + H))}
Hb = {"tl": rp((0, 0)), "tr": rp((WL, 0))}

def word(t, cap, font=HGWD, tr=-0.015):
    gl, _ = glyph_shapes(font, t, cap, tr)
    g = unary_union([g for ch, g, x in gl if g is not None]); return affinity.translate(g, -g.bounds[0], 0)

def edge_x(y0, y1, geom=MARK):
    """Right-most x of the mark within the horizontal band y0..y1 (or the nearest band if empty)."""
    band = geom.intersection(box(mx0 - 10, y0, mx1 + 10, y1))
    return band.bounds[2] if not band.is_empty else geom.bounds[2]

def place(lines, cap, top, gapk=0.45, lead=None, mode="follow", font=HGWD, x_fixed=None):
    """lines placed level; mode 'follow' = each line clears the mark's silhouette by the same gap."""
    out = []; gap = gapk * cap; lead = lead or LEADV
    for i, s in enumerate(lines):
        base = top + cap + i * cap * lead
        w = word(s, cap, font)
        if mode == "follow": x = edge_x(base - cap, base + cap * 0.25) + gap
        else: x = x_fixed
        out.append(affinity.translate(w, x, base))
    return unary_union(out)

ITER = {}
cap_g = H / (1 + 2 * LEADV)          # three lines as tall as one block
# 1 stepped: follows the silhouette, block centred on the g block
def it1():
    top = (G["tr"][1] + G["br"][1]) / 2 - (cap_g * (1 + 2 * LEADV)) / 2
    return place(["Happy", "Gaming", "World"], cap_g, top)
# 2 corner-locked: cap line level with the g block's top-right corner, last baseline level with its bottom-right corner
def it2():
    span = G["br"][1] - G["tr"][1]; cap = span / (1 + 2 * LEADV)
    return place(["Happy", "Gaming", "World"], cap, G["tr"][1])
# 3 ground line: one line; its baseline is the mark's lowest point - the mark stands on the word
def it3():
    cap = cap_g * 0.95; base = my1 - D * 0.0
    w = word("Happy Gaming World", cap); x = edge_x(base - cap, base) + 0.45 * cap
    return affinity.translate(w, x, my1 - (my1 - G["br"][1]) * 0.0 - 0)
# 4 ground stack: three lines, last baseline on the mark's lowest point; flush left at one x (cleanest column)
def it4():
    cap = cap_g; top = my1 - cap * (1 + 2 * 1.18)
    x = edge_x(top, my1) + 0.45 * cap
    return place(["Happy", "Gaming", "World"], cap, top, mode="fixed", x_fixed=x)
# 5 hang line: three lines, cap line level with the mark's highest point (h block top); flush left
def it5():
    cap = cap_g; top = my0 + O
    x = edge_x(top, top + cap * 3.4) + 0.45 * cap
    return place(["Happy", "Gaming", "World"], cap, top, mode="fixed", x_fixed=x)
# 6 cascade: lines step down and right like the blocks do (h high, g lower, then the words)
def it6():
    cap = cap_g * 0.92; out = []
    x0 = edge_x(G["tr"][1], G["tr"][1] + cap) + 0.4 * cap
    for i, s in enumerate(["Happy", "Gaming", "World"]):
        base = G["tr"][1] + cap + i * cap * LEADV
        out.append(affinity.translate(word(s, cap), x0 + i * cap * 0.42, base))
    return unary_union(out)
# 7 two lines: Happy / Gaming World, following the silhouette
def it7():
    cap = cap_g * 1.15; top = (G["tr"][1] + G["br"][1]) / 2 - cap * (1 + LEADV) / 2
    return place(["Happy", "Gaming World"], cap, top)
# 8 stacked under: mark above, one level line below, left edge on the h block's left-most point
def it8():
    cap = cap_g * 0.95; w = word("Happy Gaming World", cap)
    return affinity.translate(w, mx0 + O, my1 + 0.55 * cap + cap)
# 9 stacked under, centred, three lines
def it9():
    cap = cap_g * 0.8; out = []
    for i, s in enumerate(["Happy", "Gaming", "World"]):
        w = word(s, cap); ww = w.bounds[2]
        out.append(affinity.translate(w, (mx0 + mx1) / 2 - ww / 2, my1 + 0.6 * cap + cap + i * cap * LEADV))
    return unary_union(out)
# 10 big type: name as tall as the whole mark, following the silhouette (last-resort option)
def it10():
    cap = (my1 - my0) / (1 + 2 * 1.12); return place(["Happy", "Gaming", "World"], cap, my0, lead=1.12, gapk=0.38)
# 11 other font (grotesk), corner-locked like 2
def it11():
    span = G["br"][1] - G["tr"][1]; cap = span / (1 + 2 * LEADV)
    return place(["Happy", "Gaming", "World"], cap, G["tr"][1], font=GROT)
# 12 axis rule: a level line under the name that the tilted mark's lowest corner touches - the floor it tips on
def it12():
    cap = cap_g; top = my1 - cap * (1 + 2 * 1.18) - cap * 0.55
    x = edge_x(top, my1 - cap * 0.4) + 0.45 * cap
    t = place(["Happy", "Gaming", "World"], cap, top, mode="fixed", x_fixed=x)
    rule = box(mx0 + (mx1 - mx0) * 0.55, my1 - 7, t.bounds[2], my1 + 7)
    return unary_union([t, rule])
ITER = {"01-stepped": it1, "02-corner-locked": it2, "03-ground-line": it3, "04-ground-stack": it4, "05-hang-line": it5,
        "06-cascade": it6, "07-two-lines": it7, "08-under-line": it8, "09-under-stack": it9, "10-big-type": it10,
        "11-grotesk-corner-locked": it11, "12-floor-rule": it12}
if __name__ == "__main__":
    OUT = sys.argv[1]
    for k, fn in ITER.items():
        t = fn(); vb = vbox([MARK, t], 40)
        open(f"{OUT}/tilt-{k}-black.svg", "w").write(svg([("mark", SOLO, "#0A0A10"), ("type", t, "#0A0A10")], vb, "Happy Gaming World"))
        open(f"{OUT}/tilt-{k}-on-dark.svg", "w").write(svg(L + [("type", t, "#FFFFFF")], vb, "Happy Gaming World"))
    print("ok")
