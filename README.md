# RGLee's Wiki

This repository contains a personal wiki that accumulates AI-generated and
AI-organized scientific knowledge. The published site currently focuses on
cross-verified device-physics research documents.

Site: [https://yhklab-rglee.github.io/RGLee-Wiki/](https://yhklab-rglee.github.io/RGLee-Wiki/)

The wiki maintains three fixed subject areas:

1. Device physics
2. Solid-state physics
3. Computational science

When creating or revising content, follow `AGENTS.md`, `refs/format.md`,
`refs/research-workflow.md`, and
`.agents/skills/research-and-write-wiki/SKILL.md`. Document quality is measured and
reviewed with `.agents/skills/evaluate-wiki-quality/SKILL.md`; each page's current topic,
scope, metrics, scores, and history are stored in `refs/quality/documents.yaml`. Research and verification methods
shown to be effective in actual content work are recorded in
`refs/research-workflow.md`.

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

Create a strict production build:

```bash
./build.sh build
```

Synchronize quality records after any page is added, edited, moved, restored, or deleted:

```bash
./quality.sh sync
```

Check that every current article has a passing review and every navigation page is synchronized:

```bash
./quality.sh check --all
```

The generated site is written to `site/`.

## Publishing

GitHub Actions builds and deploys the MkDocs site automatically whenever a
commit is pushed to `main`. Configure the repository once under
`Settings > Pages > Build and deployment > Source` by selecting
`GitHub Actions`.

To validate the site, commit the current changes, and push the current branch
to its configured upstream:

```bash
./build.sh publish "Describe the changes"
```

The generated `site/` directory remains local and is not committed. The GitHub
Actions workflow rebuilds it and uploads it directly as a GitHub Pages
artifact.
