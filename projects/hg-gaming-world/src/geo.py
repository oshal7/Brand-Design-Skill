"""Geometry helpers: build shapes with shapely, emit clean SVG paths."""
import math
from shapely.geometry import Polygon, Point, box, LineString
from shapely.ops import unary_union
from shapely import affinity

RES = 32  # arc segments per quarter

def rrect(x0, y0, x1, y1, tl=0, tr=0, br=0, bl=0):
    """Rounded rectangle with per-corner radii (y down)."""
    pts = []
    def arc(cx, cy, r, a0, a1):
        if r == 0:
            pts.append((cx, cy)); return
        n = RES
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    arc(x0 + tl, y0 + tl, tl, 180, 270)
    arc(x1 - tr, y0 + tr, tr, 270, 360)
    arc(x1 - br, y1 - br, br, 0, 90)
    arc(x0 + bl, y1 - bl, bl, 90, 180)
    return Polygon(pts)

def circle(cx, cy, r):
    return Point(cx, cy).buffer(r, quad_segs=RES)

def stroke(coords, w, cap="round"):
    return LineString(coords).buffer(w / 2, quad_segs=RES, cap_style=cap, join_style="round")

def arcpts(cx, cy, r, a0, a1, n=48):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

def fillet(g, r):
    """Round convex+concave corners by r (open/close)."""
    if r <= 0: return g
    return g.buffer(r, quad_segs=RES, join_style="round").buffer(-2 * r, quad_segs=RES, join_style="round").buffer(r, quad_segs=RES, join_style="round")

def sweep(g, dx, dy, steps=None):
    """Area swept by g translated from (0,0) to (dx,dy) — extrusion silhouette."""
    parts = [g]
    polys = [g] if g.geom_type == "Polygon" else list(g.geoms)
    for p in polys:
        ring = list(p.exterior.coords)
        for a, b in zip(ring, ring[1:]):
            quad = Polygon([a, b, (b[0] + dx, b[1] + dy), (a[0] + dx, a[1] + dy)])
            if quad.is_valid and quad.area > 1e-6:
                parts.append(quad)
        parts.append(affinity.translate(Polygon(p.exterior), dx, dy))
    return unary_union(parts)

def _ring(coords):
    c = [(round(x, 2), round(y, 2)) for x, y in coords]
    out = [c[0]]
    for p in c[1:]:
        if p != out[-1]: out.append(p)
    s = "M" + " L".join(f"{x:g} {y:g}" for x, y in out[:-1]) + "Z"
    return s

def to_d(g):
    if g.is_empty: return ""
    polys = [g] if g.geom_type == "Polygon" else [p for p in g.geoms if p.geom_type == "Polygon"]
    d = []
    for p in polys:
        d.append(_ring(p.exterior.coords))
        for i in p.interiors:
            d.append(_ring(i.coords))
    return " ".join(d)

def svg(layers, viewbox, title, bg=None, size=None):
    vb = " ".join(f"{v:g}" for v in viewbox)
    w, h = viewbox[2], viewbox[3]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{size or w:g}" height="{(size or w) * h / w:g}" role="img" aria-labelledby="title">',
           f'  <title id="title">{title}</title>']
    if bg:
        out.append(f'  <rect x="{viewbox[0]:g}" y="{viewbox[1]:g}" width="{w:g}" height="{h:g}" fill="{bg}"/>')
    for gid, geom, fill in layers:
        out.append(f'  <path id="{gid}" fill="{fill}" fill-rule="evenodd" d="{to_d(geom)}"/>')
    out.append("</svg>")
    return "\n".join(out) + "\n"
