#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "Usage: $0 INPUT.pdf PAGE OUTPUT.svg|OUTPUT.png" >&2
  exit 64
fi

input_path=$1
page_number=$2
output_path=$3

if [[ ! -f "$input_path" ]]; then
  echo "Input PDF not found: $input_path" >&2
  exit 66
fi

if [[ ! "$page_number" =~ ^[1-9][0-9]*$ ]]; then
  echo "PAGE must be a positive one-based page number" >&2
  exit 64
fi

case "$output_path" in
  *.svg)
    command -v pdftocairo >/dev/null
    pdftocairo -f "$page_number" -l "$page_number" -svg "$input_path" "$output_path"
    ;;
  *.png)
    command -v pdftoppm >/dev/null
    output_stem=${output_path%.png}
    pdftoppm \
      -f "$page_number" \
      -l "$page_number" \
      -singlefile \
      -png \
      -r 144 \
      "$input_path" \
      "$output_stem"
    ;;
  *)
    echo "OUTPUT must end in .svg or .png" >&2
    exit 64
    ;;
esac

echo "$output_path"
