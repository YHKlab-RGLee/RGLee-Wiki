---
name: assess-wiki-article
description: Independently assess a final scientific wiki article against the existing full or outline rubric and return an evidence-backed assessment. Use for the assessment stage of evaluate-wiki-quality; does not edit articles, register reviews, or run final builds.
---

# Assess Wiki Article

Read `AGENTS.md`, `refs/quality/README.md`, and `refs/quality/rubric.yaml`; for science, follow `refs/format.md` and `refs/research-workflow.md`. Preserve all existing criteria and gates. Follow `refs/subagent-execution.md` for independent review inputs and handoff.

1. Read the supplied final article and necessary prerequisites. Form initial findings without the author's conversation, rationale, self-assessment, prior scores, or other reviewers' verdicts. For whole-document review, read the complete body; full review covers every criterion. Do not search the registry/evidence for past scores as a shortcut.
2. Read H1–H3 alone and compare with the body: concise noun phrases must reveal scope, classification, dependencies, and progressive logic. In full review, verify that the article and each major section give the governing concept, relation, or equation before details.
3. Use the coordinator's required scope, based on `quality.sh report`; do not downgrade it. For pending full reviews run `./quality.sh benchmark <page>` before filling the rubric. Unsynchronized drafts can be measured, but cannot be registered. Coverage failure requires useful explanatory improvements, not filler. Navigation/presentation work does not acquire a scientific review requirement through this skill.
4. Fill the existing `refs/quality/assessment-template.yaml` or `outline-assessment-template.yaml` in the assigned experiment directory. Give concrete locations, evidence, and reasons for ratings; neither polish, effort, previous approval nor passing metrics establishes quality. Apply every compliance and forced-revise rule. Report unassessed criteria instead of assuming maximum scores.
5. After recording initial findings, reconcile the independent reference report and applicable prior evidence if needed. Unchanged valid evidence may be reused only with matching scope and provenance. Another agent's summary is not personally inspected evidence. Directly check sources when required by the existing research rules; unresolved support or convention conflicts prevent pass.
6. Record only checks actually run on this version. Missing build/check evidence remains incomplete under the existing template. The coordinator supplies real results, after which the assessment can be completed. Return reviewed SHA-256, findings, assessment path, actual checks and unresolved dependencies. For delegated reviews put version metadata in a separate temporary handoff file, not new assessment fields.

Do not modify articles, synchronize, register, or run final builds. Return corrections to the coordinator. Recheck the reviewed version before delivery and reassess affected findings after revisions. A completed draft is not publication approval. Keep unverifiable assessor model fields blank; never replace them with the registering agent's model.
