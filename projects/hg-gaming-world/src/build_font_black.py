"""Build HGW Display: Rubik ExtraBold (OFL, no Reserved Font Name) with the mark's diagonal rounding on every glyph."""
import sys, io; sys.path.insert(0, '.')
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient
from shapely import affinity
from typo import FlatPen, nonzero, font_path
from morph import diag_round

SRC = font_path("rubik", "rubik", 900)
R_OUT, R_IN = 0.14, 0.05
OUT = sys.argv[1]
tt = TTFont(SRC); tt.flavor = None
cap = tt["OS/2"].sCapHeight
gs = tt.getGlyphSet()
cmap = tt.getBestCmap()
wanted = {cp: n for cp, n in cmap.items() if 0x20 <= cp <= 0x7E or cp in (0xA0, 0xA3, 0xA9, 0xAE, 0xB0, 0xD7, 0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x20AC, 0x20B9, 0x2192)}
names = sorted(set(wanted.values()))
glyf = tt["glyf"]
done = 0
for name in names:
    pen = FlatPen(gs, n=10); gs[name].draw(pen)
    if not pen.contours: continue
    g = nonzero([[(x, -y) for x, y in c] for c in pen.contours])          # to y-down
    if g is None or g.is_empty: continue
    r_out, r_in = R_OUT * cap, R_IN * cap
    for _ in range(4):
        h = diag_round(g, r_out, r_in)
        if not h.is_empty and h.area > 0.88 * g.area: break
        r_out *= 0.6; r_in *= 0.6
    else:
        h = g
    h = affinity.scale(h, 1, -1, origin=(0, 0)).simplify(0.6)              # back to y-up
    polys = [h] if h.geom_type == "Polygon" else [p for p in h.geoms if p.geom_type == "Polygon"]
    tp = TTGlyphPen(None)
    for p in polys:
        p = orient(p, sign=-1.0)                                           # TrueType: outer clockwise
        for ring in [p.exterior] + list(p.interiors):
            c = list(ring.coords)[:-1]
            tp.moveTo((round(c[0][0]), round(c[0][1])))
            for x, y in c[1:]: tp.lineTo((round(x), round(y)))
            tp.closePath()
    glyf[name] = tp.glyph()
    done += 1
# keep only the glyphs we rebuilt (plus .notdef), so nothing unprocessed ships
from fontTools import subset
opts = subset.Options(); opts.layout_features = ["kern", "liga", "calt", "tnum"]; opts.name_IDs = ["*"]; opts.notdef_outline = True
sub = subset.Subsetter(opts); sub.populate(unicodes=list(wanted.keys())); sub.subset(tt)
for t in ("fpgm", "prep", "cvt ", "gasp", "hdmx", "LTSH", "VDMX"):
    if t in tt: del tt[t]
from fontTools.ttLib.tables.ttProgram import Program
for gname in tt.getGlyphOrder():
    g = tt["glyf"][gname]
    if g.numberOfContours > 0:
        p = Program(); p.fromBytecode(b""); g.program = p
name = tt["name"]
fam, sty, full, ps = "HGW Display", "Black", "HGW Display Black", "HGWDisplay-Black"
for rec in list(name.names):
    if rec.nameID in (1, 4, 6, 16, 17, 3):
        name.removeNames(nameID=rec.nameID)
for pid, eid, lid in ((3, 1, 0x409), (1, 0, 0)):
    name.setName(fam, 1, pid, eid, lid); name.setName("Regular", 2, pid, eid, lid) if False else None
    name.setName(full, 4, pid, eid, lid); name.setName(ps, 6, pid, eid, lid); name.setName(f"{ps};1.000", 3, pid, eid, lid)
    name.setName(fam, 16, pid, eid, lid); name.setName(sty, 17, pid, eid, lid)
name.setName("Copyright 2015 The Rubik Project Authors (https://github.com/googlefonts/rubik). Modified for HG Gaming World (diagonal corner rounding).", 0, 3, 1, 0x409)
name.setName("This Font Software is licensed under the SIL Open Font License, Version 1.1.", 13, 3, 1, 0x409)
name.setName("https://openfontlicense.org", 14, 3, 1, 0x409)
tt.save(f"{OUT}/HGWDisplay-Black.ttf")
tt.flavor = "woff2"; tt.save(f"{OUT}/HGWDisplay-Black.woff2")
print("glyphs rebuilt:", done, "of", len(names))
