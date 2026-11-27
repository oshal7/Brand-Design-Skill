import sys, math; sys.path.insert(0, '.')
from integrate import build, g_frame, one_colour, TILT, H, LEAD, D, O
from geo import to_d
from shapely.geometry import LineString
from shapely.ops import unary_union
OUT = sys.argv[1]
for name, tilt, rule in [("straight", 0, "aligned"), ("tilted", TILT, "rotated")]:
    L, t, vb = build(rule, tilt); fr = g_frame(tilt)
    a = math.radians(tilt); ux, uy = math.cos(a), math.sin(a); vx, vy = -math.sin(a), math.cos(a)
    cap = H / (1 + 2 * LEAD)
    def line(p, d, L0=-900, L1=2600): return LineString([(p[0] + d[0]*L0, p[1] + d[1]*L0), (p[0] + d[0]*L1, p[1] + d[1]*L1)])
    guides = [line(fr["tr"], (ux, uy)), line(fr["br"], (ux, uy))]                  # g top + bottom edges, extended
    bx, by = fr["tr"][0] + ux*(D + O + 0.45*cap), fr["tr"][1] + uy*(D + O + 0.45*cap)
    guides.append(line((bx, by), (vx, vy), -300, 1100))                               # type's left edge, parallel to the g's side
    for i in range(3):                                                                # baselines
        p = (bx + vx*(cap + i*cap*LEAD), by + vy*(cap + i*cap*LEAD)); guides.append(line(p, (ux, uy), -60, 1300))
    x, y, w, h = vb; pad = 120; vb2 = (x - pad, y - pad, w + 2*pad, h + 2*pad)
    paths = "".join(f'<path d="M{g.coords[0][0]:.1f} {g.coords[0][1]:.1f} L{g.coords[1][0]:.1f} {g.coords[1][1]:.1f}" stroke="#2E1FF5" stroke-width="3" stroke-dasharray="14 10" fill="none"/>' for g in guides)
    body = f'<path fill="#0A0A10" fill-rule="evenodd" d="{to_d(one_colour(tilt))}"/><path fill="#0A0A10" d="{to_d(t)}"/>'
    open(f"{OUT}/construction-{name}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join(f"{v:.1f}" for v in vb2)}"><rect x="{vb2[0]}" y="{vb2[1]}" width="{vb2[2]}" height="{vb2[3]}" fill="#fff"/>{body}{paths}</svg>')
print("ok")
