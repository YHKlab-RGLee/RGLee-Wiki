# RGLee's Wiki

This repository contains a personal wiki that accumulates AI-generated and
AI-organized scientific knowledge. The published site currently focuses on
cross-verified device-physics research documents.

Site: [https://yhklab-rglee.github.io/RGLee-Wiki/](https://yhklab-rglee.github.io/RGLee-Wiki/)

The wiki maintains three fixed subject areas:

1. Device physics
2. Material science
3. Computational science

`Research Note` is an optional non-scientific support section for reproducible procedures.

When creating or revising content, start with `AGENTS.md`. It routes article format,
research, structural maintenance, focused revision, reference audit, image acquisition,
and quality validation to their canonical references and skills. The compact quality
registry stores only current derived metadata and review attestations; Git provides history.

## Getting Started

Python 3.10 or later is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Start a local preview:

```bash
./build.sh serve
```

Synchronize quality records after the intended `docs/` changes are complete:

```bash
./quality.sh sync
```

Run the read-only quality gate:

```bash
./quality.sh check --all
```

The generated site is written to `site/`.

Generate a strict build. This also runs the quality gate:

```bash
./build.sh build
```

Use the narrower build routes during scoped work:

```bash
./build.sh nav       # navigation checks + strict build; no article review check
./build.sh changed   # changed docs + navigation checks + strict build
```

## Publishing

GitHub Actions builds and deploys the MkDocs site automatically whenever a
commit is pushed to `main`. Configure the repository once under
`Settings > Pages > Build and deployment > Source` by selecting
`GitHub Actions`.

Run a non-mutating preflight before publishing:

```bash
./build.sh preflight
```

Review the listed files, then stage, commit, and push explicitly with Git. The helper does
not stage unrelated worktree changes or perform external mutations.

The generated `site/` directory remains local and is not committed. The GitHub
Actions workflow rebuilds it and uploads it directly as a GitHub Pages
artifact.

## Home document graph

The Home graph is generated on every MkDocs build by `hooks/document_graph.py`.
It includes navigation sections, articles, and all resolved internal document
links. Index pages are represented by their sections. Reciprocal links share one
visible edge. Node colors and initial layout clusters follow their top-level navigation domain.
Navigation tree links hold topics together, with weaker document links between them. A small,
translucent Reset button in the upper left clears selection and fits the full graph.

Click any node or its label to smoothly move it to the center and enlarge it by
1.5×; the selected node, its direct neighbors, all ancestors, incident links and the path to the root remain
emphasized. Other nodes are dimmed but can still be selected. Drag nodes to rearrange them, drag the
background to pan, and use the wheel or a touch pinch to zoom. Node dragging starts
only after movement exceeds 8 screen pixels; pressing or slight finger jitter
keeps the layout still and is treated as a click/tap on release. Labels remain 14
screen pixels at every zoom level. Overlapping overview labels are suppressed;
zooming reveals more titles, and the selected node and its neighbors take priority. Double-click or double-tap an article node to open its page;
Ctrl/Cmd-click opens a new tab. Keyboard Enter/Space centers a node, and Enter on
the centered article opens it. Reduced-motion preferences disable the camera
animation. The ordinary Home contents remain available without JavaScript.

### Code provenance

`overrides/partials/document-graph.js` adapts the D3 force simulation, link/node
rendering, tick updates and drag handlers from
[develmusa/mkdocs-network-graph-plugin](https://github.com/develmusa/mkdocs-network-graph-plugin/blob/79bcdf5db686086e316ffab77c73030f75565426/src/mkdocs_graph_plugin/static/graph.js),
commit `79bcdf5db686086e316ffab77c73030f75565426` (Copyright © 2025 develmusa,
MIT). This is a source adaptation, not an installed Python plugin or a GitHub
fork. The upstream modal/sidebar controls and neighbor/full selector are removed;
this adaptation adds animated camera focus, constant-size wrapped labels,
keyboard access and responsive sizing. The wiki's existing build hook supplies
the graph data. The MIT notice is embedded in the adapted script and preserved
in `overrides/partials/vendor/mkdocs-network-graph-plugin.LICENSE`.

D3 **7.9.0** is vendored in `overrides/partials/vendor/d3.v7.9.0.min.js` from
<https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js>, with its ISC license in
`d3.LICENSE`. Both scripts are embedded in Home; no runtime CDN is needed.

Graph data regression checks: `python3 -m unittest discover -s tests`.
Browser interaction checks: `node tests/document-graph.browser.cjs` (requires
Playwright and Chromium; see the script header for the local command).
