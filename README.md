# Research-Oriented Science and Computing Wiki

This repository contains a personal scientific wiki for advanced topics selected
by the researcher. Each article is based on internet research and includes only
claims that are consistent with scientific knowledge and supported by multiple
independent sources.

Site: [https://yhklab-rglee.github.io/RGLee-Wiki/](https://yhklab-rglee.github.io/RGLee-Wiki/)

The wiki maintains three fixed subject areas:

1. Device Physics
2. Solid-State Physics
3. Computational Science

When creating or revising content, follow `AGENTS.MD`, `refs/format.md`,
`docs/research-workflow.md`, and
`skills/research-and-write-wiki/SKILL.md`. Research and verification methods
shown to be effective in actual content work are recorded in
`docs/research-workflow.md`.

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

The generated site is written to `site/`.

## Publishing

To build the site, commit the current changes, and push the current branch to
its configured upstream:

```bash
./build.sh publish "Describe the changes"
```

This command publishes the source changes to the Git repository. A public
website requires a separate hosting configuration, such as GitHub Pages.
