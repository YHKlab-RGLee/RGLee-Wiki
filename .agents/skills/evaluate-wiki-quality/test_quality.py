from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).with_name("scripts") / "quality.py"
SPEC = importlib.util.spec_from_file_location("wiki_quality", SCRIPT)
assert SPEC and SPEC.loader
quality = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(quality)


class QualityHashTests(unittest.TestCase):
    def test_inline_math_does_not_swallow_intervening_prose(self) -> None:
        before = "$G^<$\n\n점유와 전류를 설명한다.\n\n$G^>$"
        pieces = ["$G^<$", "점유와 전류를 설명한다.", "$G^>$"]
        self.assertEqual(
            quality.visible_character_count(before),
            sum(quality.visible_character_count(part) for part in pieces),
        )

    def test_html_tags_are_removed_but_math_is_preserved(self) -> None:
        plain = "상태 $E<0$와 $G^>$를 비교한다."
        html = "<span>상태 $E<0$와 $G^>$를 비교한다.</span>"
        self.assertEqual(
            quality.visible_character_count(plain),
            quality.visible_character_count(html),
        )

    def test_h1_and_front_matter_do_not_change_scientific_content(self) -> None:
        first = "---\ntitle: Old\n---\n# 1.1. Old\n\n같은 과학 본문이다.\n"
        second = "---\ndescription: 범위\n---\n# New\n\n같은 과학 본문이다.\n"
        _, first_body = quality.strip_front_matter(first)
        _, second_body = quality.strip_front_matter(second)
        self.assertEqual(
            quality.hash_text(quality.canonical_content(first_body)),
            quality.hash_text(quality.canonical_content(second_body)),
        )

    def test_display_numbers_do_not_change_outline(self) -> None:
        first = "# Topic\n## 1. 정의\n### (1) 조건\n"
        second = "# Topic\n## 7. 정의\n### (4) 조건\n"
        self.assertEqual(quality.canonical_outline(first), quality.canonical_outline(second))

    def test_scientific_text_change_changes_content_hash(self) -> None:
        first = "# Topic\n\n첫 번째 주장이다.\n"
        second = "# Topic\n\n다른 주장이다.\n"
        self.assertNotEqual(
            quality.hash_text(quality.canonical_content(first)),
            quality.hash_text(quality.canonical_content(second)),
        )

    def test_code_comment_is_scientific_content_not_a_heading(self) -> None:
        first = "# Topic\n```python\n# first behavior\nvalue = 1\n```\n"
        second = "# Topic\n```python\n# changed behavior\nvalue = 1\n```\n"
        self.assertNotEqual(quality.canonical_content(first), quality.canonical_content(second))

    def test_legacy_metadata_and_numbered_h1_are_rejected(self) -> None:
        path = quality.DOCS / "device-physics" / "example.md"
        metadata = {
            "title": "Wrong",
            "description": "범위",
            "status": "draft",
            "last_verified": "not-a-date",
        }
        body = "# 1.1. Different\n\n## 1. 정의\n\n본문이다.\n"
        issues = quality.automatic_issues(path, metadata, body, 0)
        self.assertIn("H1에 navigation 번호가 있다", issues)
        self.assertTrue(any("title" in issue for issue in issues))
        self.assertTrue(any("status" in issue for issue in issues))
        self.assertTrue(any("last_verified" in issue for issue in issues))

    def test_presentation_change_preserves_pass_review(self) -> None:
        previous = {
            "kind": "article",
            "hashes": {"content": "content", "outline": "outline", "presentation": "old"},
            "review": {"status": "pass", "rubric_version": quality.RUBRIC_VERSION},
        }
        measured = {
            "kind": "article",
            "hashes": {"content": "content", "outline": "outline", "presentation": "new"},
        }
        self.assertEqual(quality.preserve_review(previous, measured)["status"], "pass")

    def test_outline_and_content_changes_request_different_scopes(self) -> None:
        previous = {
            "kind": "article",
            "hashes": {"content": "content", "outline": "old"},
            "review": {"status": "pass", "rubric_version": quality.RUBRIC_VERSION},
        }
        outline_change = {
            "kind": "article",
            "hashes": {"content": "content", "outline": "new"},
        }
        content_change = {
            "kind": "article",
            "hashes": {"content": "new-content", "outline": "new"},
        }
        self.assertEqual(
            quality.preserve_review(previous, outline_change)["required_scope"], "outline"
        )
        self.assertEqual(
            quality.preserve_review(previous, content_change)["required_scope"], "full"
        )

    def test_stricter_legacy_pass_is_carried_to_current_rubric(self) -> None:
        previous = {
            "kind": "article",
            "hashes": {"content": "content", "outline": "outline"},
            "review": {
                "status": "pass",
                "rubric_version": 2,
                "migrated_from_legacy": True,
            },
        }
        measured = {
            "kind": "article",
            "hashes": {"content": "content", "outline": "outline"},
        }
        review = quality.preserve_review(previous, measured)
        self.assertEqual(review["status"], "pass")
        self.assertEqual(review["rubric_version"], quality.RUBRIC_VERSION)

    def test_quantitative_comparison_prefers_topic_group_average(self) -> None:
        def record(path: str, group: str, characters: int, elements: int) -> dict:
            return {
                "path": path,
                "kind": "article",
                "group": group,
                "metrics": {
                    "characters": characters,
                    "explanatory_elements": {"total": elements},
                },
                "review": {"status": "pass"},
            }

        target = record("docs/device-physics/mosfet/target.md", "device-physics / mosfet", 800, 4)
        target["review"] = {"status": "pending"}
        registry = {
            "documents": [
                target,
                record("docs/device-physics/mosfet/a.md", target["group"], 1000, 5),
                record("docs/device-physics/mosfet/b.md", target["group"], 1000, 5),
                record("docs/device-physics/other/c.md", "device-physics / other", 10000, 20),
            ]
        }
        result = quality.quantitative_comparison(target, registry)
        self.assertEqual(result["level"], "topic_group")
        self.assertTrue(result["passed"])
        self.assertEqual(result["characters"]["minimum"], 800)

    def test_outline_scope_excludes_scientific_criteria(self) -> None:
        criteria = quality.applicable_criteria("outline")
        self.assertEqual(set(criteria), {"A", "C"})
        self.assertNotIn("A3", criteria["A"])
        self.assertEqual(set(quality.applicable_compliance("outline")), {"D1", "D2", "D6"})


    def test_pending_full_cannot_be_downgraded_by_heading_edit(self) -> None:
        previous = {"kind": "article", "hashes": {"content": "body", "outline": "old"},
                    "review": {"status": "pending", "required_scope": "full"}}
        measured = {"kind": "article", "hashes": {"content": "body", "outline": "new"}}
        self.assertEqual(quality.preserve_review(previous, measured)["required_scope"], "full")

    def test_repeated_sync_keeps_outline_scope(self) -> None:
        previous = {"kind": "article", "hashes": {"content": "body", "outline": "old"},
                    "review": {"status": "pass", "scope": "full", "rubric_version": quality.RUBRIC_VERSION}}
        measured = {"kind": "article", "hashes": {"content": "body", "outline": "new"}}
        first = quality.preserve_review(previous, measured)
        second = quality.preserve_review(dict(measured, review=first), measured)
        self.assertEqual(first["required_scope"], "outline")
        self.assertEqual(second["required_scope"], "outline")

    def test_failed_full_keeps_blockers_after_heading_edit(self) -> None:
        previous = {"kind": "article", "hashes": {"content": "body", "outline": "old"},
                    "review": {"status": "revise", "scope": "full", "forced_revise": ["F3"]}}
        measured = {"kind": "article", "hashes": {"content": "body", "outline": "new"}}
        review = quality.preserve_review(previous, measured)
        self.assertEqual(review["required_scope"], "full")
        self.assertEqual(review["forced_revise"], ["F3"])

    def test_last_pass_survives_repeated_pending_sync(self) -> None:
        previous = {"kind": "article", "hashes": {"content": "body", "outline": "old"},
                    "review": {"status": "pass", "scope": "full", "rubric_version": quality.RUBRIC_VERSION}}
        measured = {"kind": "article", "hashes": {"content": "changed", "outline": "old"}}
        first = quality.preserve_review(previous, measured)
        next_record = dict(measured, review=first)
        second = quality.preserve_review(next_record, measured)
        self.assertEqual(second["last_pass"]["scope"], "full")
        self.assertEqual(second["required_scope"], "full")

    def test_math_and_inline_code_are_not_file_links(self) -> None:
        body = '# Topic\n\n## 1. 정의\n\n$G[a](x)$와 `[sample](missing)`이다.\n\n$$G[b](y)$$\n'
        issues = quality.automatic_issues(quality.DOCS / "example.md", {"description": "범위"}, body, 0)
        self.assertFalse(any("연결 대상" in issue for issue in issues))

    def test_real_missing_link_is_still_rejected(self) -> None:
        issues = quality.automatic_issues(quality.DOCS / "example.md", {"description": "범위"},
                                         '# Topic\n\n[문서](missing-file.md)\n', 0)
        self.assertTrue(any("연결 대상" in issue for issue in issues))

    def test_copy_is_not_classified_as_move(self) -> None:
        from unittest.mock import patch
        previous = {"path": "docs/source.md", "kind": "article", "hashes": {"content": "a", "outline": "b"}}
        with patch.object(Path, "exists", return_value=True):
            self.assertIsNone(quality.find_move_candidate(previous, [previous], set()))

    def run_mock_review(self, previous_review, scope, model=None):
        from argparse import Namespace
        from unittest.mock import patch
        page = quality.DOCS / "device-physics" / "test.md"
        measured = {"path": "docs/device-physics/test.md", "kind": "article",
                    "hashes": {"content": "body", "outline": "new"}, "automatic_check": "pass"}
        record = dict(measured, review=previous_review)
        registry = {"schema_version": quality.SCHEMA_VERSION, "documents": [record]}
        assessment = {"scope": scope, "areas": {"A": {"percent": 100}}, "points": 100,
                      "compliance": {"D1": {"status": "pass"}}, "critical_zero_failures": [],
                      "forced_revise": [], "critical_questions": {}, "summary": "검토 근거"}
        if model is not None:
            assessment["model"] = model
        rubric = quality.rubric_definition()
        with patch.object(quality, "rubric_definition", return_value=rubric), \
             patch.object(quality, "resolve_doc", return_value=page), \
             patch.object(quality, "measure", return_value=measured), \
             patch.object(quality, "load_yaml", return_value=registry), \
             patch.object(quality, "parse_assessment", return_value=assessment), \
             patch.object(quality, "save_yaml") as save, \
             patch.object(Path, "is_file", return_value=True):
            quality.review_document(Namespace(path=str(page), assessment="experiment/assessment.yaml"))
            return record, save.call_args_list

    def test_review_model_roundtrip_and_no_inheritance(self) -> None:
        model = {"name": "example-model", "reasoning_effort": "low", "source": "user_declared"}
        prior = {"status": "pass", "scope": "full", "model": model}
        record, writes = self.run_mock_review(prior, "outline", model)
        self.assertEqual(record["review"]["model"], model)
        self.assertEqual(writes[0].args[1]["assessment"]["model"], model)
        record, _ = self.run_mock_review(prior, "outline")
        self.assertEqual(record["review"]["model"], quality.review_model())
        self.assertEqual(record["review"]["scientific_review"]["model"], model)

    def test_model_survives_sync_and_moves_to_last_pass(self) -> None:
        model = {"name": "example-model", "reasoning_effort": "low", "source": "user_declared"}
        previous = {"kind": "article", "hashes": {"content": "a", "outline": "b"},
                    "review": {"status": "pass", "scope": "full", "model": model,
                               "rubric_version": quality.RUBRIC_VERSION}}
        self.assertEqual(quality.preserve_review(previous, previous)["model"], model)
        measured = dict(previous, hashes={"content": "changed", "outline": "b"})
        result = quality.preserve_review(previous, measured)
        self.assertEqual(result["model"], quality.review_model())
        self.assertEqual(result["last_pass"]["model"], model)

    def test_model_assessment_accepts_missing_blank_and_explicit(self) -> None:
        from unittest.mock import patch
        path = quality.QUALITY_DIR / "outline-assessment-template.yaml"
        original = quality.load_yaml
        assessment = quality.load_yaml(path, {})
        for model in (None, {"name": "example-model", "reasoning_effort": "low", "source": "user_declared"}):
            assessment["model"] = model
            with patch.object(quality, "load_yaml", side_effect=lambda p, default: assessment if p == path else original(p, default)):
                result = quality.parse_assessment(path)
            self.assertEqual(result["model"], quality.review_model(model))
        assessment.pop("model")
        with patch.object(quality, "load_yaml", side_effect=lambda p, default: assessment if p == path else original(p, default)):
            self.assertEqual(quality.parse_assessment(path)["model"], quality.review_model())
        for invalid in ([], "model", {"name": 123}, {"unknown": "value"}):
            with self.assertRaises(SystemExit):
                quality.review_model(invalid)

    def test_outline_review_retains_science_and_durable_evidence(self) -> None:
        prior = {"status": "pass", "scope": "full", "content_hash": "body"}
        record, writes = self.run_mock_review(
            {"status": "pending", "required_scope": "outline", "last_pass": prior}, "outline")
        self.assertEqual(record["review"]["scientific_review"], prior)
        self.assertEqual(len(writes), 2)
        evidence_path, evidence = writes[0].args
        self.assertEqual(evidence_path.parent, quality.QUALITY_DIR / "evidence")
        self.assertEqual(evidence["hashes"]["content"], "body")
        self.assertEqual(evidence["assessment"]["summary"], "검토 근거")
        self.assertEqual(record["review"]["evidence_path"], quality.relative_path(evidence_path))

    def test_outline_cannot_override_failed_full_without_sync(self) -> None:
        with self.assertRaises(SystemExit):
            self.run_mock_review({"status": "revise", "scope": "full", "forced_revise": ["F3"]}, "outline")

    def test_scoped_report_omits_unselected_articles_and_never_writes(self) -> None:
        from unittest.mock import patch
        from contextlib import redirect_stdout
        from io import StringIO
        records = [{"path": "docs/" + name + ".md", "metrics": {"characters": 1,
                    "explanatory_elements": {"total": 0}}, "review": {"status": "pass"}}
                   for name in ["selected", "unrelated"]]
        output = StringIO()
        with patch.object(quality, "load_yaml", return_value={"documents": records}), \
             patch.object(quality, "save_yaml") as save, redirect_stdout(output):
            quality.report([quality.DOCS / "selected.md"])
        self.assertIn("docs/selected.md", output.getvalue())
        self.assertNotIn("docs/unrelated.md", output.getvalue())
        save.assert_not_called()

    def test_benchmark_measures_draft_without_sync_or_writes(self) -> None:
        from unittest.mock import patch
        measured = {"kind": "article", "path": "docs/new.md"}
        with patch.object(quality, "resolve_doc", return_value=quality.DOCS / "new.md"), \
             patch.object(quality, "measure", return_value=measured), \
             patch.object(quality, "load_yaml", return_value={"documents": []}), \
             patch.object(quality, "quantitative_comparison", return_value={"passed": True}) as compare, \
             patch.object(quality, "print_quantitative"), \
             patch.object(quality, "save_yaml") as save:
            quality.benchmark_document("docs/new.md")
        self.assertEqual(compare.call_args.args[0], measured)
        save.assert_not_called()

    def test_assessment_templates_match_rubric(self) -> None:
        full = quality.parse_assessment(quality.QUALITY_DIR / "assessment-template.yaml")
        outline = quality.parse_assessment(
            quality.QUALITY_DIR / "outline-assessment-template.yaml"
        )
        self.assertEqual(full["scope"], "full")
        self.assertEqual(outline["scope"], "outline")
        self.assertEqual(set(full["areas"]), {"A", "B", "C"})
        self.assertEqual(set(outline["areas"]), {"A", "C"})


class ScopedSyncTests(unittest.TestCase):
    def setUp(self):
        from tempfile import TemporaryDirectory
        from unittest.mock import patch
        self.temp = TemporaryDirectory(dir=quality.ROOT / "experiment")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name, value in {"ROOT": self.root, "DOCS": self.root / "docs",
                            "REGISTRY_PATH": self.root / "registry.yaml"}.items():
            patcher = patch.object(quality, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.write("a.md", "첫 주장이다.")
        self.write("b.md", "다른 주장이다.")
        registry = quality.sync_registry(verbose=False)
        for record in registry["documents"]:
            record["review"] = {"status": "pass", "scope": "full",
                                "model": quality.review_model(),
                                "rubric_version": quality.RUBRIC_VERSION}
        quality.save_yaml(quality.REGISTRY_PATH, registry)

    def write(self, name, body):
        path = quality.DOCS / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("---\ndescription: 시험\n---\n# Topic\n\n## 1. 정의\n\n" + body + "\n")
        return path

    def records(self):
        return {r["path"]: r for r in quality.load_yaml(quality.REGISTRY_PATH, {})["documents"]}

    def test_only_selected_document_is_measured_and_updated(self):
        from unittest.mock import patch
        before = self.records()
        self.write("a.md", "수정된 주장이다.")
        self.write("b.md", "미완성 주장이다.")
        self.write("unrelated-new.md", "미완성 신규 문서이다.")
        with patch.object(quality, "measure", wraps=quality.measure) as measure:
            quality.sync_registry(verbose=False, paths=["docs/a.md", "docs/a.md"])
        measure.assert_called_once_with(quality.DOCS / "a.md")
        after = self.records()
        self.assertEqual(after["docs/b.md"], before["docs/b.md"])
        self.assertNotIn("docs/unrelated-new.md", after)
        self.assertEqual(after["docs/a.md"]["review"]["required_scope"], "full")

    def test_selected_move_preserves_review_and_unrelated_deleted_record(self):
        before = self.records()
        (quality.DOCS / "a.md").rename(quality.DOCS / "moved.md")
        (quality.DOCS / "b.md").unlink()
        quality.sync_registry(verbose=False, paths=["docs/a.md", "docs/moved.md"])
        after = self.records()
        self.assertNotIn("docs/a.md", after)
        self.assertEqual(after["docs/moved.md"]["review"], before["docs/a.md"]["review"])
        self.assertEqual(after["docs/b.md"], before["docs/b.md"])

    def test_move_does_not_consume_unselected_record(self):
        before = self.records()
        (quality.DOCS / "a.md").rename(quality.DOCS / "moved.md")
        quality.sync_registry(verbose=False, paths=["docs/moved.md"])
        after = self.records()
        self.assertEqual(after["docs/a.md"], before["docs/a.md"])
        self.assertEqual(after["docs/moved.md"]["review"]["status"], "pending")

    def test_delete_and_new_document(self):
        (quality.DOCS / "a.md").unlink()
        self.write("new.md", "신규 내용이다.")
        quality.sync_registry(verbose=False, paths=["docs/a.md", "docs/new.md"])
        self.assertEqual(set(self.records()), {"docs/b.md", "docs/new.md"})
        self.assertEqual(self.records()["docs/new.md"]["review"]["status"], "pending")

    def test_invalid_paths_do_not_write_even_after_valid_argument(self):
        before = quality.REGISTRY_PATH.read_bytes()
        self.write("a.md", "변경이다.")
        for invalid in ["docs/typo.md", "../outside.md", "docs", "docs/a.txt"]:
            with self.subTest(path=invalid), self.assertRaises(SystemExit):
                quality.sync_registry(verbose=False, paths=["docs/a.md", invalid])
            self.assertEqual(quality.REGISTRY_PATH.read_bytes(), before)

    def test_legacy_scoped_sync_rejected_without_write(self):
        registry = quality.load_yaml(quality.REGISTRY_PATH, {})
        registry["hash_version"] = 0
        quality.save_yaml(quality.REGISTRY_PATH, registry)
        before = quality.REGISTRY_PATH.read_bytes()
        with self.assertRaises(SystemExit):
            quality.sync_registry(verbose=False, paths=["docs/a.md"])
        self.assertEqual(quality.REGISTRY_PATH.read_bytes(), before)

    def test_full_sync_still_updates_all_and_removes_deleted(self):
        self.write("a.md", "변경이다.")
        (quality.DOCS / "b.md").unlink()
        self.write("new.md", "신규이다.")
        quality.sync_registry(verbose=False)
        self.assertEqual(set(self.records()), {"docs/a.md", "docs/new.md"})
        self.assertEqual(self.records()["docs/a.md"]["review"]["required_scope"], "full")

    def test_cli_passes_explicit_paths_and_default_full(self):
        from unittest.mock import patch
        for paths in [[], ["docs/a.md", "docs/b.md"]]:
            with patch("sys.argv", ["quality.py", "sync", *paths]), \
                 patch.object(quality, "sync_registry") as sync:
                quality.main()
            sync.assert_called_once_with(paths=paths or None)


if __name__ == "__main__":
    unittest.main()
