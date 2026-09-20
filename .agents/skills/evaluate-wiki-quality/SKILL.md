---
name: evaluate-wiki-quality
description: Run deterministic checks, classify Markdown changes, preserve valid scientific reviews across presentation-only edits, and record compact full or outline review attestations for this MkDocs wiki. Use for docs changes, publication readiness, or wiki quality audits.
---

# Evaluate Wiki Quality

Own the existing quality workflow. Read `refs/quality/README.md` and follow the context bounds in `AGENTS.md`. The scientific assessment procedure is at `.agents/skills/assess-wiki-article/SKILL.md`; synchronization, registration, and final validation remain here. Existing callers still use this entrypoint. In delegated execution the main agent runs this skill and the independent quality agent performs assessment, following `refs/subagent-execution.md`.

## Route by change

- Navigation-only: no sync; run `./build.sh nav` for navigation and strict build.
- Presentation-only: synchronize finished docs changes and preserve valid scientific review.
- Outline: changed normalized H2/H3 logic with unchanged science requires outline review when reported.
- Full: new articles or changed prose, equations, numbers, code behavior, figure meaning, or citations require full review.

## Workflow

1. Finish intended edits and inspect the diff. Perform the existing heading/body readiness check: H1–H3 should expose a progressive logical structure; in full review each major section introduces the governing concept or relation before details. This is editing preflight, not the independent assessment.
2. If docs changed, run `./quality.sh sync <completed-page> ...` once for the completed edit batch; include both old and new paths for moves. Use argument-free sync only for an intentional whole-wiki synchronization, following `refs/quality/README.md`. Never sync for a read-only report or when docs is unchanged. Read `./quality.sh report --changed` or explicit paths and retain the required scope.
3. For required full/outline review use `$assess-wiki-article`. It retains the existing templates, complete rubric, source requirements, and full-review benchmark. Apply the independent-input rules in `refs/subagent-execution.md`. For this configured independent workflow use a fresh assessor; inability to delegate must be reported, not silently treated as independent review.
4. Resolve findings through the appropriate original editing skill. If content changes, inspect the new diff, synchronize after edits, and reassess affected claims and dependent conclusions. Do not manufacture evidence, add filler, downgrade full to outline, or replace a reviewer's failure with an unsupported pass.
5. Obtain actual automatic-check and strict-render evidence for the reviewed version before completing compliance. If pending reviews prevent the publication gate from reaching MkDocs, the main agent can run `python3 -m mkdocs build --strict --clean --site-dir experiment/<task>/site` using the project's build environment. This is rendering evidence, not a publication pass. Supply results and the synchronized automatic-check state to the assessor; unresolved failures remain failures. This avoids requiring a registered pass merely to obtain strict-render evidence.
6. Check the returned page hash and scope against the current version, then record the completed assessment with `./quality.sh review <page> --assessment <file>`. The unchanged command enforces coverage and stores durable evidence. Serialize registry writes; retain the actual assessor's verified model information or blanks.
7. Finish the scoped docs task with `./build.sh changed` and `git diff --check`; use `./build.sh build` for the whole-wiki publication gate. This final gate remains required even if standalone rendering was necessary before registration. Calling skills and subagents must not duplicate the final gate. No publication-readiness claim until assessment, compliance, automatic checks, and strict build all pass.

For checker changes, run regression tests and one full read-only publication gate. Do not sync when docs is untouched. `check`, `report`, and `benchmark` remain read-only. A standalone assessment request does not authorize edits or registration. The rubric, thresholds, classification, scientific-review preservation, CLI, and evidence schema are unchanged.
