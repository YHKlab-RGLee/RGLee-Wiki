#!/usr/bin/env bash

set -Eeuo pipefail

readonly PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

usage() {
    printf '사용법:\n'
    printf '  %s serve\n' "$0"
    printf '  %s build\n' "$0"
    printf '  %s publish "Commit message"\n' "$0"
}

require_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        printf '오류: 필요한 명령을 찾을 수 없음: %s\n' "$1" >&2
        exit 1
    fi
}

run_mkdocs() {
    require_command python3
    if ! python3 -c 'import mkdocs' >/dev/null 2>&1; then
        printf '오류: MkDocs가 설치되지 않았습니다.\n' >&2
        printf '먼저 다음 명령을 실행하십시오: python3 -m pip install -r requirements.txt\n' >&2
        exit 1
    fi
    python3 -m mkdocs "$@"
}

build_site() {
    run_mkdocs build --strict --clean
    printf '빌드 완료: %s/site/\n' "$PROJECT_ROOT"
}

publish_site() {
    local commit_message="${1:-}"
    if [[ -z "${commit_message//[[:space:]]/}" ]]; then
        printf '오류: 비어 있지 않은 커밋 메시지가 필요합니다.\n' >&2
        usage
        exit 1
    fi

    require_command git
    build_site

    local -a changed_paths=()
    mapfile -d '' changed_paths < <(
        {
            git diff --name-only -z
            git diff --cached --name-only -z
            git ls-files --others --exclude-standard -z
        } | sort -zu
    )

    if (( ${#changed_paths[@]} == 0 )); then
        printf '게시할 변경 사항이 없습니다.\n'
        exit 0
    fi

    printf '커밋할 파일:\n'
    printf '  %s\n' "${changed_paths[@]}"
    printf '위 파일을 커밋하고 현재 브랜치의 upstream으로 push합니까? [y/N] '
    read -r confirmation
    if [[ ! "$confirmation" =~ ^[Yy]$ ]]; then
        printf '게시를 취소했습니다.\n'
        exit 1
    fi

    git add -A -- "${changed_paths[@]}"
    git diff --cached --check
    git diff --cached --stat
    git commit -m "$commit_message"
    git push
}

case "${1:-}" in
    serve)
        run_mkdocs serve --dev-addr 0.0.0.0:8000
        ;;
    build)
        build_site
        ;;
    publish)
        publish_site "${2:-}"
        ;;
    *)
        usage
        exit 1
        ;;
esac

