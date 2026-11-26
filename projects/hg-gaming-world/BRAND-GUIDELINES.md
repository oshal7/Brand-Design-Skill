# HG Gaming World — Brand Guidelines

*Living document. Sections marked **draft** are waiting on a decision.*

Names in use: **Happy Gaming World** (full name) · **HG World** (short) · **HGW** (monogram/initials).

---

## 1. The mark

Two solid blocks, the two halves of a controller: the **H** block (D-pad, sharp corners, one large
grip corner) and the **G** block (button ring, softer corners, one large grip corner). Each block is
extruded at **45°**; the notches left open between the two extrusions form a **W** — so the mark
reads **H · G · W**.

### 1.1 The depth rule (non-negotiable)

> **The HG mark is never shown flat. It always appears with its 45° depth** — in two colours
> (white face, signature-colour depth and border) or as the one-colour depth version.

- The depth always runs **down and to the right at exactly 45°**. Never flip, rotate or change the angle.
- Each block keeps **its own** extrusion so the V / Λ notches between H and G (the W) stay open.
- The face is always the lightest value; depth and border are always the same colour.
- One-colour needs (print, embroidery, engraving, stamps, single-ink merch) use the
  **one-colour depth** files, not a flat silhouette.

Why: without the depth the two blocks read as the numerals "69". The depth turns them into two
physical objects, creates the W, and is the most ownable part of the identity.

### 1.2 Versions

| Version | File | Use |
|---|---|---|
| Primary | `01-logo/hg-primary.svg` | Default everywhere; dark (70% of the brand) and light backgrounds |
| One colour, white | `01-logo/hg-one-colour-white.svg` | On the signature colour, photos, dark single-ink |
| One colour, signature | `01-logo/hg-one-colour-blue.svg` | On light, single-ink |
| One colour, black | `01-logo/hg-one-colour-black.svg` | Print, emboss, stamp, engraving |
| Small sizes (≤ 32 px) | `01-logo/hg-small.svg` (+ one-colour) | Favicons, tabs, notifications, tiny UI |
| App icon | `01-logo/hg-app-icon.svg` | App stores, home screens, social avatars |
| Favicon | `01-logo/hg-favicon.svg` | Browser favicon source |

### 1.3 Small-size version

**Approved — small sizes only.** Below **32 px** tall the full mark's detail fills in, so use `hg-small.svg`: same blocks, same 45°
depth and W notches, with the arrow-key D-pad simplified to a plus, the four buttons to a single
button ring (circle with a centre dot), wider hook/smile cuts and a heavier depth and border.

| Size (mark height) | Use |
|---|---|
| ≥ 48 px / 15 mm | Primary master |
| 33–47 px | Either; prefer the master |
| ≤ 32 px | Small-size version only |
| Minimum | 16 px (small-size version) |

### 1.4 Clear space

Unit **X** = the depth offset (≈ 13% of a block's height). Keep **2X** clear on every side of the
mark, measured from the outside of the depth and border.

### 1.5 Don'ts

- Show it flat (no depth), or with depth at any angle other than 45° down-right.
- Merge the two extrusions (closing the W notches) or move the blocks apart/together.
- Recolour the face, use two different colours for depth and border, or add gradients, glows, bevels or drop shadows.
- Stretch, skew, rotate or mirror the mark.
- Place the primary on mid-tone or busy backgrounds where the depth disappears — use a one-colour version.
- Redraw the D-pad, buttons, hook or smile, or swap in other icons.

---

## 2. Colour — Indigo + Volt (approved)

Board: `02-colour/colour-system.png` · tokens: `02-colour/tokens.css` · data: `02-colour/palette.json`

### 2.1 Brand colours
| Token | HEX | RGB | CMYK (approx.) | Pantone (approx., verify on a physical guide) | Role |
|---|---|---|---|---|---|
| **Indigo 500** — signature | `#2E1FF5` | 46 31 245 | 85 80 0 0 | 2726 C / Blue 072 C | Logo depth, brand blocks, badges, links on light |
| Indigo 300 | `#8C83FF` | 140 131 255 | 45 45 0 0 | 2715 C | Links and indigo text **on dark** |
| Indigo 400 | `#5E52FF` | 94 82 255 | 68 65 0 0 | 2725 C | Hover on dark |
| Indigo 600 | `#2216C4` | 34 22 196 | 95 90 0 0 | 2736 C | Pressed on light |
| Indigo 100 / 800 | `#E7E5FF` / `#120B6B` | | | | Light tints / deep shades |
| **Volt 400** — accent | `#C6FF33` | 198 255 51 | 25 0 85 0 | 375 C / 802 C (neon) | Primary CTA on dark, deals, prices, highlights |
| Volt 800 | `#3F5500` | 63 85 0 | 60 30 100 45 | 371 C | Volt-family **text on light** |
| Volt 300 / 600 | `#DBFF85` / `#9ACC14` | | | | Tints for charts/states |

Indigo 500 and Volt 400 sit outside the CMYK gamut — use the Pantone spot colours for premium print.

### 2.2 Modes (≈70% dark / 30% light)
| Token | Dark (default) | Dim | Light |
|---|---|---|---|
| bg | `#0A0A10` Void | `#16161F` | `#F4F4F8` Paper |
| surface | `#15151E` Carbon | `#20202B` | `#FFFFFF` |
| raised | `#24242F` Graphite | `#2C2C38` | `#EBEBF1` |
| border | `#34343F` | `#3C3C49` | `#DADAE3` |
| text | `#F4F4F8` | `#F4F4F8` | `#0A0A10` |
| text-2 | `#A3A3B3` | `#ABABBC` | `#55556A` |
| link | `#8C83FF` | `#9A92FF` | `#2E1FF5` |
| primary CTA | Volt fill, Void text | Volt fill, Void text | Void fill, Volt text |
| brand fill | Indigo, white text | Indigo, white text | Indigo, white text |

Every text pair above is ≥ 4.5 : 1 (WCAG AA) in all three modes.

### 2.3 Colour rules
- Proportion: dark neutrals ≈ 70%, light ≈ 30%, Indigo ≈ 5–10%, Volt ≤ 5% — Volt is a highlight, never a background for long text.
- Never set Indigo 500 as text on dark (2.5 : 1) — use Indigo 300.
- Never set Volt as text on light — use Volt 800, or Volt on a Void button.
- An Indigo fill on dark is low-contrast as a shape (2.5 : 1): give Indigo buttons white labels and don't rely on the fill alone to show a boundary; the main dark-mode CTA is Volt.
- Logo on colour: primary on Void/Carbon/Paper; one-colour white on Indigo or Graphite; one-colour Void on Volt.

## 3. Typography — **draft: Unbounded or Rubik, tuned** (see `03-typography/type-tuned.png`)

Type is **flat**. The 45° depth belongs to the mark only.

The display face is a tuned version of Unbounded Black or Rubik ExtraBold, both under the SIL Open
Font License, which allows logo use. Body and UI text is set in Inter. Tuning carries the mark into the letters:

1. **Soft outer corners.** Convex corners are rounded at 7.5% of cap height, which brings the logo's curviness into the type.
2. **Grip corners.** The H gets the mark's big top-left corner and the G gets its big bottom-right corner, echoing the two blocks.
3. **Sharp inner joins.** Concave corners stay crisp, like the cuts in the mark.
4. **Tight spacing.** Negative tracking plus hand-kerned pairs (AP, PY, WO, GW and others) set the letters close, like the two blocks.

Lockups are in `03-typography/lockups/`. The type is outlined, so no font is needed:
- `stack3`: three lines, as tall as the mark (primary)
- `stack2`: HAPPY / GAMING WORLD
- `line`: one line, for headers
- `hg-world`: compact
- `hgw`: the mark stacked over the monogram, for avatars and merch

Each lockup comes in three versions: `-black` (with the one-colour mark), `-on-dark` and `-on-light`.

## 4. Patterns — *to revisit*
