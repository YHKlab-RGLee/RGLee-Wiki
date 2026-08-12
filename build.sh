#!/usr/bin/env bash

set -Eeuo pipefail

readonly PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

usage() {
    printf '사용법:\n'
    printf '  %s serve\n' "$0"
    printf '  %s build\n' "$0"
    printf '  %s publish "Commit message"\n' "$0"
    printf '\nserve 종료 또는 실행 중인 작업 취소: Ctrl+C\n'
}

cancel_on_interrupt() {
    printf '\n작업을 취소했습니다. 터미널로 돌아갑니다.\n' >&2
    exit 130
}

trap cancel_on_interrupt INT TERM

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
    local build_output

    if build_output="$(run_mkdocs build --strict --clean 2>&1)"; then
        printf '빌드 완료: site/\n'
        return 0
    fi

    printf '빌드 실패\n' >&2
    if [[ -n "$build_output" ]]; then
        printf '%s\n' "$build_output" >&2
    fi
    return 1
}

validate_prospective_commit() {
    local -n paths_ref=$1
    local git_index git_objects temporary_git_state temporary_index
    local temporary_objects check_output

    git_index="$(git rev-parse --git-path index)"
    git_objects="$(git rev-parse --git-path objects)"
    if [[ "$git_objects" != /* ]]; then
        git_objects="$PROJECT_ROOT/$git_objects"
    fi

    temporary_git_state="$(mktemp -d "${TMPDIR:-/tmp}/wiki-publish-git.XXXXXX")"
    temporary_index="$temporary_git_state/index"
    temporary_objects="$temporary_git_state/objects"
    mkdir -- "$temporary_objects"

    if [[ -f "$git_index" ]]; then
        cp -- "$git_index" "$temporary_index"
    else
        GIT_INDEX_FILE="$temporary_index" \
            GIT_OBJECT_DIRECTORY="$temporary_objects" \
            GIT_ALTERNATE_OBJECT_DIRECTORIES="$git_objects" \
            git read-tree HEAD
    fi

    if ! GIT_INDEX_FILE="$temporary_index" \
        GIT_OBJECT_DIRECTORY="$temporary_objects" \
        GIT_ALTERNATE_OBJECT_DIRECTORIES="$git_objects" \
        git add -A -- "${paths_ref[@]}"; then
        rm -rf -- "$temporary_git_state"
        printf '오류: 게시 대상 파일을 검사용 index에 추가하지 못했습니다.\n' >&2
        return 1
    fi

    if ! check_output="$(
        GIT_INDEX_FILE="$temporary_index" \
            GIT_OBJECT_DIRECTORY="$temporary_objects" \
            GIT_ALTERNATE_OBJECT_DIRECTORIES="$git_objects" \
            git diff --cached --check
    )"; then
        rm -rf -- "$temporary_git_state"
        printf '%s\n' "$check_output" >&2
        printf '\n오류: 표시된 줄에 행 끝 공백 또는 CRLF 줄바꿈이 있습니다.\n' >&2
        printf '해당 파일을 수정한 뒤 publish를 다시 실행하십시오.\n' >&2
        printf '실제 stage 영역은 변경하지 않았고 commit과 push도 실행하지 않았습니다.\n' >&2
        return 1
    fi

    rm -rf -- "$temporary_git_state"
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

    validate_prospective_commit changed_paths

    printf '커밋할 파일:\n'
    printf '  %s\n' "${changed_paths[@]}"
    printf '위 파일을 커밋하고 현재 브랜치의 upstream으로 push합니까? [y/N, Ctrl+C=취소] '
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
