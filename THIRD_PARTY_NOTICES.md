# Third-party notices

The Week 1 interactive tools derive from **bioinformatis-web**, the prior bioinformatics teaching repository. Its Apache License 2.0 is preserved in [third_party/bioinformatis-web-LICENSE](third_party/bioinformatis-web-LICENSE).

Reused source paths:

- `assets/styles.css` and `assets/lecture.css` → the same relative paths; original design tokens and lecture layout retained. Pilot-specific additions are in `assets/pilot.css`.
- `markdown_resources/lesson1_md_files/lecture-01.md` and selected ideas from L14 → `weeks/week-01.html`; rewritten, shortened prose, new classroom examples and timetable.
- `coding_exercises/lecture-01/build_notebook.py` → teaching ideas for the rewritten practical; see `practicals/week-01/README.md` and its retained upstream license.
- `artifacts/lecture-01/01-dna-explorer.html` → `artifacts/week-01/01-dna-explorer.html`.
- `artifacts/lecture-01/06-fastq-inspector.html` → `artifacts/week-01/02-fastq-inspector.html` and `fastq-core.js` (adapted interface and quality decoding concepts; rewritten parser and rendering).
- `artifacts/_shared/artifact-theme.css` → the same relative path, unchanged palette, typography tokens and base styles.
- `artifacts/_shared/resize.js` → the same relative path, same iframe resize messaging; height measurement adapted to allow shrinking after results are hidden.

The modified files carry modification notices. Adaptations add week-specific prompts, explicit sequence orientations, stricter validation, per-base expected-error calculations, local FASTQ upload, and trailing-quality trimming with retained-data summaries. They remove external font, chart and mathematics dependencies so the selected tools work offline. The prior repository’s logos and restricted logo assets are not included.

## Week 1 diagrams

Ten SVGs in `diagrams/week-01/` are adapted from the same Apache-2.0 source repository:

| Upstream path | Local filename |
|---|---|
| `diagrams/lecture-01/01-cell-organelles.svg` | `cell-organelles.svg` |
| `diagrams/lecture-01/02-dna-double-helix.svg` | `dna-double-helix.svg` |
| `diagrams/lecture-01/03-central-dogma-flow.svg` | `central-dogma.svg` |
| `diagrams/lecture-01/05-bioinformatics-pipeline.svg` | `analysis-pipeline.svg` |
| `diagrams/lecture-01/11-nanopore-squiggle.svg` | `nanopore-signal.svg` |
| `diagrams/lecture-01/12-fastq-anatomy.svg` | `fastq-anatomy.svg` |
| `book/figures/ch01/f3-intensity-trace.svg` | `basecalling-signal.svg` |
| `book/figures/ch01/f4-phred-encoding.svg` | `phred-encoding.svg` |
| `diagrams/lecture-01/04-genetic-code-table.svg` | `genetic-code.svg` |
| `diagrams/lecture-01/09-adapter-structure.svg` and paired-end teaching idea in `diagrams/lecture-03/03-read-types.svg` | `library-preparation.svg` |

The adaptations retain the original drawing style and palette. They correct strand-end labeling, FASTQ position/quality consistency, the nanopore highlighted sequence, ASCII quality encoding, and position tick locations; they clarify biological scope and estimated uncertainty, update course coverage, and repair clipped labels. Details and source references are in [the figure review](diagrams/week-01/README.md). Each modified SVG includes its upstream source path and a modification notice. No upstream logo assets were copied.

## Translation and nanopore tools

`artifacts/week-01/03-central-dogma.html` adapts upstream
`artifacts/lecture-01/02-central-dogma.html`.
`artifacts/week-01/04-nanopore-squiggle.html` adapts upstream
`artifacts/lecture-01/05-nanopore-squiggle.html`.
They retain Apache 2.0 source/modification notices and local theme/resize support.
The translator labels coding-strand transcription, reading frames, and stop
signals. The nanopore activity uses invented signal models. Both add input
validation and explicit model limits and remove remote font dependencies.
See the [Week 1 tool inventory](artifacts/week-01/README.md).

The library-preparation diagram adds adapter read-through, optional PCR lineage,
explicit read orientations, and an unsequenced middle to the original
adapter/insert composition and paired-read idea. It omits the source's
mixed-scale technology comparison and performance claims.

## Colab packaging

The direct GitHub Colab launch links and collapsible reference-cell packaging
follow the original repository's lecture pages and
`coding_exercises/apply_colab_form.py`. The shared helper uses both
`#@title` and `metadata.cellView = "form"`, with portable Jupyter source-hidden
metadata. Setup checks, deterministic-data instructions, launch URLs, and the
adapted exercise/reference pairs are specific to this repository.

The optional input/settings/result/limit prompts in the homework handoff adapt
reproducibility themes from upstream
`markdown_resources/lesson14_md_files/lecture-14.md`. Their wording and examples
are specific to this assignment.

## Week 2 material

Week 2 rewrites and condenses curriculum ideas from upstream `lectures/lecture-02.html`,
`lectures/lecture-19.html`, and their coding exercises. The lesson, small browser
algorithms, and scaffolded notebook tasks are authored for this ten-week course.
The notebook packaging continues Week 1. The upstream licence is retained in
`practicals/week-02/LICENSE.upstream.txt`.

Five illustrations in `diagrams/week-02/` retain Apache 2.0 source and modification notices:

| Upstream path | Local filename |
|---|---|
| `diagrams/lecture-02/01-alignment-problem-overview.svg` | `alignment-context.svg` |
| `diagrams/lecture-02/02-brute-force-sliding.svg` | `sliding-search.svg` |
| `diagrams/lecture-02/08-smith-waterman-matrix.svg` | `local-alignment-matrix.svg` |
| `diagrams/lecture-02/10-seed-and-extend-pipeline.svg` | `seed-and-extend.svg` |
| `diagrams/lecture-19/12-blast-output.svg` | `search-hit-evidence.svg` |

The adaptations correct sliding positions and comparison counts, verify the
local-alignment matrix, remove unsupported performance and significance claims,
and replace the search report with explicitly synthetic identity/coverage
arithmetic. See [the Week 2 figure review](diagrams/week-02/README.md).
The source examples have their own labelled sequences and coordinate conventions.


Additional Week 2 adaptations retain Apache 2.0 source and modification notices:

| Upstream path | Local path |
|---|---|
| `artifacts/lecture-02/01-brute-force.html` | `artifacts/week-02/01-brute-force.html` |
| `artifacts/lecture-02/05-smith-waterman.html` | `artifacts/week-02/02-smith-waterman.html` |
| `artifacts/lecture-19/03-evalue-calculator.html` | `artifacts/week-02/03-evalue-explorer.html` |
| `diagrams/lecture-19/10-database-scaling.svg` | `diagrams/week-02/search-space.svg` |
| `diagrams/lecture-02/09-cigar-rle-diagram.svg` | `diagrams/week-02/cigar-walkthrough.svg` |

Exact search retains overlapping hits; the alignment animator uses a verified
local-alignment core. The E-value explorer removes categorical significance and
homology verdicts and illustrates a simplified effective-search-space model.
The CIGAR example adds checked aligned sequences, operation counts, query and
reference consumption, and coordinates. Tools use local styles and have no
remote font or script requirements. See the [tool inventory](artifacts/week-02/README.md)
and [figure inventory](diagrams/week-02/README.md).

`diagrams/week-02/coverage-comparison.svg` is an original course illustration
using synthetic placements. Definition sources are linked in the lesson and
speaker notes. The worked global cell and fitting/candidate-window explanations
are authored for this course.
