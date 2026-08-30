---
name: research-and-write-wiki
description: Research an advanced scientific or computational topic on the internet, reconcile model knowledge with multiple independent references, enforce one consistent scientific convention, and create or substantially revise a verified Korean MkDocs article in this repository. Use for requests to investigate, document, expand, or update technical wiki content under Device physics, Material science, or Computational science.
---

# Research and Write Wiki

Create only source-grounded wiki content. Treat internal knowledge as a consistency check, never as a reference.

## Required context

Before acting, read `AGENTS.md`, `refs/format.md`, `refs/research-workflow.md`, `refs/quality/README.md`, and `.agents/skills/evaluate-wiki-quality/SKILL.md` completely. Check the existing source tree and `mkdocs.yml`.

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
10. Draft explanatory prose in Korean using `refs/format.md`. Lead the document and each major section with the governing concept, model, relation, or equation and its meaning, then unfold derivation, terms, cases, procedures, exceptions, and limits in subsections. Retain conventional English only for the limited set of representative scientific terms and stable labels whose translation would reduce identification or precision; translate ordinary descriptive vocabulary and sentence functions into Korean. Apply sentence-case capitalization when an English expression begins a Korean sentence, without converting the full expression to title case or altering conventional forms such as `nMOS` and `p-type`. Attach a multi-source citation cluster to each nontrivial claim and preserve original bibliographic titles.
11. After scientific verification passes, add the required domain-index link and navigation. Finish every intended Markdown change before quality synchronization.
12. Use `$evaluate-wiki-quality`: run `./quality.sh sync` once, pass the automatic peer coverage baseline, and record the atomic `full` review for each new or scientifically changed article. Add only material that performs a necessary explanatory role.
13. Check internal links, equations, references, source URLs, terminology, and conventions. Run `./quality.sh check --all`, then `./build.sh build`.
14. Briefly report the review scope and result.
15. Append a concise entry to the proven-method log in `refs/research-workflow.md` only when the completed task demonstrates that a reusable method improved correctness, coverage, or efficiency.

## Claim ledger

Keep the ledger in working notes unless the user requests publication. Use one row per atomic claim:

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
