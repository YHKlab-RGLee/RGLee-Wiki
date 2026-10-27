# AGENTS.md

## Project invariants

This repository is a Korean scientific reference wiki built with MkDocs and Material for MkDocs. Its fixed scientific domains, in order, are:

1. Device physics
2. Material science
3. Computational science

Do not rename, reorder, merge, remove, or nest these domains without the project owner's explicit request. `Home` may precede them. `Research Note` may follow them as a non-scientific support section for reproducible research procedures; it is not a fourth scientific domain.

Keep the site readable on desktop and mobile. Modify only the requested content and the smallest dependent surface.

## Classify the change first

| Change class | Examples | Required route |
| --- | --- | --- |
| Navigation | Menu label or order in `mkdocs.yml` | Edit only `mkdocs.yml`; run `./build.sh nav`. |
| Presentation | H1, description, path, index text, internal link | Use `$maintain-wiki-structure`; confirm unchanged meaning and carry evidence with `sync --non-scientific`. |
| Outline | H2/H3 title or logical order, unchanged scientific paragraphs | Confirm unchanged meaning; use `sync --non-scientific`. Editorial review is optional and advisory. |
| Polish | Meaning-preserving prose, terminology or heading wording | Use `$polish-wiki-korean`; carry forward existing review with `sync --polish`. |
| Scientific | Changed claims, equations, numbers, code behavior, figure meaning, citations | Use `$revise-wiki-article` for a bounded edit or `$research-and-write-wiki` for a new/substantially rewritten article, then scoped independent factual verification. |
| Reference audit | Claim support, source independence, link or version freshness | Use `$audit-wiki-references`; do not edit unless correction was requested. |

Do not run `quality.sh sync` for checks, reports, or tooling/instruction-only changes. Synchronizing stale records for already committed document changes is allowed when requested. A check or report must never modify files.

## Canonical instructions

### Task-scoped context and validation

Optimize quality, context cost, and maintainability together. Load this file and the selected skill once per task; reread only when they change or a new dependency appears. Do not load every skill, every article, or the entire quality registry by default. Detailed rules remain in the canonical files below.

| Task | Context to inspect |
| --- | --- |
| Navigation/presentation | Relevant nav entries, metadata, indexes and affected links |
| Outline | Complete heading list, affected sections and transitions |
| Bounded science edit | Changed claims and source passages, their definitions, assumptions and dependent conclusions |
| New article/substantial rewrite | Full writing and research rules, relevant prerequisites and topic navigation |
| Quality tooling | Checker, applicable policy, regression tests; article samples only as needed |

Expand the scope when symbols, assumptions or conclusions depend on material outside the initial selection. Reuse recorded evidence for unchanged claims only when its scope and provenance still apply. Compare with the last verified version, not only the latest commit. Verify changed claims and affected assumptions/conclusions; a new article requires all claims. Editorial structure and prose advice are optional and do not gate publication.

Use programs for repository-wide scans and read their scoped results. Prefer `./quality.sh report --changed` or explicit page paths to dumping `documents.yaml`. The primary workflow owns final validation: supporting skills must not repeat the same build. For tooling changes, run regression tests and one full read-only publication gate. Do not synchronize article metadata for tooling-only work; committed document changes may still require their requested record refresh.

Keep detailed rules in one place instead of copying them into skills or workflow files.

- Article format, language, headings, equations, figures, citations: `refs/format.md`
- Research and evidence verification: `refs/research-workflow.md`
- Quality state and commands: `refs/quality/README.md`
- Quality gates: `refs/quality/rubric.yaml`
- Task-specific procedure: the selected `.agents/skills/<name>/SKILL.md`

When a general article-format rule changes, update `refs/format.md`. Apply it only to new pages and pages explicitly in scope.

## Independent review agents

Use one independent `wiki_references` reviewer for scientific changes; the main agent or `wiki_revision` writes. Follow `refs/subagent-execution.md` for isolated reviewer inputs, one-document/one-role ownership, and compact handoff. Main owns `evaluate-wiki-quality`, registry writes and final validation. Do not replace independent factual verification with the author's self-evaluation. `wiki_quality`/`assess-wiki-article` provides optional editorial advice only when requested, without scores or publication blocking. Additional factual reviewers are for unresolved conflicts or explicit user requests, not the default path. Navigation, meaning-preserving edits and tooling work do not require scientific review agents.

## Source structure

```text
docs/
├── index.md
├── device-physics/
├── computational-materials-science/
├── computational-science/
├── research/                 # optional Research Note support section
└── assets/
```

Use lowercase kebab-case English paths. Classify every scientific article under one fixed domain and one meaningful topic-group directory. Do not add empty or hypothetical topic groups.

An `index.md` is a navigation hub, not a scientific article. Every published topic group must have an `index.md` registered as its first `mkdocs.yml` child so the topic-group label is consistently selectable. The index must list every published page in that group; add, move, rename, or remove a child page and its index entry in the same change. Document-list entries in an index contain only the linked title, without per-page summaries. A scientific `Overview` article is separate from this navigation hub and may coexist with it.

Store page-specific images under the nearest topic `images/` directory. Use `docs/assets/images/` only for assets reused across domains.

## Titles, metadata, headings, and navigation

The page H1 is the single canonical article title. Article front matter contains only a concise Korean `description` unless a new field has a demonstrated consumer.

```yaml
---
description: 문서의 범위와 목적을 설명하는 한 문장
---
```

- Use a stable, number-free H1 such as `# MOSFET: Basic operation`.
- Use numbered H2 headings: `## 1. 기준 모형`.
- Use parenthesized H3 headings: `### (1) 적용 조건`.
- Do not use H4 or deeper headings.
- Keep navigation labels and domain-index links number-free. YAML list order is the only navigation order source.
- Use exactly one topic-group level below a scientific domain.
- Keep fixed domain labels exactly as listed above.
- Add every published Markdown page to `mkdocs.yml` exactly once.
- Use concise sentence-case English navigation labels; preserve conventional acronyms and proper names.

For a move or rename, update the affected nav entry, index links, internal links, and page-specific image paths. Do not alter scientific prose merely to mirror a path or menu change.

## Scientific writing

Write explanatory prose, definitions, captions, summaries, and ordinary table text primarily in Korean technical declarative style (`~이다`, `~한다`). Keep conventional English names for central methods, phenomena, models, software, abbreviations, symbols, and searchable technical labels. Translate ordinary descriptive vocabulary and sentence functions naturally.

Expand an abbreviation at first body use as `full English name (ABBR.)`. Preserve commands, code identifiers, filenames, equations, variable names, software names, and bibliography text in their original language.

Before drafting or substantially restructuring an article, design the dependency order from definition and baseline model through physical origin, governing relation, application or measurement, limitations, and summary. Link an existing prerequisite instead of duplicating it.

Introduce variables before use, distinguish exact relations from approximations, state assumptions and validity ranges, and explain the physical or computational meaning of important equations. Mark inference as inference.

The following are non-delegable publication invariants. Skills may explain how to satisfy them but may not weaken or replace them.

- Publication uses factual findings and automatic checks, not editorial scores, character-count thresholds or peer-average element counts.
- Every nontrivial scientific claim must be supported by at least two independent, directly inspected sources that agree on the relevant meaning, scope, and assumptions.
- Never invent references, passages, equations, numerical values, experimental results, quotations, or software behavior.
- A core equation must define its symbols and conventions and explain its meaning, assumptions, approximation level, and validity range.
- Confirmed source/claim conflicts, incorrect equations and inconsistent conventions force `revise`. Missing evidence or inaccessible sources produce `unverified`; both states block publication.
- New/changed claims must have resolved factual findings; current automatic checks and strict build must pass before publication. Distinguish confirmed errors from missing evidence or inaccessible sources. Preserve old reviews as historical evidence, not newly verified claims.

## Evidence

Model knowledge is a consistency screen, not a source. For a new or changed nontrivial scientific claim:

1. Inspect the supporting passage, equation, table, figure, or official documentation directly.
2. Check that the source supports the same scope and assumptions as the prose.
3. Use independent provenance rather than multiple mirrors of one source.
4. Reconcile terminology, symbols, units, signs, coordinates, and normalization.
5. Omit or explicitly qualify unresolved claims.

Use at least two independent sources for every nontrivial scientific claim. For consequential, disputed, numerical, convention-sensitive, or central claims, add further independent evidence when two sources do not resolve uncertainty. Preserve disagreements rather than manufacturing consensus.

For derived formulas and numerical examples, verify the source-supported premises and record a reproducible derivation or calculation; two sources need not print the identical illustrative example. Keep bibliography titles, author names, publication names, and identifiers in their original language. Put citations immediately after the supported claim.

## Figures

Do not generate new scientific figures. Use `$acquire-scientific-images` for sourced diagrams, plots, measurement curves, screenshots, or other scientific visuals.

Every copied or adapted figure needs descriptive Korean alt text and caption, author, original work and figure/page identifier, stable URL or DOI, reuse license, and modification status. Do not hotlink external image files. If reuse permission is unclear, link to the source instead of copying the asset.

## Experiment workspace

Use root-level `experiment/` exclusively for temporary builds, exploratory scripts, raw outputs, intermediate files, and drafts. Keep it ignored. Promote only reviewed, publication-ready artifacts to `docs/`, together with durable provenance and a reproducible method.

## Quality workflow

`refs/quality/documents.yaml` stores current derived metadata and compact review attestations. Git provides history.

- Navigation-only: run `./build.sh nav`; it checks navigation and strict build only.
- Any `docs/` change: finish the edit, inspect the diff, then run `./quality.sh sync <completed-page> ...` once for the completed scope. See `refs/quality/README.md` for moves, deletions, and whole-wiki synchronization.
- Confirm meaning preservation for presentation, heading/order or polish changes and use `sync --non-scientific` (`--polish` alias) to carry valid evidence. Do not automatically exempt claims in headings, descriptions or figures.
- New articles require full claim coverage; changed articles require changed claims and affected dependencies from `./quality.sh baseline <page>`. Record explicit reused evidence and scope.
- Record a review with `./quality.sh review <page> --assessment <temporary-yaml>`.
- For a scoped `docs/` task, finish with `./build.sh changed` and `git diff --check`. Use `./build.sh build` for the whole-wiki publication gate and CI.

Use `refs/quality/README.md` for the factual record schema, historical-review compatibility and commands. The checker validates record structure, hashes and declared source counts; it does not automatically prove scientific truth or complete claim coverage.

## Build, dependencies, and publication

Use:

```bash
./build.sh serve
./build.sh build
./build.sh preflight
```

`build` performs the read-only quality gate and strict MkDocs build. `preflight` additionally checks the diff and prints the pending files; it does not stage, commit, or push. Commit and push explicitly with Git after reviewing the intended scope.

Keep `mkdocs.yml` minimal and valid. Prefer Material and supported Markdown features over custom HTML, JavaScript, or CSS. Keep light/dark schemes and mobile readability.

Add a dependency only when required. Pin build dependencies sufficiently for reproducible CI and document intentional upgrades.

## Scope and safety

Preserve unrelated user changes in a dirty worktree. Do not apply repository-wide cleanup as a side effect of a local request. After editing, inspect the diff and reduce it if it exceeds the intended surface.

Do not commit generated `site/`, caches, virtual environments, or `experiment/`. Avoid destructive Git operations. Before completion, report changed files, validation results, and any unresolved limitation.
