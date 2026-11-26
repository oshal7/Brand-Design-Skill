"""Set text with HarfBuzz (kerning), outline it with fontTools, return shapely geometry (y down)."""
import io, sys; sys.path.insert(0, '.')
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely import affinity
from geo import sweep, RES

FONTDIR = "/tmp/claude-0/-home-user-Brand-Design-Skill/3003aa12-3088-5bf0-8260-ffaf0ef41262/scratchpad/fonts"
def font_path(pkg, fam, w): return f"{FONTDIR}/fontsource-{pkg}-5.3.0/package/files/{fam}-latin-{w}-normal.woff2"

class FlatPen(BasePen):
    def __init__(self, gs, n=12):
        super().__init__(gs); self.contours = []; self.cur = []; self.n = n
    def _moveTo(self, p): self.cur = [p]
    def _lineTo(self, p): self.cur.append(p)
    def _curveToOne(self, p1, p2, p3):
        p0 = self.cur[-1]
        for i in range(1, self.n + 1):
            t = i / self.n; u = 1 - t
            self.cur.append((u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
                             u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]))
    def _qCurveToOne(self, p1, p2):
        p0 = self.cur[-1]
        for i in range(1, self.n + 1):
            t = i / self.n; u = 1 - t
            self.cur.append((u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0], u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1]))
    def _closePath(self):
        if len(self.cur) > 2: self.contours.append(self.cur)
        self.cur = []
    _endPath = _closePath

_cache = {}
def load(path):
    if path not in _cache:
        tt = TTFont(path); tt.flavor = None          # woff2 -> plain sfnt for HarfBuzz
        bio = io.BytesIO(); tt.save(bio); data = bio.getvalue()
        tt = TTFont(io.BytesIO(data))
        _cache[path] = (tt, hb.Font(hb.Face(hb.Blob(data))))
    return _cache[path]

def text_shape(path, text, size, tracking=0.0):
    """Return (geometry, cap_height) in px for font size `size`; baseline at y=0, y down. tracking in em."""
    tt, hbf = load(path)
    upem = tt["head"].unitsPerEm; s = size / upem
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hbf, buf, {"kern": True, "liga": True})
    gs = tt.getGlyphSet(); order = tt.getGlyphOrder()
    x = 0; geoms = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        pen = FlatPen(gs); gs[name].draw(pen)
        g = None
        for c in pen.contours:
            poly = Polygon([((x + pos.x_offset + px) * s, -(py + pos.y_offset) * s) for px, py in c]).buffer(0)
            g = poly if g is None else g.symmetric_difference(poly)
        if g is not None: geoms.append(g)
        x += pos.x_advance + tracking * upem
    cap = tt["OS/2"].sCapHeight * s if hasattr(tt["OS/2"], "sCapHeight") else size * 0.7
    return unary_union(geoms), cap

def extrude(face, cap, d_ratio=0.133, o_ratio=0.027):
    """Logo DNA on type: 45-degree depth + thin border, proportional to cap height (logo block = 600)."""
    D, O = cap * d_ratio, cap * o_ratio
    parts = [face] if face.geom_type == "Polygon" else list(face.geoms)
    body = unary_union([sweep(Polygon(p.exterior), D, D).buffer(O, quad_segs=RES, join_style="mitre") for p in parts])
    return body

def _signed(c):
    return sum(c[i][0] * c[(i + 1) % len(c)][1] - c[(i + 1) % len(c)][0] * c[i][1] for i in range(len(c))) / 2

def nonzero(contours):
    """Fill contours with the nonzero rule: same-direction contours union (overlaps merge), opposite ones cut."""
    if not contours: return None
    ref = max(contours, key=lambda c: abs(_signed(c)))
    sgn = 1 if _signed(ref) > 0 else -1
    pos = [Polygon(c).buffer(0) for c in contours if _signed(c) * sgn > 0]
    neg = [Polygon(c).buffer(0) for c in contours if _signed(c) * sgn < 0]
    return unary_union(pos).difference(unary_union(neg)) if neg else unary_union(pos)

def glyph_shapes(path, text, cap_px, tracking=0.0, kern_adj=None):
    """Per-glyph geometry, scaled so cap height == cap_px. Returns list of (char, geom, advance_px).
    kern_adj: {pair: em} extra kerning applied between characters."""
    tt, hbf = load(path)
    upem = tt["head"].unitsPerEm
    cap_units = getattr(tt["OS/2"], "sCapHeight", 0) or upem * 0.7
    s = cap_px / cap_units
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hbf, buf, {"kern": True, "liga": False})
    gs = tt.getGlyphSet(); order = tt.getGlyphOrder()
    out = []; x = 0.0
    for idx, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        ch = text[info.cluster]
        if kern_adj and idx > 0:
            x += kern_adj.get(text[buf.glyph_infos[idx - 1].cluster] + ch, 0) * upem
        pen = FlatPen(gs, n=16); gs[order[info.codepoint]].draw(pen)
        g = nonzero([[((x + pos.x_offset + px) * s, -(py + pos.y_offset) * s) for px, py in c] for c in pen.contours])
        out.append((ch, g, (x * s)))
        x += pos.x_advance + tracking * upem
    return out, cap_px
