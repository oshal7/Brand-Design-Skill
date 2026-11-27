"""Five different strategies for making the name part of the mark's family. Tilted mark, level text."""
import sys, glob; sys.path.insert(0, '.')
import tilt_iter as T
from typo import glyph_shapes
from geo import svg, rrect, sweep, RES
from shapely import affinity
from shapely.ops import unary_union
from shapely.geometry import Polygon, box
FD = "/home/user/Brand-Design-Skill/projects/hg-gaming-world/03-typography/font/"
FT = "/tmp/claude-0/-home-user-Brand-Design-Skill/3003aa12-3088-5bf0-8260-ffaf0ef41262/scratchpad/fonts/"
BLACK = FD + "HGWDisplay-Black.ttf"
def ff(pkg, fam, w): return glob.glob(f"{FT}fontsource-{pkg}-*/package/files/{fam}-latin-{w}-normal.woff2")[0]
INK, WHITE, IND, IND_D, VOID = "#0A0A10", "#FFFFFF", "#2E1FF5", "#2216C4", "#0A0A10"
MARK, SOLO, LAY = T.MARK, T.SOLO, T.L
mit = dict(quad_segs=RES, join_style="mitre")

def word(t, cap, font=BLACK, tr=-0.01):
    gl, _ = glyph_shapes(font, t, cap, tr)
    g = unary_union([g for ch, g, x in gl if g is not None]); return affinity.translate(g, -g.bounds[0], 0)
def extrude(g, d, o=0):
    ps = [g] if g.geom_type == "Polygon" else list(g.geoms)
    b = unary_union([sweep(Polygon(p.exterior), d, d) for p in ps])
    return b.buffer(o, **mit) if o else b
def out(name, black_layers, colour_layers, geoms, OUT):
    vb = T.vbox(geoms, 44)
    open(f"{OUT}/{name}-black.svg", "w").write(svg(black_layers, vb, "Happy Gaming World"))
    open(f"{OUT}/{name}-on-dark.svg", "w").write(svg(colour_layers, vb, "Happy Gaming World", bg=VOID))

def c1_keycaps(OUT, lines=("happy", "gaming", "world"), tag="c1-keycaps"):
    """The name typed on keys: same outline, depth and grip corner as the h block; letters cut into the face."""
    span = T.G["br"][1] - T.G["tr"][1]; n = len(lines)
    kh = span / (n + (n - 1) * 0.10)                 # key height: n keys + gaps fill the g block's height
    cap = kh * 0.46; pad = kh * 0.30; d = kh * 0.13; o = kh * 0.028
    words = [word(s, cap) for s in lines]; kw = max(w.bounds[2] for w in words) + 2 * pad
    keys, faces, letters = [], [], []
    top = T.G["tr"][1]
    for i, w in enumerate(words):
        y = top + i * kh * 1.10
        x = T.edge_x(y, y + kh + d) + 0.32 * kh
        k = rrect(x, y, x + kw, y + kh, tl=kh * 0.48, tr=kh * 0.10, br=kh * 0.10, bl=kh * 0.10)
        lt = affinity.translate(w, x + pad, y + kh / 2 + cap / 2)
        keys.append(extrude(k, d, o).union(k.buffer(o, **mit))); faces.append(k); letters.append(lt)
    body = unary_union(keys); face = unary_union(faces).difference(unary_union(letters))
    out(tag, [("mark", SOLO, INK), ("keys", body.difference(face), INK)],
        LAY + [("key-depth", body, IND), ("key-face", face, WHITE)], [MARK, body], OUT)

def c2_plinth(OUT):
    """One object: the name lives on a plinth block; the tilted mark sits on its corner like a sticker on a console."""
    cap = T.cap_g * 0.9; w1, w2 = word("happy gaming", cap), word("world", cap)
    lead = cap * 1.42; pad = cap * 0.62
    mx0, my0, mx1, my1 = MARK.bounds
    px0 = mx0 + (mx1 - mx0) * 0.58; py0 = my0 + (my1 - my0) * 0.34
    tx = mx1 + cap * 0.35
    pw = (tx - px0) + max(w1.bounds[2], w2.bounds[2]) + pad; ph = cap + lead + pad * 2
    plinth = rrect(px0, py0, px0 + pw, py0 + ph, tl=ph * 0.42, br=ph * 0.42)
    d = ph * 0.11; o = ph * 0.02
    pbody = extrude(plinth, d, o).union(plinth.buffer(o, **mit))
    t = unary_union([affinity.translate(w1, tx, py0 + pad + cap), affinity.translate(w2, tx, py0 + pad + cap + lead)])
    clear = MARK.buffer(cap * 0.18, **mit)
    out("c2-plinth", [("plinth", pbody.difference(clear), INK), ("type", t.difference(clear), WHITE), ("mark", SOLO, INK)],
        [("plinth-depth", pbody.difference(clear), IND_D), ("plinth", plinth.difference(clear), IND), ("type", t.difference(clear), WHITE)] + LAY,
        [MARK, pbody], OUT)

def c3_interlock(OUT):
    """The dropped g leaves a step; 'happy' sits in it, the rest follows the g. One locked silhouette."""
    cap = T.cap_g * 1.0; gap = 0.42 * cap; lead = 1.42
    base1 = T.G["tr"][1] - 0.30 * cap                      # first baseline just above the g block's top corner
    parts = []
    for i, s in enumerate(["happy", "gaming", "world"]):
        base = base1 + i * cap * lead
        if i == 2: base += 0.0
        w = word(s, cap); x = T.edge_x(base - cap * 1.02, base + cap * 0.28) + gap
        parts.append(affinity.translate(w, x, base))
    t = unary_union(parts)
    out("c3-interlock", [("mark", SOLO, INK), ("type", t, INK)], LAY + [("type", t, WHITE)], [MARK, t], OUT)

def c4_shared_depth(OUT):
    """The name gets the mark's 45-degree extrusion in indigo, no outline: both speak 3D."""
    span = T.G["br"][1] - T.G["tr"][1]; lead = 1.42; cap = span / (1 + 2 * lead) * 1.05
    parts = []
    for i, s in enumerate(["happy", "gaming", "world"]):
        base = T.G["tr"][1] + cap + i * cap * lead
        w = word(s, cap); x = T.edge_x(base - cap, base + cap * 0.3) + 0.5 * cap
        parts.append(affinity.translate(w, x, base))
    t = unary_union(parts); dep = extrude(t, cap * 0.13)
    out("c4-shared-depth", [("mark", SOLO, INK), ("type-depth", dep.difference(t).buffer(0), INK), ("type", t.buffer(-cap*0.02).boundary.buffer(cap*0.02).union(dep.difference(t)), INK)],
        LAY + [("type-depth", dep, IND), ("type", t, WHITE)], [MARK, dep], OUT)

def c5_fonts(OUT):
    """Personality match: chunky, rounded, friendly display faces."""
    for key, path in [("lilita", ff("lilita-one", "lilita-one", 400)), ("baloo", ff("baloo-2", "baloo-2", 800)),
                      ("fredoka", ff("fredoka", "fredoka", 700)), ("titan", ff("titan-one", "titan-one", 400))]:
        for case in ("lower", "title"):
            lines = ["happy", "gaming", "world"] if case == "lower" else ["Happy", "Gaming", "World"]
            span = T.G["br"][1] - T.G["tr"][1]; lead = 1.32 if case == "lower" else 1.12; cap = span / (1 + 2 * lead) * (1.06 if case == "lower" else 1.0)
            parts = []
            for i, s in enumerate(lines):
                base = T.G["tr"][1] + cap + i * cap * lead
                w = word(s, cap, path, 0.0); x = T.edge_x(base - cap, base + cap * 0.3) + 0.45 * cap
                parts.append(affinity.translate(w, x, base))
            t = unary_union(parts)
            out(f"c5-{key}-{case}", [("mark", SOLO, INK), ("type", t, INK)], LAY + [("type", t, WHITE)], [MARK, t], OUT)

if __name__ == "__main__":
    OUT = sys.argv[1]
    c1_keycaps(OUT); c1_keycaps(OUT, ("happy", "gaming world"), "c1-keycaps-2line")
    c2_plinth(OUT); c3_interlock(OUT); c4_shared_depth(OUT); c5_fonts(OUT)
    print("ok")
