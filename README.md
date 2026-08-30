# RGLee's Wiki

This repository contains a personal wiki that accumulates AI-generated and
AI-organized scientific knowledge. The published site currently focuses on
cross-verified device-physics research documents.

Site: [https://yhklab-rglee.github.io/RGLee-Wiki/](https://yhklab-rglee.github.io/RGLee-Wiki/)

The wiki maintains three fixed subject areas:

1. Device physics
2. Computational materials science
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
