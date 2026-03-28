#!/usr/bin/env python3
"""Validate embedded CISSP_DATA in index.html."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = ROOT / "index.html"

REQUIRED_OPTION_KEYS = {"A", "B", "C", "D"}
ARTIFACT_PATTERNS = [
    re.compile(r"QUESTION\s*NO\s*:", re.IGNORECASE),
    re.compile(r"Answer\s*:\s*Explanation\s*:", re.IGNORECASE),
]


def _extract_cissp_data_blob(html: str) -> str:
    marker = "const CISSP_DATA="
    marker_idx = html.find(marker)
    if marker_idx == -1:
        raise ValueError("Could not find `const CISSP_DATA=` in index.html")

    array_start = html.find("[", marker_idx)
    if array_start == -1:
        raise ValueError("Could not find array start for CISSP_DATA")

    in_string = False
    escaping = False
    depth = 0

    for i in range(array_start, len(html)):
        ch = html[i]

        if in_string:
            if escaping:
                escaping = False
            elif ch == "\\":
                escaping = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
            continue

        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return html[array_start : i + 1]

    raise ValueError("Could not find matching array end for CISSP_DATA")


def _validate_item_shape(item: Any, idx: int, errors: list[str]) -> None:
    if not isinstance(item, dict):
        errors.append(f"Item at index {idx} is not an object")
        return

    for key in ("id", "question", "options", "answer"):
        if key not in item:
            errors.append(f"Item at index {idx} is missing `{key}`")

    if "id" in item and not isinstance(item["id"], int):
        errors.append(f"Item at index {idx} has non-integer `id`: {item['id']!r}")

    question = item.get("question")
    if question is not None and not isinstance(question, str):
        errors.append(f"Item at index {idx} has non-string `question`")

    options = item.get("options")
    if not isinstance(options, dict):
        errors.append(f"Item at index {idx} has non-object `options`")
    else:
        option_keys = set(options.keys())
        missing = REQUIRED_OPTION_KEYS - option_keys
        extra = option_keys - REQUIRED_OPTION_KEYS
        if missing:
            errors.append(f"Item id={item.get('id', idx)} missing option keys: {sorted(missing)}")
        if extra:
            errors.append(f"Item id={item.get('id', idx)} has unexpected option keys: {sorted(extra)}")
        for key in REQUIRED_OPTION_KEYS & option_keys:
            if not isinstance(options[key], str):
                errors.append(f"Item id={item.get('id', idx)} option {key} is not a string")

    answer = item.get("answer")
    if answer not in REQUIRED_OPTION_KEYS:
        errors.append(
            f"Item id={item.get('id', idx)} has invalid answer {answer!r}; expected one of A|B|C|D"
        )

    if isinstance(question, str):
        for pattern in ARTIFACT_PATTERNS:
            if pattern.search(question):
                errors.append(
                    f"Item id={item.get('id', idx)} question contains import artifact matching `{pattern.pattern}`"
                )


def validate_cissp_data() -> list[str]:
    html = INDEX_HTML.read_text(encoding="utf-8")
    blob = _extract_cissp_data_blob(html)

    try:
        data = json.loads(blob)
    except json.JSONDecodeError as exc:
        return [f"CISSP_DATA is not valid JSON: {exc}"]

    errors: list[str] = []

    if not isinstance(data, list):
        return ["CISSP_DATA is not a JSON array"]

    for idx, item in enumerate(data):
        _validate_item_shape(item, idx, errors)

    ids = [item.get("id") for item in data if isinstance(item, dict) and isinstance(item.get("id"), int)]

    if len(ids) != len(data):
        errors.append("At least one item is missing a valid integer `id`; skipping full id invariant checks")
    else:
        seen: set[int] = set()
        for item_id in ids:
            if item_id in seen:
                errors.append(f"Duplicate id detected: {item_id}")
            seen.add(item_id)

        for prev, curr in zip(ids, ids[1:]):
            if curr <= prev:
                errors.append(f"IDs must be strictly increasing; found {prev} followed by {curr}")

    return errors


def main() -> int:
    errors = validate_cissp_data()
    if errors:
        print("CISSP_DATA validation failed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print("CISSP_DATA validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
