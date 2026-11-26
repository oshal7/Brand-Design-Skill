"""HG Gaming World pattern library. Every pattern is generated from an identity rule:
45-degree depth, the W notch, the NW/SE diagonal axis, the two blocks, controller parts, HGW Display type, ecosystem."""
import sys, math, random; sys.path.insert(0, '.')
from shapely.geometry import box, Polygon, Point, LineString
from shapely.ops import unary_union
from shapely import affinity
from geo import rrect, circle, sweep, RES, to_d
from logo import dpad, buttons, HOOK, L_blk, R_blk, face as LF, body as LB, WL, WR, GAP, H
from small import s_face, s_body

W_, H_ = 1600, 1000
CANVAS = box(0, 0, W_, H_)
WAYS = {
  "void":   dict(bg="#0A0A10", face="#1B1B26", depth="#11111A", line="#262633", acc="#2E1FF5", hi="#C6FF33", ink="#F4F4F8"),
  "indigo": dict(bg="#2E1FF5", face="#4537FF", depth="#2216C4", line="#5E52FF", acc="#FFFFFF", hi="#C6FF33", ink="#FFFFFF"),
  "volt":   dict(bg="#C6FF33", face="#0A0A10", depth="#2E1FF5", line="#0A0A10", acc="#2E1FF5", hi="#FFFFFF", ink="#0A0A10"),
  "light":  dict(bg="#F4F4F8", face="#E2E0F7", depth="#2E1FF5", line="#DADAE3", acc="#2E1FF5", hi="#C6FF33", ink="#0A0A10"),
}

def ab(x0, y0, x1, y1, r):            # axis block: NW + SE rounded (the mark's silhouette rule)
    return rrect(x0, y0, x1, y1, tl=r, br=r)
def extrude(g, d):
    parts = [g] if g.geom_type == "Polygon" else list(g.geoms)
    return unary_union([sweep(Polygon(p.exterior), d, d) for p in parts])
def solid(face, d, out=0):
    """3D item: (depth body, face). out = thin border like the mark."""
    body = extrude(face, d)
    if out: body = body.buffer(out, join_style="mitre")
    return body, face

# --------------------------------------------------------------------------------------------- DEPTH
def p_extrude_field():
    """Axis blocks on a grid, each extruded 45 deg, heights vary like keys on a keypad."""
    random.seed(3); items = []; s = 120
    for j in range(-1, 10):
        for i in range(-1, 15):
            x, y = i * s + (s / 2 if j % 2 else 0), j * s * 0.9
            w = s * random.choice([0.55, 0.7, 0.7, 0.85]); d = random.choice([10, 18, 26, 34])
            f = ab(x, y, x + w, y + w * 0.62, w * 0.28)
            b, f = solid(f, d)
            items += [(b, "depth"), (f, "face" if random.random() > 0.08 else "acc")]
    return items

def p_depth_steps():
    """Long axis bars stacked at 45 deg like stairs; each step's extrusion is the next step's shadow."""
    items = []; bh, step = 46, 64
    for k in range(-14, 24):
        x0 = k * step - 400; y0 = k * step * 0.0
        for row in range(0, 18):
            y = row * 120 - 60; x = (row * 64 + k * 300) % 2100 - 300
            f = ab(x, y, x + 260, y + bh, bh * 0.5)
            b, f = solid(f, 40)
            items += [(b, "depth"), (f, "face")]
        break
    return items

def p_w_chain():
    """Rows of the mark's block pair, extruded per block: the notches between them chain into W's."""
    items = []; sc = 0.17
    hb = affinity.scale(L_blk, sc, sc, origin=(0, 0)); gb = affinity.scale(R_blk, sc, sc, origin=(0, 0))
    pw = (WL + GAP + WR) * sc + 16; ph = H * sc + 40
    for j in range(-1, 10):
        for i in range(-1, 12):
            x, y = i * pw + (pw / 2 if j % 2 else 0), j * ph
            for blk in (hb, gb):
                b, f = solid(affinity.translate(blk, x, y), 14, 3)
                items += [(b, "depth"), (f, "face")]
    return items

def p_speed_lines():
    """45-deg extrusion edges as speed lines; bands thicken toward the lower-right, like depth."""
    items = []
    for k in range(-30, 60):
        t = 6 + 22 * max(0, min(1, (k + 30) / 90)) ** 1.6
        off = k * 46
        items.append((Polygon([(off, 0), (off + t, 0), (off + t + H_, H_), (off + H_, H_)]), "line"))
    # a few blocks punching through, extruded the same way
    mark_b, mark_f = s_body, s_face
    minx, miny, maxx, maxy = mark_b.bounds
    for (x, y, sc) in [(180, 160, 0.42), (880, 470, 0.55), (1290, 110, 0.3)]:
        b = affinity.translate(affinity.scale(mark_b, sc, sc, origin=(minx, miny)), x - minx, y - miny)
        f = affinity.translate(affinity.scale(mark_f, sc, sc, origin=(minx, miny)), x - minx, y - miny)
        items += [(b.buffer(18), "bg"), (b, "depth"), (f, "acc")]
    return items

def p_iso_stack():
    """Blocks stacked into 45-deg towers; the depth of each sits on the next. City of controllers."""
    random.seed(11); items = []
    cols = list(range(-1, 14))
    for i in cols:
        x = i * 128; n = random.randint(2, 7)
        for k in range(n):
            y = H_ - 80 - k * 70 - (i % 3) * 30
            f = ab(x - k * 0, y - 60, x + 100, y, 30)
            b, f = solid(f, 22, 2)
            items += [(b, "depth"), (f, "acc" if (k == n - 1 and random.random() < .35) else "face")]
    return items

# --------------------------------------------------------------------------------------------- AXIS
def leaf(cx, cy, s, rot=0):
    g = ab(cx - s/2, cy - s/2, cx + s/2, cy + s/2, s / 2)
    return affinity.rotate(g, rot, origin=(cx, cy)) if rot else g

def p_grip_weave():
    """Square cells with full NW/SE rounding (leaves). Rotating every other cell 90 deg weaves eyes and diamonds."""
    items = []; s = 100; g = 8
    for j in range(-1, 11):
        for i in range(-1, 17):
            items.append((leaf(i * s + s/2, j * s + s/2, s - g, 90 if (i + j) % 2 else 0), "face"))
    return items

def p_grip_flow():
    """Leaves scaled along a sine field: big at the crest, tiny in the trough. Reads as motion."""
    items = []; s = 64
    for j in range(-1, 17):
        for i in range(-1, 26):
            cx, cy = i * s + s/2, j * s + s/2
            k = 0.5 + 0.5 * math.sin(i * 0.33 + j * 0.42)
            items.append((leaf(cx, cy, 10 + k * (s - 12)), "acc" if (k > 0.97 and (i * 7 + j * 5) % 13 == 0) else "face"))
    return items

def p_axis_grid():
    """The diagonal axis drawn as a 45-deg grid; small axis blocks sit on the crossings."""
    items = []; s = 110
    for k in range(-20, 40):
        items.append((LineString([(k * s, 0), (k * s + H_, H_)]).buffer(1.5, cap_style="flat"), "line"))
        items.append((LineString([(k * s, H_), (k * s + H_, 0)]).buffer(1.5, cap_style="flat"), "line"))
    for j in range(0, 20):
        for i in range(-1, 32):
            x = i * s / 2 + (s / 4 if j % 2 else 0); y = j * s / 2
            if (i * 7 + j * 3) % 5 == 0:
                items.append((ab(x - 14, y - 14, x + 14, y + 14, 12), "acc"))
    return items

def p_grip_corners():
    """Only the grip corners, as quarter rings, rotated in 2 states (NW / SE) - a maze of the mark's curve."""
    random.seed(5); items = []; s = 90; t = 18
    for j in range(-1, 12):
        for i in range(-1, 19):
            x, y = i * s, j * s
            ring = Point(x + s, y + s).buffer(s - t/2, quad_segs=RES).difference(Point(x + s, y + s).buffer(s/2 - t/2, quad_segs=RES))
            q = ring.intersection(box(x, y, x + s, y + s))
            if random.random() < 0.5: q = affinity.rotate(q, 180, origin=(x + s/2, y + s/2))
            items.append((q, "face"))
    return items

# --------------------------------------------------------------------------------------------- CONTROLLER PARTS
def p_arrow_flow():
    """Single arrow keys from the D-pad, each pointing along a circular flow field around a centre."""
    items = []; s = 96
    arrow = dpad(0, 0).intersection(box(-60, -130, 60, -1))
    minx, miny, maxx, maxy = arrow.bounds; arrow = affinity.translate(arrow, 0, -(miny + maxy) / 2)
    cx, cy = W_ * 0.62, H_ * 0.55
    for j in range(-1, 16):
        for i in range(-1, 24):
            x, y = i * s + (s/2 if j % 2 else 0), j * s
            ang = math.degrees(math.atan2(y - cy, x - cx)) + 180
            d = math.hypot(x - cx, y - cy)
            a = affinity.rotate(affinity.scale(arrow, 0.5, 0.5, origin=(0, 0)), ang + 90, origin=(0, 0))
            items.append((affinity.translate(a, x, y), "acc" if 300 < d < 380 else "face"))
    return items

def p_button_fractal():
    """The button ring arranged as rings of rings: 4 rings around a ring around a ring."""
    items = []
    ring = circle(0, 0, 118).difference(buttons(0, 0))
    def place(x, y, s, depth):
        items.append((affinity.translate(affinity.scale(ring, s, s, origin=(0, 0)), x, y), "acc" if depth == 0 else "face"))
        if depth < 2:
            off = 64 * s * 2.6
            for dx, dy in [(0, -off), (off, 0), (0, off), (-off, 0)]:
                place(x + dx, y + dy, s * 0.42, depth + 1)
    for j in range(-1, 4):
        for i in range(-1, 6):
            place(i * 400 + (200 if j % 2 else 0), j * 340, 0.62, 0)
    return items

def p_smile_field():
    """The hook/smile cut, scaled and rotated in 4 states, tiling into a field of grins."""
    items = []; s = 110
    h = HOOK.intersection(box(0, 0, WL, 400)); minx, miny, maxx, maxy = h.bounds
    h = affinity.translate(h, -(minx + maxx)/2, -(miny + maxy)/2); h = affinity.scale(h, 0.42, 0.42, origin=(0, 0))
    for j in range(-1, 11):
        for i in range(-1, 16):
            items.append((affinity.translate(affinity.rotate(h, [0, 90, 180, 270][(i + 2*j) % 4], origin=(0, 0)), i * s, j * s), "face"))
    return items

def p_halves():
    """h-blocks and g-blocks (with their cuts) tiled in alternating orientation like a puzzle of controller halves."""
    items = []; sc = 0.2
    hface = affinity.scale(LF.intersection(L_blk.buffer(1)), sc, sc, origin=(0, 0))
    gface = affinity.scale(affinity.translate(LF.intersection(R_blk.buffer(1)), -(WL + GAP), 0), sc, sc, origin=(0, 0))
    w, h = WL * sc + 10, H * sc + 10
    for j in range(-1, 9):
        for i in range(-1, 21):
            g = hface if (i + j) % 2 == 0 else gface
            items.append((affinity.translate(g, i * w, j * h), "acc" if (i * 5 + j * 3) % 11 == 0 else "face"))
    return items

def p_dpad_lattice():
    """Arrow-key D-pads interlocking on a 45-deg lattice: each arrow points into a neighbour's gap."""
    items = []; s = 150
    for j in range(-1, 16):
        for i in range(-1, 14):
            x, y = i * s + (s/2 if j % 2 else 0), j * s * 0.5
            items.append((affinity.translate(affinity.rotate(affinity.scale(dpad(0, 0), 0.5, 0.5, origin=(0, 0)), 45, origin=(0, 0)), x, y), "face"))
    return items

# --------------------------------------------------------------------------------------------- TYPE
def _word(t, cap):
    from typo import glyph_shapes
    gl, _ = glyph_shapes(FONT, t, cap, -0.01)
    return unary_union([g for ch, g, x in gl if g is not None])
FONT = "/home/user/Brand-Design-Skill/projects/hg-gaming-world/03-typography/font/HGWDisplay-ExtraBold.ttf"

def p_hgw_monogram():
    """HGW set huge, extruded 45 deg, cropped and offset row to row."""
    items = []; w = _word("HGW", 220); minx, miny, maxx, maxy = w.bounds; ww = maxx - minx + 70
    for j in range(-1, 6):
        for i in range(-1, 4):
            g = affinity.translate(w, i * ww + (ww / 2 if j % 2 else 0) - minx, j * 230 + 200)
            b, f = solid(g, 22)
            items += [(b, "depth"), (f, "face")]
    return items

def p_word_ticker():
    """Ecosystem verbs in HGW Display, alternating solid / outline rows, like a shop ticker."""
    items = []; words = ["BUY", "REPAIR", "REFUEL", "PLAY"]
    for j in range(-1, 10):
        x = -200 - (j * 137) % 400
        while x < W_ + 200:
            for k, t in enumerate(words):
                g = _word(t, 70); minx, miny, maxx, maxy = g.bounds
                g = affinity.translate(g, x - minx, j * 110 + 90)
                items.append((g if j % 2 == 0 else g.boundary.buffer(2.2), "face" if t != "PLAY" else "acc"))
                x += maxx - minx + 40
                arrow = Polygon([(0, -14), (22, 0), (0, 14)])
                items.append((affinity.translate(arrow, x, j * 110 + 90 - 26), "acc")); x += 60
    return items

def p_letter_crops():
    """Single HGW Display letters at giant scale, cropped to axis blocks - the type's diagonal curves become shapes."""
    items = []; letters = "HGWHAPPYGAMINGWORLD"; s = 200; k = 0
    for j in range(0, 5):
        for i in range(0, 8):
            ch = letters[k % len(letters)]; k += 1
            g = _word(ch, 300); minx, miny, maxx, maxy = g.bounds
            g = affinity.translate(g, -(minx + maxx)/2 + i * s + s/2, -(miny + maxy)/2 + j * s + s/2)
            cell = ab(i * s + 6, j * s + 6, i * s + s - 6, j * s + s - 6, 60)
            items.append((cell, "face")); items.append((g.intersection(cell), "acc" if (i + j) % 3 == 0 else "depth"))
    return items

# --------------------------------------------------------------------------------------------- ECOSYSTEM
def icon(kind, s=100):
    """Ecosystem icons in the identity grammar: axis blocks, 45-deg cuts, grip corners."""
    r = s * 0.22
    if kind == "buy":      # bag: axis block + handle cut
        bag = ab(-s/2, -s*0.25, s/2, s/2, r)
        handle = Point(0, -s*0.25).buffer(s*0.28, quad_segs=RES).difference(Point(0, -s*0.25).buffer(s*0.16, quad_segs=RES)).intersection(box(-s, -s, s, -s*0.25))
        return unary_union([bag, handle])
    if kind == "repair":   # wrench: rotated bar with a notched head
        bar = ab(-s*0.12, -s*0.2, s*0.12, s*0.55, s*0.12)
        head = Point(0, -s*0.32).buffer(s*0.26, quad_segs=RES).difference(box(-s*0.09, -s*0.62, s*0.09, -s*0.32))
        return affinity.rotate(unary_union([bar, head]), -45, origin=(0, 0))
    if kind == "refuel":   # bolt: two axis parallelograms at 45
        p = Polygon([(s*0.12, -s*0.55), (-s*0.32, s*0.08), (-s*0.02, s*0.08), (-s*0.14, s*0.55), (s*0.32, -s*0.08), (s*0.02, -s*0.08)])
        return p
    if kind == "play":     # play triangle with the mark's grip on its top-left
        tri = Polygon([(-s*0.35, -s*0.45), (s*0.45, 0), (-s*0.35, s*0.45)])
        return tri.intersection(ab(-s*0.35, -s*0.45, s*0.45, s*0.45, s*0.3))
def p_ecosystem():
    """Buy / Repair / Refuel / Play icons on axis tiles, extruded - one row per service, offset like a schedule."""
    items = []; s = 150; kinds = ["buy", "repair", "refuel", "play"]
    for j in range(-1, 8):
        for i in range(-1, 12):
            x, y = i * s + (s/2 if j % 2 else 0), j * s
            tile = ab(x - 58, y - 58, x + 58, y + 58, 40)
            b, f = solid(tile, 14)
            k = kinds[(i + j) % 4]
            items += [(b, "depth"), (f, "face"), (affinity.translate(icon(k, 64), x, y), "acc" if k == "play" else "ink")]
    return items
def p_network():
    """Ecosystem nodes joined by grip-corner paths: every service connects - the 'World'."""
    random.seed(8); items = []; s = 200; nodes = []
    for j in range(0, 6):
        for i in range(0, 9):
            nodes.append((i * s + 100 + random.uniform(-20, 20) * 0, j * s + 0))
    paths = []
    for (x, y) in nodes:
        if random.random() < 0.7:
            paths.append(LineString([(x, y), (x + s - 60, y)] + [(x + s - 60 + 60 * math.sin(a), y + 60 - 60 * math.cos(a)) for a in [k * math.pi / 20 for k in range(11)]] + [(x + s, y + s)]))
        if random.random() < 0.5:
            paths.append(LineString([(x, y), (x, y + s)]))
    items.append((unary_union([p.buffer(14, cap_style="flat") for p in paths]), "line"))
    kinds = ["buy", "repair", "refuel", "play"]
    for n, (x, y) in enumerate(nodes):
        b, f = solid(ab(x - 52, y - 52, x + 52, y + 52, 36), 12)
        items += [(b, "depth"), (f, "face"), (affinity.translate(icon(kinds[n % 4], 58), x, y), "acc" if n % 4 == 3 else "ink")]
    return items

PATTERNS = {
  "01-extrude-field": ("Extrude field", "Depth", p_extrude_field),
  "02-w-chain": ("W chain", "Depth", p_w_chain),
  "03-speed-lines": ("Speed lines", "Depth", p_speed_lines),
  "04-controller-city": ("Controller city", "Depth", p_iso_stack),
  "05-grip-weave": ("Grip weave", "Axis", p_grip_weave),
  "06-grip-flow": ("Grip flow", "Axis", p_grip_flow),
  "07-axis-grid": ("Axis grid", "Axis", p_axis_grid),
  "08-grip-maze": ("Grip maze", "Axis", p_grip_corners),
  "09-arrow-flow": ("Arrow flow", "Controller", p_arrow_flow),
  "10-button-fractal": ("Button fractal", "Controller", p_button_fractal),
  "11-grin-field": ("Grin field", "Controller", p_smile_field),
  "12-halves": ("Halves", "Controller", p_halves),
  "13-dpad-lattice": ("D-pad lattice", "Controller", p_dpad_lattice),
  "14-hgw-monogram": ("HGW monogram", "Type", p_hgw_monogram),
  "15-ticker": ("Ticker", "Type", p_word_ticker),
  "16-letter-crops": ("Letter crops", "Type", p_letter_crops),
  "17-ecosystem-tiles": ("Ecosystem tiles", "Ecosystem", p_ecosystem),
  "18-network": ("Network", "Ecosystem", p_network),
}

def write(name, items, way, out):
    c = WAYS[way]
    paths = [f'<rect width="{W_}" height="{H_}" fill="{c["bg"]}"/>']
    for g, role in items:
        g = g.intersection(CANVAS)
        if g.is_empty: continue
        if g.geom_type not in ("Polygon", "MultiPolygon"):
            polys = [p for p in getattr(g, "geoms", []) if p.geom_type in ("Polygon", "MultiPolygon")]
            if not polys: continue
            g = unary_union(polys)
        paths.append(f'<path fill="{c[role]}" fill-rule="evenodd" d="{to_d(g.simplify(0.3))}"/>')
    open(f"{out}/{name}-{way}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W_} {H_}" width="{W_}" height="{H_}">' + "".join(paths) + "</svg>\n")

if __name__ == "__main__":
    out = sys.argv[1]; only = sys.argv[2:] or list(PATTERNS)
    for name in only:
        items = PATTERNS[name][2]()
        for way in WAYS: write(name, items, way, out)
        print(name, len(items))
