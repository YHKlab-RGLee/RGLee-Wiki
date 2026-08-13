#!/usr/bin/env bash

set -Eeuo pipefail

readonly PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

if ! command -v python3 >/dev/null 2>&1; then
    printf '오류: 필요한 명령을 찾을 수 없음: python3\n' >&2
    exit 1
fi

if ! python3 -c 'import yaml' >/dev/null 2>&1; then
    printf '오류: PyYAML이 설치되지 않았습니다.\n' >&2
    printf '먼저 다음 명령을 실행하십시오: python3 -m pip install -r requirements.txt\n' >&2
    exit 1
fi

exec python3 -B .agents/skills/evaluate-wiki-quality/scripts/quality.py "$@"
