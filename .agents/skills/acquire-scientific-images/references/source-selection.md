# Source and license checklist

Use this reference while shortlisting and attributing scientific figures.

## Contents

- Candidate acceptance
- License preference
- Candidate ledger and attribution templates
- Common failure modes
- Processing recipes

## Candidate acceptance

A candidate is acceptable only when all answers are yes:

- Does the actual visible figure show the relationship required by the prose?
- Are important labels, symbols, axes, units, signs, and ordering compatible with the page?
- Is the original source or derivative chain identifiable?
- Does the file-level license allow local redistribution?
- If modification is needed, does the license allow derivatives?
- Can the final image remain readable at mobile article width?
- Can the required attribution be written without guessing?

## License preference

Prefer:

1. Public domain or CC0.
2. CC BY.
3. CC BY-SA when share-alike obligations can be met.

Treat CC BY-NC, publisher permissions, fair-use claims, and custom licenses as requiring explicit project-owner judgment unless repository policy already resolves them. Do not infer that free access means permission to redistribute.

## Candidate ledger template

```markdown
| Candidate | Exact visible content | Author/source | License | Required changes | Decision |
| --- | --- | --- | --- | --- | --- |
| <name> | <labels, axes, ordering> | <provenance> | <license + URL> | <none/crop/etc.> | <accept/reject + reason> |
```

Keep rejected candidates in working notes long enough to avoid rediscovering and downloading them.

## Attribution template

Record:

```text
Author or organization
Original work title
Figure, slide, page, or section number
Publication or hosting organization
Stable URL or DOI
License name and license URL
Modification status
Access date when required by page format
```

Korean caption pattern:

```markdown
그림 N. <그림에서 읽어야 하는 핵심 관계>.
출처: <저자>, “<원제>,” <작품>, <그림/슬라이드/쪽>, <라이선스>.
<발췌·크롭·레이블 변경·요소 제거 등 모든 수정 내역>.[참고문헌 번호]
```

Use “수정 없음” only after comparing the stored file with the source original.

## Common failure modes

- The landing-page description is correct but the actual file uses different levels or terminology.
- Two similarly named SVG variants contain different labels.
- A preview URL is mistaken for the original file URL.
- A PDF's displayed slide number differs from its file page index.
- SVG labels are paths, so grep falsely suggests that text is absent.
- Changing only an SVG `viewBox` hides but does not remove unrelated source content.
- A downloaded figure is scientifically suitable but cannot legally be redistributed.
- A license is cited without the original author, work title, or modification status.
- Multiple slow downloads occur before a figure contract is written.

## Processing recipes

Inspect metadata and embedded text:

```bash
python3 .agents/skills/acquire-scientific-images/scripts/inspect_candidate.py \
  /tmp/candidate.svg \
  --expect register \
  --expect cache \
  --expect "main memory" \
  --expect storage \
  --reject-external-svg
```

Extract PDF page 6 as SVG:

```bash
.agents/skills/acquire-scientific-images/scripts/extract_pdf_page.sh \
  /tmp/source.pdf 6 /tmp/source-page-6.svg
```

Render an SVG preview:

```bash
inkscape /tmp/candidate.svg \
  --export-type=png \
  --export-width=1600 \
  --export-filename=/tmp/candidate-preview.png
```

Validate a final SVG:

```bash
xmllint --noout docs/<domain>/<topic>/images/<asset>.svg
rg -n 'https?://' docs/<domain>/<topic>/images/<asset>.svg
```
