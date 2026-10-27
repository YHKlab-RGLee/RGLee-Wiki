from __future__ import annotations

from argparse import Namespace
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
import hashlib
import importlib.util
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location("facts_quality", Path(__file__).with_name("scripts") / "quality.py")
quality = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(quality)


class FactReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(dir=quality.ROOT / "experiment")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name, value in {"ROOT": self.root, "DOCS": self.root / "docs",
                            "QUALITY_DIR": self.root / "refs/quality",
                            "REGISTRY_PATH": self.root / "refs/quality/documents.yaml"}.items():
            context = patch.object(quality, name, value)
            context.start()
            self.addCleanup(context.stop)
        context = patch.object(quality, "navigation_issues", return_value=[])
        context.start()
        self.addCleanup(context.stop)
        self.page = quality.DOCS / "test.md"
        self.page.parent.mkdir()
        self.page.write_text("---\ndescription: 검산\n---\n# Test\n\n## 1. 관계\n\n수치 1이다.\n")
        self.assessment_path = self.root / "assessment.yaml"
        quality.sync_registry(verbose=False)

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True, text=True).stdout

    def commit(self):
        if not (self.root / ".git").exists():
            self.git("init", "-q")
        self.git("add", "docs")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture")

    def record(self):
        return quality.load_yaml(quality.REGISTRY_PATH, {})["documents"][0]

    def assessment(self, status="supported"):
        return {
            "scope": "facts", "source_hash": hashlib.sha256(self.page.read_bytes()).hexdigest(),
            "assets": quality.local_assets(self.page),
            "coverage": {"mode": "full", "baseline_source_hash": None, "checked": ["§1 수치와 관계"],
                         "dependencies": [], "reused_evidence": []},
            "findings": [{"id": "numeric", "claim": "전제식에 대입한 수치 1", "locations": ["§1"],
                          "category": "scientific", "status": status, "method": "calculation",
                          "sources": [{"id": "original-A", "provenance": "author-A-work", "locator": "Eq. 1",
                                       "supports": "기본 관계"},
                                      {"id": "original-B", "provenance": "author-B-work", "locator": "Eq. 2",
                                       "supports": "동일 가정의 관계"}],
                          "check": "fixture: supported premises and a reproducible substitution",
                          "assumptions": "fixture: same units and model assumptions"}],
            "summary": "시험용 원문 확인 기록 (실제 과학 검증 아님)",
        }

    def register(self, assessment=None):
        quality.save_yaml(self.assessment_path, assessment or self.assessment())
        quality.review_document(Namespace(path=str(self.page), assessment=str(self.assessment_path)))
        return self.record()

    def test_short_article_without_peers_can_pass_and_has_no_score(self):
        record = self.register()
        self.assertEqual(record["review"]["status"], "pass")
        self.assertNotIn("points", record["review"])
        self.assertNotIn("quantitative", record["review"])
        quality.check_documents([self.page])

    def test_wrong_numeric_or_quote_finding_blocks_publication(self):
        for category in ("scientific", "quotation"):
            data = self.assessment("mismatch")
            data["findings"][0]["category"] = category
            record = self.register(data)
            self.assertEqual(record["review"]["status"], "revise")
            with self.assertRaises(SystemExit):
                quality.check_documents([self.page])

    def test_unknown_is_not_an_error_but_cannot_publish(self):
        for status in ("insufficient", "inaccessible"):
            data = self.assessment(status)
            data["findings"][0]["sources"] = []
            self.assertEqual(self.register(data)["review"]["status"], "unverified")
            with self.assertRaises(SystemExit):
                quality.check_documents([self.page])

    def test_two_mirrors_do_not_satisfy_independence(self):
        data = self.assessment()
        data["findings"][0]["sources"][1]["provenance"] = "author-A-work"
        with self.assertRaises(SystemExit):
            self.register(data)
        self.assertEqual(self.record()["review"]["status"], "pending")

    def test_source_locator_and_derivation_are_required(self):
        for section, key in (("source", "locator"), ("finding", "check")):
            data = self.assessment()
            finding = data["findings"][0]
            (finding["sources"][0] if section == "source" else finding)[key] = ""
            with self.assertRaises(SystemExit):
                self.register(data)

    def test_old_scoring_schema_is_not_accepted_as_new_review(self):
        with self.assertRaises(SystemExit):
            self.register({"scope": "full", "areas": {}, "compliance": {}, "summary": "old"})

    def test_stale_assessment_rejected_after_equation_change(self):
        data = self.assessment()
        self.page.write_text(self.page.read_text().replace("수치 1", "수치 2"))
        quality.sync_registry(verbose=False, paths=[str(self.page)])
        with self.assertRaises(SystemExit):
            self.register(data)

    def test_model_information_not_inherited(self):
        data = self.assessment()
        data["model"] = {"name": "fixture", "reasoning_effort": "", "source": "test"}
        self.assertEqual(self.register(data)["review"]["model"]["name"], "fixture")
        self.assertEqual(self.register()["review"]["model"]["name"], "")

    def test_last_verified_diff_spans_multiple_commits_and_syncs(self):
        original = self.register()
        self.commit()
        self.page.write_text(self.page.read_text().replace("수치 1", "수치 2"))
        self.commit()
        quality.sync_registry(verbose=False, paths=[str(self.page)])
        self.page.write_text(self.page.read_text().replace("수치 2", "수치 3"))
        self.commit()
        quality.sync_registry(verbose=False, paths=[str(self.page)])
        baseline, text = quality.baseline_text(self.record())
        self.assertIn("수치 1", text)
        self.assertNotIn("수치 2", text)
        self.assertEqual(baseline["hashes"], original["hashes"])
        data = self.assessment()
        evidence = original["review"]["evidence_path"]
        data["coverage"].update(mode="changes", baseline_source_hash=baseline["hashes"]["source"],
                                reused_evidence=[{"path": evidence, "sha256": hashlib.sha256((self.root / evidence).read_bytes()).hexdigest(),
                                                  "scope": "unchanged assumptions only"}])
        self.assertEqual(self.register(data)["review"]["coverage"], "changes")
        quality.check_documents([self.page])

    def test_changes_reject_wrong_baseline_and_missing_reuse(self):
        self.register()
        data = self.assessment()
        data["coverage"].update(mode="changes", baseline_source_hash="0" * 64)
        with self.assertRaises(SystemExit):
            self.register(data)
        data["coverage"]["baseline_source_hash"] = data["source_hash"]
        with self.assertRaises(SystemExit):
            self.register(data)

    def test_missing_baseline_never_falls_back_to_latest_commit(self):
        self.register()
        self.page.write_text(self.page.read_text().replace("수치 1", "수치 2"))
        self.commit()  # only the unreviewed version is in Git
        quality.sync_registry(verbose=False, paths=[str(self.page)])
        with self.assertRaises(SystemExit):
            quality.baseline_text(self.record())

    def test_failed_review_does_not_erase_verified_baseline(self):
        original = self.register()
        self.commit()
        self.page.write_text(self.page.read_text().replace("수치 1", "수치 2"))
        quality.sync_registry(verbose=False, paths=[str(self.page)])
        self.register(self.assessment("mismatch"))
        quality.sync_registry(verbose=False, paths=[str(self.page)])
        baseline, _ = quality.baseline_text(self.record())
        self.assertEqual(baseline["hashes"], original["hashes"])

    def test_heading_or_description_claim_cannot_automatically_carry(self):
        for old, new in (("# Test", "# New claim"), ("description: 검산", "description: 다른 주장")):
            self.register()
            self.page.write_text(self.page.read_text().replace(old, new))
            quality.sync_registry(verbose=False, paths=[str(self.page)])
            self.assertEqual(self.record()["review"]["status"], "pending")

    def test_explicit_meaning_preservation_carries_evidence(self):
        original = self.register()
        self.page.write_text(self.page.read_text().replace("## 1. 관계", "## 1. 기본 관계"))
        quality.sync_registry(verbose=False, paths=[str(self.page)], polish=True)
        record = self.record()
        self.assertEqual(record["review"]["evidence_path"], original["review"]["evidence_path"])
        self.assertEqual(record["review"]["scientific_review"], original["review"])
        quality.check_documents([self.page])

    def test_asset_change_invalidates_review_without_markdown_edit(self):
        asset = quality.DOCS / "figure.svg"
        asset.write_text("first fixture")
        self.page.write_text(self.page.read_text() + "\n![시험 그림](figure.svg)\n")
        quality.sync_registry(verbose=False, paths=[str(self.page)])
        self.register()
        self.commit()
        asset.write_text("changed fixture")
        self.assertIn(self.page, quality.changed_docs())
        with self.assertRaises(SystemExit):
            quality.check_documents([self.page])
        with self.assertRaises(SystemExit):
            quality.sync_registry(verbose=False, paths=[str(self.page)], polish=True)
        quality.sync_registry(verbose=False, paths=[str(self.page)])
        self.assertEqual(self.record()["review"]["status"], "pending")

    def test_evidence_tampering_cannot_pass(self):
        record = self.register()
        path = self.root / record["review"]["evidence_path"]
        path.write_text(path.read_text().replace("supported", "mismatch"))
        with self.assertRaises(SystemExit):
            quality.check_documents([self.page])

    def test_figure_changed_after_review_cannot_be_registered(self):
        asset = quality.DOCS / "figure.svg"
        asset.write_text("first")
        self.page.write_text(self.page.read_text() + "\n![시험](figure.svg)\n")
        data = self.assessment()
        asset.write_text("second")
        quality.sync_registry(verbose=False, paths=[str(self.page)])
        with self.assertRaises(SystemExit):
            self.register(data)

    def test_deleted_legacy_figure_selects_its_consumer(self):
        asset = quality.DOCS / "figure.svg"
        asset.write_text("first")
        self.page.write_text(self.page.read_text() + "\n![시험](figure.svg)\n")
        self.commit()
        asset.unlink()
        self.assertIn(self.page, quality.changed_docs())

    def test_meaning_preserving_move_keeps_original_evidence(self):
        original = self.register()
        new = self.page.with_name("moved.md")
        self.page.rename(new)
        quality.sync_registry(verbose=False, paths=[str(self.page), str(new)], polish=True)
        self.assertEqual(self.record()["review"]["status"], "pass")
        self.assertEqual(self.record()["review"]["evidence_path"], original["review"]["evidence_path"])
        quality.check_documents([new])

    def test_record_only_update_is_included_in_changed_gate(self):
        self.commit()
        self.git("add", "refs")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "registry")
        self.register()
        self.assertIn(self.page, quality.changed_docs())

    def test_reused_evidence_checksum_is_required(self):
        first = self.register()
        data = self.assessment()
        data["coverage"].update(mode="changes", baseline_source_hash=data["source_hash"],
                                reused_evidence=[{"path": first["review"]["evidence_path"], "sha256": "0" * 64,
                                                  "scope": "same assumptions"}])
        with self.assertRaises(SystemExit):
            self.register(data)

    def test_evidence_chain_detects_older_missing_dependency(self):
        first = self.register()
        first_path = first["review"]["evidence_path"]
        def delta_data(previous):
            data = self.assessment()
            path = previous["review"]["evidence_path"]
            data["coverage"].update(mode="changes", baseline_source_hash=data["source_hash"],
                                    reused_evidence=[{"path": path, "sha256": hashlib.sha256((self.root / path).read_bytes()).hexdigest(),
                                                      "scope": "same assumptions"}])
            return data
        second = self.register(delta_data(first))
        self.register(delta_data(second))
        (self.root / first_path).unlink()
        with self.assertRaises(SystemExit):
            quality.check_documents([self.page])

    def test_legacy_is_read_only_history_not_new_verification(self):
        registry = quality.load_yaml(quality.REGISTRY_PATH, {})
        record = registry["documents"][0]
        record["review"] = {"status": "pass", "scope": "full", "points": 100,
                            "rubric_version": 3, "content_hash": record["hashes"]["content"],
                            "outline_hash": record["hashes"]["outline"]}
        quality.save_yaml(quality.REGISTRY_PATH, registry)
        before = quality.REGISTRY_PATH.read_bytes()
        output = StringIO()
        with redirect_stdout(output):
            quality.report([self.page])
            quality.check_documents([self.page])
            quality.benchmark_document(str(self.page))
            quality.show_baseline(str(self.page))
        self.assertIn("legacy", output.getvalue())
        self.assertNotIn("100", output.getvalue().splitlines()[1])
        self.assertEqual(before, quality.REGISTRY_PATH.read_bytes())


if __name__ == "__main__":
    unittest.main()
