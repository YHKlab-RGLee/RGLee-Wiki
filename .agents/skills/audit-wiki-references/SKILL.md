---
name: audit-wiki-references
description: Audit existing wiki references for broken links, bibliographic identity, claim support, source independence, and freshness. Use for explicit citation audits or periodic maintenance, not as an automatic side effect of ordinary prose edits.
---

# Audit Wiki References

Audit references without changing scientific conclusions unless the user also requests revision. Read the target pages and `refs/research-workflow.md`.

## Workflow

1. Select the requested pages or the smallest risk-based sample. Prioritize current software behavior, numerical claims, standards, and time-sensitive documentation.
2. Open each cited source at the supporting passage. Confirm bibliographic identity, claim scope, assumptions, and whether nominally different URLs share one provenance.
3. Record broken links, unsupported claims, stale version-dependent statements, convention conflicts, and missing independent support.
4. Report findings before editing when the request is audit-only. If correction is requested, use `$revise-wiki-article` for affected claims.
5. For changed pages, use `$evaluate-wiki-quality` and the review scope determined by the actual content diff.

Do not update a verification date solely because a URL still resolves.
