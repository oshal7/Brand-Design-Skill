import sys; sys.path.insert(0, '.')
from typo import *
from logo import face as LF, body as LB
from shapely import affinity
from geo import svg
OUT = sys.argv[1]
BLUE, WHITE = "#2E1FF5", "#FFFFFF"
DIRS = {
  "t1-unbounded":      (font_path("unbounded", "unbounded", 900), 0.0),
  "t2-archivo":        (font_path("archivo", "archivo", 900), 0.01),
  "t3-big-shoulders":  (font_path("big-shoulders-display", "big-shoulders-display", 900), 0.03),
}
def lockup(fp, track, text, logo=True, cap_px=150):
    tf, cap = text_shape(fp, text, cap_px / 0.70 if True else cap_px, track)
    # normalise so cap height == cap_px
    sc = cap_px / cap; tf = affinity.scale(tf, sc, sc, origin=(0, 0)); cap = cap_px
    tb = extrude(tf, cap)
    layers_b, layers_f = [tb], [tf]
    if logo:
        h = cap * 1.9                          # symbol face height vs cap height
        s = h / 600
        lf = affinity.scale(LF, s, s, origin=(0, 0)); lb = affinity.scale(LB, s, s, origin=(0, 0))
        # centre symbol face on the cap band, gap = 0.55 cap
        x1 = lf.bounds[2]; dy = -cap / 2 - h / 2
        lf = affinity.translate(lf, 0, dy); lb = affinity.translate(lb, 0, dy)
        gap = cap * 0.55 + (x1 - lf.bounds[0]) * 0  # constant
        shift = x1 + gap - tf.bounds[0]
        tf2 = affinity.translate(tf, shift, 0); tb2 = affinity.translate(tb, shift, 0)
        layers_b, layers_f = [lb, tb2], [lf, tf2]
    body = unary_union(layers_b); face = unary_union(layers_f)
    x0, y0, x1, y1 = body.bounds; p = cap * 0.3
    return svg([("depth", body, BLUE), ("face", face, WHITE)], (x0 - p, y0 - p, x1 - x0 + 2*p, y1 - y0 + 2*p), text)
for key, (fp, tr) in DIRS.items():
    open(f"{OUT}/{key}-happy-gaming-world.svg", "w").write(lockup(fp, tr, "HAPPY GAMING WORLD"))
    open(f"{OUT}/{key}-hg-world.svg", "w").write(lockup(fp, tr, "HG WORLD"))
    open(f"{OUT}/{key}-hgw.svg", "w").write(lockup(fp, tr, "HGW", logo=False, cap_px=300))
print("ok")
