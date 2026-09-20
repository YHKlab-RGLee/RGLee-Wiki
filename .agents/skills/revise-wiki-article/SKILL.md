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
5. Use `$evaluate-wiki-quality`. Scientific prose, equation, number, code-behavior, or citation changes require `full` review; heading-only logic changes require `outline` review.

Do not re-research or rewrite unaffected sections merely to make the page stylistically uniform.

## Independent review handoff

In the project's three-agent execution, this skill owns revision and its source verification, not final self-assessment. Return the final article to the main agent, which continues the required `evaluate-wiki-quality` workflow with independent reference and quality reviewers under `refs/subagent-execution.md`. Correct returned findings within scope; handoff does not remove any review or publication gate.
