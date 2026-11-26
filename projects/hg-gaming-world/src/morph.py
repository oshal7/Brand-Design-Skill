"""Exact directional rounding by morphological opening with a quarter-disc.
open(g, Q_nw) rounds only the corners that face up-left (NW); Q_se only those facing down-right (SE).
All other corners, curves and widths are left exactly as drawn (if every stroke is wider than r)."""
import math, sys; sys.path.insert(0, '.')
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from shapely import affinity

def sweep(g, dx, dy):
    """Area swept by g (holes included) translated by (dx, dy)."""
    polys = [g] if g.geom_type == "Polygon" else [p for p in getattr(g, "geoms", []) if p.geom_type == "Polygon"]
    parts = [g, affinity.translate(g, dx, dy)]
    for p in polys:
        for ring in [p.exterior] + list(p.interiors):
            c = list(ring.coords)
            for a, b in zip(c, c[1:]):
                q = Polygon([a, b, (b[0] + dx, b[1] + dy), (a[0] + dx, a[1] + dy)])
                if q.area > 1e-9: parts.append(q.buffer(0))
    return unary_union(parts)

def quarter(r, facing, n=8):
    """Quarter disc of radius r whose arc faces `facing` (NW or SE). Anchor at its bounding box."""
    if facing == "NW":   # centre at (r, r); arc from W to N
        pts = [(r, r)] + [(r - r*math.cos(math.radians(a)), r - r*math.sin(math.radians(a))) for a in [90*i/n for i in range(n + 1)]]
    else:                # SE: centre at (0, 0); arc from E to S
        pts = [(0, 0)] + [(r*math.cos(math.radians(a)), r*math.sin(math.radians(a))) for a in [90*i/n for i in range(n + 1)]]
    return Polygon(pts).buffer(0)

def dilate(a, q):
    """Minkowski sum a (+) q for convex q: sweep a along every edge of q."""
    v = list(q.exterior.coords)
    parts = []
    for (x0, y0), (x1, y1) in zip(v, v[1:]):
        parts.append(sweep(affinity.translate(a, x0, y0), x1 - x0, y1 - y0))
    return unary_union(parts)

def erode(a, q, frame):
    neg = affinity.scale(q, -1, -1, origin=(0, 0))
    return frame.difference(dilate(frame.difference(a), neg))

def opening(a, q, pad):
    x0, y0, x1, y1 = a.bounds
    frame = box(x0 - pad, y0 - pad, x1 + pad, y1 + pad)
    return dilate(erode(a, q, frame), q).intersection(a.buffer(0.01))

def diag_round(g, r_out, r_in=0.0):
    """NW + SE outer corners -> r_out; NW + SE corners of counters/joins -> r_in."""
    if g is None or g.is_empty: return g
    pad = 2 * max(r_out, r_in) + 2
    out = opening(g, quarter(r_out, "NW"), pad).intersection(opening(g, quarter(r_out, "SE"), pad))
    if out.is_empty: return out
    if r_in > 0:
        x0, y0, x1, y1 = out.bounds
        frame = box(x0 - pad, y0 - pad, x1 + pad, y1 + pad)
        comp = frame.difference(out)
        comp2 = opening(comp, quarter(r_in, "NW"), pad).intersection(opening(comp, quarter(r_in, "SE"), pad))
        out = frame.difference(comp2.union(frame.difference(frame.buffer(-pad / 2))))
        out = out.intersection(box(x0, y0, x1, y1))
    return out.buffer(0)
