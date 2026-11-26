"""Geometry helpers: build shapes with shapely, emit clean SVG paths."""
import math
from shapely.geometry import Polygon, Point, box, LineString
from shapely.ops import unary_union
from shapely import affinity

RES = 64  # arc segments per quarter

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
        out.append(f'  <path id="{gid}" fill="{fill}" fill-rule="evenodd" d="{to_d_arcs(geom)}"/>')
    out.append("</svg>")
    return "\n".join(out) + "\n"

# ---------- true-curve output: replace runs of on-circle points with SVG arcs ----------
def _circ3(a, b, c):
    ax, ay = a; bx, by = b; cx, cy = c
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-9: return None
    ux = ((ax*ax + ay*ay) * (by - cy) + (bx*bx + by*by) * (cy - ay) + (cx*cx + cy*cy) * (ay - by)) / d
    uy = ((ax*ax + ay*ay) * (cx - bx) + (bx*bx + by*by) * (ax - cx) + (cx*cx + cy*cy) * (bx - ax)) / d
    return ux, uy, math.hypot(ax - ux, ay - uy)

def _fits(pts, i, j, tol):
    c = _circ3(pts[i], pts[(i + j) // 2], pts[j])
    if not c or c[2] > 4000: return None
    ux, uy, rr = c
    tot = 0; sgn = 0; das = []
    for k in range(i, j + 1):
        if abs(math.hypot(pts[k][0] - ux, pts[k][1] - uy) - rr) > tol: return None
    for k in range(i, j):
        a0 = math.atan2(pts[k][1] - uy, pts[k][0] - ux); a1 = math.atan2(pts[k+1][1] - uy, pts[k+1][0] - ux)
        da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        if da == 0 or abs(da) > 0.35: return None
        s = 1 if da > 0 else -1
        if sgn and s != sgn: return None
        sgn = s; tot += da; das.append(abs(da))
    m = sorted(das)[len(das) // 2]
    if any(x > 1.6 * m + 1e-6 for x in das): return None
    if abs(tot) > math.radians(170): return None
    return rr, (1 if tot > 0 else 0)

def _ring_arcs(coords, tol=0.02):
    pts = [(x, y) for x, y in coords[:-1]]
    n = len(pts)
    # start at a corner (a point that is not the middle of an arc) to avoid splitting arcs at the seam
    def turn(k):
        a, b, c = pts[k - 1], pts[k], pts[(k + 1) % n]
        v1 = math.atan2(b[1]-a[1], b[0]-a[0]); v2 = math.atan2(c[1]-b[1], c[0]-b[0])
        return abs((v2 - v1 + math.pi) % (2*math.pi) - math.pi)
    st = max(range(n), key=turn)
    pts = pts[st:] + pts[:st]; pts.append(pts[0])
    f = lambda v: f"{round(v, 2):g}"
    out = [f"M{f(pts[0][0])} {f(pts[0][1])}"]
    i = 0; N = len(pts) - 1
    while i < N:
        best = None; j = i + 3
        while j <= N:
            r_ = _fits(pts, i, j, tol)
            if not r_: break
            best = (j, r_); j += 1
        if best:
            j, (rr, sw) = best
            out.append(f"A{f(rr)} {f(rr)} 0 0 {sw} {f(pts[j][0])} {f(pts[j][1])}")
            i = j
        else:
            # merge collinear run
            j = i + 1
            while j < N:
                a, b, c = pts[i], pts[j], pts[j + 1]
                cross = (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
                if abs(cross) / max(1e-9, math.hypot(c[0]-a[0], c[1]-a[1])) > 0.01: break
                j += 1
            if j == N: break
            out.append(f"L{f(pts[j][0])} {f(pts[j][1])}")
            i = j
    return "".join(out) + "Z"

def to_d_arcs(g):
    polys = [g] if g.geom_type == "Polygon" else [p for p in g.geoms if p.geom_type == "Polygon"]
    d = []
    for p in polys:
        d.append(_ring_arcs(list(p.exterior.coords)))
        for i in p.interiors: d.append(_ring_arcs(list(i.coords)))
    return " ".join(d)
