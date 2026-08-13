#!/usr/bin/env python3
"""Collect and check simple, human-readable quality records for this wiki."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import os
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
DOCS = ROOT / "docs"
QUALITY_DIR = ROOT / "refs" / "quality"
REGISTRY_PATH = QUALITY_DIR / "documents.yaml"
RUBRIC_PATH = QUALITY_DIR / "rubric.yaml"
CITATION_RE = re.compile(r"\[(?:\d+)(?:\s*[,;–—-]\s*\d+)*\]")
FENCED_CODE_BLOCK_RE = re.compile(
    r"(^|\n)(```|~~~).*?\n\2(?=\n|$)", re.DOTALL
)
REFERENCE_HEADING_RE = re.compile(
    r"^##\s+(?:\d+\.\s*)?(?:참고문헌|References)\s*$", re.MULTILINE
)


def fail(message: str) -> None:
    raise SystemExit(f"오류: {message}")


def load_yaml(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as stream:
        loaded = yaml.safe_load(stream)
    return default if loaded is None else loaded


def save_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", dir=path.parent, text=True
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            yaml.safe_dump(
                data,
                stream,
                allow_unicode=True,
                sort_keys=False,
                width=120,
            )
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
        fail(f"docs/ 아래의 문서만 평가할 수 있음: {raw_path}")
    if path.suffix != ".md":
        fail(f"Markdown 문서가 아님: {raw_path}")
    if not path.is_file():
        fail(f"문서를 찾을 수 없음: {raw_path}")
    return path


def all_docs() -> list[Path]:
    return sorted(DOCS.rglob("*.md"))


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_front_matter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "", text
    return text[4:end], text[end + 5 :]


def split_references(text: str) -> tuple[str, str]:
    match = REFERENCE_HEADING_RE.search(text)
    if not match:
        return text, ""
    return text[: match.start()], text[match.end() :]


def without_code(text: str) -> str:
    return FENCED_CODE_BLOCK_RE.sub("\n", text)


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
    if path.name == "index.md":
        return parts[0]
    return " / ".join(parts[:-1])


def page_title(front_matter: str, body: str) -> str:
    metadata = yaml.safe_load(front_matter) if front_matter else {}
    if isinstance(metadata, dict) and metadata.get("title"):
        return str(metadata["title"])
    match = re.search(r"^#\s+(.+?)\s*$", without_code(body), flags=re.MULTILINE)
    return match.group(1) if match else ""


def page_scope(front_matter: str, body: str) -> str:
    metadata = yaml.safe_load(front_matter) if front_matter else {}
    if isinstance(metadata, dict) and metadata.get("description"):
        return str(metadata["description"])
    for paragraph in re.split(r"\n\s*\n", without_code(body)):
        paragraph = paragraph.strip()
        if paragraph and not paragraph.startswith(("#", "<", "-", "|", "!")):
            return re.sub(r"\s+", " ", paragraph)
    return ""


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


def automatic_issues(path: Path, front_matter: str, body: str, reference_count: int) -> list[str]:
    issues: list[str] = []
    kind = page_kind(path)
    body_without_code = without_code(body)
    if len(re.findall(r"^#\s+", body_without_code, flags=re.MULTILINE)) != 1:
        issues.append("H1 제목은 하나여야 한다")
    if re.search(r"^####+\s+", body_without_code, flags=re.MULTILINE):
        issues.append("H4 이하 제목이 있다")
    if kind == "article":
        for field in ("title:", "description:", "status:", "last_verified:"):
            if field not in front_matter:
                issues.append(f"front matter에 {field[:-1]}가 없다")
    citation_numbers = [
        int(number)
        for cluster in CITATION_RE.findall(body_without_code)
        for number in re.findall(r"\d+", cluster)
    ]
    if citation_numbers and max(citation_numbers) > reference_count:
        issues.append("본문 인용 번호가 참고문헌 수보다 크다")

    for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", body_without_code):
        target = match.group(1).strip().split()[0].strip("<>")
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean_target = target.split("#", 1)[0]
        if not clean_target:
            continue
        resolved = (path.parent / clean_target).resolve()
        if not resolved.exists():
            issues.append(f"연결 대상을 찾을 수 없다: {clean_target}")
    return sorted(set(issues))


def measure(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    front_matter, body = strip_front_matter(raw)
    code_blocks = len(list(FENCED_CODE_BLOCK_RE.finditer(body)))
    body_without_code = without_code(body)
    main_text, reference_text = split_references(body_without_code)
    references = len(re.findall(r"^\s*\d+\.\s+\S", reference_text, flags=re.MULTILINE))
    figures = len(re.findall(r"!\[[^\]]*\]\([^)]*\)", body_without_code))
    tables = len(
        re.findall(
            r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$",
            body_without_code,
            flags=re.MULTILINE,
        )
    )
    equations = len(re.findall(r"\$\$.*?\$\$", body_without_code, flags=re.DOTALL))
    metrics = {
        "characters": visible_character_count(main_text),
        "explanatory_elements": {
            "total": figures + tables + equations + code_blocks,
            "figures": figures,
            "tables": tables,
            "equations": equations,
            "code_blocks": code_blocks,
        },
    }
    issues = automatic_issues(path, front_matter, body, references)
    return {
        "path": relative_path(path),
        "topic": page_title(front_matter, body),
        "scope": page_scope(front_matter, body),
        "kind": page_kind(path),
        "group": page_group(path),
        "source_hash": source_hash(path),
        "measured_at": date.today().isoformat(),
        "metrics": metrics,
        "automatic_check": "pass" if not issues else "fail",
        "issues": issues,
    }


def default_registry() -> dict[str, Any]:
    return {
        "updated_at": date.today().isoformat(),
        "archived_documents": [],
        "documents": [],
    }


def load_registry() -> dict[str, Any]:
    data = load_yaml(REGISTRY_PATH, default_registry())
    data.setdefault("documents", [])
    data.setdefault("archived_documents", [])
    return data


def compact_history(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": record.get("path"),
        "topic": record.get("topic"),
        "scope": record.get("scope"),
        "source_hash": record.get("source_hash"),
        "measured_at": record.get("measured_at"),
        "metrics": deepcopy(record.get("metrics")),
        "review": deepcopy(record.get("review")),
    }


def latest_archive(registry: dict[str, Any], relative: str) -> dict[str, Any] | None:
    matches = [item for item in registry["archived_documents"] if item.get("path") == relative]
    return matches[-1] if matches else None


def sync_registry(verbose: bool = True) -> tuple[dict[str, Any], dict[str, list[str]]]:
    """Synchronize every docs page while preserving reviews and deletion history."""
    registry = load_registry()
    existing = {item["path"]: item for item in registry["documents"]}
    current = {relative_path(path): path for path in all_docs()}
    updated: dict[str, dict[str, Any]] = {}
    changes: dict[str, list[str]] = {
        "added": [],
        "modified": [],
        "deleted": [],
        "restored": [],
    }

    for relative, path in current.items():
        measured = measure(path)
        previous = existing.get(relative)
        if previous:
            history = list(previous.get("history", []))
            if previous.get("source_hash") == measured["source_hash"]:
                measured["measured_at"] = previous.get(
                    "measured_at", measured["measured_at"]
                )
                measured["review"] = previous.get("review")
            else:
                history.append(compact_history(previous))
                measured["review"] = None
                changes["modified"].append(relative)
        else:
            archived = latest_archive(registry, relative)
            if archived:
                history = list(archived.get("history", []))
                history.append(compact_history(archived))
                measured["review"] = None
                changes["restored"].append(relative)
            else:
                history = []
                measured["review"] = None
                changes["added"].append(relative)
        if measured["kind"] in excluded_kinds():
            prior_review = measured.get("review")
            if prior_review and prior_review.get("status") != "excluded":
                history.append(compact_history(measured))
            measured["review"] = {
                "reviewed_at": date.today().isoformat(),
                "reason": rubric_definition()["evaluation_scope"]["excluded_reason"],
                "status": "excluded",
            }
        measured["history"] = history
        updated[relative] = measured

    for relative in sorted(set(existing) - set(current)):
        archived = deepcopy(existing[relative])
        archived["deleted_at"] = date.today().isoformat()
        registry["archived_documents"].append(archived)
        changes["deleted"].append(relative)

    defaults = default_registry()
    if any(changes.values()):
        registry["updated_at"] = defaults["updated_at"]
    else:
        registry.setdefault("updated_at", defaults["updated_at"])
    registry["documents"] = [updated[key] for key in sorted(updated)]
    refresh_review_statuses(registry)
    save_yaml(REGISTRY_PATH, registry)
    if verbose:
        counts = ", ".join(f"{key}={len(value)}" for key, value in changes.items())
        print(f"품질 기록 동기화: {len(updated)}개 현재 문서 ({counts})")
    return registry, changes


def passing_rules() -> dict[str, Any]:
    rubric = load_yaml(RUBRIC_PATH, {})
    if "passing" not in rubric:
        fail(f"통과 기준을 찾을 수 없음: {relative_path(RUBRIC_PATH)}")
    return rubric["passing"]


def rubric_definition() -> dict[str, Any]:
    rubric = load_yaml(RUBRIC_PATH, {})
    for key in (
        "evaluation_scope",
        "scored_areas",
        "compliance",
        "forced_revise_rules",
        "passing",
    ):
        if key not in rubric:
            fail(f"채점표에 {key} 정의가 없음: {relative_path(RUBRIC_PATH)}")
    return rubric


def excluded_kinds() -> set[str]:
    return set(rubric_definition()["evaluation_scope"].get("excluded_kinds", []))


def quantitative_rules() -> dict[str, Any]:
    rubric = load_yaml(RUBRIC_PATH, {})
    if "quantitative" not in rubric:
        fail(f"정량 기준을 찾을 수 없음: {relative_path(RUBRIC_PATH)}")
    return rubric["quantitative"]


def refresh_review_statuses(registry: dict[str, Any]) -> None:
    rules = passing_rules()
    records = registry["documents"]
    for record in records:
        review = record.get("review")
        if not review:
            continue
        if record.get("kind") in excluded_kinds():
            review["status"] = "excluded"
            continue
        area_pass = all(
            float(area["percent"]) >= float(rules["minimum_area_percent"])
            for area in review["areas"].values()
        )
        compliance_pass = all(
            item["status"] == "pass" for item in review["compliance"].values()
        )
        checklist_pass = (
            record["automatic_check"] == "pass"
            and float(review["points"]) >= float(rules["minimum_overall_points"])
            and area_pass
            and compliance_pass
            and not review.get("critical_zero_failures")
            and not review.get("forced_revise")
        )
        review["status"] = "pass" if checklist_pass else "revise"


def required_text(value: Any, label: str, korean: bool = False) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label}은 비워 둘 수 없음")
    value = value.strip()
    if korean and not re.search(r"[가-힣]", value):
        fail(f"{label}은 한국어 문장을 포함해야 함")
    return value


def required_text_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        fail(f"{label}에는 한 개 이상의 항목이 필요함")
    return [required_text(item, label) for item in value]


def parse_assessment(path: Path, kind: str) -> dict[str, Any]:
    assessment = load_yaml(path, {})
    if not isinstance(assessment, dict):
        fail("평가 파일의 최상위 값은 mapping이어야 함")
    expected_sections = {
        "areas",
        "compliance",
        "forced_revise",
        "critical_questions",
        "summary",
    }
    if set(assessment) != expected_sections:
        fail(
            "평가 파일 최상위 항목 불일치: "
            f"누락={sorted(expected_sections - set(assessment))}, "
            f"초과={sorted(set(assessment) - expected_sections)}"
        )
    rubric = rubric_definition()
    submitted_areas = assessment.get("areas")
    if not isinstance(submitted_areas, dict):
        fail("평가 파일에 areas mapping이 필요함")
    expected_areas = set(rubric["scored_areas"])
    if set(submitted_areas) != expected_areas:
        fail(
            "채점 영역 불일치: "
            f"누락={sorted(expected_areas - set(submitted_areas))}, "
            f"초과={sorted(set(submitted_areas) - expected_areas)}"
        )

    areas: dict[str, Any] = {}
    total_points = 0.0
    ratings: dict[str, int] = {}
    for area_id, area_rule in rubric["scored_areas"].items():
        submitted_area = submitted_areas.get(area_id)
        if not isinstance(submitted_area, dict):
            fail(f"평가 파일에 {area_id} 영역이 필요함")
        applicable: list[tuple[str, dict[str, Any]]] = []
        for criterion_id, criterion_rule in area_rule["criteria"].items():
            applies_to = criterion_rule.get("applies_to")
            if applies_to and kind not in applies_to:
                continue
            applicable.append((criterion_id, criterion_rule))
        submitted_ids = set(submitted_area)
        expected_ids = {criterion_id for criterion_id, _ in applicable}
        if submitted_ids != expected_ids:
            missing = sorted(expected_ids - submitted_ids)
            extra = sorted(submitted_ids - expected_ids)
            fail(f"{area_id} 채점 항목 불일치: 누락={missing}, 초과={extra}")
        earned = 0.0
        possible = 0.0
        criteria: dict[str, Any] = {}
        for criterion_id, criterion_rule in applicable:
            item = submitted_area[criterion_id]
            if not isinstance(item, dict):
                fail(f"{criterion_id} 평가는 mapping이어야 함")
            rating = item.get("rating")
            if type(rating) is not int or rating not in (0, 1, 2):
                fail(f"{criterion_id}.rating은 0, 1, 2 중 하나여야 함")
            evidence = required_text_list(item.get("evidence"), f"{criterion_id}.evidence")
            locations = required_text_list(item.get("locations"), f"{criterion_id}.locations")
            reason = required_text(item.get("reason"), f"{criterion_id}.reason", korean=True)
            weight = float(criterion_rule["weight"])
            possible += weight
            earned += weight * rating / 2
            ratings[criterion_id] = rating
            criteria[criterion_id] = {
                "rating": rating,
                "evidence": evidence,
                "locations": locations,
                "reason": reason,
            }
        if possible <= 0:
            fail(f"{area_id}에 적용 가능한 채점 항목이 없음")
        percent = 100 * earned / possible
        points = float(area_rule["weight"]) * earned / possible
        total_points += points
        areas[area_id] = {
            "name": area_rule["name"],
            "points": round(points, 2),
            "maximum": float(area_rule["weight"]),
            "percent": round(percent, 2),
            "criteria": criteria,
        }

    submitted_compliance = assessment.get("compliance")
    if not isinstance(submitted_compliance, dict):
        fail("평가 파일에 compliance mapping이 필요함")
    expected_compliance = set(rubric["compliance"])
    if set(submitted_compliance) != expected_compliance:
        fail(
            "compliance 항목 불일치: "
            f"누락={sorted(expected_compliance - set(submitted_compliance))}, "
            f"초과={sorted(set(submitted_compliance) - expected_compliance)}"
        )
    compliance: dict[str, Any] = {}
    for check_id in rubric["compliance"]:
        item = submitted_compliance[check_id]
        if not isinstance(item, dict) or item.get("status") not in ("pass", "fail"):
            fail(f"{check_id}.status는 pass 또는 fail이어야 함")
        compliance[check_id] = {
            "status": item["status"],
            "evidence": required_text_list(item.get("evidence"), f"{check_id}.evidence"),
            "locations": required_text_list(item.get("locations"), f"{check_id}.locations"),
            "reason": required_text(item.get("reason"), f"{check_id}.reason", korean=True),
        }

    submitted_forced = assessment.get("forced_revise")
    if not isinstance(submitted_forced, list):
        fail("forced_revise는 list여야 하며 해당 사항이 없으면 []로 제출해야 함")
    forced_revise: list[dict[str, Any]] = []
    known_forced = rubric["forced_revise_rules"]
    for index, item in enumerate(submitted_forced):
        if not isinstance(item, dict) or item.get("id") not in known_forced:
            fail(f"forced_revise[{index}].id가 알려진 규칙이 아님")
        forced_revise.append(
            {
                "id": item["id"],
                "evidence": required_text_list(
                    item.get("evidence"), f"forced_revise[{index}].evidence"
                ),
                "locations": required_text_list(
                    item.get("locations"), f"forced_revise[{index}].locations"
                ),
                "reason": required_text(
                    item.get("reason"), f"forced_revise[{index}].reason", korean=True
                ),
            }
        )

    questions = assessment.get("critical_questions")
    if not isinstance(questions, dict):
        fail("critical_questions mapping이 필요함")
    question_ids = ("dependency_chain", "reader_blocker", "strongest_revise_case")
    if set(questions) != set(question_ids):
        fail(f"critical_questions에는 {', '.join(question_ids)}만 필요함")
    critical_questions = {
        key: required_text(questions[key], f"critical_questions.{key}", korean=True)
        for key in question_ids
    }
    critical_zero_failures = [
        criterion_id
        for criterion_id in rubric["critical_zero"]
        if criterion_id in ratings and ratings[criterion_id] == 0
    ]
    return {
        "areas": areas,
        "points": round(total_points, 2),
        "overall": round(total_points / 10, 2),
        "compliance": compliance,
        "critical_zero_failures": critical_zero_failures,
        "forced_revise": forced_revise,
        "critical_questions": critical_questions,
        "summary": required_text(assessment.get("summary"), "summary", korean=True),
    }


def review_document(args: argparse.Namespace) -> None:
    path = resolve_doc(args.path)
    registry, _ = sync_registry(verbose=False)
    record = next(item for item in registry["documents"] if item["path"] == relative_path(path))
    if record["kind"] in excluded_kinds():
        fail(f"{record['kind']} 문서는 article 읽기 평가 대상이 아님: {record['path']}")
    records = {item["path"]: item for item in registry["documents"]}
    reference_paths = list(dict.fromkeys(relative_path(resolve_doc(raw)) for raw in args.references))
    if record["path"] in reference_paths:
        fail("대상 문서를 비교 문서로 사용할 수 없음")
    rules = quantitative_rules()
    minimum_references = int(rules["minimum_references"])
    if len(reference_paths) < minimum_references:
        fail(f"비교 문서는 최소 {minimum_references}개가 필요함")
    references = [records[reference_path] for reference_path in reference_paths]
    if any(reference["kind"] != record["kind"] for reference in references):
        fail("대상과 같은 문서 종류만 비교할 수 있음")
    minimum_percent = float(rules["minimum_percent_of_average"])
    if not 0 < minimum_percent <= 100:
        fail("비교 평균 기준은 0보다 크고 100 이하여야 함")
    ratio = minimum_percent / 100
    comparisons = (
        (
            "글자 수",
            record["metrics"]["characters"],
            sum(reference["metrics"]["characters"] for reference in references) / len(references),
        ),
        (
            "설명 요소",
            record["metrics"]["explanatory_elements"]["total"],
            sum(
                reference["metrics"]["explanatory_elements"]["total"]
                for reference in references
            )
            / len(references),
        ),
    )
    shortfalls = []
    print("비교 문서:")
    for reference_path in reference_paths:
        print(f"  - {reference_path}")
    print(f"정량 비교 (비교 평균의 {minimum_percent:g}% 이상):")
    for label, target_value, average in comparisons:
        minimum = average * ratio
        passed = target_value >= minimum
        print(
            f"  {label}: 대상={target_value}, 비교 평균={average:.1f}, "
            f"최소={minimum:.1f} -> {'통과' if passed else '보강'}"
        )
        if not passed:
            shortfalls.append(label)
    if shortfalls:
        fail(f"정량 기준 미달: {', '.join(shortfalls)}")
    assessment_path = Path(args.assessment)
    if not assessment_path.is_absolute():
        assessment_path = ROOT / assessment_path
    if not assessment_path.is_file():
        fail(f"평가 파일을 찾을 수 없음: {args.assessment}")
    assessment = parse_assessment(assessment_path, record["kind"])
    if record.get("review"):
        record.setdefault("history", []).append(compact_history(record))
    record["review"] = {
        "reviewed_at": date.today().isoformat(),
        **assessment,
        "status": "revise",
    }
    refresh_review_statuses(registry)
    registry["updated_at"] = date.today().isoformat()
    save_yaml(REGISTRY_PATH, registry)
    print(
        f"평가 기록: {record['path']} -> {record['review']['status']} "
        f"({record['review']['points']:.2f}/100)"
    )


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
    paths = []
    for name in sorted(names):
        if name.startswith("docs/") and name.endswith(".md"):
            candidate = ROOT / name
            if candidate.is_file():
                paths.append(candidate)
    return paths


def check_documents(paths: list[Path]) -> None:
    registry = load_registry()
    records = {item["path"]: item for item in registry["documents"]}
    errors: list[str] = []
    current_paths = {relative_path(path) for path in all_docs()}
    recorded_paths = set(records)
    for missing in sorted(current_paths - recorded_paths):
        errors.append(f"{missing}: 품질 기록이 없다")
    for removed in sorted(recorded_paths - current_paths):
        errors.append(f"{removed}: 삭제된 문서의 품질 기록이 남아 있다")
    excluded_count = 0
    for path in paths:
        relative = relative_path(path)
        record = records.get(relative)
        if not record:
            if relative not in current_paths - recorded_paths:
                errors.append(f"{relative}: 품질 기록이 없다")
            continue
        if record.get("source_hash") != source_hash(path):
            errors.append(f"{relative}: 문서가 평가 후 변경되었다")
        if not record.get("topic") or not record.get("scope"):
            errors.append(f"{relative}: topic 또는 scope metadata가 없다")
        if record.get("automatic_check") != "pass":
            errors.append(f"{relative}: 자동 검사 오류가 있다")
        review = record.get("review")
        if not review:
            errors.append(f"{relative}: 읽기 평가가 없다")
            continue
        status = review.get("status")
        if record.get("kind") in excluded_kinds():
            if status != "excluded":
                errors.append(f"{relative}: 제외 문서의 품질 상태가 {status!r}이다")
            else:
                excluded_count += 1
            continue
        if status != "pass":
            errors.append(f"{relative}: 품질 상태가 {status!r}이다")
    if errors:
        print("품질 검사 실패:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        raise SystemExit(1)
    print(
        f"품질 검사 통과: 평가 대상 {len(paths) - excluded_count}개, "
        f"제외 {excluded_count}개"
    )


def report() -> None:
    registry = load_registry()
    print("상태      총점   글자  설명요소  그림  표  수식  코드  문서")
    for record in registry["documents"]:
        review = record.get("review") or {}
        metrics = record["metrics"]
        status = review.get("status", "pending")
        overall = review.get("overall")
        overall_text = f"{overall:.2f}" if isinstance(overall, (int, float)) else "-"
        elements = metrics["explanatory_elements"]
        print(
            f"{status:<9} {overall_text:>5} {metrics['characters']:>6} {elements['total']:>8} "
            f"{elements['figures']:>5} {elements['tables']:>3} {elements['equations']:>5} "
            f"{elements.get('code_blocks', 0):>5}  "
            f"{record['path']}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("sync", help="docs/와 품질 기록 전체를 동기화한다")

    review_parser = subparsers.add_parser(
        "review", help="유사 문서와 정량 비교한 뒤 근거 기반 채점표를 기록한다"
    )
    review_parser.add_argument("path")
    review_parser.add_argument(
        "--assessment",
        required=True,
        help="현재 채점표 형식의 YAML 평가 파일",
    )
    review_parser.add_argument(
        "--reference",
        dest="references",
        action="append",
        required=True,
        help="Codex가 topic과 scope를 읽고 선택한 유사 문서; 두 번 이상 지정",
    )

    check_parser = subparsers.add_parser("check", help="품질 기록이 최신이고 통과 상태인지 검사한다")
    check_parser.add_argument("paths", nargs="*")
    check_parser.add_argument("--all", action="store_true")
    check_parser.add_argument("--changed", action="store_true")

    subparsers.add_parser("report", help="전체 품질 표를 출력한다")
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
    elif args.command == "check":
        sync_registry()
        check_documents(selected_paths(args))
    elif args.command == "report":
        sync_registry()
        report()


if __name__ == "__main__":
    main()
