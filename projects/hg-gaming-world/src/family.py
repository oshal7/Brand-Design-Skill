"""Family iterations: same four approved layouts, type treatments that close the gap between name and mark."""
import sys; sys.path.insert(0, '.')
import tilt_iter as T
from typo import glyph_shapes
from geo import svg, circle, sweep, RES
from shapely import affinity
from shapely.ops import unary_union
from shapely.geometry import Polygon
FD = "/home/user/Brand-Design-Skill/projects/hg-gaming-world/03-typography/font/"
FONTS = {"eb": FD + "HGWDisplay-ExtraBold.ttf", "black": FD + "HGWDisplay-Black.ttf"}
CFG = dict(font="eb", lower=False, button=False)
DOTS = []

def word(t, cap, font=None, tr=-0.015):
    t = t.lower() if CFG["lower"] else t
    gl, _ = glyph_shapes(FONTS[CFG["font"]], t, cap, tr)
    parts = []
    for ch, g, x in gl:
        if g is None: continue
        if CFG["button"] and ch == "i":
            polys = [g] if g.geom_type == "Polygon" else list(g.geoms)
            dot = min(polys, key=lambda p: p.bounds[1]); stem = unary_union([p for p in polys if p is not dot])
            sw = stem.bounds[2] - stem.bounds[0]
            c = dot.centroid; d = circle(c.x, c.y - 0.02 * cap, sw * 0.62)       # button: a perfect circle, slightly larger than the stem
            parts.append(stem); parts.append(d)
        else:
            parts.append(g)
    w = unary_union(parts)
    if CFG["lower"]: w = affinity.scale(w, 1.1, 1.1, origin=(0, 0))      # optical: lowercase carries less mass than caps
    dx = -w.bounds[0]
    if CFG["button"]:
        for i in range(len(DOTS)):
            if not getattr(DOTS[i], "_placed", False): pass
    return affinity.translate(w, dx, 0)

T.word = word
LAYOUTS = {"02": T.it2, "06": T.it6, "07": T.it7, "09": T.it9}
TREAT = {"F1": dict(font="eb", lower=False, button=False), "F2": dict(font="black", lower=False, button=False),
         "F3": dict(font="black", lower=True, button=False), "F4": dict(font="black", lower=True, button=True),
         "F5": dict(font="black", lower=True, button=True, built=True)}

def i_dots(t, cap_guess=None):
    """Find button dots in the final text geometry: small round components near the top of each line."""
    polys = [t] if t.geom_type == "Polygon" else list(t.geoms)
    out = []
    for p in polys:
        x0, y0, x1, y1 = p.bounds
        if abs((x1 - x0) - (y1 - y0)) < 2 and p.area > 0.7 * 3.1416 * ((x1 - x0) / 2) ** 2: out.append(p)
    return unary_union(out) if out else None

if __name__ == "__main__":
    OUT = sys.argv[1]
    for tk, cfg in TREAT.items():
        CFG.update(font=cfg["font"], lower=cfg["lower"], button=cfg["button"])
        T.LEADV = 1.42 if cfg["lower"] else 1.18
        T.cap_g = T.H / (1 + 2 * T.LEADV) * (1.08 if cfg["lower"] else 1.0)
        for lk, fn in LAYOUTS.items():
            t = fn()
            vb = T.vbox([T.MARK, t], 40)
            dots = i_dots(t) if cfg["button"] else None
            cap = T.cap_g
            if cfg.get("built"):
                parts = [t] if t.geom_type == "Polygon" else list(t.geoms)
                dd = 0.11 * cap; oo = 0.022 * cap
                body = unary_union([sweep(Polygon(p.exterior), dd, dd) for p in parts]).buffer(oo, join_style="mitre")
                face = t
                vb = T.vbox([T.MARK, body], 40)
                black = [("mark", T.SOLO, "#0A0A10"), ("type-depth", body.difference(face), "#0A0A10")]
                dark = T.L + [("type-depth", body, "#2E1FF5"), ("type", face, "#FFFFFF")]
            else:
                black = [("mark", T.SOLO, "#0A0A10"), ("type", t, "#0A0A10")]
                dark = T.L + [("type", t, "#FFFFFF")]
            if dots is not None and not cfg.get("built"):
                dark = dark + [("button", dots, "#5E52FF")]
            open(f"{OUT}/{tk}-{lk}-black.svg", "w").write(svg(black, vb, "Happy Gaming World"))
            open(f"{OUT}/{tk}-{lk}-on-dark.svg", "w").write(svg(dark, vb, "Happy Gaming World"))
    print("ok")
