#!/usr/bin/env python3
"""Deterministic checks and compact review attestations for the wiki."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import date
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
DOCS = ROOT / "docs"
MKDOCS_PATH = ROOT / "mkdocs.yml"
QUALITY_DIR = ROOT / "refs" / "quality"
REGISTRY_PATH = QUALITY_DIR / "documents.yaml"
RUBRIC_PATH = QUALITY_DIR / "rubric.yaml"
SCHEMA_VERSION = 2
RUBRIC_VERSION = 3
HASH_VERSION = 2

FENCED_CODE_BLOCK_RE = re.compile(r"(^|\n)(```|~~~).*?\n\2(?=\n|$)", re.DOTALL)
CITATION_RE = re.compile(r"\[(?:\d+)(?:\s*[,;–—-]\s*\d+)*\]")
REFERENCE_HEADING_RE = re.compile(
    r"^##\s+(?:\d+\.\s*)?(?:참고문헌|References)\s*$", re.MULTILINE
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
NAV_NUMBER_RE = re.compile(r"^\d+(?:\.\d+)*\.\s+")


class MkDocsLoader(yaml.SafeLoader):
    """Safe loader that treats MkDocs Python-name tags as inert strings."""


MkDocsLoader.add_multi_constructor(
    "tag:yaml.org,2002:python/name:",
    lambda _loader, suffix, _node: suffix,
)


def fail(message: str) -> None:
    raise SystemExit(f"오류: {message}")


def load_yaml(path: Path, default: Any) -> Any:
    if not path.exists():
        return deepcopy(default)
    with path.open(encoding="utf-8") as stream:
        loaded = yaml.safe_load(stream)
    return deepcopy(default) if loaded is None else loaded


def save_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", dir=path.parent, text=True
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            yaml.safe_dump(data, stream, allow_unicode=True, sort_keys=False, width=120)
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def relative_path(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def resolve_doc(raw_path: str) -> Path:
    path = Path(raw_path)
    if not path.is_absolute():
        path = ROOT / path
    path = path.resolve()
    try:
        path.relative_to(DOCS)
    except ValueError:
        fail(f"docs/ 아래의 문서만 검사할 수 있음: {raw_path}")
    if path.suffix != ".md" or not path.is_file():
        fail(f"Markdown 문서를 찾을 수 없음: {raw_path}")
    return path


def all_docs() -> list[Path]:
    return sorted(DOCS.rglob("*.md"))


def page_kind(path: Path) -> str:
    if path == DOCS / "index.md":
        return "home"
    if path.name == "index.md":
        return "index"
    return "article"


def page_group(path: Path) -> str:
    parts = path.relative_to(DOCS).parts
    if len(parts) == 1:
        return "home"
    return parts[0] if path.name == "index.md" else " / ".join(parts[:-1])


def strip_front_matter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "", text
    return text[4:end], text[end + 5 :]


def parse_metadata(front_matter: str) -> dict[str, Any]:
    if not front_matter:
        return {}
    metadata = yaml.safe_load(front_matter)
    return metadata if isinstance(metadata, dict) else {}


def without_code(text: str) -> str:
    return FENCED_CODE_BLOCK_RE.sub("\n", text)


def headings(body: str) -> list[tuple[int, str]]:
    return [
        (len(match.group(1)), match.group(2).strip())
        for match in HEADING_RE.finditer(without_code(body))
    ]


def page_title(body: str) -> str:
    h1 = [title for level, title in headings(body) if level == 1]
    return h1[0] if len(h1) == 1 else ""


def page_scope(metadata: dict[str, Any], body: str) -> str:
    description = metadata.get("description")
    if isinstance(description, str) and description.strip():
        return description.strip()
    for paragraph in re.split(r"\n\s*\n", without_code(body)):
        paragraph = paragraph.strip()
        if paragraph and not paragraph.startswith(("#", "<", "-", "|", "!")):
            return re.sub(r"\s+", " ", paragraph)
    return ""


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_content(body: str) -> str:
    """Scientific content without presentation headings or front matter."""
    lines: list[str] = []
    blank = False
    fence: str | None = None
    for line in body.replace("\r\n", "\n").splitlines():
        fence_match = re.match(r"^\s*(```|~~~)", line)
        if fence_match:
            marker = fence_match.group(1)
            fence = None if fence == marker else marker
        if fence is None and not fence_match and re.match(r"^#{1,3}\s+", line):
            continue
        cleaned = line.rstrip()
        if not cleaned:
            if not blank:
                lines.append("")
            blank = True
        else:
            lines.append(cleaned)
            blank = False
    return "\n".join(lines).strip()


def normalize_outline_title(level: int, title: str) -> str:
    if level == 2:
        title = re.sub(r"^\d+\.\s*", "", title)
    elif level == 3:
        title = re.sub(r"^\(\d+\)\s*", "", title)
    return re.sub(r"\s+", " ", title).strip()


def canonical_outline(body: str) -> str:
    return "\n".join(
        f"{level}:{normalize_outline_title(level, title)}"
        for level, title in headings(body)
        if level in (2, 3)
    )


def canonical_presentation(path: Path, metadata: dict[str, Any], body: str) -> str:
    metadata_text = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=True)
    return f"{relative_path(path)}\n{page_title(body)}\n{metadata_text}"


def split_references(text: str) -> tuple[str, str]:
    match = REFERENCE_HEADING_RE.search(text)
    return (text, "") if not match else (text[: match.start()], text[match.end() :])


def visible_character_count(main_text: str) -> int:
    text = without_code(main_text)
    text = re.sub(r"\$\$.*?\$\$", "", text, flags=re.DOTALL)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = CITATION_RE.sub("", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[`*_>|{}\\]", "", text)
    return len(re.sub(r"\s+", "", text))


def automatic_issues(
    path: Path,
    metadata: dict[str, Any],
    body: str,
    reference_count: int,
) -> list[str]:
    issues: list[str] = []
    kind = page_kind(path)
    body_without_code = without_code(body)
    page_headings = headings(body)
    h1 = [title for level, title in page_headings if level == 1]
    if len(h1) != 1:
        issues.append("H1 제목은 하나여야 한다")
    elif NAV_NUMBER_RE.match(h1[0]):
        issues.append("H1에 navigation 번호가 있다")
    if any(level >= 4 for level, _title in page_headings):
        issues.append("H4 이하 제목이 있다")

    if kind == "article":
        if not isinstance(metadata.get("description"), str) or not metadata["description"].strip():
            issues.append("front matter에 비어 있지 않은 description이 없다")
        for legacy_field in ("title", "status", "last_verified"):
            if legacy_field in metadata:
                issues.append(f"중복 또는 review용 metadata가 본문에 남아 있다: {legacy_field}")
        for level, title in page_headings:
            if level == 2 and not re.match(r"^\d+\.\s+", title):
                issues.append(f"H2 번호 형식이 잘못되었다: {title}")
            if level == 3 and not re.match(r"^\(\d+\)\s+", title):
                issues.append(f"H3 번호 형식이 잘못되었다: {title}")

    citation_numbers = [
        int(number)
        for cluster in CITATION_RE.findall(body_without_code)
        for number in re.findall(r"\d+", cluster)
    ]
    if citation_numbers and max(citation_numbers) > reference_count:
        issues.append("본문 인용 번호가 참고문헌 수보다 크다")

    for match in re.finditer(r"(!?)\[([^\]]*)\]\(([^)]+)\)", body_without_code):
        label = match.group(2).strip()
        target = match.group(3).strip().split()[0].strip("<>")
        if kind in ("home", "index") and NAV_NUMBER_RE.match(label):
            issues.append(f"index 링크 문구에 navigation 번호가 있다: {label}")
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean_target = target.split("#", 1)[0]
        if clean_target and not (path.parent / clean_target).resolve().exists():
            issues.append(f"연결 대상을 찾을 수 없다: {clean_target}")
    return sorted(set(issues))


def measure(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    front_matter, body = strip_front_matter(raw)
    metadata = parse_metadata(front_matter)
    code_blocks = len(list(FENCED_CODE_BLOCK_RE.finditer(body)))
    body_without_code = without_code(body)
    main_text, reference_text = split_references(body_without_code)
    reference_count = len(re.findall(r"^\s*\d+\.\s+\S", reference_text, flags=re.MULTILINE))
    figures = len(re.findall(r"!\[[^\]]*\]\([^)]*\)", body_without_code))
    tables = len(
        re.findall(
            r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$",
            body_without_code,
            flags=re.MULTILINE,
        )
    )
    equations = len(re.findall(r"\$\$.*?\$\$", body_without_code, flags=re.DOTALL))
    issues = automatic_issues(path, metadata, body, reference_count)
    return {
        "path": relative_path(path),
        "topic": page_title(body),
        "scope": page_scope(metadata, body),
        "kind": page_kind(path),
        "group": page_group(path),
        "hashes": {
            "source": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            "content": hash_text(canonical_content(body)),
            "outline": hash_text(canonical_outline(body)),
            "presentation": hash_text(canonical_presentation(path, metadata, body)),
        },
        "metrics": {
            "characters": visible_character_count(main_text),
            "explanatory_elements": {
                "total": figures + tables + equations + code_blocks,
                "figures": figures,
                "tables": tables,
                "equations": equations,
                "code_blocks": code_blocks,
            },
        },
        "automatic_check": "pass" if not issues else "fail",
        "issues": issues,
    }


def collect_nav(items: Any, labels: list[str], paths: list[str]) -> None:
    if not isinstance(items, list):
        return
    for item in items:
        if not isinstance(item, dict) or len(item) != 1:
            continue
        label, value = next(iter(item.items()))
        labels.append(str(label))
        if isinstance(value, str):
            paths.append(value)
        else:
            collect_nav(value, labels, paths)


def navigation_issues() -> list[str]:
    with MKDOCS_PATH.open(encoding="utf-8") as stream:
        config = yaml.load(stream, Loader=MkDocsLoader)
    nav = config.get("nav") if isinstance(config, dict) else None
    if not isinstance(nav, list):
        return ["mkdocs.yml에 nav list가 없다"]
    top_labels = [next(iter(item)) for item in nav if isinstance(item, dict) and len(item) == 1]
    required = ["Home", "Device physics", "Material science", "Computational science"]
    issues: list[str] = []
    if top_labels[:4] != required:
        issues.append("고정 top-level navigation 이름 또는 순서가 잘못되었다")
    if any(label != "Research Note" for label in top_labels[4:]):
        issues.append("고정 domain 뒤에 허용되지 않은 top-level section이 있다")

    labels: list[str] = []
    nav_paths: list[str] = []
    collect_nav(nav, labels, nav_paths)
    numbered = [label for label in labels if NAV_NUMBER_RE.match(label)]
    if numbered:
        issues.append(f"navigation label에 수동 번호가 있다: {', '.join(numbered[:5])}")
    duplicates = sorted({path for path in nav_paths if nav_paths.count(path) > 1})
    if duplicates:
        issues.append(f"navigation에 중복 문서가 있다: {', '.join(duplicates)}")
    doc_paths = {path.relative_to(DOCS).as_posix() for path in all_docs()}
    nav_path_set = set(nav_paths)
    missing = sorted(doc_paths - nav_path_set)
    extra = sorted(nav_path_set - doc_paths)
    if missing:
        issues.append(f"navigation에 없는 문서가 있다: {', '.join(missing)}")
    if extra:
        issues.append(f"존재하지 않는 navigation 문서가 있다: {', '.join(extra)}")
    return issues


def check_navigation() -> None:
    errors = navigation_issues()
    if errors:
        print("navigation 검사 실패:", file=sys.stderr)
        for error in sorted(set(errors)):
            print(f"  - {error}", file=sys.stderr)
        raise SystemExit(1)
    print("navigation 검사 통과")


def default_registry() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "rubric_version": RUBRIC_VERSION,
        "hash_version": HASH_VERSION,
        "updated_at": date.today().isoformat(),
        "documents": [],
    }


def pending_review(scope: str) -> dict[str, Any]:
    return {"status": "pending", "required_scope": scope}


def excluded_review() -> dict[str, Any]:
    return {
        "status": "excluded",
        "reason": "Home과 index는 navigation hub이므로 scientific review에서 제외한다.",
    }


def rubric_definition() -> dict[str, Any]:
    rubric = load_yaml(RUBRIC_PATH, {})
    required = {
        "review_scopes",
        "scored_areas",
        "critical_zero",
        "compliance",
        "forced_revise_rules",
        "passing",
        "quantitative",
    }
    missing = required - set(rubric)
    if missing:
        fail(f"rubric 필수 항목이 없음: {', '.join(sorted(missing))}")
    return rubric


def applicable_criteria(scope: str) -> dict[str, dict[str, Any]]:
    rubric = rubric_definition()
    areas: dict[str, dict[str, Any]] = {}
    for area_id, area_rule in rubric["scored_areas"].items():
        criteria = {
            criterion_id: rule
            for criterion_id, rule in area_rule["criteria"].items()
            if scope in rule.get("scopes", ["full"])
        }
        if criteria:
            areas[area_id] = criteria
    return areas


def applicable_compliance(scope: str) -> dict[str, dict[str, Any]]:
    return {
        check_id: rule
        for check_id, rule in rubric_definition()["compliance"].items()
        if scope in rule.get("scopes", ["full"])
    }


def full_gate_ids() -> list[str]:
    return [
        criterion_id
        for criteria in applicable_criteria("full").values()
        for criterion_id in criteria
    ]


def imported_review(previous: dict[str, Any], measured: dict[str, Any]) -> dict[str, Any]:
    old_review = previous.get("review") or {}
    if measured["kind"] in ("home", "index"):
        return excluded_review()
    if old_review.get("status") != "pass":
        return pending_review("full")
    return {
        "status": "pass",
        "scope": "full",
        "reviewed_at": old_review.get("reviewed_at", date.today().isoformat()),
        "rubric_version": RUBRIC_VERSION,
        "content_hash": measured["hashes"]["content"],
        "outline_hash": measured["hashes"]["outline"],
        "criteria": {
            criterion_id: {
                "status": "pass",
                "evidence": ["이전 schema 또는 hash version의 current pass review에서 이전함"],
                "reason": "기존 검증 결과를 compact attestation으로 이전했다.",
            }
            for criterion_id in full_gate_ids()
        },
        "summary": old_review.get("summary", "기존 pass review를 compact schema로 이전했다."),
        "migrated_from_legacy": True,
    }


def preserve_review(previous: dict[str, Any], measured: dict[str, Any]) -> dict[str, Any]:
    if measured["kind"] in ("home", "index"):
        return excluded_review()
    review = deepcopy(previous.get("review") or pending_review("full"))
    old_hashes = previous.get("hashes", {})
    same_content = old_hashes.get("content") == measured["hashes"]["content"]
    same_outline = old_hashes.get("outline") == measured["hashes"]["outline"]
    current_rubric = review.get("rubric_version") == RUBRIC_VERSION
    if (
        review.get("status") == "pass"
        and review.get("migrated_from_legacy") is True
        and same_content
        and same_outline
        and review.get("rubric_version") == 2
    ):
        return {
            "status": "pass",
            "scope": "full",
            "reviewed_at": review.get("reviewed_at", date.today().isoformat()),
            "rubric_version": RUBRIC_VERSION,
            "content_hash": measured["hashes"]["content"],
            "outline_hash": measured["hashes"]["outline"],
            "summary": review.get("summary", "축약 전 원자적 review의 pass를 승계했다."),
            "migrated_from_legacy": True,
            "carried_forward_from": "pre-refactor atomic rubric pass",
        }
    if review.get("status") == "pass" and same_content and same_outline and current_rubric:
        return review
    if same_content and not same_outline:
        return pending_review("outline")
    if not same_content:
        return pending_review("full")
    if not current_rubric:
        return pending_review("full")
    return review


def find_move_candidate(
    measured: dict[str, Any],
    previous_records: list[dict[str, Any]],
    used_paths: set[str],
) -> dict[str, Any] | None:
    candidates = [
        record
        for record in previous_records
        if record.get("path") not in used_paths
        and record.get("kind") == measured["kind"]
        and record.get("hashes", {}).get("content") == measured["hashes"]["content"]
        and record.get("hashes", {}).get("outline") == measured["hashes"]["outline"]
    ]
    return candidates[0] if len(candidates) == 1 else None


def sync_registry(verbose: bool = True) -> dict[str, Any]:
    old = load_yaml(REGISTRY_PATH, default_registry())
    legacy = (
        old.get("schema_version") != SCHEMA_VERSION
        or old.get("hash_version") != HASH_VERSION
    )
    previous_records = old.get("documents", []) if isinstance(old, dict) else []
    by_path = {record.get("path"): record for record in previous_records}
    used_paths: set[str] = set()
    records: list[dict[str, Any]] = []
    changes = {"added": 0, "content": 0, "outline": 0, "presentation": 0, "moved": 0}

    for path in all_docs():
        measured = measure(path)
        previous = by_path.get(measured["path"])
        if previous is None and not legacy:
            previous = find_move_candidate(measured, previous_records, used_paths)
            if previous:
                changes["moved"] += 1
        if previous:
            used_paths.add(previous.get("path", ""))
            if legacy:
                review = imported_review(previous, measured)
            else:
                review = preserve_review(previous, measured)
                old_hashes = previous.get("hashes", {})
                if old_hashes.get("content") != measured["hashes"]["content"]:
                    changes["content"] += 1
                elif old_hashes.get("outline") != measured["hashes"]["outline"]:
                    changes["outline"] += 1
                elif old_hashes.get("presentation") != measured["hashes"]["presentation"]:
                    changes["presentation"] += 1
        else:
            review = excluded_review() if measured["kind"] in ("home", "index") else pending_review("full")
            changes["added"] += 1
        records.append({**measured, "review": review})

    registry = {
        "schema_version": SCHEMA_VERSION,
        "rubric_version": RUBRIC_VERSION,
        "hash_version": HASH_VERSION,
        "updated_at": date.today().isoformat(),
        "documents": records,
    }
    old_compare = deepcopy(old)
    new_compare = deepcopy(registry)
    old_compare.pop("updated_at", None)
    new_compare.pop("updated_at", None)
    if old_compare != new_compare:
        save_yaml(REGISTRY_PATH, registry)
    elif verbose:
        registry["updated_at"] = old.get("updated_at", registry["updated_at"])

    if verbose:
        counts = ", ".join(f"{key}={value}" for key, value in changes.items())
        print(f"품질 기록 동기화: {len(records)}개 문서 ({counts})")
    return registry


def required_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label}은 비워 둘 수 없음")
    return value.strip()


def required_text_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        fail(f"{label}에는 한 개 이상의 항목이 필요함")
    return [required_text(item, label) for item in value]


def parse_assessment(path: Path) -> dict[str, Any]:
    assessment = load_yaml(path, {})
    if not isinstance(assessment, dict):
        fail("평가 파일의 최상위 값은 mapping이어야 함")
    scope = assessment.get("scope")
    rubric = load_yaml(RUBRIC_PATH, {})
    scopes = rubric.get("review_scopes", {})
    if scope not in scopes:
        fail(f"알 수 없는 review scope: {scope!r}")
    expected_top = {"scope", "areas", "compliance", "summary"}
    if scope == "full":
        expected_top.update({"forced_revise", "critical_questions"})
    if set(assessment) != expected_top:
        fail(
            f"{scope} 평가 최상위 항목 불일치: "
            f"누락={sorted(expected_top - set(assessment))}, "
            f"초과={sorted(set(assessment) - expected_top)}"
        )

    submitted_areas = assessment.get("areas")
    expected_areas = applicable_criteria(scope)
    if not isinstance(submitted_areas, dict) or set(submitted_areas) != set(expected_areas):
        fail(f"{scope} area 불일치: 기대={sorted(expected_areas)}, 입력={sorted(submitted_areas or {})}")

    area_results: dict[str, Any] = {}
    total_points = 0.0
    total_area_weight = 0.0
    ratings: dict[str, int] = {}
    for area_id, criteria_rules in expected_areas.items():
        submitted = submitted_areas[area_id]
        if not isinstance(submitted, dict) or set(submitted) != set(criteria_rules):
            fail(
                f"{area_id} criterion 불일치: "
                f"기대={sorted(criteria_rules)}, 입력={sorted(submitted or {})}"
            )
        earned = 0.0
        possible = 0.0
        criteria: dict[str, Any] = {}
        for criterion_id, criterion_rule in criteria_rules.items():
            item = submitted[criterion_id]
            rating = item.get("rating") if isinstance(item, dict) else None
            if type(rating) is not int or rating not in (0, 1, 2):
                fail(f"{criterion_id}.rating은 0, 1, 2 중 하나여야 함")
            weight = float(criterion_rule["weight"])
            evidence = required_text_list(item.get("evidence"), f"{criterion_id}.evidence")
            locations = required_text_list(item.get("locations"), f"{criterion_id}.locations")
            reason = required_text(item.get("reason"), f"{criterion_id}.reason")
            possible += weight
            earned += weight * rating / 2
            ratings[criterion_id] = rating
            criteria[criterion_id] = {
                "rating": rating,
                "evidence": evidence,
                "locations": locations,
                "reason": reason,
            }
        percent = 100 * earned / possible
        area_weight = float(rubric["scored_areas"][area_id]["weight"])
        total_points += area_weight * percent / 100
        total_area_weight += area_weight
        area_results[area_id] = {
            "percent": round(percent, 2),
            "criteria": criteria,
        }

    submitted_compliance = assessment.get("compliance")
    expected_compliance = applicable_compliance(scope)
    if not isinstance(submitted_compliance, dict) or set(submitted_compliance) != set(expected_compliance):
        fail(
            f"{scope} compliance 불일치: "
            f"기대={sorted(expected_compliance)}, 입력={sorted(submitted_compliance or {})}"
        )
    compliance: dict[str, Any] = {}
    for check_id in expected_compliance:
        item = submitted_compliance[check_id]
        if not isinstance(item, dict) or item.get("status") not in ("pass", "fail"):
            fail(f"{check_id}.status는 pass 또는 fail이어야 함")
        compliance[check_id] = {
            "status": item["status"],
            "evidence": required_text_list(item.get("evidence"), f"{check_id}.evidence"),
            "locations": required_text_list(item.get("locations"), f"{check_id}.locations"),
            "reason": required_text(item.get("reason"), f"{check_id}.reason"),
        }

    forced_revise: list[dict[str, Any]] = []
    critical_questions: dict[str, str] = {}
    if scope == "full":
        submitted_forced = assessment.get("forced_revise")
        if not isinstance(submitted_forced, list):
            fail("forced_revise는 list여야 함")
        known_forced = rubric["forced_revise_rules"]
        for index, item in enumerate(submitted_forced):
            if not isinstance(item, dict) or item.get("id") not in known_forced:
                fail(f"forced_revise[{index}].id가 알려진 규칙이 아님")
            forced_revise.append(
                {
                    "id": item["id"],
                    "evidence": required_text_list(item.get("evidence"), f"forced_revise[{index}].evidence"),
                    "locations": required_text_list(item.get("locations"), f"forced_revise[{index}].locations"),
                    "reason": required_text(item.get("reason"), f"forced_revise[{index}].reason"),
                }
            )
        questions = assessment.get("critical_questions")
        question_ids = {"dependency_chain", "reader_blocker", "strongest_revise_case"}
        if not isinstance(questions, dict) or set(questions) != question_ids:
            fail(f"critical_questions에는 {', '.join(sorted(question_ids))}만 필요함")
        critical_questions = {
            key: required_text(value, f"critical_questions.{key}")
            for key, value in questions.items()
        }

    critical_zero_failures = [
        criterion_id
        for criterion_id in rubric["critical_zero"]
        if ratings.get(criterion_id) == 0
    ]
    normalized_points = 100 * total_points / total_area_weight
    return {
        "scope": scope,
        "areas": area_results,
        "points": round(normalized_points, 2),
        "compliance": compliance,
        "critical_zero_failures": critical_zero_failures,
        "forced_revise": forced_revise,
        "critical_questions": critical_questions,
        "summary": required_text(assessment.get("summary"), "summary"),
    }


def quantitative_comparison(record: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    rules = rubric_definition()["quantitative"]
    minimum_peers = int(rules["minimum_peer_count"])
    candidates = [
        item
        for item in registry.get("documents", [])
        if item.get("kind") == "article"
        and item.get("path") != record.get("path")
        and (item.get("review") or {}).get("status") == "pass"
    ]
    target_domain = record["path"].split("/", 2)[1]
    pools = {
        "topic_group": [item for item in candidates if item.get("group") == record.get("group")],
        "scientific_domain": [
            item for item in candidates if item["path"].split("/", 2)[1] == target_domain
        ],
        "all_articles": candidates,
    }
    level, peers = next(
        (
            (name, pools[name])
            for name in rules["peer_order"]
            if name in pools and len(pools[name]) >= minimum_peers
        ),
        ("all_articles", candidates),
    )
    if len(peers) < minimum_peers:
        fail(f"정량 baseline에 필요한 pass article이 {minimum_peers}개 미만임")
    ratio = float(rules["minimum_percent_of_peer_average"]) / 100
    character_average = sum(item["metrics"]["characters"] for item in peers) / len(peers)
    element_average = sum(
        item["metrics"]["explanatory_elements"]["total"] for item in peers
    ) / len(peers)
    actual_characters = record["metrics"]["characters"]
    actual_elements = record["metrics"]["explanatory_elements"]["total"]
    minimum_characters = character_average * ratio
    minimum_elements = element_average * ratio
    return {
        "passed": actual_characters >= minimum_characters and actual_elements >= minimum_elements,
        "level": level,
        "peer_count": len(peers),
        "characters": {
            "actual": actual_characters,
            "peer_average": round(character_average, 2),
            "minimum": round(minimum_characters, 2),
        },
        "explanatory_elements": {
            "actual": actual_elements,
            "peer_average": round(element_average, 2),
            "minimum": round(minimum_elements, 2),
        },
    }


def print_quantitative(comparison: dict[str, Any]) -> None:
    print(
        "정량 coverage: "
        f"{comparison['level']} peer {comparison['peer_count']}개, "
        f"글자 {comparison['characters']['actual']}/"
        f"{comparison['characters']['minimum']:.2f}, "
        f"설명요소 {comparison['explanatory_elements']['actual']}/"
        f"{comparison['explanatory_elements']['minimum']:.2f}"
    )


def benchmark_document(raw_path: str) -> None:
    path = resolve_doc(raw_path)
    measured = measure(path)
    if measured["kind"] != "article":
        fail("article만 정량 coverage 대상이다")
    registry = load_yaml(REGISTRY_PATH, default_registry())
    records = {record["path"]: record for record in registry.get("documents", [])}
    record = records.get(measured["path"])
    if not record or record.get("hashes") != measured["hashes"]:
        fail("문서 변경 뒤 ./quality.sh sync를 먼저 실행하십시오")
    comparison = quantitative_comparison(record, registry)
    print_quantitative(comparison)
    if not comparison["passed"]:
        fail("정량 coverage 기준 미달: 필요한 설명을 보강하십시오")


def review_document(args: argparse.Namespace) -> None:
    path = resolve_doc(args.path)
    measured = measure(path)
    if measured["kind"] != "article":
        fail("article만 scientific review 대상이다")
    registry = load_yaml(REGISTRY_PATH, default_registry())
    if registry.get("schema_version") != SCHEMA_VERSION:
        fail("먼저 ./quality.sh sync로 registry schema를 갱신하십시오")
    records = {record["path"]: record for record in registry.get("documents", [])}
    record = records.get(measured["path"])
    if not record or record.get("hashes") != measured["hashes"]:
        fail("문서 변경 뒤 ./quality.sh sync를 먼저 실행하십시오")
    if measured["automatic_check"] != "pass":
        fail(f"automatic check가 실패함: {', '.join(measured['issues'])}")

    assessment_path = Path(args.assessment)
    if not assessment_path.is_absolute():
        assessment_path = ROOT / assessment_path
    if not assessment_path.is_file():
        fail(f"평가 파일을 찾을 수 없음: {args.assessment}")
    assessment = parse_assessment(assessment_path)
    required_scope = (record.get("review") or {}).get("required_scope")
    if required_scope == "full" and assessment["scope"] != "full":
        fail("scientific content 변경에는 full review가 필요함")
    quantitative = None
    if assessment["scope"] == "full":
        quantitative = quantitative_comparison(record, registry)
        print_quantitative(quantitative)
        if not quantitative["passed"]:
            fail("정량 coverage 기준 미달: 필요한 설명을 보강한 뒤 다시 review하십시오")

    rules = rubric_definition()["passing"]
    area_pass = all(
        float(area["percent"]) >= float(rules["minimum_area_percent"])
        for area in assessment["areas"].values()
    )
    compliance_pass = all(
        item["status"] == "pass" for item in assessment["compliance"].values()
    )
    passed = (
        float(assessment["points"]) >= float(rules["minimum_overall_points"])
        and area_pass
        and compliance_pass
        and not assessment["critical_zero_failures"]
        and not assessment["forced_revise"]
    )
    record["review"] = {
        "status": "pass" if passed else "revise",
        "scope": assessment["scope"],
        "reviewed_at": date.today().isoformat(),
        "rubric_version": RUBRIC_VERSION,
        "content_hash": measured["hashes"]["content"],
        "outline_hash": measured["hashes"]["outline"],
        "points": assessment["points"],
        "area_percent": {
            area_id: result["percent"] for area_id, result in assessment["areas"].items()
        },
        "compliance": {
            check_id: item["status"] for check_id, item in assessment["compliance"].items()
        },
        "critical_zero_failures": assessment["critical_zero_failures"],
        "forced_revise": [item["id"] for item in assessment["forced_revise"]],
        "critical_questions": assessment["critical_questions"],
        "summary": assessment["summary"],
    }
    if quantitative is not None:
        record["review"]["quantitative"] = quantitative
    registry["updated_at"] = date.today().isoformat()
    save_yaml(REGISTRY_PATH, registry)
    print(f"평가 기록: {record['path']} -> {record['review']['status']} ({assessment['scope']})")


def changed_docs() -> list[Path]:
    commands = [
        ["git", "diff", "--name-only"],
        ["git", "diff", "--cached", "--name-only"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    names: set[str] = set()
    for command in commands:
        completed = subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
        names.update(line.strip() for line in completed.stdout.splitlines() if line.strip())
    return [
        ROOT / name
        for name in sorted(names)
        if name.startswith("docs/") and name.endswith(".md") and (ROOT / name).is_file()
    ]


def check_documents(paths: list[Path]) -> None:
    registry = load_yaml(REGISTRY_PATH, default_registry())
    errors = navigation_issues()
    if registry.get("schema_version") != SCHEMA_VERSION:
        errors.append("registry schema가 현재 quality script와 다르다")
    records = {record.get("path"): record for record in registry.get("documents", [])}
    current = {relative_path(path): path for path in all_docs()}
    for missing in sorted(set(current) - set(records)):
        errors.append(f"{missing}: 품질 기록이 없다")
    for removed in sorted(set(records) - set(current)):
        errors.append(f"{removed}: 삭제된 문서 기록이 남아 있다")

    excluded = 0
    for path in paths:
        measured = measure(path)
        record = records.get(measured["path"])
        if not record:
            continue
        if record.get("hashes") != measured["hashes"]:
            errors.append(f"{measured['path']}: ./quality.sh sync가 필요하다")
        if measured["automatic_check"] != "pass":
            errors.extend(f"{measured['path']}: {issue}" for issue in measured["issues"])
        review = record.get("review") or {}
        if measured["kind"] in ("home", "index"):
            if review.get("status") != "excluded":
                errors.append(f"{measured['path']}: index review 상태가 excluded가 아니다")
            else:
                excluded += 1
            continue
        if review.get("status") != "pass":
            errors.append(f"{measured['path']}: review 상태가 {review.get('status', 'missing')!r}이다")
            continue
        if review.get("content_hash") != measured["hashes"]["content"]:
            errors.append(f"{measured['path']}: scientific content review가 현재 본문과 다르다")
        if review.get("outline_hash") != measured["hashes"]["outline"]:
            errors.append(f"{measured['path']}: outline review가 현재 목차와 다르다")
        if review.get("rubric_version") != RUBRIC_VERSION:
            errors.append(f"{measured['path']}: review rubric version이 오래되었다")
    if errors:
        print("품질 검사 실패:", file=sys.stderr)
        for error in sorted(set(errors)):
            print(f"  - {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"품질 검사 통과: article {len(paths) - excluded}개, index/home {excluded}개")


def report() -> None:
    registry = load_yaml(REGISTRY_PATH, default_registry())
    print("상태      범위      점수   글자  설명요소  문서")
    for record in registry.get("documents", []):
        review = record.get("review") or {}
        elements = record["metrics"]["explanatory_elements"]["total"]
        points = review.get("points")
        points_text = f"{points:.1f}" if isinstance(points, (int, float)) else "-"
        print(
            f"{review.get('status', 'missing'):<9} "
            f"{review.get('required_scope', review.get('scope', '-')):<9} "
            f"{points_text:>5} {record['metrics']['characters']:>6} "
            f"{elements:>8}  {record['path']}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("sync", help="derived metadata를 명시적으로 갱신한다")
    review_parser = subparsers.add_parser("review", help="compact scientific review를 기록한다")
    review_parser.add_argument("path")
    review_parser.add_argument("--assessment", required=True)
    benchmark_parser = subparsers.add_parser(
        "benchmark", help="full review 전에 정량 coverage를 읽기 전용으로 검사한다"
    )
    benchmark_parser.add_argument("path")
    check_parser = subparsers.add_parser("check", help="파일을 쓰지 않고 현재 상태를 검사한다")
    check_parser.add_argument("paths", nargs="*")
    check_parser.add_argument("--all", action="store_true")
    check_parser.add_argument("--changed", action="store_true")
    subparsers.add_parser("check-nav", help="article review와 무관한 navigation 규칙만 검사한다")
    subparsers.add_parser("report", help="파일을 쓰지 않고 현재 registry를 출력한다")
    return parser.parse_args()


def selected_paths(args: argparse.Namespace) -> list[Path]:
    modes = int(bool(getattr(args, "all", False))) + int(bool(getattr(args, "changed", False)))
    if modes > 1:
        fail("--all과 --changed는 함께 사용할 수 없음")
    if getattr(args, "all", False):
        return all_docs()
    if getattr(args, "changed", False):
        return changed_docs()
    paths = getattr(args, "paths", [])
    if not paths:
        fail("문서 경로 또는 --all/--changed가 필요함")
    return [resolve_doc(raw_path) for raw_path in paths]


def main() -> None:
    args = parse_args()
    if args.command == "sync":
        sync_registry()
    elif args.command == "review":
        review_document(args)
    elif args.command == "benchmark":
        benchmark_document(args.path)
    elif args.command == "check":
        check_documents(selected_paths(args))
    elif args.command == "check-nav":
        check_navigation()
    elif args.command == "report":
        report()


if __name__ == "__main__":
    main()
