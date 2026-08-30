#!/usr/bin/env bash

set -Eeuo pipefail

readonly PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

usage() {
    printf '사용법:\n'
    printf '  %s serve\n' "$0"
    printf '  %s nav\n' "$0"
    printf '  %s changed\n' "$0"
    printf '  %s build\n' "$0"
    printf '  %s preflight\n' "$0"
}

cancel_on_interrupt() {
    printf '\n작업을 취소했습니다.\n' >&2
    exit 130
}

trap cancel_on_interrupt INT TERM

require_python_module() {
    if ! python3 -c "import $1" >/dev/null 2>&1; then
        printf '오류: 필요한 Python module을 찾을 수 없음: %s\n' "$1" >&2
        printf 'python3 -m pip install -r requirements.txt 를 먼저 실행하십시오.\n' >&2
        exit 1
    fi
}

run_mkdocs() {
    command -v python3 >/dev/null 2>&1 || {
        printf '오류: python3를 찾을 수 없음\n' >&2
        exit 1
    }
    require_python_module mkdocs
    python3 -m mkdocs "$@"
}

build_site() {
    local quality_mode="$1"
    case "$quality_mode" in
        nav) ./quality.sh check-nav ;;
        changed) ./quality.sh check --changed ;;
        all) ./quality.sh check --all ;;
        *) printf '오류: 알 수 없는 quality mode: %s\n' "$quality_mode" >&2; return 1 ;;
    esac
    if run_mkdocs build --strict --clean; then
        printf '빌드 완료: site/\n'
    else
        printf '빌드 실패\n' >&2
        return 1
    fi
}

preflight() {
    build_site all
    git diff --check
    printf '검토할 변경 파일:\n'
    {
        git diff --name-only
        git diff --cached --name-only
        git ls-files --others --exclude-standard
    } | sort -u | sed 's/^/  /'
    printf 'preflight 완료: stage, commit, push는 수행하지 않았습니다.\n'
}

case "${1:-}" in
    serve)
        run_mkdocs serve --dev-addr 0.0.0.0:8000
        ;;
    nav)
        build_site nav
        ;;
    changed)
        build_site changed
        ;;
    build)
        build_site all
        ;;
    preflight)
        preflight
        ;;
    *)
        usage
        exit 1
        ;;
esac
