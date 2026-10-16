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

The Home page's document map is generated automatically on every MkDocs build
(including GitHub Pages builds and normal `mkdocs serve` rebuilds). No separate
generation command or checked-in graph data is required.

- `hooks/document_graph.py` traverses the resolved `mkdocs.yml` navigation in its
  configured order. Sections become structural nodes; `index.md` pages are omitted.
- After Markdown rendering, internal document links add directed relationships.
  Repeated links to the same target collapse, including section fragments. External
  links, self-links and links to excluded pages do not add edges. Reciprocal links
  remain two relationships, drawn on the same dotted curve.
- `overrides/partials/document-graph.*` renders the map above the Home contents.
  Purple, blue and green distinguish domains, topic groups and documents; node
  sizes also distinguish those levels. Search, focus highlighting, zoom controls,
  background dragging and document links work without a graph library or CDN.
  The ordinary contents remain available without JavaScript.

### Code provenance

The feature was inspired by the interactive documentation graph concept in
[develmusa/mkdocs-network-graph-plugin](https://github.com/develmusa/mkdocs-network-graph-plugin)
(MIT license). This repository does **not** install that plugin or copy/adapt its
source code. The build hook, SVG layout, interactions and styles are an independent
implementation for this wiki's navigation-first structure. They use MkDocs' public
hook API, the Python standard library and native browser APIs; no third-party
visualization code is bundled.

Graph regression checks: `python3 -m unittest discover -s tests`.
