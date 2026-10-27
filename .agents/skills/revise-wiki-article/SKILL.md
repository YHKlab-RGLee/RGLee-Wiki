---
name: revise-wiki-article
description: Revise a bounded part of an existing scientific wiki article while rechecking only affected claims, equations, conventions, and citations. Use for corrections, focused expansions, or localized scientific updates. Use research-and-write-wiki for a new article or a substantial rewrite.
---

# Revise Wiki Article

Preserve unaffected prose and evidence. Read the current diff and follow the task-scoped context table in `AGENTS.md`. Read affected sections, prerequisite definitions and dependent conclusions; consult only the applicable sections of `refs/format.md` and `refs/research-workflow.md`. Expand to the full page when the dependency boundary is unclear.

## Workflow

1. State the exact paragraphs, claims, equations, figures, headings, or references in scope. When headings or order are in scope, read H1–H3 alone and revise the outline until concise noun phrases reveal a consistent, progressive logical structure without body text.
2. Inspect at least two independent authoritative sources for each changed nontrivial claim. Reuse an existing citation only after directly confirming that it supports the revised wording and remains independent from the other evidence.
3. Reconcile terminology, symbols, units, signs, coordinates, and approximation limits with the unchanged article.
4. Edit only the affected section and necessary transitions, references, links, or captions. Within that scope, state the governing concept, relation, or equation before its derivation, cases, procedures, exceptions, and limits.
5. Use `$evaluate-wiki-quality`. Compare against the last verified version and verify changed claims plus dependent assumptions/conclusions. Meaning-preserving heading/order changes carry evidence with `sync --non-scientific`.

Do not re-research or rewrite unaffected sections merely to make the page stylistically uniform.

## Independent review handoff

Return the fixed final version to the main agent for one independent factual reviewer under `refs/subagent-execution.md`. The reviewer returns factual findings, not editorial scores. Correct factual findings within authorized scope; main owns registration and final validation.
