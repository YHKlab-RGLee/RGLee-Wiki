---
name: acquire-scientific-images
description: Find, verify, download, minimally process, and integrate reuse-permitted scientific figures for this MkDocs wiki. Use when Codex must add or replace a diagram, schematic, plot, measurement curve, screenshot, or other sourced image under docs/, especially when figure-content matching, license verification, PDF/SVG extraction, attribution, or mobile-readable rendering matters.
---

# Acquire Scientific Images

Acquire an existing scientific figure whose visible content matches the article's explanation. Minimize network requests and irreversible processing by deciding what the figure must show before downloading it.

## Required context

Read `AGENTS.md` and the target page before searching. If the task creates or substantially revises scientific prose, also follow `.agents/skills/research-and-write-wiki/SKILL.md`, `refs/format.md`, and `refs/research-workflow.md`.

Read [references/source-selection.md](references/source-selection.md) when evaluating candidates, licensing, attribution, or permitted modifications.

## Workflow

### 1. Write a figure contract

Record these items in working notes before searching:

- Scientific purpose: the single relationship the figure must clarify.
- Required visible concepts, labels, ordering, axes, or device terminals.
- Unacceptable extras that would contradict or blur the prose.
- Preferred format and mobile-layout constraint.
- Whether an unmodified figure is required or a disclosed crop is acceptable.

For a replacement, inspect the current asset, alt text, caption, and paragraph. State the exact mismatch. Do not search from the old filename alone.

### 2. Shortlist from source pages

Search candidate landing pages and figure descriptions before downloading files. Batch related web and image searches when possible.

Prefer, in order:

1. Original paper or authoritative review with explicit reuse permission.
2. Standard or official technical documentation with explicit reuse permission.
3. Open textbook or university material with a clear license.
4. Wikimedia Commons or another public repository with file-level provenance and license.

Create a small candidate ledger containing:

| Candidate | Visible match | Provenance | License | Processing needed | Decision |
| --- | --- | --- | --- | --- | --- |

Reject a candidate before download when its visible hierarchy, axes, symbols, bias conditions, or grouping do not match the figure contract. A descriptive landing-page title is not evidence that the actual figure matches.

### 3. Verify provenance and reuse

Open the source page and verify all of the following:

- Original author or responsible organization.
- Work title and figure, slide, page, or section number when applicable.
- Stable source URL or DOI.
- File-specific license and license URL.
- Whether modification and redistribution are allowed.
- Whether the candidate is an independent original or a derivative.

Do not copy a figure with unclear reuse rights. Link to the original instead when permission cannot be established. Do not rely on a search thumbnail, snippet, or copied attribution.

### 4. Download once, into `/tmp`

Choose one primary candidate and at most one fallback before downloading.

Use the exact direct asset URL and download into a task-specific `/tmp` path. Do not write an unverified download directly into `docs/`.

If a necessary exact download fails because of sandboxed network access, rerun that same command with scoped approval. Do not broaden the URL or download unrelated candidates.

After download, run:

```bash
python3 .agents/skills/acquire-scientific-images/scripts/inspect_candidate.py /tmp/<asset>
```

For text-bearing SVG or PDF candidates, add repeated `--expect` arguments for required labels. Treat an incomplete text check as a signal to render and inspect, not as permission to assume the label exists.

### 5. Inspect the actual figure

Render the exact downloaded file before editing:

- Raster file: inspect it directly with the available image viewer.
- SVG: render a PNG preview with Inkscape, then inspect the preview.
- PDF: extract only the relevant displayed page with `scripts/extract_pdf_page.sh`, then inspect it.

Check the visible ordering, arrows, labels, legend, axes, units, color meaning, and cropping. SVG text may be converted to paths, so a text search can be inconclusive even when the labels are visible.

Do not proceed merely because the source metadata describes the right concept.

### 6. Process minimally

Prefer the original file without modification. For diagrams, prefer SVG; for plots and screenshots, prefer PNG.

Permitted processing when the license allows it:

- Crop unrelated margins or surrounding slide material.
- Extract a single figure or slide region.
- Convert a permitted raster/vector format without changing scientific meaning.
- Remove an optional explanatory element only when the resulting simplification remains scientifically accurate and the modification is disclosed.

Do not silently relabel axes, change signs, recolor encoded quantities, remove caveats, or merge separate source figures. Do not generate a new scientific figure with an image model unless the project owner explicitly requests it and `AGENTS.md` permits it.

Keep intermediate files in `/tmp`. Inspect the final rendered asset again. When cropping an SVG by changing only `viewBox`, verify that unintended off-canvas slide content is not still embedded; prune it or disclose the retained source structure when material.

### 7. Integrate and attribute

Store the final asset near the page under the appropriate `images/` directory. Use lowercase kebab-case.

Update only the dependent page content:

- Korean alt text describing the visible relationship.
- Korean caption explaining the scientific takeaway.
- Author, work title, figure/slide/page number, stable URL or DOI.
- Reuse license and license URL.
- Modification status, including every crop, extraction, relabeling, or removed element.
- Bibliography entry when the page format uses numbered references.

Do not hotlink external assets. Remove the replaced local asset only when it is no longer referenced and deletion is within the request.

### 8. Validate

Run the relevant checks:

```bash
python3 .agents/skills/acquire-scientific-images/scripts/inspect_candidate.py docs/<path>/<asset>
xmllint --noout docs/<path>/<asset.svg>
rg -n 'https?://' docs/<path>/<asset.svg>
git diff --check
./build.sh build
git status --short
```

Render the built page or final asset when visual correctness is material. Confirm that the diff contains only the requested page, image, and necessary attribution changes.

## Efficiency rules

- Validate the concept and license on landing pages before requesting a binary.
- Prefer one authoritative candidate over many speculative downloads.
- Reuse an already downloaded `/tmp` source during conversion iterations.
- Separate displayed page numbers from zero-based screenshot page indices.
- Prefer direct original-file URLs over redirect endpoints once the URL is known.
- Preserve exact source and license metadata in working notes as soon as verified.

## Stop conditions

Stop and report the blocker when:

- No candidate satisfies the figure contract.
- Reuse permission or original provenance is unclear.
- Required labels or scientific conventions cannot be verified.
- A modification would change the scientific meaning.
- The final asset is unreadable on mobile at article width.
