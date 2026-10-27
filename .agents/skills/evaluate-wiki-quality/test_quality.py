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
    def test_polish_preserves_original_assessment_and_tracks_versions(self) -> None:
        previous = {
            "hashes": {"source": "old", "content": "old", "outline": "old"},
            "review": {"status": "pass", "rubric_version": quality.RUBRIC_VERSION,
                       "content_hash": "old", "outline_hash": "old",
                       "evidence_path": "original.yaml", "reviewed_at": "2026-01-01"},
        }
        measured = {"path": "docs/example.md", "kind": "article",
                    "hashes": {"source": "new", "content": "new", "outline": "new"}}
        result = quality.polish_review(previous, measured)
        self.assertEqual(result["scientific_review"], previous["review"])
        self.assertEqual(result["content_hash"], "new")
        self.assertEqual(result["outline_hash"], "new")
        self.assertEqual(result["polish"]["from_source_hash"], "old")
        self.assertEqual(result["polish"]["to_source_hash"], "new")
        self.assertEqual(previous["review"]["content_hash"], "old")
        repeated = quality.polish_review({**measured, "review": result}, measured)
        self.assertEqual(repeated, result)
        next_version = {**measured, "hashes": {"source": "next", "content": "next", "outline": "new"}}
        repeated = quality.polish_review({**measured, "review": result}, next_version)
        self.assertEqual(repeated["scientific_review"], previous["review"])
        self.assertEqual(repeated["polish"]["from_source_hash"], "new")
        self.assertEqual(quality.preserve_review({**next_version, "review": repeated}, measured)["status"], "pending")

    def test_polish_cannot_clear_pending_failed_or_stale_reviews(self) -> None:
        measured = {"path": "docs/example.md", "kind": "article",
                    "hashes": {"source": "new", "content": "new", "outline": "new"}}
        for status, version, content in [("pending", quality.RUBRIC_VERSION, "old"),
                                         ("revise", quality.RUBRIC_VERSION, "old"),
                                         ("pass", 0, "old"),
                                         ("pass", quality.RUBRIC_VERSION, "stale")]:
            with self.subTest(status=status, version=version, content=content):
                previous = {"hashes": {"content": "old", "outline": "old"},
                            "review": {"status": status, "rubric_version": version,
                                       "content_hash": content, "outline_hash": "old"}}
                with self.assertRaises(SystemExit):
                    quality.polish_review(previous, measured)

    def test_polish_requires_explicit_paths(self) -> None:
        with self.assertRaises(SystemExit):
            quality.sync_registry(polish=True)

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






    def test_pending_full_cannot_be_downgraded_by_heading_edit(self) -> None:
        previous = {"kind": "article", "hashes": {"content": "body", "outline": "old"},
                    "review": {"status": "pending", "required_scope": "full"}}
        measured = {"kind": "article", "hashes": {"content": "body", "outline": "new"}}
        self.assertEqual(quality.preserve_review(previous, measured)["required_scope"], "facts")


    def test_failed_full_keeps_blockers_after_heading_edit(self) -> None:
        previous = {"kind": "article", "hashes": {"content": "body", "outline": "old"},
                    "review": {"status": "revise", "scope": "full", "forced_revise": ["F3"]}}
        measured = {"kind": "article", "hashes": {"content": "body", "outline": "new"}}
        review = quality.preserve_review(previous, measured)
        self.assertEqual(review["required_scope"], "facts")
        self.assertEqual(review["forced_revise"], ["F3"])

    def test_last_pass_survives_repeated_pending_sync(self) -> None:
        previous = {"kind": "article", "hashes": {"content": "body", "outline": "old"},
                    "review": {"status": "pass", "scope": "full", "rubric_version": quality.RUBRIC_VERSION}}
        measured = {"kind": "article", "hashes": {"content": "changed", "outline": "old"}}
        first = quality.preserve_review(previous, measured)
        next_record = dict(measured, review=first)
        second = quality.preserve_review(next_record, measured)
        self.assertEqual(second["last_pass"]["scope"], "full")
        self.assertEqual(second["required_scope"], "facts")

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




class ScopedSyncTests(unittest.TestCase):
    def setUp(self):
        from tempfile import TemporaryDirectory
        from unittest.mock import patch
        (quality.ROOT / "experiment").mkdir(exist_ok=True)
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
                                "content_hash": record["hashes"]["content"],
                                "outline_hash": record["hashes"]["outline"],
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
        self.assertEqual(after["docs/a.md"]["review"]["required_scope"], "facts")

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
        self.assertEqual(self.records()["docs/a.md"]["review"]["required_scope"], "facts")

    def test_cli_passes_explicit_paths_and_default_full(self):
        from unittest.mock import patch
        for paths in [[], ["docs/a.md", "docs/b.md"]]:
            with patch("sys.argv", ["quality.py", "sync", *paths]), \
                 patch.object(quality, "sync_registry") as sync:
                quality.main()
            sync.assert_called_once_with(paths=paths or None, polish=False)
        with patch("sys.argv", ["quality.py", "sync", "--polish", "docs/a.md"]), \
             patch.object(quality, "sync_registry") as sync:
            quality.main()
        sync.assert_called_once_with(paths=["docs/a.md"], polish=True)

    def test_polish_sync_preserves_review_and_unselected_records(self):
        before = self.records()
        self.write("a.md", "첫 번째 주장이다.")
        quality.sync_registry(verbose=False, paths=["docs/a.md"], polish=True)
        after = self.records()
        self.assertEqual(after["docs/b.md"], before["docs/b.md"])
        self.assertEqual(after["docs/a.md"]["review"]["status"], "pass")
        self.assertEqual(after["docs/a.md"]["review"]["scientific_review"], before["docs/a.md"]["review"])
        quality.sync_registry(verbose=False, paths=["docs/a.md"])
        self.assertEqual(self.records(), after)

    def test_polish_rejects_new_page_without_partial_registry_write(self):
        before = quality.REGISTRY_PATH.read_bytes()
        self.write("a.md", "첫 번째 주장이다.")
        self.write("new.md", "새 주장이다.")
        with self.assertRaises(SystemExit):
            quality.sync_registry(verbose=False, paths=["docs/a.md", "docs/new.md"], polish=True)
        self.assertEqual(quality.REGISTRY_PATH.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
