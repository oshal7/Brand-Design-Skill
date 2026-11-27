import sys; sys.path.insert(0, '.')
from concepts5 import *
FRED = ff("fredoka", "fredoka", 700)

def r1_depth(OUT, font=BLACK, tag="r1-depth-hgwd", tr=-0.01, dk=0.12):
    span = T.G["br"][1] - T.G["tr"][1]; lead = 1.36; cap = span / (1 + 2 * lead) * 1.08
    parts = []
    for i, s in enumerate(["happy", "gaming", "world"]):
        base = T.G["tr"][1] + cap + i * cap * lead
        w = word(s, cap, font, tr); x = T.edge_x(base - cap, base + cap * 0.3) + 0.5 * cap
        parts.append(affinity.translate(w, x, base))
    t = unary_union(parts); o = cap * 0.035
    dep = extrude(t, cap * dk).union(t).buffer(o, **mit)          # same construction as the mark: depth + thin edge
    out(tag, [("mark", SOLO, INK), ("type-body", dep.difference(t), INK)],
        LAY + [("type-body", dep, IND), ("type", t, WHITE)], [MARK, dep], OUT)
    # two-line and under-the-mark versions of the same treatment
    for lines, tg in [(("happy", "gaming world"), "2line"), (("happy", "gaming", "world"), "under")]:
        parts = []
        if tg == "2line":
            cap2 = span / (1 + lead) * 0.78
            for i, s in enumerate(lines):
                base = (T.G["tr"][1] + T.G["br"][1]) / 2 - cap2 * (1 + lead) / 2 + cap2 + i * cap2 * lead
                w = word(s, cap2, font, tr); x = T.edge_x(base - cap2, base + cap2 * 0.3) + 0.5 * cap2
                parts.append(affinity.translate(w, x, base))
            c = cap2
        else:
            c = cap * 0.85; mx0, my0, mx1, my1 = MARK.bounds
            for i, s in enumerate(lines):
                w = word(s, c, font, tr); ww = w.bounds[2]
                parts.append(affinity.translate(w, (mx0 + mx1) / 2 - ww / 2, my1 + 0.7 * c + c + i * c * lead))
        t2 = unary_union(parts); dep2 = extrude(t2, c * dk).union(t2).buffer(c * 0.035, **mit)
        out(f"{tag}-{tg}", [("mark", SOLO, INK), ("type-body", dep2.difference(t2), INK)],
            LAY + [("type-body", dep2, IND), ("type", t2, WHITE)], [MARK, dep2], OUT)

def r2_plinth(OUT, font=BLACK, tag="r2-plinth"):
    mx0, my0, mx1, my1 = MARK.bounds
    ph = (my1 - my0) * 0.56; cap = ph * 0.26; lead = 1.38
    w1, w2 = word("happy", cap, font), word("gaming world", cap, font)
    py0 = my1 - ph - (my1 - my0) * 0.06; px0 = mx0 + (mx1 - mx0) * 0.55
    tx = mx1 + cap * 0.45
    pad_r = cap * 0.9
    pw = (tx - px0) + max(w1.bounds[2], w2.bounds[2]) + pad_r
    plinth = rrect(px0, py0, px0 + pw, py0 + ph, tl=ph * 0.5, tr=ph * 0.12, br=ph * 0.5, bl=ph * 0.12)   # the mark's diagonal rule
    d = ph * 0.13; o = ph * 0.022
    pbody = extrude(plinth, d, o).union(plinth.buffer(o, **mit))
    block_h = cap + lead * cap; ty = py0 + ph / 2 - block_h / 2 + cap
    t = unary_union([affinity.translate(w1, tx, ty), affinity.translate(w2, tx, ty + lead * cap)])
    clear = MARK.buffer(cap * 0.22, **mit)
    out(tag, [("plinth", pbody.difference(clear), INK), ("type", t, WHITE), ("mark", SOLO, INK)],
        [("plinth-depth", pbody.difference(clear), IND_D), ("plinth", plinth.difference(clear), IND), ("type", t, WHITE)] + LAY,
        [MARK, pbody], OUT)

def r3_keycaps(OUT, font=BLACK, lines=("happy", "gaming", "world"), tag="r3-keycaps"):
    span = T.G["br"][1] - T.G["tr"][1]; n = len(lines)
    kh = span / (n + (n - 1) * 0.12) * 1.06; cap = kh * 0.50; padx = kh * 0.34; d = kh * 0.15; o = kh * 0.03
    keys, faces, letters = [], [], []
    for i, s in enumerate(lines):
        w = word(s, cap, font); y = T.G["tr"][1] - kh * 0.05 + i * kh * 1.12
        x = T.edge_x(y, y + kh + d) + 0.30 * kh
        kw = w.bounds[2] + 2 * padx
        k = rrect(x, y, x + kw, y + kh, tl=kh * 0.5, tr=kh * 0.12, br=kh * 0.12, bl=kh * 0.12)
        letters.append(affinity.translate(w, x + padx, y + kh / 2 + cap * 0.5))
        keys.append(extrude(k, d, o).union(k.buffer(o, **mit))); faces.append(k)
    body = unary_union(keys); face = unary_union(faces).difference(unary_union(letters))
    out(tag, [("mark", SOLO, INK), ("keys", body.difference(face), INK)],
        LAY + [("key-depth", body, IND), ("key-face", face, WHITE)], [MARK, body], OUT)

if __name__ == "__main__":
    OUT = sys.argv[1]
    r1_depth(OUT); r1_depth(OUT, FRED, "r1-depth-fredoka", 0.0)
    r2_plinth(OUT); r2_plinth(OUT, FRED, "r2-plinth-fredoka")
    r3_keycaps(OUT); r3_keycaps(OUT, lines=("happy", "gaming world"), tag="r3-keycaps-2line")
    print("ok")
