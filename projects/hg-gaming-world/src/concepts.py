import sys; sys.path.insert(0, '.')
from geo import *
OUT = sys.argv[1]
BLUE, INK, WHITE, BLACK = "#3B2DFF", "#121214", "#FFFFFF", "#111111"
CUT, R_S, R_L = 24, 20, 96        # one cut width, small radius, large "grip" radius
D, O = 20, 10                     # depth offset, outline

def dpad(cx, cy, L=72, arm=24):
    return unary_union([rrect(cx-L/2, cy-arm/2, cx+L/2, cy+arm/2, 3,3,3,3),
                        rrect(cx-arm/2, cy-L/2, cx+arm/2, cy+L/2, 3,3,3,3)])
def buttons(cx, cy, off=34, r=16):
    return unary_union([circle(cx+dx, cy+dy, r) for dx, dy in [(0,-off),(off,0),(0,off),(-off,0)]])

def emit(name, blocks, face, title):
    body = sweep(unary_union(blocks), D, D).buffer(O, quad_segs=RES)
    minx, miny, maxx, maxy = body.bounds
    s = max(maxx-minx, maxy-miny) + 48
    vb = ((minx+maxx)/2 - s/2, (miny+maxy)/2 - s/2, s, s)
    open(f"{OUT}/{name}-depth-on-dark.svg","w").write(svg([("depth", body, BLUE), ("face", face, WHITE)], vb, title+" (depth)", bg=INK, size=512))
    open(f"{OUT}/{name}-flat-black.svg","w").write(svg([("symbol", face, BLACK)], vb, title+" (flat)", size=512))
    open(f"{OUT}/{name}-flat-blue-on-dark.svg","w").write(svg([("symbol", face, BLUE)], vb, title+" (flat, blue)", bg=INK, size=512))

# ================= A: refined lowercase "hg" =================
ASC, XH, BASE, DESC = 48, 176, 400, 464
hx0, slit_x, hx1 = 48, 168, 272
h = unary_union([rrect(hx0, ASC, slit_x, BASE, tl=R_L, tr=R_S, br=0, bl=R_S),
                 rrect(slit_x-40, XH, hx1, BASE, tl=0, tr=80, br=R_S, bl=0)])
h_blk = h
h = h.difference(stroke([(slit_x+CUT/2, BASE+60), (slit_x+CUT/2, 296)], CUT))
cy = (XH + BASE) / 2
h = h.difference(dpad((hx0+slit_x)/2, cy))
gx0, gx1 = 288, 496
g_blk = rrect(gx0, XH, gx1, DESC, tl=R_S, tr=R_S, br=R_L, bl=R_S)
g = g_blk.difference(circle((gx0+gx1)/2, cy, 64))
smile = stroke([(gx0-30, BASE+12), (400, BASE+12)] + arcpts(400, BASE-28, 40, 90, 0, 40), CUT)
g = g.difference(smile)
faceA = unary_union([h, g, buttons((gx0+gx1)/2, cy)])
emit("a", [h_blk, g_blk], faceA, "HG Gaming World — concept A")

# ================= B: uppercase "HG", equal blocks =================
T, B_ = 96, 416
Hb = rrect(48, T, 256, B_, tl=R_L, tr=R_S, br=R_S, bl=R_S)
H = Hb.difference(stroke([(152, T-60), (152, T+104)], CUT)).difference(stroke([(152, B_+60), (152, B_-104)], CUT))
H = H.difference(dpad(100, 256, L=64, arm=22))
Gb = rrect(272, T, 480, B_, tl=R_S, tr=R_S, br=R_L, bl=R_S)
gc = (376, 256)
G = Gb.difference(circle(*gc, 64))
G = G.difference(stroke([(gc[0], gc[1]-12), (520, gc[1]-12)], CUT))   # mouth of the G (opens right, above bar)
faceB = unary_union([H, G, buttons(*gc, off=32, r=15)])
emit("b", [Hb, Gb], faceB, "HG Gaming World — concept B")

# ================= C: one controller block, minimal =================
C0 = rrect(48, 112, 464, 400, tl=R_L, tr=R_L, br=R_L, bl=R_L)
C = C0.difference(stroke([(256, 60), (256, 452)], CUT))          # split into two halves (two grips)
# h: notch from bottom in left half; g: bowl + smile in right half
C = C.difference(stroke([(176, 460), (176, 300)], CUT))
C = C.difference(dpad(124, 236, L=64, arm=22))
C = C.difference(circle(360, 236, 56))
C = C.difference(stroke([(268, 340), (352, 340)] + arcpts(352, 308, 32, 90, 0, 32), CUT))
faceC = unary_union([C, buttons(360, 236, off=30, r=14)])
emit("c", [C0], faceC, "HG Gaming World — concept C")
