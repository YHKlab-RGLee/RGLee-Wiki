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
| Presentation | H1, description, path, index text, internal link | Use `$maintain-wiki-structure`; synchronize derived quality metadata without invalidating scientific review. |
| Outline | H2/H3 title or logical order, unchanged scientific paragraphs | Use `$evaluate-wiki-quality` with `outline` review when required. |
| Scientific | Prose, equation, number, code behavior, figure meaning, citation | Use `$revise-wiki-article` for a bounded edit or `$research-and-write-wiki` for a new/substantially rewritten article, then a `full` review. |
| Reference audit | Claim support, source independence, link or version freshness | Use `$audit-wiki-references`; do not edit unless correction was requested. |

If no file under `docs/` changes, do not run `quality.sh sync`. A check or report must never modify files.

## Canonical instructions

Keep detailed rules in one place instead of copying them into skills or workflow files.

- Article format, language, headings, equations, figures, citations: `refs/format.md`
- Research and evidence verification: `refs/research-workflow.md`
- Quality state and commands: `refs/quality/README.md`
- Quality gates: `refs/quality/rubric.yaml`
- Task-specific procedure: the selected `.agents/skills/<name>/SKILL.md`

When a general article-format rule changes, update `refs/format.md`. Apply it only to new pages and pages explicitly in scope.

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

- A new or scientifically revised article must pass the quantitative coverage gate in `refs/quality/rubric.yaml`; character count and genuinely useful figures, tables, display equations, and code blocks are quality guardrails against under-explanation.
- Every nontrivial scientific claim must be supported by at least two independent, directly inspected sources that agree on the relevant meaning, scope, and assumptions.
- Never invent references, passages, equations, numerical values, experimental results, quotations, or software behavior.
- A core equation must define its symbols and conventions and explain its meaning, assumptions, approximation level, and validity range.
- Unresolved source conflicts, unsupported claims, incorrect equations, and inconsistent symbols, signs, units, dimensions, coordinates, or normalization force `revise`.
- A document may pass only after the atomic review, publication-compliance gates, automatic checks, and strict build all pass.

## Evidence

Model knowledge is a consistency screen, not a source. For a new or changed nontrivial scientific claim:

1. Inspect the supporting passage, equation, table, figure, or official documentation directly.
2. Check that the source supports the same scope and assumptions as the prose.
3. Use independent provenance rather than multiple mirrors of one source.
4. Reconcile terminology, symbols, units, signs, coordinates, and normalization.
5. Omit or explicitly qualify unresolved claims.

Use at least two independent sources for every nontrivial scientific claim. For consequential, disputed, numerical, convention-sensitive, or central claims, add further independent evidence when two sources do not resolve uncertainty. Preserve disagreements rather than manufacturing consensus.

Keep bibliography titles, author names, publication names, and identifiers in their original language. Put citations immediately after the supported claim.

## Figures

Do not generate new scientific figures. Use `$acquire-scientific-images` for sourced diagrams, plots, measurement curves, screenshots, or other scientific visuals.

Every copied or adapted figure needs descriptive Korean alt text and caption, author, original work and figure/page identifier, stable URL or DOI, reuse license, and modification status. Do not hotlink external image files. If reuse permission is unclear, link to the source instead of copying the asset.

## Experiment workspace

Use root-level `experiment/` exclusively for temporary builds, exploratory scripts, raw outputs, intermediate files, and drafts. Keep it ignored. Promote only reviewed, publication-ready artifacts to `docs/`, together with durable provenance and a reproducible method.

## Quality workflow

`refs/quality/documents.yaml` stores current derived metadata and compact review attestations. Git provides history.

- Navigation-only: run `./build.sh nav`; it checks navigation and strict build only.
- Any `docs/` change: finish the edit, inspect the diff, then run `./quality.sh sync` once.
- Presentation-only changes must preserve article `pass` reviews.
- New or scientifically changed articles require the review scope reported by `./quality.sh report`.
- Record a review with `./quality.sh review <page> --assessment <temporary-yaml>`.
- For a scoped `docs/` task, finish with `./build.sh changed` and `git diff --check`. Use `./build.sh build` for the whole-wiki publication gate and CI.

For a `full` review, the article must reach the rubric's automatically calculated peer baseline for both character count and explanatory-element count. This gate applies only to new or scientifically changed articles, never to navigation, presentation, or outline-only work. Do not add filler or decorative elements: anything added to meet coverage must perform a necessary explanatory role.

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
