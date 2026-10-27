---
name: audit-wiki-references
description: Independently verify scientific claims, equations, numerical examples, quotations, citations, and source provenance. Use for scoped factual review or an explicit citation audit; does not edit articles or register results.
---

# Audit Wiki References

Follow the factual scope and record schema in `refs/quality/README.md` and evidence rules in `refs/research-workflow.md`. Read each once. Do not load unrelated articles, the whole registry or old scores.

For an existing changed article compare with its last verified version using `quality.sh baseline`, then inspect changed claims plus affected definitions, assumptions and conclusions. A new article or unrecoverable baseline needs full claim coverage. An explicit narrow audit stays narrow and does not become publication approval.

Start from the final article, original sources and neutral assigned scope, not the author's verdict. Record initial findings before reconciling prior evidence. Reuse unchanged valid evidence with explicit scope and provenance; do not represent another reviewer's source inspection as your own.

Inspect original passages, equations, tables or official documentation directly. Check claim support, source identity/independence, assumptions, signs, units, conventions and applicability. Check numerical examples and derived identities from supported premises; record reproducible calculation or derivation instead of searching for identical illustrative numbers in two papers. Check quotations against the original wording and context. Link resolution alone proves neither identity nor support.

Group connected claims when they share premises and evidence. Record `supported`, `mismatch`, `insufficient`, or `inaccessible` with concrete locations and source passages. A source access failure is not a scientific error. Do not add editorial scores, minimum-length demands, or rewrite suggestions unrelated to factual findings.

For publication verification return `assessment-template.yaml` completed with exact article SHA, full/changes coverage, explicit reused evidence, findings and limitations. Keep drafts in the assigned experiment directory. The main agent owns registration and final build. For audit-only requests return findings without modifying the article, registry, dates or build state. Follow `refs/subagent-execution.md` when delegated; do not spawn additional agents.
