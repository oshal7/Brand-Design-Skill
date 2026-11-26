"""Small-size cut (<= 32 px): same blocks and 45-degree depth; detail reduced, cuts opened up."""
import sys; sys.path.insert(0, '.')
from logo import *            # blocks, slits, constants from the master
from shapely.geometry import box

T = 8                              # extra opening for the hook / smile cuts
SD, SO = 104, 26                   # deeper extrusion + heavier border so they survive downsampling

def plus(cx, cy, a=34, reach=118):
    return unary_union([box(cx - reach, cy - a, cx + reach, cy + a), box(cx - a, cy - reach, cx + a, cy + reach)])

mit = dict(quad_segs=RES, join_style="mitre")
hook = HOOK.buffer(T, **mit)
smile = rot(SMILE_F).buffer(T, **mit)
sL = L_blk.difference(hook).difference(plus(*P(185.5, 409.5)))
sR = R_blk.difference(smile).difference(circle(*bc, 116)).union(circle(*bc, 46))
s_face = unary_union([sL, sR])
L_back = rrect(0, 0, WL, H, tl=R_GRIP, br=RHO)
s_body = unary_union([L_blk.buffer(SO, **mit), sweep(L_back, SD, SD).buffer(SO, **mit),
                      sweep(R_blk, SD, SD).buffer(SO, **mit)])

if __name__ == "__main__":
    OUT = sys.argv[1]
    BLUE, WHITE, BLACK = "#2E1FF5", "#FFFFFF", "#111111"
    minx, miny, maxx, maxy = s_body.bounds; pad = 24
    vb = (minx - pad, miny - pad, maxx - minx + 2*pad, maxy - miny + 2*pad)
    open(f"{OUT}/hg-small.svg","w").write(svg([("depth", s_body, BLUE), ("face", s_face, WHITE)], vb, "HG Gaming World logo — small sizes", size=512))
    for name, col in [("white", WHITE), ("black", BLACK)]:
        open(f"{OUT}/hg-small-one-colour-{name}.svg","w").write(svg([("symbol", s_body.difference(s_face), col)], vb, f"HG Gaming World logo — small, one colour {name}", size=512))
    # square app-icon / favicon tile: small cut, optically centred on an ink tile
    s = max(maxx - minx, maxy - miny); tile = s * 1.42
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2 - s * 0.01
    vbt = (cx - tile/2, cy - tile/2, tile, tile)
    bg = rrect(vbt[0], vbt[1], vbt[0] + tile, vbt[1] + tile, tl=tile*.22, tr=tile*.22, br=tile*.22, bl=tile*.22)
    open(f"{OUT}/hg-app-icon.svg","w").write(svg([("tile", bg, "#121214"), ("depth", s_body, BLUE), ("face", s_face, WHITE)], vbt, "HG Gaming World app icon", size=512))
    sq = box(*vbt[:2], vbt[0] + tile, vbt[1] + tile)
    open(f"{OUT}/hg-favicon.svg","w").write(svg([("tile", sq, "#121214"), ("depth", s_body, BLUE), ("face", s_face, WHITE)], vbt, "HG Gaming World favicon", size=512))
