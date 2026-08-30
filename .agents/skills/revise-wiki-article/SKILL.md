---
name: revise-wiki-article
description: Revise a bounded part of an existing scientific wiki article while rechecking only affected claims, equations, conventions, and citations. Use for corrections, focused expansions, or localized scientific updates. Use research-and-write-wiki for a new article or a substantial rewrite.
---

# Revise Wiki Article

Preserve unaffected prose and evidence. Read the target page, `refs/format.md`, `refs/research-workflow.md`, and the current diff before deciding the verification scope.

## Workflow

1. State the exact paragraphs, claims, equations, figures, or references in scope.
2. Inspect at least two independent authoritative sources for each changed nontrivial claim. Reuse an existing citation only after directly confirming that it supports the revised wording and remains independent from the other evidence.
3. Reconcile terminology, symbols, units, signs, coordinates, and approximation limits with the unchanged article.
4. Edit only the affected section and necessary transitions, references, links, or captions.
5. Use `$evaluate-wiki-quality`. Scientific prose, equation, number, code-behavior, or citation changes require `full` review; heading-only logic changes require `outline` review.

Do not re-research or rewrite unaffected sections merely to make the page stylistically uniform.
