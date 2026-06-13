<img width="1756" height="986" alt="Adobe Express - Screen Recording 2026-06-12 at 10 34 17 PM" src="https://github.com/user-attachments/assets/e8a34511-fdf2-494f-89cc-36b95c4b9948" />

<p align="center">
  <img src="assets/ido-banner.png" alt="idō" width="640" />
</p>

# idō

idō is one local companion for two separate CAD workflows:

- `adapters/blender/` renders editable Engineering IR inside Blender.
- `adapters/openscad/` compiles Engineering IR into a watched `.scad` file and
  exports STL, PNG, 3MF, and SVG artifacts.

The shared FastAPI backend, CLI, and status model live on `main`.
Blender and OpenSCAD project state remain separate in v1.

## Install

Python 3.11 or newer is required for development.

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
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
ido status
```

`ido` starts the API on `http://127.0.0.1:8010` and opens the local control
website. OpenSCAD projects are written under `~/.ido/projects/default` unless
`IDO_OUTPUT_DIR` is set.

## Blender

Build the add-on archive:

```bash
cd adapters/blender
zip -r ../../ido_blender.zip ido_blender
```

Install it through `Blender → Edit → Preferences → Add-ons → Install from Disk`,
press `N` in the 3D View, and open the `idō` tab. The default backend URL
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

The same build is served locally by the companion at http://127.0.0.1:8010 when
you run `ido serve`.

## Verification

```bash
.venv/bin/pytest
cd web && npm run lint && npm run build
```

Run the exact two-prompt flow in headless Blender while the backend is running:

```bash
ido render blender "make a house" --follow-up "add more windows"
# or directly:
/Applications/Blender.app/Contents/MacOS/Blender \
  --background --factory-startup --python scripts/blender_smoke.py
```

GitHub Actions tests Python on macOS, Windows, and Linux, and creates companion
plus Blender add-on artifacts for version tags.

## TrueFoundry

The backend includes a Dockerfile and `deploy_truefoundry.py`. Install and
authenticate the current TrueFoundry CLI/SDK:

```bash
.venv/bin/pip install truefoundry
export TFY_HOST=https://your-org.truefoundry.cloud
export TFY_API_KEY=your-token
export TFY_WORKSPACE_FQN=your-workspace-fqn
export TFY_SERVICE_HOST=cad-agent-api.your-domain.example
export OPENAI_API_KEY=your-openai-key
.venv/bin/python deploy_truefoundry.py
```

The token values remain local environment variables and must never be committed.
The application emits structured `parse`, `validate`, `route`, and `execute`
events that are forwarded to Guild when trace export is enabled.

## Guild AI

Enable OpenTelemetry trace export to Guild after each prompt and execution
report:

```bash
export GUILD_TRACE_ENABLED=true
export GUILD_OTLP_ENDPOINT=https://your-guild-collector/v1/traces
export GUILD_API_KEY=your-guild-token
export GUILD_WORKSPACE_ID=your-workspace-id
```

After a successful generate in Blender (for example `add more windows`), the
sidebar shows the full request timeline (`parse → validate → route → execute`)
with timings. Use **Open in Guild** to inspect the exported trace, or enable
**Auto-open Guild after generate** in Connection Settings.

## OpenUI

Every prompt response includes OpenUI Lang that describes the request timeline
and Engineering IR summary. In Blender, use **Show OpenUI Lang** to inspect the
generative UI description in the Text Editor.

## ClickHouse

Enable trace storage for analytics across requests:

```bash
export CLICKHOUSE_ENABLED=true
export CLICKHOUSE_HOST=your-host.clickhouse.cloud
export CLICKHOUSE_PORT=8443
export CLICKHOUSE_SECURE=true
export CLICKHOUSE_USERNAME=default
export CLICKHOUSE_PASSWORD=your-password
```

Trace rows are inserted into `cad_agent_traces` after each prompt and execution
report.

## Composio

Notify an external action after Blender execution completes:

```bash
export COMPOSIO_ENABLED=true
export COMPOSIO_API_KEY=your-composio-key
export COMPOSIO_USER_ID=cad-agent-user
export COMPOSIO_TOOL_SLUG=YOUR_CONFIGURED_TOOL
```

Composio receives a summary of the full request timeline when execution is
reported.

## Pioneer

Use Pioneer as the inference provider with the OpenAI-compatible API:

```bash
export CAD_AGENT_PROVIDER=pioneer
export PIONEER_API_KEY=your-pioneer-key
export PIONEER_MODEL_ID=your-model-id
```

Pioneer runs with the same Engineering IR schema as OpenAI. If inference fails,
the deterministic house demo fallback still applies.

## Airbyte

Export design context for Airbyte to sync into your context layer:

```bash
export AIRBYTE_ENABLED=true
export AIRBYTE_CONTEXT_DIR=./airbyte/context
# optional HTTP sink:
export AIRBYTE_CONTEXT_ENDPOINT=https://your-context-endpoint
```

Each prompt and execution appends a JSONL record with the prompt, IR, and trace.

## Render

Deploy the API on [Render](https://render.com) using the included blueprint:

1. Open [Render Blueprint deploy](https://dashboard.render.com/select-repo?type=blueprint)
2. Connect **arora13/Ido** and select the **`main`** branch
3. Render reads `render.yaml`, builds the Docker image (API + web panel), and health-checks `/api/health`
4. Optional: add `PIONEER_API_KEY`, `OPENAI_API_KEY`, or sponsor env vars in the Render dashboard

Demo mode is enabled by default so the service works without inference keys. Set
`CAD_AGENT_DEMO_MODE=false` and configure a provider when you add API keys.
