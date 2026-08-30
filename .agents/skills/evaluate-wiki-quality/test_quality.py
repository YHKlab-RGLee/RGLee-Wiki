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

    def test_assessment_templates_match_rubric(self) -> None:
        full = quality.parse_assessment(quality.QUALITY_DIR / "assessment-template.yaml")
        outline = quality.parse_assessment(
            quality.QUALITY_DIR / "outline-assessment-template.yaml"
        )
        self.assertEqual(full["scope"], "full")
        self.assertEqual(outline["scope"], "outline")
        self.assertEqual(set(full["areas"]), {"A", "B", "C"})
        self.assertEqual(set(outline["areas"]), {"A", "C"})


if __name__ == "__main__":
    unittest.main()
