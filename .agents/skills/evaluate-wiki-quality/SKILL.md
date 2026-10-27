---
name: evaluate-wiki-quality
description: Coordinate factual verification, preserve valid evidence across meaning-preserving edits, register scoped findings, and run publication checks for this MkDocs wiki. No editorial scoring or minimum-length gate.
---

# Evaluate Wiki Quality

The main agent owns synchronization, registration and final validation. Read `refs/quality/README.md` once for the canonical scope, schema, legacy transition and commands. Use `AGENTS.md` for task context bounds.

1. For existing articles run `./quality.sh baseline <page>` and compare against the last verified version, including already committed changes. Identify changed claims and affected assumptions/conclusions. New articles or unrecoverable baselines need full claim coverage, not a full editorial assessment.
2. Finish the authorized docs edits and inspect the diff. Sync the completed paths once. For a verified meaning-preserving change use `--non-scientific` (alias `--polish`) to carry prior evidence; otherwise require facts. Do not sync for reports or tooling-only work.
3. Assign one independent `wiki_references` reviewer using `audit-wiki-references`, following `refs/subagent-execution.md`. Supply final article, baseline and neutral scope; no author verdict. Default to changed claims plus dependencies and reuse applicable evidence. Do not add a second quality assessor or an editorial rubric.
4. Resolve factual findings only within authorized edit scope. On review-only tasks report errors without editing. Distinguish mismatch from insufficient or inaccessible evidence. If the article changes, verify the changed and dependent findings against the new SHA.
5. Register the matching facts assessment with `./quality.sh review <page> --assessment <file>`. Do not override the independent verdict or accept an unsupported pass. Registration validates structure and hashes, not scientific truth.
6. Run the scoped final build and `git diff --check`; use `./build.sh build` for whole-wiki publication. Render failures do not require repeating source review. Report scope, verified/reused/unverified evidence and actual check results without a quality score.

For tooling changes run regression tests and one read-only whole-wiki publication gate; leave article metadata and historical evidence untouched. Read-only checks and reports must never write. Editorial feedback uses `assess-wiki-article` only when requested and is not a publication gate.
