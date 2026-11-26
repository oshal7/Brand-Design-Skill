# HG Gaming World — brand identity

Built with the `logo-design` skill in this repo, one step at a time, around the existing HG mark.

1. **Logo refinement** — `01-logo/` ✅ refined master (awaiting sign-off)
2. Final master kit (small-size cut, favicon/app icon, lockups)
3. Typography for *Happy Gaming World*, *HG World*, *HGW*
4. Pattern system
5. Brand guidelines

## 01-logo files
Faithful refinement of the original mark: sharp h-block, rounded g-block, pointed arrow-key
D-pad, tapered cuts with sharp ends; rebuilt with true curves, centred buttons, even 45° depth
and a thin border.

| File | Use |
|---|---|
| `hg-primary.svg` | Primary logo (white face, blue depth + border), transparent — dark or light backgrounds |
| `hg-primary-on-dark.svg` / `hg-primary-on-light.svg` | Same, with background baked in |
| `hg-flat-white.svg` | Flat, reversed — on dark or brand blue |
| `hg-flat-blue.svg` | Flat brand blue — on light |
| `hg-flat-black.svg` | One colour — print, emboss, stamp |
| `refined-mark-board.png` | Before/after and all versions |
| `original-mark.webp` | The original artwork, for reference |

`src/` regenerates everything: `pip install shapely`, then `python3 src/logo.py 01-logo`.
