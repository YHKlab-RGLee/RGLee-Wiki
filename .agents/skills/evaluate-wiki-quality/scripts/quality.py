#!/usr/bin/env python3
"""Collect and check simple, human-readable quality records for this wiki."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import math
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
METRIC_VERSION = 3
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
        "metric_version": METRIC_VERSION,
        "metrics": metrics,
        "automatic_check": "pass" if not issues else "fail",
        "issues": issues,
    }


def default_registry() -> dict[str, Any]:
    rubric = load_yaml(RUBRIC_PATH, {})
    return {
        "schema_version": 2,
        "rubric_version": rubric.get("version", 1),
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
        measured["history"] = history
        updated[relative] = measured

    for relative in sorted(set(existing) - set(current)):
        archived = deepcopy(existing[relative])
        archived["deleted_at"] = date.today().isoformat()
        registry["archived_documents"].append(archived)
        changes["deleted"].append(relative)

    defaults = default_registry()
    registry["schema_version"] = defaults["schema_version"]
    registry["rubric_version"] = defaults["rubric_version"]
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
        if review.get("mode") == "baseline":
            review["status"] = "baseline"
            continue
        scores = review["scores"].values()
        absolute_pass = (
            record["automatic_check"] == "pass"
            and min(scores) >= float(rules["minimum_each"])
            and float(review["overall"]) >= float(rules["minimum_overall"])
        )
        review["status"] = "pass" if absolute_pass else "revise"


def review_document(args: argparse.Namespace) -> None:
    path = resolve_doc(args.path)
    if args.baseline and load_registry().get("baseline_completed"):
        fail("기존 문서의 baseline 이관이 이미 완료되어 --baseline을 사용할 수 없음")
    registry, _ = sync_registry(verbose=False)
    record = next(item for item in registry["documents"] if item["path"] == relative_path(path))
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
    scores = {
        "content": round(args.content, 1),
        "evidence": round(args.evidence, 1),
        "explanation": round(args.explanation, 1),
        "format": round(args.format, 1),
    }
    if any(not math.isfinite(score) or score < 0 or score > 10 for score in scores.values()):
        fail("점수는 0에서 10 사이여야 함")
    summary = args.summary.strip()
    if not summary:
        fail("평가 요약은 비워 둘 수 없음")
    if not re.search(r"[가-힣]", summary):
        fail("평가 요약은 한국어 문장을 포함해야 함")
    if record.get("review"):
        record.setdefault("history", []).append(compact_history(record))
    record["review"] = {
        "mode": "baseline" if args.baseline else "gate",
        "reviewed_at": date.today().isoformat(),
        "scores": scores,
        "overall": round(sum(scores.values()) / len(scores), 2),
        "summary": summary,
        "status": "baseline" if args.baseline else "revise",
    }
    refresh_review_statuses(registry)
    registry["updated_at"] = date.today().isoformat()
    save_yaml(REGISTRY_PATH, registry)
    print(f"평가 기록: {record['path']} -> {record['review']['status']} ({record['review']['overall']:.2f}/10)")


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


def check_documents(paths: list[Path], allow_baseline: bool) -> None:
    registry = load_registry()
    records = {item["path"]: item for item in registry["documents"]}
    errors: list[str] = []
    current_paths = {relative_path(path) for path in all_docs()}
    recorded_paths = set(records)
    for missing in sorted(current_paths - recorded_paths):
        errors.append(f"{missing}: 품질 기록이 없다")
    for removed in sorted(recorded_paths - current_paths):
        errors.append(f"{removed}: 삭제된 문서의 품질 기록이 남아 있다")
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
            errors.append(f"{relative}: LLM 평가가 없다")
            continue
        status = review.get("status")
        if status != "pass" and not (allow_baseline and status == "baseline"):
            errors.append(f"{relative}: 품질 상태가 {status!r}이다")
    if errors:
        print("품질 검사 실패:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"품질 검사 통과: {len(paths)}개 문서")


def report() -> None:
    registry = load_registry()
    print("상태      총점   글자  설명요소  그림  표  수식  코드  문서")
    for record in registry["documents"]:
        review = record.get("review") or {}
        metrics = record["metrics"]
        status = review.get("status", "unreviewed")
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
        "review", help="유사 문서와 정량 비교한 뒤 네 가지 읽기 점수를 기록한다"
    )
    review_parser.add_argument("path")
    review_parser.add_argument("--content", type=float, required=True)
    review_parser.add_argument("--evidence", type=float, required=True)
    review_parser.add_argument("--explanation", type=float, required=True)
    review_parser.add_argument("--format", type=float, required=True)
    review_parser.add_argument("--summary", required=True)
    review_parser.add_argument(
        "--reference",
        dest="references",
        action="append",
        required=True,
        help="Codex가 topic과 scope를 읽고 선택한 유사 문서; 두 번 이상 지정",
    )
    review_parser.add_argument("--baseline", action="store_true")

    check_parser = subparsers.add_parser("check", help="품질 기록이 최신이고 통과 상태인지 검사한다")
    check_parser.add_argument("paths", nargs="*")
    check_parser.add_argument("--all", action="store_true")
    check_parser.add_argument("--changed", action="store_true")
    check_parser.add_argument("--allow-baseline", action="store_true")

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
        check_documents(selected_paths(args), args.allow_baseline)
    elif args.command == "report":
        sync_registry()
        report()


if __name__ == "__main__":
    main()
