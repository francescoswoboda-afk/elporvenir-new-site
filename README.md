# El Porvenir Farm — showcase website

A single-page showcase site for El Porvenir Farm, a pecan orchard in Rio Grande do Sul, Brazil.

## Files

- `index.html` — the finished site, one self-contained file (open it in a browser). This is what gets published.
- `src/` — the source you edit:
  - `index.template.html` — page structure
  - `style.css` — design (type scale, colours, layout)
  - `i18n.js` — all text, in English, Portuguese and Spanish (`«TBD»` / `«VERIFY»` show as placeholders)
  - `tree.js` — the living pecan tree (canvas)
  - `map.js` — the animated map
  - `audio.js` — the ambient sound
  - `main.js` — scroll, seasons, navigation, gallery and everything that ties it together
- `assets/` — the photos and logo that get embedded into `index.html`
- `build.py` — bundles `src/` and `assets/` into `index.html`
- `DECISIONES.md` — design decisions (in Spanish)
- `type-study.html` — the typography study

## Editing

1. Change files in `src/`.
2. Rebuild: `python3 build.py` (needs Python 3 and Pillow: `pip install pillow`).
3. Open `index.html` in a browser to check.

Tip: in VS Code, the "Live Server" extension shows `index.html` and reloads it on save.
