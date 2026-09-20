---
name: research-and-write-wiki
description: Research an advanced scientific or computational topic on the internet, reconcile model knowledge with multiple independent references, enforce one consistent scientific convention, and create or substantially revise a verified Korean MkDocs article in this repository. Use for requests to investigate, document, expand, or update technical wiki content under Device physics, Material science, or Computational science.
---

# Research and Write Wiki

Create only source-grounded wiki content. Treat internal knowledge as a consistency check, never as a reference.

## Required context

Follow the task-scoped context table in `AGENTS.md`. For new or substantially rewritten articles, read `refs/format.md` and `refs/research-workflow.md` once. Inspect only the relevant source tree and navigation. Load the quality skill at the validation stage; do not preload its implementation or the full registry.

## Workflow

1. Restate the requested topic as a bounded research question. Identify the correct fixed domain and any needed prerequisite concepts.
2. Search broadly enough to locate primary papers, authoritative reviews or textbooks, and official documentation where relevant.
3. Open and inspect the relevant passages. Do not treat search snippets, copied citations, or abstracts without supporting detail as evidence.
4. Build a claim ledger before drafting. For each nontrivial claim, record its scope, assumptions, supporting passages, and source provenance.
5. Require agreement between internal scientific knowledge and at least two independent, directly inspected sources for every nontrivial claim. Add further evidence for disputed, consequential, numerical, convention-sensitive, or central claims when two sources do not resolve uncertainty.
6. Treat mirrors, versions of one paper, and downstream summaries of one original result as one source. If independence or agreement is unclear, investigate further.
7. Choose one terminology, notation, unit, sign, coordinate, and normalization convention. Map differing source conventions to it before comparing claims.
8. Omit unresolved claims. If disagreement itself is important, describe it as a disagreement with citations and scope; do not manufacture consensus.
9. Design the H1–H3 outline before drafting prose. Read the headings alone and revise them until concise noun phrases reveal the scope, dependency order, consistent classification, and progressive logic without help from the body text.
10. Draft in Korean following `refs/format.md`, including its heading, prose, equation, visual-selection and citation rules. Do not duplicate those rules in working notes.
11. After scientific verification passes, add the required domain-index link and navigation. Finish every intended Markdown change before quality synchronization.
12. Use `$evaluate-wiki-quality`: run `./quality.sh sync` once, pass the automatic peer coverage baseline, and record the atomic `full` review for each new or scientifically changed article. Add only material that performs a necessary explanatory role.
13. Complete the scoped validation owned by `$evaluate-wiki-quality`; do not repeat its build. Reserve the full build for explicit whole-wiki publication or CI.
14. Briefly report the review scope and result.
15. Append a concise entry to the proven-method log in `refs/research-workflow.md` only when the completed task demonstrates that a reusable method improved correctness, coverage, or efficiency.

## Claim ledger

Keep draft notes in `experiment/`. Include the verified claim ledger in the full assessment's evidence fields (claim, scope, independent sources and inspected locations); the review command retains that assessment under `refs/quality/evidence/`. Do not archive copyrighted source text or raw browsing output. Use one row per atomic claim:

| Field | Record |
| --- | --- |
| Claim | One testable statement |
| Scope | Conditions, approximation, and exclusions |
| Sources | At least two independent sources and directly inspected locations |
| Knowledge check | Consistent, uncertain, or conflicting |
| Convention check | Symbols, units, signs, coordinates, normalization |
| Decision | Publish, investigate, describe disagreement, or omit |

## Stop conditions

Do not publish when a nontrivial claim lacks two independent directly inspected sources, conventions cannot be reconciled, or a material conflict remains unresolved. Report what is missing and keep the page out of navigation.
