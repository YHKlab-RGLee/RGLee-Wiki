---
name: evaluate-wiki-quality
description: Run deterministic checks, classify Markdown changes, preserve valid scientific reviews across presentation-only edits, and record compact full or outline review attestations for this MkDocs wiki. Use for docs changes, publication readiness, or wiki quality audits.
---

# Evaluate Wiki Quality

Separate mechanical validity from scientific judgment. Read `refs/quality/README.md` and the changed page. For a `full` or `outline` review, also read `refs/quality/rubric.yaml`; for scientific content, follow `refs/format.md` and `refs/research-workflow.md`.

## Route by change

- Navigation-only: do not run `sync`; run `./build.sh nav`, which performs navigation-specific checks and a strict build without reading article review state.
- Presentation-only: H1, description, path, index text, or links may change without altering claims. Run `sync`; existing review must remain valid.
- Outline: when normalized H2·H3 logic changes but scientific paragraphs do not, record an `outline` review.
- Full: new pages or changes to prose, equations, numerical values, code behavior, or citations require a `full` review.

## Workflow

1. Finish the intended edits and inspect the diff.
2. For a `full` or `outline` review, read H1–H3 without the body and verify that concise noun-phrase headings alone reveal the scope, consistent classification, dependency order, and progressive logic. For a `full` review, also verify that the document and each major section expose the governing concept, relation, or equation before details.
3. If `docs/` changed, run `./quality.sh sync` once.
4. Run `./quality.sh report` and identify only articles in `pending` or `revise`.
5. For a pending `full` article, run `./quality.sh benchmark <page>` before spending context on the checklist. It automatically compares coverage with current passed peers; no manual reference selection is required. If it fails, add only necessary explanation, synchronize once, and rerun the benchmark.
6. Use `refs/quality/assessment-template.yaml` for `full` or `refs/quality/outline-assessment-template.yaml` for `outline`. Fill a temporary copy with concrete evidence and record it with `./quality.sh review <page> --assessment <file>`.
7. Run `./build.sh changed` and `git diff --check`. Use `./build.sh build` only for a whole-wiki publication gate.

Do not manufacture evidence to obtain `pass`. A `full` review must meet both quantitative coverage thresholds, but filler and decorative elements are failures of explanatory quality. Forced-revise and publication-compliance rules cannot be offset by scores. `check` and `report` are read-only; use `sync` only when intentionally updating derived state.
