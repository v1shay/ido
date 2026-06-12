# idō

idō is one local companion for two separate CAD workflows:

- `adapters/blender/` renders editable Engineering IR inside Blender.
- `adapters/openscad/` compiles Engineering IR into a watched `.scad` file and
  exports STL, PNG, 3MF, and SVG artifacts.

The shared FastAPI backend, CLI, status model, and desktop pet live on `main`.
Blender and OpenSCAD project state remain separate in v1.

## Install

Python 3.11 or newer is required for development.

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev,desktop]'
cp .env.example .env
```

Set `OPENAI_API_KEY` in `.env`, or run deterministic demo prompts with:

```bash
CAD_AGENT_DEMO_MODE=true ido
```

## CLI

```bash
ido
ido open blender
ido open openscad
ido prompt --tool blender "make a house"
ido prompt --tool openscad "make a bracket with two mounting holes"
ido pet show
ido pet hide
ido status
```

`ido` starts the API on `http://127.0.0.1:8010` and opens the local control
website. OpenSCAD projects are written under `~/.ido/projects/default` unless
`IDO_OUTPUT_DIR` is set.

## Blender

Build the add-on archive:

```bash
cd adapters/blender
zip -r cad_agent.zip cad_agent
```

Install it through `Blender → Edit → Preferences → Add-ons → Install from Disk`,
press `N` in the 3D View, and open the `CAD-Agent` tab. The default backend URL
is `http://127.0.0.1:8010`.

## OpenSCAD

Install OpenSCAD so its CLI is on `PATH`, then run:

```bash
ido open openscad
ido prompt --tool openscad "make a 30 mm cube with a centered hole"
```

The adapter writes and verifies `ido_current.scad`. Missing export tooling is
reported without discarding the generated source.

## Website

The React/Vite product and documentation site is in `web/`.

```bash
cd web
npm ci
npm run dev
npm run build
```

The same build is deployed to GitHub Pages and served by the local companion.

## Verification

```bash
.venv/bin/pytest
cd web && npm run lint && npm run build
```

GitHub Actions tests Python on macOS, Windows, and Linux, deploys Pages from
`main`, and creates companion plus Blender add-on artifacts for version tags.
