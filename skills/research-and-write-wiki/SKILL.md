---
name: research-and-write-wiki
description: Research an advanced scientific or computational topic on the internet, reconcile model knowledge with multiple independent references, enforce one consistent scientific convention, and create or substantially revise a verified Korean MkDocs article in this repository. Use for requests to investigate, document, expand, or update technical wiki content under Device physics, Solid-state physics, or Computational science.
---

# Research and Write Wiki

Create only source-grounded wiki content. Treat internal knowledge as a consistency check, never as a reference.

## Required context

Before acting, read `AGENTS.md`, `refs/format.md`, `refs/research-workflow.md`, and `refs/writing-benchmarks/README.md` completely. Check the existing source tree and `mkdocs.yml`.

## Workflow

1. Restate the requested topic as a bounded research question. Identify the correct fixed domain and any needed prerequisite concepts.
2. Search broadly enough to locate primary papers, authoritative reviews or textbooks, and official documentation where relevant.
3. Open and inspect the relevant passages. Do not treat search snippets, copied citations, or abstracts without supporting detail as evidence.
4. Build a claim ledger before drafting. For each nontrivial claim, record its scope, assumptions, supporting passages, and source provenance.
5. Require agreement between internal scientific knowledge and at least two independent sources. Prefer three sources for disputed, consequential, numerical, or convention-sensitive claims.
6. Treat mirrors, versions of one paper, and downstream summaries of one original result as one source. If independence or agreement is unclear, investigate further.
7. Choose one terminology, notation, unit, sign, coordinate, and normalization convention. Map differing source conventions to it before comparing claims.
8. Omit unresolved claims. If disagreement itself is important, describe it as a disagreement with citations and scope; do not manufacture consensus.
9. Draft explanatory prose in Korean using `refs/format.md`. Retain conventional English only for the limited set of representative scientific terms and stable labels whose translation would reduce identification or precision; translate ordinary descriptive vocabulary and sentence functions into Korean. Apply sentence-case capitalization when an English expression begins a Korean sentence, without converting the full expression to title case or altering conventional forms such as `nMOS` and `p-type`. Attach a multi-source citation cluster to each nontrivial claim and preserve original bibliographic titles.
10. At the completion stage, read the closest example under `refs/writing-benchmarks/high/`. Compare whether the draft reaches a similar quantitative, qualitative, and formatting level for its own scope, and revise clear shortcomings. Do not mechanically match length or counts of sections, equations, figures, or references.
11. Add `status: verified` and navigation only after all acceptance checks pass.
12. Check internal links, equations, references, source URLs, terminology, and conventions. Run `./build.sh build`.
13. Briefly report the example used and whether the draft reached a similar quantitative, qualitative, and formatting level.
14. Append a concise entry to the proven-method log in `refs/research-workflow.md` only when the completed task demonstrates that a reusable method improved correctness, coverage, or efficiency.

## Claim ledger

Keep the ledger in working notes unless the user requests publication. Use one row per atomic claim:

| Field | Record |
| --- | --- |
| Claim | One testable statement |
| Scope | Conditions, approximation, and exclusions |
| Sources | At least two independent sources and relevant locations |
| Knowledge check | Consistent, uncertain, or conflicting |
| Convention check | Symbols, units, signs, coordinates, normalization |
| Decision | Publish, investigate, describe disagreement, or omit |

## Stop conditions

Do not publish when fewer than two independent sources support a nontrivial claim, relevant source text cannot be inspected, conventions cannot be reconciled, or a material conflict remains unresolved. Report what is missing and keep the page out of navigation.
