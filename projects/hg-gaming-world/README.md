# HG Gaming World — brand identity

Built with the `logo-design` skill in this repo, one step at a time, around the existing HG mark.

1. **Logo refinement** — `01-logo/` ✅ refined master (awaiting sign-off)
2. Final master kit (small-size cut, favicon/app icon, lockups)
3. Typography for *Happy Gaming World*, *HG World*, *HGW*
4. Pattern system
5. Brand guidelines

## 01-logo files
| File | Use |
|---|---|
| `hg-depth-transparent.svg` | Primary logo (white face, blue depth) — dark or light backgrounds |
| `hg-depth-on-dark.svg` / `hg-depth-on-light.svg` | Same, with background baked in |
| `hg-flat-white.svg` | Flat, reversed — on dark or brand blue |
| `hg-flat-blue.svg` | Flat brand blue — on light |
| `hg-flat-black.svg` | One colour — print, emboss, stamp |
| `refined-mark-board.png` | Before/after and all versions |

`src/` regenerates everything: `pip install shapely`, then `python3 src/refined.py 01-logo`.
