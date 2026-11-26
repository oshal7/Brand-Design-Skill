"""Tune Unbounded / Rubik toward the HG mark: soft outer corners, grip corners on H and G, tighter kerning."""
import sys; sys.path.insert(0, '.')
from typo import glyph_shapes, font_path
from geo import rrect, RES, svg
from shapely.ops import unary_union
from shapely import affinity

FONTS = {
  "unbounded": dict(path=font_path("unbounded", "unbounded", 900), tracking=-0.035,
                    kern={"AP": -0.02, "PP": -0.01, "PY": -0.03, "WO": -0.03, "LD": -0.01, "HG": -0.01, "GW": -0.02}),
  "rubik":     dict(path=font_path("rubik", "rubik", 800), tracking=-0.02,
                    kern={"AP": -0.02, "PY": -0.03, "WO": -0.03, "GW": -0.02}),
}
SOFT, GRIP = 0.075, 0.37           # x cap height; grip = logo's 220/600

def soft(g, r):
    """Round convex corners only (concave joins stay sharp, like the mark's cuts)."""
    return g.buffer(-r, quad_segs=RES, join_style="round").buffer(r, quad_segs=RES, join_style="round")

def grip(g, corner, R, cap):
    x0, _, x1, _ = g.bounds
    kw = {"tl": R} if corner == "tl" else {"br": R}
    return g.intersection(rrect(x0, -cap, x1, 0, **kw))

GRIP_RULES = {"H": ("tl", GRIP), "G": ("br", 0.62)}   # the mark's two blocks: H top-left, G bottom-right (G follows its bowl)

def set_word(font, text, cap, tuned=True):
    f = FONTS[font]
    glyphs, _ = glyph_shapes(f["path"], text, cap, f["tracking"] if tuned else 0.0, f["kern"] if tuned else None)
    out = []
    for ch, g, x in glyphs:
        if g is None: continue
        if tuned:
            if ch in GRIP_RULES: g = grip(g, GRIP_RULES[ch][0], GRIP_RULES[ch][1] * cap, cap)
            g = soft(g, SOFT * cap)
        out.append(g)
    return unary_union(out)

def set_lines(font, lines, cap, leading=1.18, tuned=True):
    geoms = [affinity.translate(set_word(font, t, cap, tuned), 0, i * cap * leading) for i, t in enumerate(lines)]
    return unary_union(geoms)

if __name__ == "__main__":
    OUT = sys.argv[1]
    for font in FONTS:
        for tuned in (False, True):
            for name, lines in [("happy-gaming-world", ["HAPPY GAMING WORLD"]), ("hgw", ["HGW"]), ("stack", ["HAPPY", "GAMING", "WORLD"])]:
                g = set_lines(font, lines, 200, tuned=tuned)
                x0, y0, x1, y1 = g.bounds; p = 20
                tag = "tuned" if tuned else "original"
                open(f"{OUT}/{font}-{tag}-{name}.svg", "w").write(svg([("type", g, "#0A0A10")], (x0 - p, y0 - p, x1 - x0 + 2*p, y1 - y0 + 2*p), f"{font} {tag} {name}"))
    print("ok")
