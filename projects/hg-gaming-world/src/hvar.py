"""h-block iterations from the founder's sketch: keep the hook, add an h opening from the bottom. g block unchanged."""
import sys, math; sys.path.insert(0, '.')
import refined2 as M
from geo import rrect, circle, sweep, svg, RES
from shapely.geometry import box, Polygon, Point
from shapely.ops import unary_union
from shapely import affinity
WL, H, k = M.WL, M.H, M.k
L_blk, HOOK, dpad = M.L_blk, M.HOOK, M.dpad
DP0 = M.P(185.5, 409.5)

def arch(xc, w, top, r=None):
    """opening from the bottom edge with a round top."""
    r = w / 2 if r is None else r
    return rrect(xc - w/2, top, xc + w/2, H + 2, tl=r, tr=r)
def slot_sharp(xc, w, top, ang=35):
    """opening from the bottom with a sharp, angled top - the hook's terminal."""
    dy = w * math.tan(math.radians(ang))
    return Polygon([(xc - w/2, H + 2), (xc - w/2, top + dy), (xc + w/2, top), (xc + w/2, H + 2)])
def flare(xc, w, R=46):
    """the master's lobe: the opening widens with round shoulders where it meets the bottom edge."""
    return box(xc - w/2 - R, H - R, xc + w/2 + R, H + 2).difference(
        unary_union([Point(xc - w/2 - R, H - R).buffer(R, quad_segs=RES), Point(xc + w/2 + R, H - R).buffer(R, quad_segs=RES)]))
SLIT = 36 * k      # the hook's cut width
VARS = {
  "h1-sketch":        dict(cut=lambda: arch(0.47 * WL, 84, 0.68 * H), dp=None),
  "h2-sketch-dpad":   dict(cut=lambda: arch(0.50 * WL, 84, 0.70 * H), dp=("up", 0.62)),
  "h3-wide-arch":     dict(cut=lambda: arch(0.52 * WL, 112, 0.56 * H), dp=None),
  "h4-line-round":    dict(cut=lambda: arch(0.50 * WL, SLIT, 0.52 * H), dp=("left", 0.55)),
  "h5-line-sharp":    dict(cut=lambda: slot_sharp(0.50 * WL, SLIT, 0.50 * H), dp=("left", 0.55)),
  "h6-line-flared":   dict(cut=lambda: arch(0.50 * WL, SLIT, 0.50 * H).union(flare(0.50 * WL, SLIT)), dp=("left", 0.55)),
  "h7-arch-flared":   dict(cut=lambda: arch(0.50 * WL, 84, 0.64 * H).union(flare(0.50 * WL, 84, 40)), dp=("up", 0.6)),
  "h8-offset-leg":    dict(cut=lambda: arch(0.60 * WL, 90, 0.58 * H), dp=("left", 0.58)),
}
def dpad_at(mode, s):
    if mode == "up":   return affinity.translate(affinity.scale(dpad(0, 0), s, s, origin=(0, 0)), 0.46 * WL, 0.43 * H)
    if mode == "left": return affinity.translate(affinity.scale(dpad(0, 0), s, s, origin=(0, 0)), 0.235 * WL, 0.62 * H)
def h_face(v):
    cfg = VARS[v]; f = L_blk.difference(HOOK).difference(cfg["cut"]())
    if cfg["dp"]: f = f.difference(dpad_at(*cfg["dp"]))
    return f

if __name__ == "__main__":
    OUT = sys.argv[1]
    import logo2
    Rf_al = M.face.difference(L_blk.buffer(1))                 # g face from the aligned master
    for v in VARS:
        hf = h_face(v)
        # aligned (as sketched): master depth
        face = unary_union([hf, Rf_al]); body = M.body
        minx, miny, maxx, maxy = body.bounds; vb = (minx - 48, miny - 48, maxx - minx + 96, maxy - miny + 96)
        open(f"{OUT}/{v}-aligned-black.svg", "w").write(svg([("mark", body.difference(face), "#0A0A10")], vb, v))
        open(f"{OUT}/{v}-aligned-on-dark.svg", "w").write(svg([("depth", body, "#2E1FF5"), ("face", face, "#FFFFFF")], vb, v, bg="#0A0A10"))
        # staggered (approved straight composition)
        orig = logo2.parts
        def parts_v(drop=logo2.DROP, hf=hf, orig=orig):
            Lb, Lf, Rb, Rf = orig(drop); return Lb, hf, Rb, Rf
        logo2.parts = parts_v
        L = logo2.layers(0); vb2 = logo2.vbox([g for _, g, _ in L])
        open(f"{OUT}/{v}-staggered-black.svg", "w").write(svg([("mark", logo2.one_colour(0), "#0A0A10")], vb2, v))
        open(f"{OUT}/{v}-staggered-on-dark.svg", "w").write(svg(L, vb2, v, bg="#0A0A10"))
        Lt = logo2.layers(logo2.TILT); vb3 = logo2.vbox([g for _, g, _ in Lt])
        open(f"{OUT}/{v}-tilted-black.svg", "w").write(svg([("mark", logo2.one_colour(logo2.TILT), "#0A0A10")], vb3, v))
        logo2.parts = orig
    print("ok")
