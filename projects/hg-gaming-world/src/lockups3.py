import sys; sys.path.insert(0, '.')
from logo2 import layers, one_colour, TILT, vbox
from typo import glyph_shapes
from geo import svg
from shapely import affinity
from shapely.ops import unary_union
OUT = sys.argv[1]
FONTS = {"hgwd": ("/home/user/Brand-Design-Skill/projects/hg-gaming-world/03-typography/font/HGWDisplay-ExtraBold.ttf", -0.015),
         "grotesk": ("/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf", -0.02)}
def word(font, t, cap):
    path, tr = FONTS[font]
    gl, _ = glyph_shapes(path, t, cap, tr)
    return unary_union([g for ch, g, x in gl if g is not None])
def lockup(font, tilt, lines=("Happy", "Gaming", "World"), mode="black"):
    L = layers(tilt); allm = unary_union([g for _, g, _ in L]); mx0, my0, mx1, my1 = allm.bounds
    cap = 100; lead = 1.22
    t = unary_union([affinity.translate(word(font, s, cap), 0, i * cap * lead) for i, s in enumerate(lines)])
    tx0, ty0, tx1, ty1 = t.bounds
    # type block = 78% of mark height, centred on the mark
    s = 0.78 * (my1 - my0) / (ty1 - ty0); t = affinity.scale(t, s, s, origin=(0, 0)); tx0, ty0, tx1, ty1 = t.bounds
    t = affinity.translate(t, mx1 + 0.10 * (mx1 - mx0) - tx0, (my0 + my1) / 2 - (ty0 + ty1) / 2)
    vb = vbox([allm, t], 40)
    if mode == "black": lay = [("mark", one_colour(tilt), "#0A0A10"), ("type", t, "#0A0A10")]
    elif mode == "white": lay = [("mark", one_colour(tilt), "#FFFFFF"), ("type", t, "#FFFFFF")]
    elif mode == "on-dark": lay = layers(tilt) + [("type", t, "#FFFFFF")]
    else: lay = layers(tilt) + [("type", t, "#0A0A10")]
    return svg(lay, vb, "Happy Gaming World")
if __name__ == "__main__":
    pre = sys.argv[2] if len(sys.argv) > 2 else ""
    if pre == "b-":
        import logo3; logo3.use_b()
    for font in FONTS:
        for name, tilt in [("straight", 0), ("tilted", TILT)]:
            for mode in ("black", "white", "on-dark", "on-light"):
                open(f"{OUT}/hgw-{pre}{name}-{font}-stack3-{mode}.svg", "w").write(lockup(font, tilt, mode=mode))
            open(f"{OUT}/hgw-{pre}{name}-{font}-line-black.svg", "w").write(lockup(font, tilt, lines=("Happy Gaming World",), mode="black"))
    print("ok")
