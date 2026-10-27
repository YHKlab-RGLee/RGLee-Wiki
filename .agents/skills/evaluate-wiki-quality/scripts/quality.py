#!/usr/bin/env python3
"""Deterministic checks and compact review attestations for the wiki."""

from __future__ import annotations

import argparse
import difflib
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
RUBRIC_VERSION = 4
LEGACY_RUBRIC_VERSIONS = (3,)
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
    # Preserve inline mathematics before matching HTML: G^< ... G^> is not a tag.
    text = re.sub(
        r"(?<!\\)\$(?!\$)(?:\\.|[^$])*\$|<[^>]+>",
        lambda match: match.group(0) if match.group(0).startswith("$") else "",
        text,
        flags=re.DOTALL,
    )
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

    # Exclude Markdown code spans and MathJax delimiters before link matching.
    link_text = re.sub(r"(`+).*?\1", "", body_without_code, flags=re.DOTALL)
    link_text = re.sub(r"\$\$.*?\$\$|(?<!\\)\$(?!\$).*?(?<!\\)\$", "", link_text, flags=re.DOTALL)
    for match in re.finditer(r"(!?)\[([^\]]*)\]\(([^)]+)\)", link_text):
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


def local_assets(path: Path) -> dict[str, str]:
    """Track Markdown-local scientific figures separately from prose hashes."""
    assets = {}
    text = without_code(path.read_text(encoding="utf-8"))
    for target in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text):
        target = target.strip().split()[0].strip("<>").split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "data:")):
            continue
        asset = (path.parent / target).resolve()
        if asset.is_relative_to(DOCS.resolve()):
            assets[relative_path(asset)] = hashlib.sha256(asset.read_bytes()).hexdigest() if asset.is_file() else "missing"
    return assets


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
        "assets": local_assets(path),
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


def review_model(value: Any = None) -> dict[str, str]:
    if value is None:
        value = {}
    fields = ("name", "reasoning_effort", "source")
    if not isinstance(value, dict) or set(value) - set(fields):
        fail("model에는 name, reasoning_effort, source만 사용할 수 있음")
    result = {}
    for field in fields:
        item = value.get(field)
        if item is not None and not isinstance(item, str):
            fail(f"model.{field}는 문자열 또는 빈 값이어야 함")
        result[field] = (item or "").strip()
    return result


def pending_review(scope: str) -> dict[str, Any]:
    return {"status": "pending", "required_scope": scope, "model": review_model()}


def excluded_review() -> dict[str, Any]:
    return {
        "status": "excluded",
        "reason": "Home과 index는 navigation hub이므로 scientific review에서 제외한다.",
    }


def rubric_definition() -> dict[str, Any]:
    rubric = load_yaml(RUBRIC_PATH, {})
    required = {"version", "finding_statuses", "categories", "methods"}
    missing = required - set(rubric)
    if missing:
        fail(f"rubric 필수 항목이 없음: {', '.join(sorted(missing))}")
    if rubric["version"] != RUBRIC_VERSION:
        fail("검증 규칙 version이 checker와 다르다")
    return rubric


def imported_review(previous: dict[str, Any], measured: dict[str, Any]) -> dict[str, Any]:
    if measured["kind"] in ("home", "index"):
        return excluded_review()
    # A changed hash algorithm cannot establish scientific equivalence.
    return {**pending_review("facts"), "legacy_review": deepcopy(previous.get("review", {}))}


def preserve_review(previous: dict[str, Any], measured: dict[str, Any]) -> dict[str, Any]:
    if measured["kind"] in ("home", "index"):
        return excluded_review()
    review = deepcopy(previous.get("review") or pending_review("facts"))
    old_hashes = previous.get("hashes", {})
    same_content = old_hashes.get("content") == measured["hashes"]["content"]
    same_outline = old_hashes.get("outline") == measured["hashes"]["outline"]
    same_source = old_hashes.get("source") == measured["hashes"].get("source")
    same_assets = previous.get("assets", measured.get("assets", {})) == measured.get("assets", {})
    known_version = review.get("rubric_version") in (RUBRIC_VERSION, *LEGACY_RUBRIC_VERSIONS)
    if review.get("status") == "pass" and same_content and same_outline and same_source and same_assets and known_version:
        return review
    # Pending obligations and failed-review evidence survive further edits/syncs.
    if review.get("status") == "pass":
        baseline = {"path": previous.get("path"), "hashes": deepcopy(old_hashes),
                    "assets": previous.get("assets", {}), "review": review}
        review = {**pending_review("facts"), "last_pass": review, "baseline": baseline}
    review["required_scope"] = "facts"
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
        and not (ROOT / record["path"]).exists()
        and record.get("kind") == measured["kind"]
        and record.get("hashes", {}).get("content") == measured["hashes"]["content"]
        and record.get("hashes", {}).get("outline") == measured["hashes"]["outline"]
    ]
    return candidates[0] if len(candidates) == 1 else None


def polish_review(previous: dict[str, Any], measured: dict[str, Any]) -> dict[str, Any]:
    review = deepcopy(previous.get("review") or {})
    if (review.get("status") != "pass"
            or review.get("rubric_version") not in (RUBRIC_VERSION, *LEGACY_RUBRIC_VERSIONS)
            or any(review.get(f"{key}_hash") != previous.get("hashes", {}).get(key)
                   for key in ("content", "outline"))):
        fail(f"윤문 승계에는 유효한 기존 pass가 필요함: {measured['path']}")
    if sorted(previous.get("assets", measured.get("assets", {})).values()) != sorted(measured.get("assets", {}).values()):
        fail("그림 파일 변경은 의미 보존 승계할 수 없음: 사실 검증이 필요하다")
    if previous["hashes"] == measured["hashes"]:
        return review
    review.setdefault("scientific_review", deepcopy(review))
    review["polish"] = {
        "updated_at": date.today().isoformat(),
        "from_source_hash": previous["hashes"]["source"],
        "to_source_hash": measured["hashes"]["source"],
    }
    for key in ("content", "outline"):
        review[f"{key}_hash"] = measured["hashes"][key]
    review["source_hash"] = measured["hashes"]["source"]
    if review.get("rubric_version") == RUBRIC_VERSION:
        review["assets"] = measured.get("assets", {})
    return review


def sync_registry(verbose: bool = True, paths: list[str] | None = None,
                  polish: bool = False) -> dict[str, Any]:
    if polish and not paths:
        fail("윤문 동기화에는 문서 경로가 필요함")
    old = load_yaml(REGISTRY_PATH, default_registry())
    legacy = (
        old.get("schema_version") != SCHEMA_VERSION
        or old.get("hash_version") != HASH_VERSION
    )
    previous_records = old.get("documents", []) if isinstance(old, dict) else []
    by_path = {record.get("path"): record for record in previous_records}
    selected = None
    targets = None
    if paths is not None:
        if not paths:
            fail("동기화할 문서 경로가 필요함")
        if legacy:
            fail("이전 registry schema/hash는 전체 sync로 먼저 갱신해야 함")
        selected = set()
        targets = []
        for raw_path in paths:
            path = Path(raw_path)
            path = (path if path.is_absolute() else ROOT / path).resolve()
            if not path.is_relative_to(DOCS.resolve()) or path.suffix != ".md":
                fail(f"docs/ 아래 Markdown 경로가 필요함: {raw_path}")
            key = relative_path(path)
            if key in selected:
                continue
            if path.is_file():
                targets.append(path)
            elif path.exists() or key not in by_path:
                fail(f"문서 또는 삭제할 기존 기록을 찾을 수 없음: {raw_path}")
            selected.add(key)
    used_paths: set[str] = set()
    records: list[dict[str, Any]] = [
        record for record in previous_records
        if selected is not None and record.get("path") not in selected
    ]
    move_candidates = previous_records if selected is None else [
        record for record in previous_records if record.get("path") in selected
    ]
    changes = {"added": 0, "content": 0, "outline": 0, "presentation": 0, "moved": 0}

    for path in all_docs() if targets is None else sorted(targets):
        measured = measure(path)
        previous = by_path.get(measured["path"])
        if previous is None and not legacy:
            previous = find_move_candidate(measured, move_candidates, used_paths)
            if previous:
                changes["moved"] += 1
        if polish and measured["kind"] == "article" and previous is None:
            fail(f"새 문서는 윤문 승계할 수 없음: {measured['path']}")
        if previous:
            used_paths.add(previous.get("path", ""))
            if legacy:
                review = imported_review(previous, measured)
            else:
                review = (polish_review(previous, measured)
                          if polish and measured["kind"] == "article"
                          else preserve_review(previous, measured))
                old_hashes = previous.get("hashes", {})
                if old_hashes.get("content") != measured["hashes"]["content"]:
                    changes["content"] += 1
                elif old_hashes.get("outline") != measured["hashes"]["outline"]:
                    changes["outline"] += 1
                elif old_hashes.get("presentation") != measured["hashes"]["presentation"]:
                    changes["presentation"] += 1
        else:
            review = excluded_review() if measured["kind"] in ("home", "index") else pending_review("facts")
            changes["added"] += 1
        records.append({**measured, "review": review})

    records.sort(key=lambda record: record["path"])
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


def require_keys(value: Any, keys: set[str], label: str, optional: set[str] | None = None) -> None:
    if not isinstance(value, dict) or set(value) - keys - (optional or set()) or keys - set(value):
        fail(f"{label} 항목 불일치: 필수={sorted(keys)}")


def valid_sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        fail(f"{label}: SHA-256이 필요하다")
    return value


def evidence_file(raw: str) -> Path:
    path = (ROOT / raw).resolve()
    if not path.is_relative_to((QUALITY_DIR / "evidence").resolve()) or not path.is_file():
        fail(f"영속 검토 근거 파일을 찾을 수 없음: {raw}")
    return path


def parse_assessment(path: Path) -> dict[str, Any]:
    assessment = load_yaml(path, {})
    require_keys(assessment, {"scope", "source_hash", "assets", "coverage", "findings", "summary"}, "assessment", {"model"})
    if assessment["scope"] != "facts":
        fail("새 검토는 scope: facts만 등록한다. 이전 full/outline 점수 평가는 이력으로 보존한다")
    valid_sha(assessment["source_hash"], "source_hash")
    if not isinstance(assessment["assets"], dict):
        fail("assets에는 검토한 로컬 이미지 경로와 SHA-256 mapping이 필요하다")
    for asset, digest in assessment["assets"].items():
        required_text(asset, "asset path")
        valid_sha(digest, "asset hash")
    coverage = assessment["coverage"]
    require_keys(coverage, {"mode", "baseline_source_hash", "checked", "dependencies", "reused_evidence"}, "coverage")
    if coverage["mode"] not in ("full", "changes"):
        fail("coverage.mode는 full 또는 changes이다")
    if coverage["mode"] == "changes":
        valid_sha(coverage["baseline_source_hash"], "baseline_source_hash")
    elif coverage["baseline_source_hash"] is not None:
        fail("full 검증은 baseline_source_hash를 null로 둔다")
    coverage["checked"] = required_text_list(coverage["checked"], "coverage.checked")
    if not isinstance(coverage["dependencies"], list):
        fail("dependencies는 list이다")
    coverage["dependencies"] = [required_text(item, "dependency") for item in coverage["dependencies"]]
    if not isinstance(coverage["reused_evidence"], list):
        fail("reused_evidence는 list이다")
    for item in coverage["reused_evidence"]:
        require_keys(item, {"path", "sha256", "scope"}, "reused evidence")
        original = evidence_file(required_text(item["path"], "evidence.path"))
        if hashlib.sha256(original.read_bytes()).hexdigest() != valid_sha(item["sha256"], "evidence.sha256"):
            fail("재사용 근거 파일이 기록한 SHA-256과 다르다")
        required_text(item["scope"], "reused evidence.scope")
    findings = assessment["findings"]
    if not isinstance(findings, list) or not findings:
        fail("검증한 주장 또는 주장 묶음이 하나 이상 필요하다")
    rules = rubric_definition()
    seen = set()
    for item in findings:
        require_keys(item, {"id", "claim", "locations", "category", "status", "method", "sources", "check", "assumptions"}, "finding")
        identifier = required_text(item["id"], "finding.id")
        if identifier in seen:
            fail(f"중복 finding id: {identifier}")
        seen.add(identifier)
        for key in ("claim", "check", "assumptions"):
            required_text(item[key], f"finding.{key}")
        required_text_list(item["locations"], "finding.locations")
        if item["status"] not in rules["finding_statuses"] or item["category"] not in rules["categories"] or item["method"] not in rules["methods"]:
            fail("알 수 없는 finding status/category/method")
        if not isinstance(item["sources"], list):
            fail("finding.sources는 list이다")
        provenance = set()
        identifiers = set()
        for source in item["sources"]:
            require_keys(source, {"id", "provenance", "locator", "supports"}, "source")
            for key, value in source.items():
                required_text(value, f"source.{key}")
            provenance.add(source["provenance"].strip().casefold())
            identifiers.add(source["id"].strip().casefold())
        minimum = rules["categories"][item["category"]]["minimum_sources"]
        if item["status"] == "supported" and (len(provenance) < minimum or len(identifiers) < minimum):
            fail(f"{identifier}: 확인 판정에 필요한 독립 출처가 {minimum}개 미만이다")
    assessment["model"] = review_model(assessment.get("model"))
    assessment["summary"] = required_text(assessment["summary"], "summary")
    return assessment


def baseline_record(record: dict[str, Any]) -> dict[str, Any] | None:
    review = record.get("review") or {}
    if review.get("status") == "pass":
        return record
    if review.get("baseline"):
        return review["baseline"]
    prior = review.get("last_pass")
    if prior:
        source = prior.get("source_hash") or prior.get("polish", {}).get("to_source_hash")
        if not source and prior.get("evidence_path"):
            source = load_yaml(evidence_file(prior["evidence_path"]), {}).get("hashes", {}).get("source")
        return {"path": record["path"], "hashes": {"source": source}, "review": prior}
    return None


def baseline_text(record: dict[str, Any]) -> tuple[dict[str, Any], str]:
    baseline = baseline_record(record)
    if not baseline or not baseline.get("hashes", {}).get("source"):
        fail("마지막 검증 버전을 복원할 수 없음: full 범위 검증이 필요하다")
    expected = baseline["hashes"]["source"]
    path = baseline.get("path") or record["path"]
    current = ROOT / path
    if current.is_file() and hashlib.sha256(current.read_bytes()).hexdigest() == expected:
        return baseline, current.read_text(encoding="utf-8")
    # Follow the recorded path through history, not merely HEAD~1 or the worktree diff.
    history = subprocess.run(["git", "log", "--all", "--format=%H", "--", path], cwd=ROOT,
                             check=True, capture_output=True, text=True)
    for commit in history.stdout.splitlines():
        result = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, capture_output=True)
        if result.returncode == 0 and hashlib.sha256(result.stdout).hexdigest() == expected:
            return baseline, result.stdout.decode("utf-8")
    fail("기록한 source hash를 Git에서 찾을 수 없음: 검증 범위를 full로 확장하거나 정확한 이력을 복원하십시오")


def show_baseline(raw_path: str) -> None:
    path = resolve_doc(raw_path)
    record = next((r for r in load_yaml(REGISTRY_PATH, default_registry())["documents"]
                   if r["path"] == relative_path(path)), None)
    if record is None:
        fail("새 문서: full 범위 사실 검증이 필요하다")
    baseline, text = baseline_text(record)
    print(f"baseline source: {baseline['hashes']['source']}")
    print(f"current source: {hashlib.sha256(path.read_bytes()).hexdigest()}")
    print(f"baseline evidence: {baseline['review'].get('evidence_path', '없음')}")
    print("".join(difflib.unified_diff(text.splitlines(True), path.read_text(encoding="utf-8").splitlines(True),
                                     fromfile=baseline.get("path") or record["path"], tofile=relative_path(path))), end="")
    if baseline.get("assets", baseline["review"].get("assets", {})) != local_assets(path):
        print("그림 파일 목록/해시 차이도 검토하십시오 (이전 기록에 그림 해시가 없을 수 있음).")


def benchmark_document(raw_path: str) -> None:
    measured = measure(resolve_doc(raw_path))
    print(f"참고 통계 (통과 기준 아님): 글자 {measured['metrics']['characters']}, "
          f"설명요소 {measured['metrics']['explanatory_elements']['total']}")


def review_document(args: argparse.Namespace) -> None:
    path = resolve_doc(args.path)
    measured = measure(path)
    if measured["kind"] != "article":
        fail("article만 scientific review 대상이다")
    registry = load_yaml(REGISTRY_PATH, default_registry())
    if registry.get("schema_version") != SCHEMA_VERSION:
        fail("registry schema를 먼저 확인하십시오")
    record = next((r for r in registry["documents"] if r["path"] == measured["path"]), None)
    if not record or record.get("hashes") != measured["hashes"] or record.get("assets", {}) != measured["assets"]:
        fail("문서 변경 뒤 ./quality.sh sync를 먼저 실행하십시오")
    if measured["automatic_check"] != "pass":
        fail(f"automatic check가 실패함: {', '.join(measured['issues'])}")
    assessment_path = Path(args.assessment)
    assessment_path = assessment_path if assessment_path.is_absolute() else ROOT / assessment_path
    if not assessment_path.is_file():
        fail(f"평가 파일을 찾을 수 없음: {args.assessment}")
    assessment = parse_assessment(assessment_path)
    if assessment["source_hash"] != measured["hashes"]["source"]:
        fail("검토한 문서와 현재 source hash가 다르다")
    if assessment["assets"] != measured["assets"]:
        fail("검토한 그림 목록 또는 hash가 현재 파일과 다르다")
    baseline = None
    if assessment["coverage"]["mode"] == "changes":
        baseline, _text = baseline_text(record)
        if baseline["hashes"]["source"] != assessment["coverage"]["baseline_source_hash"]:
            fail("마지막 검증 버전과 assessment baseline이 다르다")
        # Reuse is explicit, integrity checked, and scoped. A previous pass is not new verification.
        prior_path = baseline["review"].get("evidence_path")
        reused = assessment["coverage"]["reused_evidence"]
        if not prior_path or prior_path not in {item["path"] for item in reused}:
            fail("changes 검증에는 이전 검토 근거와 재사용 범위가 필요하다; 없으면 full로 검증한다")
    states = {item["status"] for item in assessment["findings"]}
    status = "revise" if "mismatch" in states else "unverified" if states - {"supported"} else "pass"
    evidence = {"page": measured["path"], "hashes": measured["hashes"], "assets": measured["assets"],
                "rubric_version": RUBRIC_VERSION, "assessment": assessment}
    serialized = yaml.safe_dump(evidence, allow_unicode=True, sort_keys=True)
    evidence_path = QUALITY_DIR / "evidence" / (hash_text(serialized) + ".yaml")
    review = {"status": status, "scope": "facts", "coverage": assessment["coverage"]["mode"],
              "rubric_version": RUBRIC_VERSION, "reviewed_at": date.today().isoformat(),
              "model": assessment["model"], "source_hash": measured["hashes"]["source"],
              "content_hash": measured["hashes"]["content"], "outline_hash": measured["hashes"]["outline"],
              "assets": measured["assets"], "evidence_path": relative_path(evidence_path),
              "finding_counts": {s: sum(i["status"] == s for i in assessment["findings"])
                                 for s in rubric_definition()["finding_statuses"]},
              "summary": assessment["summary"]}
    if status != "pass":
        review["required_scope"] = "facts"
        previous = baseline_record(record)
        if previous:
            review["baseline"] = previous
            review["last_pass"] = previous["review"]
    record["review"] = review
    save_yaml(evidence_path, evidence)
    registry["updated_at"] = date.today().isoformat()
    registry["rubric_version"] = RUBRIC_VERSION
    save_yaml(REGISTRY_PATH, registry)
    print(f"사실 검증 기록: {record['path']} -> {status} ({review['coverage']}, 점수 없음)")


def fact_evidence_issues(review: dict[str, Any], visited: set[str] | None = None) -> list[str]:
    original = review.get("scientific_review", review)
    raw_path = original.get("evidence_path", "")
    visited = set() if visited is None else visited
    if raw_path in visited:
        return []
    visited.add(raw_path)
    path = ROOT / raw_path
    if not raw_path or not path.is_file():
        return ["사실 검증 근거 파일이 없다"]
    evidence = load_yaml(path, {})
    digest = hash_text(yaml.safe_dump(evidence, allow_unicode=True, sort_keys=True))
    if path.stem != digest:
        return ["사실 검증 근거 파일의 hash가 다르다"]
    if evidence.get("hashes", {}).get("source") != original.get("source_hash"):
        return ["사실 검증 근거와 검토 source hash가 다르다"]
    assessment = evidence.get("assessment", {})
    if assessment.get("scope") != "facts" or not assessment.get("findings"):
        return ["사실 검증 근거의 형식이 잘못되었다"]
    if any(item.get("status") != "supported" for item in assessment["findings"]):
        return ["미해결 finding이 있는 근거를 pass로 기록했다"]
    for reused in assessment.get("coverage", {}).get("reused_evidence", []):
        reused_path = ROOT / reused.get("path", "")
        if not reused_path.is_file() or hashlib.sha256(reused_path.read_bytes()).hexdigest() != reused.get("sha256"):
            return ["재사용한 근거 파일이 없거나 변경됐다"]
        prior = load_yaml(reused_path, {})
        if prior.get("rubric_version") == RUBRIC_VERSION:
            issues = fact_evidence_issues({"evidence_path": reused["path"],
                                          "source_hash": prior.get("hashes", {}).get("source")}, visited)
            if issues:
                return issues
    return []


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
    paths = {
        ROOT / name
        for name in sorted(names)
        if name.startswith("docs/") and name.endswith(".md") and (ROOT / name).is_file()
    }
    # Include consumers when an asset changes but its Markdown does not.
    asset_names = {name for name in names if name.startswith("docs/") and not name.endswith(".md")}
    if asset_names:
        for path in all_docs():
            if asset_names.intersection(local_assets(path)):
                paths.add(path)
        for record in load_yaml(REGISTRY_PATH, default_registry()).get("documents", []):
            if asset_names.intersection(record.get("assets", {})) and (ROOT / record["path"]).is_file():
                paths.add(ROOT / record["path"])
    # A record-only refresh after a committed docs edit must still be checked.
    registry_name = relative_path(REGISTRY_PATH)
    if registry_name in names:
        before = subprocess.run(["git", "show", f"HEAD:{registry_name}"], cwd=ROOT, capture_output=True, text=True)
        old = yaml.safe_load(before.stdout) if before.returncode == 0 else {}
        old_records = {r["path"]: r for r in (old or {}).get("documents", [])}
        for record in load_yaml(REGISTRY_PATH, default_registry()).get("documents", []):
            path = ROOT / record["path"]
            if old_records.get(record["path"]) != record and path.is_file():
                paths.add(path)
    return sorted(paths)


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
        if review.get("rubric_version") not in (RUBRIC_VERSION, *LEGACY_RUBRIC_VERSIONS):
            errors.append(f"{measured['path']}: review rubric version이 오래되었다")
        if review.get("rubric_version") == RUBRIC_VERSION:
            if review.get("source_hash") != measured["hashes"]["source"]:
                errors.append(f"{measured['path']}: 검토 source hash가 현재 문서와 다르다")
            if review.get("assets", {}) != measured["assets"]:
                errors.append(f"{measured['path']}: 검토한 그림 파일이 변경됐다")
            errors.extend(f"{measured['path']}: {issue}" for issue in fact_evidence_issues(review))
        elif "assets" in record and record["assets"] != measured["assets"]:
            errors.append(f"{measured['path']}: 동기화 후 그림 파일이 변경됐다")
    if errors:
        print("품질 검사 실패:", file=sys.stderr)
        for error in sorted(set(errors)):
            print(f"  - {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"품질 검사 통과: article {len(paths) - excluded}개, index/home {excluded}개")


def report(paths: list[Path] | None = None) -> None:
    registry = load_yaml(REGISTRY_PATH, default_registry())
    selected = None if paths is None else {relative_path(path) for path in paths}
    print("상태         검토 방식/범위             문서")
    for record in registry.get("documents", []):
        if selected is not None and record["path"] not in selected:
            continue
        review = record.get("review") or {}
        scope = review.get("required_scope", review.get("coverage", review.get("scope", "-")))
        basis = "legacy (이전 제도)" if review.get("rubric_version") in LEGACY_RUBRIC_VERSIONS else scope
        print(
            f"{review.get('status', 'missing'):<9} "
            f"{basis:<24} {record['path']}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    sync_parser = subparsers.add_parser("sync", help="지정 문서 또는 전체 derived metadata를 갱신한다")
    sync_parser.add_argument("paths", nargs="*", help="이동은 이전·새 경로를 함께 지정한다")
    sync_parser.add_argument("--polish", "--non-scientific", dest="polish", action="store_true", help="의미 보존을 확인한 변경의 기존 review를 승계한다")
    review_parser = subparsers.add_parser("review", help="점수 없는 사실 검증 결과를 기록한다")
    review_parser.add_argument("path")
    review_parser.add_argument("--assessment", required=True)
    benchmark_parser = subparsers.add_parser(
        "benchmark", help="글자/설명요소 수를 참고 통계로 출력한다 (통과 기준 아님)"
    )
    benchmark_parser.add_argument("path")
    baseline_parser = subparsers.add_parser("baseline", help="마지막 검증 버전과 현재 문서의 diff를 출력한다 (read-only)")
    baseline_parser.add_argument("path")
    check_parser = subparsers.add_parser("check", help="파일을 쓰지 않고 현재 상태를 검사한다")
    check_parser.add_argument("paths", nargs="*")
    check_parser.add_argument("--all", action="store_true")
    check_parser.add_argument("--changed", action="store_true")
    subparsers.add_parser("check-nav", help="article review와 무관한 navigation 규칙만 검사한다")
    report_parser = subparsers.add_parser("report", help="파일을 쓰지 않고 현재 registry를 출력한다")
    report_parser.add_argument("paths", nargs="*")
    report_parser.add_argument("--changed", action="store_true")
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
        sync_registry(paths=args.paths or None, polish=args.polish)
    elif args.command == "review":
        review_document(args)
    elif args.command == "benchmark":
        benchmark_document(args.path)
    elif args.command == "baseline":
        show_baseline(args.path)
    elif args.command == "check":
        check_documents(selected_paths(args))
    elif args.command == "check-nav":
        check_navigation()
    elif args.command == "report":
        report(selected_paths(args) if args.changed or args.paths else None)


if __name__ == "__main__":
    main()
