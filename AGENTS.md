# AGENTS.md

## Project Overview

This repository is a personal AI-assisted scientific wiki built with MkDocs and Material for MkDocs.

The wiki is intended to organize scientific and technical study notes as a structured reference rather than as a chronological blog.

The following three primary domains are fixed:

1. Device Physics
2. Solid-State Physics
3. Computational Science

These three domains and their order must remain unchanged unless the project owner explicitly requests a structural revision.

The website must remain readable and easy to navigate on both desktop and mobile devices.

## Primary Objectives

Agents working in this repository must:

1. Maintain a clear and scalable documentation hierarchy.
2. Follow the predefined scientific writing format.
3. Modify only the content explicitly requested by the project owner.
4. Keep the MkDocs navigation synchronized with the source tree.
5. Preserve a clean and mobile-friendly Material for MkDocs design.
6. Validate the documentation build before publishing changes.
7. Preserve the fixed top-level domain structure.
8. Write explanatory wiki prose primarily in Korean while using conventional English technical titles.

## Content Language Rule

The primary language of explanatory wiki content must be Korean.

The following elements must use Korean explanatory sentences unless the project owner explicitly requests otherwise:

* Explanatory text.
* Figure captions.
* Table captions.
* Definitions.
* Summaries.

Use the most recognizable conventional English expression only for the small set of genuinely representative scientific and technical concepts whose Korean replacement would reduce identification, searchability, or precision. Page titles and navigation labels may retain these expressions. In body text, retain English primarily for recurring core concepts, established abbreviations, named phenomena, methods, models, and the key concepts being compared in a table. Write ordinary descriptive vocabulary, logical relations, experimental actions, conditions, and interpretations in Korean. A term being common in English-language literature is not by itself sufficient reason to keep it in English.

Do not construct Korean sentences by replacing ordinary nouns and modifiers one by one with English. For example, translate generic words such as `current`, `voltage`, `device`, `condition`, `curve`, `path`, `region`, `field`, `barrier`, `component`, `measurement`, `metric`, `extraction`, `window`, `reference`, `scaling`, and `dependence` when they serve an ordinary explanatory role. Keep an English expression when it is the actual conventional name being defined or used as a stable label, such as `subthreshold leakage`, `drain-induced barrier lowering (DIBL)`, or `carrier mobility`.

Section headings should also be primarily Korean. Retain an English heading or English term within a heading only when it names the page's central concept or an established phenomenon, method, or model. In tables, generic column headings and explanatory cells should be Korean; only the core terms, symbols, abbreviations, and standard labels that readers must identify consistently may remain in English.

Introduce an abbreviation only after its full English name. Add a Korean gloss at the first occurrence only when it materially helps comprehension; the Korean gloss is explanatory, not the representative term.

Examples:

* density functional theory (DFT)
* nonequilibrium Green's function (NEGF)
* density of states (DOS)
* Schottky barrier
* carrier mobility
* charge neutrality condition
* reciprocal space

An article title may contain an established abbreviation before this definition, but the first body sentence must expand it to the full English name and abbreviation.

Example:

```markdown
Density functional theory (DFT)는 전자 밀도를 기본 변수로 사용하는 전자구조 계산 방법이다.
```

English capitalization in Korean prose must account for sentence position. When an ordinary English expression begins a Korean sentence, capitalize the first alphabetic word as sentence case. Do not convert the entire expression to title case. Preserve the conventional spelling of established abbreviations, symbols, proper nouns, and forms whose initial lowercase letter is meaningful, such as `nMOS` and `p-type`.

Correct:

```markdown
Subthreshold leakage는 문턱전압 아래에서 흐르는 누설 전류이다.
```

Incorrect:

```markdown
subthreshold leakage는 문턱전압 아래에서 흐르는 누설 전류이다.
```

Also incorrect:

```markdown
Subthreshold Leakage는 문턱전압 아래에서 흐르는 누설 전류이다.
```

After the term has been introduced, consistently use either its representative English term or its defined abbreviation. Do not alternate irregularly among English, Korean, and abbreviated forms.

Do not repeatedly add a Korean translation or the full English name in parentheses.

Before drafting prose, design the section hierarchy from the conventional explanatory order used by standard textbooks and authoritative reviews. Establish the dependency chain from definition and baseline model through physical origin, governing relations, individual phenomena, measurement, quantitative metrics, limitations, and summary. When an existing prerequisite article already defines the shared baseline, notation, and conventions, link to it and begin the article with the representative concept rather than repeating a generic scope-and-conventions section. Do not let the order in which sources were found determine the article structure.

For repeated scientific phenomena, use a consistent local sequence: physical cause, governing model or equation, observable consequence, measurement method, quantitative metric, and interpretation caveat.

Use a Material for MkDocs admonition titled `[Measurement]` to keep the experimental procedure and the actual extraction equation or quantitative criterion together. When reporting conventions are long enough to interrupt the procedure, an optional `[Metric]` block may follow. Use `[Interpretation Caveat]` for confounders and exceptions.

Software names, commands, code identifiers, filenames, equations, variable names, and bibliographic information must retain their original language and notation.

Examples:

* MkDocs
* Material for MkDocs
* SIESTA
* VASP
* PyTorch
* `mkdocs build`
* `density-functional-theory.md`
* Kohn–Sham equation
* Schrödinger equation

Do not translate code, terminal commands, function names, class names, package names, or API names.

## Heading and Table-of-Contents Rule

Scientific article headings must use no more than two levels below the page title.

* Do not give H1 a section-style `1.` prefix. When the article has a navigation sequence number, use that parenthesized number in H1: `# (1) MOSFET: Leakage Current`.
* Use numbered H2 headings for primary sections: `## 1. Scope and Conventions`.
* Use parenthesized-number H3 headings for subsections: `### (1) Subthreshold Leakage`.
* Do not use H4 or deeper headings. Restructure the prose, lists, tables, or admonitions instead.
* A page table of contents may therefore contain only H2 and H3 entries.
* Under each fixed top-level scientific domain, navigation must link directly to articles. Do not add an intermediate topic-group layer to navigation.
* Number sibling article navigation labels with `(1)`, `(2)`, and so on in their displayed order.

Use the same English wording and article number in front matter, H1, navigation, and the relevant domain index.

## Fixed Domain Structure Rule

The following top-level scientific domains are fixed:

1. Device Physics
2. Solid-State Physics
3. Computational Science

Agents must not:

* Rename these domains.
* Translate these domain names.
* Change their order.
* Merge one domain into another.
* Place one domain below another.
* Remove one of the domains.
* Add a new top-level scientific domain without explicit instruction.
* Move an article outside these domains when it can reasonably be classified under one of them.

New scientific content must be classified under one of the three fixed domains.

When classification is ambiguous, preserve the existing structure rather than creating a new top-level category.

The Home page may remain outside the three scientific domains.

## Repository Structure

Use the following repository structure:

```text
.
├── AGENTS.md
├── README.md
├── mkdocs.yml
├── build.sh
├── requirements.txt
├── skills/
│   └── research-and-write-wiki/
│       └── SKILL.md
├── refs/
│   ├── format.md
│   ├── research-workflow.md
│   └── writing-benchmarks/
│       ├── README.md
│       └── high/
│           └── <benchmark>.md
└── docs/
    ├── index.md
    ├── device-physics/
    │   ├── index.md
    │   ├── <topic-group>/
    │   └── images/
    ├── solid-state-physics/
    │   ├── index.md
    │   ├── <topic-group>/
    │   └── images/
    ├── computational-science/
    │   ├── index.md
    │   ├── <topic-group>/
    │   └── images/
    └── assets/
        ├── stylesheets/
        └── images/
```

The three fixed source directories are:

```text
docs/device-physics/
docs/solid-state-physics/
docs/computational-science/
```

These directories must remain the top-level scientific source directories.

New subdirectories may be added when required by the requested content.

Subdirectories should reflect meaningful scientific topic groups rather than arbitrary document counts or creation dates.

Do not create empty topic groups, planned article cards, or example categories. Add a topic group only when the project owner requests the first verified article that belongs in it.

## Content Scope Rule

Only modify files that are directly required by the project owner's current request.

Do not:

* Rewrite unrelated documents.
* Reorganize unrelated sections.
* Correct unrelated wording.
* Rename unrelated files or directories.
* Update scientific content outside the requested scope.
* Apply repository-wide formatting changes unless explicitly requested.
* Change the meaning of existing technical statements without explicit instruction.
* Reformat all existing pages after a local format change.
* Modify another top-level domain when the requested task concerns only one domain.
* Add unrelated explanatory material merely to make a page appear more complete.

Small dependent changes are permitted only when necessary to keep the requested modification functional.

Examples include:

* Adding a newly created page to `mkdocs.yml`.
* Updating the relevant index page with a link to the newly created page.
* Adding an image used exclusively by the requested page.
* Fixing a broken relative link caused by a requested file movement.
* Updating a navigation entry after renaming a requested page.

When such dependent changes are made, keep them minimal.

## Writing Format Rule

Before creating or substantially restructuring a scientific page, read:

```text
refs/format.md
refs/research-workflow.md
skills/research-and-write-wiki/SKILL.md
```

All scientific articles must follow the structure and conventions defined in these files.

The format specification is authoritative for:

* Page metadata.
* Heading hierarchy.
* Definitions.
* Mathematical notation.
* Equation formatting.
* Figure placement.
* Code examples.
* References.
* Internal links.
* Terminology.
* Summary sections.
* Language style.
* Citation style.

When the project owner requests a general change to article structure or style, update `refs/format.md` first.

After updating `refs/format.md`, apply the new format only to:

1. Pages explicitly identified by the project owner.
2. New pages created after the format update.

Do not automatically reformat all existing pages.

When the requested change applies only to one page, modify that page directly without changing `refs/format.md`.

## High-Quality Writing Example Rule

Before finalizing a new or substantially revised scientific article, read the closest example under `refs/writing-benchmarks/high/`. Check whether the article reaches a similar quantitative, qualitative, and formatting level for its topic, revise shortcomings, and briefly report the result. Do not mechanically copy the example's length or component counts, and do not use it as a substitute for scientific sources. The brief comparison guidance and current examples are in `refs/writing-benchmarks/README.md`.

## Korean Writing Style

Scientific pages must use a consistent Korean technical writing style.

Use explanatory declarative forms such as:

* `~이다`
* `~한다`
* `~할 수 있다`
* `~로 정의된다`
* `~를 의미한다`

Do not mix formal polite endings such as `~입니다` and `~합니다` with declarative technical prose unless explicitly requested.

Avoid:

* Conversational filler.
* Unnecessary rhetorical questions.
* Excessive use of English sentences.
* Literal translations that are unnatural in Korean technical writing.
* Repeating the full English expansion after an abbreviation has already been introduced.
* Translating established software or method names into uncommon Korean expressions.
* Excessively long sentences containing multiple independent claims.

Reserve the conventional English terminology used by standard textbooks, review articles, and scientific literature for representative concepts that require stable identification. Translate the surrounding descriptive vocabulary and sentence functions into natural Korean rather than preserving English word by word.

## Scientific Writing Rules

Scientific content must be written as a technical reference.

Each page should:

1. Define the physical or computational problem clearly.
2. Introduce the required variables and notation before using them.
3. State the governing equations where applicable.
4. Explain the physical interpretation of the equations.
5. Distinguish established results from interpretation or inference.
6. State important assumptions and approximations.
7. Include references for nontrivial scientific claims.
8. Link prerequisite concepts to existing wiki pages when available.
9. Avoid unsupported generalizations.
10. Preserve conventional terminology used in the relevant literature.
11. Explain the scope and limitations of models when relevant.
12. Distinguish exact relations from approximations.
13. Use consistent symbols throughout a page.
14. Define abbreviations at their first occurrence.

When an explanation includes inference rather than a directly established result, state this explicitly.

Suitable expressions include:

```markdown
이는 다음과 같이 해석할 수 있다.
```

```markdown
다음 설명은 물리적 추론에 해당한다.
```

```markdown
이 결과로부터 다음 가능성을 추론할 수 있다.
```

Do not invent:

* References.
* Authors.
* Journal information.
* Book information.
* Equations.
* Numerical values.
* Experimental results.
* Quotations.
* Software behavior.
* Benchmark results.

Model knowledge is a consistency screen, not a citable source. A nontrivial claim may be published only when:

1. It is consistent with the agent's scientific knowledge after checking the claim's scope and assumptions.
2. At least two independent, directly inspected references support the same claim.
3. The references agree on the meaning relevant to the prose.
4. Terminology, symbols, units, signs, coordinate systems, and other conventions are used consistently.

Search-result snippets, abstracts viewed without the relevant supporting passage, copied bibliographies, and multiple pages that reproduce the same underlying source do not count as independent verification.

If these conditions are not met, investigate further or omit the claim from the published article. Do not leave unresolved verification markers in a page included in website navigation.

## Reference Rules

Every new or substantially revised scientific article requires current internet research. Open each source and verify the relevant passage before citing it.

Each nontrivial scientific claim must normally cite at least two independent references in the same citation cluster, for example `[1,2]`. For consequential, disputed, or convention-sensitive claims, prefer three or more independent references.

Prefer the following source hierarchy:

1. Original research papers.
2. Authoritative review articles.
3. Standard graduate-level textbooks.
4. Official software documentation.
5. Widely recognized technical documentation.

Do not rely on unsourced secondary summaries when a primary source is available.

Source independence is determined by provenance, not URL count. A publisher copy, preprint, and repository mirror of one paper are one source. Two reviews that merely repeat one original result without independent analysis do not by themselves establish agreement.

Use references with distinct roles when possible, such as an original paper plus an authoritative review or graduate-level text. For current software behavior, inspect the official documentation and an independent source that exercises or analyzes the behavior.

Reference titles, author names, journal names, and book titles must remain in their original language.

Do not translate article titles in the bibliography.

References must follow the format defined in:

```text
refs/format.md
```

When adding a reference:

1. Verify that it actually supports the associated statement.
2. Record enough bibliographic information to identify it unambiguously.
3. Link to a DOI, publisher page, official documentation page, or stable repository record when available.
4. Cite the narrowest source location practical.
5. Preserve meaningful disagreements instead of manufacturing consensus.

If only one suitable source exists, or the inspected sources disagree, do not publish the claim as established fact unless the project owner explicitly approves a clearly labeled exception.

## Page Naming Rules

Use lowercase kebab-case for directories and Markdown filenames.

Correct:

```text
carrier-transport.md
density-functional-theory.md
nonequilibrium-greens-function.md
```

Incorrect:

```text
Carrier Transport.md
density_functional_theory.md
NEGF.md
캐리어-수송.md
```

Source filenames and directories should remain in English even when the visible page content is written in Korean.

Use descriptive names rather than numbered filenames.

Section numbering such as `1`, `1.1`, and `1.2` belongs in the conceptual navigation structure, not in source filenames.

Each directory representing a major section should contain an `index.md` page that introduces the section and links to its principal topics.

## Page Title Rules

Visible scientific page titles must use the most recognizable conventional English technical expression.

Examples:

```markdown
# Carrier Transport
```

```markdown
# Density Functional Theory
```

```markdown
# MOS Capacitor
```

Avoid unnecessarily long titles.

The title should identify the topic rather than describe the entire contents of the page.

## Navigation Rules

The `nav` section of `mkdocs.yml` is the authoritative website navigation.

The fixed top-level navigation order is:

```yaml
nav:
  - Home: index.md

  - Device Physics:
      - Overview: device-physics/index.md

  - Solid-State Physics:
      - Overview: solid-state-physics/index.md

  - Computational Science:
      - Overview: computational-science/index.md
```

The top-level labels must remain exactly:

```text
Device Physics
Solid-State Physics
Computational Science
```

Do not translate these fixed labels into Korean unless explicitly requested by the project owner.

Overview and article labels below these domains must use the same conventional English wording as their H1 titles.

Example:

```yaml
nav:
  - Home: index.md

  - Device Physics:
      - Overview: device-physics/index.md
      - "(1) MOSFET: Leakage Current": device-physics/mosfet/leakage-mechanisms.md

  - Solid-State Physics:
      - Overview: solid-state-physics/index.md

  - Computational Science:
      - Overview: computational-science/index.md

```

When adding a page:

1. Classify it under one of the three fixed domains.
2. Place it in the corresponding source directory.
3. Add it to the corresponding section in `mkdocs.yml`.
4. Position it according to conceptual dependency, not creation date.
5. Verify that the page title and navigation title are concise and consistent.
6. Avoid placing the same page at multiple navigation locations.
7. Avoid excessively deep navigation.
8. Use consistent conventional English labels for overview and article names.
9. Preserve the exact fixed top-level domain names and order.
10. Do not add navigation entries for unverified or merely planned content.

Prefer the hierarchy:

```text
Fixed domain
└── Topic group
    └── Article
```

Avoid adding another navigation level unless the number of pages or scientific structure clearly requires it.

The filesystem and `nav` hierarchy should correspond closely, but `nav` determines the actual display order.

## Index Page Rules

Each top-level domain must contain an `index.md` page.

A domain index should contain:

* A short description of the domain.
* The scope of verified topics currently covered.
* A structured list or card grid linking to existing major subsections.
* Recommended prerequisite topics when relevant.
* Links to important introductory articles.
* No long-form treatment of a single technical topic.

Index pages should function as navigation hubs.

When a domain has no verified articles, state that directly. Do not populate the index with hypothetical scope lists, example cards, or planned learning sequences.

Index-page explanations must use Korean sentences while keeping representative scientific terms and article titles in conventional English.

## Source Tree Rules

The source tree must remain clean and reflect the website navigation.

Each article should be stored under the most appropriate domain and topic directory.

Use the following general pattern:

```text
docs/
└── <fixed-domain>/
    ├── index.md
    ├── <topic-group>/
    │   ├── index.md
    │   ├── <article>.md
    │   └── images/
    └── images/
```

Do not place all articles directly under a top-level domain when meaningful topic groups exist.

Do not create a new directory for a single short article unless the directory represents a meaningful expandable topic group.

Do not duplicate the same article in multiple directories.

When moving a file:

1. Update `mkdocs.yml`.
2. Update affected internal links.
3. Update affected index pages.
4. Move related page-specific images when appropriate.
5. Run a strict build.

## Image Rules

Store page-specific images near the relevant domain or topic group.

Preferred locations:

```text
docs/<domain>/images/
```

or:

```text
docs/<domain>/<topic-group>/images/
```

Use the shared directory below only for images reused across multiple domains:

```text
docs/assets/images/
```

Image filenames must use lowercase kebab-case.

Example:

```text
docs/device-physics/mos-physics/images/mos-capacitor-band-diagram.svg
```

Prefer:

1. SVG for diagrams, schematics, and vector graphics.
2. PNG for plots and screenshots requiring lossless rendering.
3. JPEG only for photographic images.

Every scientific image must include:

* Descriptive alternative text.
* A Korean caption when the meaning is not self-evident.
* A source or citation when the image is reproduced or adapted.
* The original author, work title, figure number, stable URL or DOI, reuse license, and modification status.
* Definitions of important symbols when needed.

When a representative visual materially improves understanding, place a sourced schematic or measurement curve near the introduction of each major section. Prefer device schematics for physical mechanisms and bias diagrams or extraction curves for experimental methods.

Do not generate new scientific figures. Search for an existing figure in a paper, textbook, standard, official document, or public repository. Prefer CC BY, CC BY-SA, CC0, or public-domain material. If reuse permission cannot be verified, link to the original figure instead of copying it into the repository.

Do not hotlink external image files. Store only reuse-permitted copies under the relevant `images/` directory and preserve attribution required by the source license.

Do not add large binary files without a clear need.

Do not move or rename existing images unless:

* The project owner explicitly requests it.
* A requested file movement requires it.
* The existing image reference would otherwise be broken.

## Internal Link Rules

Use relative Markdown links for internal pages.

Example:

```markdown
[density of states](../../solid-state-physics/electronic-structure/density-of-states.md)
```

Internal links that name a scientific concept or repeat an article title should use its representative conventional English expression.

Before completing a change:

* Check that all newly added internal links resolve.
* Check that moved pages do not leave broken links.
* Prefer linking to an existing explanation over duplicating it.
* Do not create placeholder links to pages that do not exist unless explicitly marked as planned content.
* Check that links between different fixed domains remain valid.
* Avoid circular navigation pages that do not provide useful content.

## MkDocs Design Rules

Use Material for MkDocs as the primary theme.

The site design should prioritize:

* Mobile readability.
* Fast navigation.
* Searchability.
* Clear heading hierarchy.
* Readable equations.
* Readable code blocks.
* Restrained visual styling.
* Consistent spacing and typography.
* Light and dark color schemes.
* Persistent access to navigation and table of contents where supported.
* Clear distinction between main text, notes, warnings, equations, and examples.

Prefer native Material for MkDocs features over custom HTML, JavaScript, or CSS.

Custom CSS may be added only when the requested result cannot be achieved cleanly through `mkdocs.yml` or supported Markdown extensions.

Do not introduce decorative components that reduce technical readability.

Do not use excessive animations, oversized banners, or visually distracting components.

## MkDocs Configuration Rule

Changes to `mkdocs.yml` must be minimal and valid YAML.

When modifying `mkdocs.yml`:

1. Preserve existing configuration unless the requested change requires otherwise.
2. Keep `nav` synchronized with created, removed, renamed, or moved pages.
3. Preserve the fixed top-level domain names and order.
4. Do not remove plugins or Markdown extensions without explicit instruction.
5. Do not add dependencies that are not used.
6. Validate the configuration with a strict build.
7. Preserve Korean text encoding.
8. Avoid duplicate navigation entries.

The recommended theme configuration is:

```yaml
theme:
  name: material
  language: ko
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.indexes
    - navigation.top
    - navigation.footer
    - search.suggest
    - search.highlight
    - content.code.copy
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      toggle:
        icon: material/brightness-7
        name: 다크 모드로 전환
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      toggle:
        icon: material/brightness-4
        name: 라이트 모드로 전환
```

Do not substantially change the visual identity without an explicit request.

## Build and Validation Rules

The repository must provide a root-level executable script:

```text
build.sh
```

The script should support at least the following modes:

```bash
./build.sh serve
./build.sh build
./build.sh publish "Commit message"
```

### `serve`

The `serve` mode must:

* Validate that required dependencies are available.
* Start the MkDocs development server.
* Enable live reload.
* Allow access from the local network when configured.
* Do not commit or push.
* Continue running until interrupted by the user.

Equivalent core command:

```bash
mkdocs serve
```

For local-network access, the script may use:

```bash
mkdocs serve --dev-addr 0.0.0.0:8000
```

### `build`

The `build` mode must:

* Remove stale generated output when appropriate.
* Run a strict production build.
* Fail immediately if MkDocs reports an error.
* Report the output location.

Equivalent core command:

```bash
mkdocs build --strict
```

### `publish`

The `publish` mode must:

* Require a nonempty commit message.
* Run `mkdocs build --strict`.
* Stop immediately if the build fails.
* Display the files that will be committed.
* Verify that changed files match the intended scope.
* Stage the intended repository changes.
* Create a Git commit.
* Push the current branch to its configured upstream.

The script must never push changes when the strict build fails.

The script must not use `git add .` blindly when unrelated untracked or modified files may exist.

Prefer explicit paths or `git add -A` only when the project owner has intentionally requested publication of the complete working tree.

Do not force-push.

Do not bypass Git hooks.

Do not automatically publish during `serve`.

## Git Safety Rules

Before committing or publishing:

1. Run `git status --short`.
2. Verify that the changed files match the requested scope.
3. Run `mkdocs build --strict`.
4. Stop if unrelated files have been modified.
5. Use a concise commit message describing the content change.
6. Push only after a successful commit.

Never:

* Use `git reset --hard`.
* Use `git clean -fd`.
* Rewrite published history.
* Force-push.
* Delete branches.
* Change remote URLs.
* Commit credentials.
* Commit access tokens.
* Commit private keys.
* Commit local environment files.
* Commit unpublished private material unless explicitly intended.

These actions require explicit permission from the project owner.

## Generated Files

The generated MkDocs output directory is normally:

```text
site/
```

The `site/` directory must not be treated as source documentation.

Unless the repository intentionally tracks built output, `site/` should be excluded through `.gitignore`.

Agents must edit source files under `docs/`, not generated HTML under `site/`.

## Dependency Rules

Python dependencies should be declared in:

```text
requirements.txt
```

Keep dependencies minimal.

At minimum, the project may require:

```text
mkdocs
mkdocs-material
```

Add plugins only when they provide a concrete function used by the wiki.

Do not add packages solely for optional visual decoration.

When a plugin is added:

1. Add it to `requirements.txt`.
2. Configure it in `mkdocs.yml`.
3. Verify that it is actually used.
4. Run `mkdocs build --strict`.
5. Avoid replacing native Material for MkDocs functionality unnecessarily.

## New Content Workflow

When the project owner requests a new article:

1. Identify the correct fixed top-level domain.
2. Read `refs/format.md`, `refs/research-workflow.md`, `refs/writing-benchmarks/README.md`, and `skills/research-and-write-wiki/SKILL.md` completely.
3. Check whether an equivalent page already exists.
4. Determine the correct topic group, creating it only when the requested article requires it.
5. Search the internet and build a claim-to-source ledger before drafting.
6. Inspect the full relevant source passages and test source independence.
7. Publish only claims that agree with the agent's knowledge and at least two independent references.
8. Select and record a consistent terminology, notation, unit, sign, and coordinate convention.
9. Create only the requested page and required assets.
10. Write the page primarily in Korean and cite nontrivial claims with multi-source citation clusters.
11. Add important English terminology in parentheses at first occurrence.
12. Compare the completed draft with the closest `high` writing example at a quantitative, qualitative, and formatting level, then revise clear shortcomings.
13. Add the page to the appropriate domain index and `mkdocs.yml` only after scientific verification passes.
14. Check headings, equations, links, images, references, unresolved markers, and convention consistency.
15. Append a method to `refs/research-workflow.md` only if this task produced evidence that the method worked and is reusable.
16. Run `mkdocs build --strict`.
17. Report the files created or modified, source disagreements, omitted claims, writing-example comparison, and validation result.

Do not publish unless the project owner explicitly requests a commit or push.

## Existing Content Update Workflow

When the project owner requests an update:

1. Locate the explicitly requested page.
2. Read `refs/format.md`, `refs/research-workflow.md`, `refs/writing-benchmarks/README.md`, and `skills/research-and-write-wiki/SKILL.md` completely.
3. Preserve correct existing content.
4. Search the internet and re-verify every scientific claim changed or made dependent on the change.
5. Apply the same multi-source agreement and convention checks used for new content.
6. Modify only the requested section.
7. Avoid unrelated rewriting.
8. Maintain Korean as the primary content language.
9. Add English terminology only where required.
10. Update references or images only when necessary.
11. Compare the completed revision with the closest `high` writing example at a quantitative, qualitative, and formatting level, then revise clear shortcomings.
12. Run `mkdocs build --strict`.
13. Report the exact files modified, any claim omitted because verification failed, and the writing-example comparison.

## Writing Format Update Workflow

When the project owner requests a general writing-format change:

1. Update `refs/format.md`.
2. Preserve unrelated rules.
3. Apply the new format only to explicitly requested pages.
4. Do not automatically rewrite the complete wiki.
5. Validate affected pages.
6. Run `mkdocs build --strict`.

## Structural Update Workflow

When the project owner requests a navigation or directory restructuring:

1. Preserve the three fixed top-level domains unless explicitly instructed otherwise.
2. Confirm the requested target hierarchy from the instruction.
3. Move only the pages covered by the request.
4. Update `mkdocs.yml`.
5. Update affected index pages.
6. Repair links affected by moved files.
7. Move related images when necessary.
8. Leave unrelated domains unchanged.
9. Run `mkdocs build --strict`.

## Completion Report

After completing a task, report:

* Files created.
* Files modified.
* Navigation changes.
* Source-tree changes.
* Build result.
* Any unresolved reference issue.
* Any unresolved link issue.
* Writing example used and a brief quantitative, qualitative, and formatting comparison, for a new or substantially revised scientific article.
* Whether changes were committed.
* Whether changes were pushed.

Do not claim that a build, commit, or push succeeded unless the corresponding command was actually executed successfully.
