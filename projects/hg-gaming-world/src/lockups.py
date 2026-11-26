"""Lockups: the mark (always with depth) + tuned flat type. Outlined geometry, no live text."""
import sys; sys.path.insert(0, '.')
from tune import set_word, FONTS
from logo import face as LF, body as LB
from geo import svg
from shapely import affinity
from shapely.ops import unary_union

LEAD = 1.16
LAYOUTS = {"stack3": ["HAPPY", "GAMING", "WORLD"], "stack2": ["HAPPY", "GAMING WORLD"],
           "line": ["HAPPY GAMING WORLD"], "hg-world": ["HG WORLD"], "hgw": ["HGW"]}

def build(font, key, cap=100):
    lines = LAYOUTS[key]
    t = unary_union([affinity.translate(set_word(font, s, cap), 0, i * cap * LEAD) for i, s in enumerate(lines)])
    tx0, ty0, tx1, ty1 = t.bounds          # ty0 = -cap (top of first line), ty1 ~ 0 + (n-1)*lead*cap
    block_h = ty1 - ty0
    fx0, fy0, fx1, fy1 = LF.bounds
    if key == "hgw":                        # mark stacked above the monogram, same width as the word
        s = (tx1 - tx0) / (fx1 - fx0)
        f = affinity.scale(LF, s, s, origin=(0, 0)); b = affinity.scale(LB, s, s, origin=(0, 0))
        dx = tx0 - f.bounds[0]; dy = ty0 - cap * 0.55 - f.bounds[3] - (b.bounds[3] - f.bounds[3])
        return affinity.translate(f, dx, dy), affinity.translate(b, dx, dy), t
    h = block_h if len(lines) > 1 else cap * 1.9
    s = h / (fy1 - fy0)
    f = affinity.scale(LF, s, s, origin=(0, 0)); b = affinity.scale(LB, s, s, origin=(0, 0))
    gap = cap * (0.42 if len(lines) == 1 else 0.36)
    # type sits after the mark's depth, so the depth never touches the letters
    dx = -f.bounds[0]; dy = (ty0 + ty1) / 2 - (f.bounds[1] + f.bounds[3]) / 2
    f = affinity.translate(f, dx, dy); b = affinity.translate(b, dx, dy)
    t = affinity.translate(t, b.bounds[2] + gap - tx0, 0)
    return f, b, t

if __name__ == "__main__":
    OUT = sys.argv[1]
    for font in FONTS:
        for key in LAYOUTS:
            f, b, t = build(font, key)
            allg = unary_union([b, t]); x0, y0, x1, y1 = allg.bounds; p = 30
            vb = (x0 - p, y0 - p, x1 - x0 + 2*p, y1 - y0 + 2*p)
            solo = b.difference(f)
            open(f"{OUT}/{font}-{key}-black.svg", "w").write(svg([("mark", solo, "#0A0A10"), ("type", t, "#0A0A10")], vb, f"Happy Gaming World — {key}"))
            open(f"{OUT}/{font}-{key}-on-dark.svg", "w").write(svg([("depth", b, "#2E1FF5"), ("face", f, "#FFFFFF"), ("type", t, "#FFFFFF")], vb, f"Happy Gaming World — {key}", bg="#0A0A10"))
            open(f"{OUT}/{font}-{key}-on-light.svg", "w").write(svg([("depth", b, "#2E1FF5"), ("face", f, "#FFFFFF"), ("type", t, "#0A0A10")], vb, f"Happy Gaming World — {key}", bg="#F4F4F8"))
    print("ok")
