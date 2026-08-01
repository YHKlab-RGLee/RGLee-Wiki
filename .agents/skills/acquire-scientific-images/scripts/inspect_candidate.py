#!/usr/bin/env python3
"""Inspect a local scientific-image candidate without third-party packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


KEBAB_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.(?:svg|png|jpe?g|webp|pdf)$")
HTTP_VALUE = re.compile(r"https?://", re.IGNORECASE)


def command_output(argv: list[str]) -> str | None:
    if shutil.which(argv[0]) is None:
        return None
    completed = subprocess.run(
        argv,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_text(value: str) -> str:
    return " ".join(value.casefold().split())


def inspect_svg(path: Path) -> dict[str, object]:
    root = ET.parse(path).getroot()
    text = normalize_text(" ".join(root.itertext()))
    external_values: list[str] = []
    element_count = 0

    for element in root.iter():
        element_count += 1
        for value in element.attrib.values():
            if HTTP_VALUE.search(value):
                external_values.append(value)

    return {
        "width": root.attrib.get("width"),
        "height": root.attrib.get("height"),
        "viewBox": root.attrib.get("viewBox"),
        "element_count": element_count,
        "embedded_text": text,
        "external_references": sorted(set(external_values)),
    }


def inspect_pdf(path: Path) -> dict[str, object]:
    info = command_output(["pdfinfo", str(path)])
    text = command_output(["pdftotext", str(path), "-"])
    return {
        "pdfinfo": info.strip() if info else None,
        "embedded_text": normalize_text(text or ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument(
        "--expect",
        action="append",
        default=[],
        help="Visible label expected in embedded SVG/PDF text; repeat as needed.",
    )
    parser.add_argument(
        "--reject-external-svg",
        action="store_true",
        help="Report SVG HTTP(S) references as a verification failure.",
    )
    args = parser.parse_args()

    path = args.path.resolve()
    if not path.is_file():
        print(json.dumps({"ok": False, "error": f"not a file: {path}"}, indent=2))
        return 1

    mime = command_output(["file", "--brief", "--mime-type", str(path)])
    result: dict[str, object] = {
        "ok": True,
        "path": str(path),
        "filename_is_lowercase_kebab_case": bool(KEBAB_NAME.fullmatch(path.name)),
        "size_bytes": path.stat().st_size,
        "sha256": sha256(path),
        "mime_type": mime.strip() if mime else None,
        "warnings": [],
    }

    warnings: list[str] = result["warnings"]  # type: ignore[assignment]
    embedded_text = ""

    try:
        if path.suffix.casefold() == ".svg":
            svg = inspect_svg(path)
            result["svg"] = svg
            embedded_text = str(svg["embedded_text"])
            if args.reject_external_svg and svg["external_references"]:
                warnings.append("SVG contains external HTTP(S) references")
        elif path.suffix.casefold() == ".pdf":
            pdf = inspect_pdf(path)
            result["pdf"] = pdf
            embedded_text = str(pdf["embedded_text"])
        elif args.expect:
            warnings.append(
                "Raster label verification is unavailable; render and inspect visually"
            )
    except (ET.ParseError, OSError) as error:
        result["ok"] = False
        result["error"] = str(error)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    expected = [normalize_text(value) for value in args.expect]
    result["expected_labels"] = {
        original: normalize_text(original) in embedded_text
        for original in args.expect
    }
    missing = [
        original
        for original, present in result["expected_labels"].items()
        if not present
    ]
    if missing:
        warnings.append(
            "Expected labels not verified in embedded text: " + ", ".join(missing)
        )
    if expected and not embedded_text:
        warnings.append(
            "No embedded text was extractable; labels may be vector paths and need visual inspection"
        )

    if not result["filename_is_lowercase_kebab_case"]:
        warnings.append("Filename is not lowercase kebab-case")

    result["ok"] = not warnings
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
