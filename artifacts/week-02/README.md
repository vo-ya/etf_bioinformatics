# Week 2 reused interactive tools

These three offline HTML artifacts adapt the original `bioinformatis-web` interactive demonstrations. They retain the source visual layouts and teaching behaviours, using local `../_shared/artifact-theme.css`, `../_shared/resize.js`, and the validated `alignment-core.js`. No font downloads, CDNs, chart libraries, build step, or live service are required. Source Apache 2.0 attribution/modification notices are included in each HTML file; the license is retained in `../../third_party/bioinformatis-web-LICENSE`.

| Local artifact | Original source | Preserved interactive pattern | Lesson anchor |
|---|---|---|---|
| `01-brute-force.html` | `artifacts/lecture-02/01-brute-force.html` | Sliding aligned-letter display, comparison counter, play/pause/step/reset, speed, early mismatch exit | `#scan-lab` |
| `02-smith-waterman.html` | `artifacts/lecture-02/05-smith-waterman.html` | Score matrix, individual cell fill, four-way candidate derivation, highlighted traceback and returned alignment | `#traceback-lab` |
| `03-evalue-explorer.html` | `artifacts/lecture-19/03-evalue-calculator.html` | Score/query/database controls, search-space statistics, live native SVG curve and explanatory output | `#evalue-lab` |

## Exact search

Default reference `ATGCCATGACCTATGCCA`, query `ATGCCA`; both are synthetic. A step examines one complete possible start, comparing left to right. It keeps searching after a hit and records overlapping hits. All 13 starts are examined, returning **0 and 12**. The overlap example `AAA` in `AAAAA` returns **0, 1, 2** with **9 comparisons**. The early-exit option changes work, not the set of exact matches. The last *tested* window stays on screen, rather than advancing the visualization one position past the comparison count.

Invalid DNA is rejected with a visible message instead of being silently removed. Query-longer-than-reference gives zero full windows; empty entries are rejected. Removed ungrounded extrapolations to CPU years and sequencing-run sizes. Limits are 60 reference bases and 20 query bases. This is forward-strand exact search; orientation handling remains in the main lesson's placement exercise.

## Local matrix and traceback

Default reference `TTACGTAA`, query `GGACGTCC`, using fixed match **+2**, mismatch **−1**, linear gap **−2 per base**. Matrix rows consume reference letters; columns consume query letters. This is the same orientation as `alignment-core.js` and the main lesson interactive table. The static original matrix SVG elsewhere in this repository labels its transposed convention separately.

Step-fill reveals one interior cell in row order, and reports its four candidates. Boundaries are zero. After filling all 64 interior cells, traceback begins at score **8** and reveals one path node per step. Five traceback steps include the stopping zero cell. The returned alignment is `ACGT / ACGT`, with reference and query intervals **[2, 6)** (zero-based, end excluded), identity 100%, query coverage 50%.

The original-example button loads `GATTACA / GCATGCA`: maximum **5**, returning `TACA / TGCA`, intervals **[3, 7)** in both strings, identity 75%. The zero-positive-score example `AAA / CCC` returns an empty alignment and score zero. Traceback uses the existing core's deterministic diagonal, above, left tie order. A revealed zero stopping cell is not an aligned base.

Source repairs include rejecting invalid/empty input (the original could crash), resetting stale output on edits, fixing the scoring model for consistency, waiting for explicit fill/trace actions, and making cell explanations accessible through buttons and arrow keys rather than hover alone. A whole-traceback button supports review after the step investigation.

## Effective search-space model

Default bit score **40**, effective protein query length **100 residues**, synthetic effective database length **1,000,000 residues**. The simplified equation is `E = m × n × 2**(-bits)`:

- Initial E = **0.00009094947017729282** (display rounded to `9.0949e-5`).
- Tenfold database, **10,000,000 residues**: E = **0.0009094947017729282**.
- Raising 40 to **41 bits** at the larger database halves E to **0.0004547473508864641**.

The source controls and native SVG plot remain. Real-database size presets and universal significance/homology verdicts were removed. No posterior false-hit probability is calculated. The model treats m and n as effective lengths and varies inputs independently to isolate effects; it does not derive bit scores from the raw DNA score in the other labs. Both the bit-score plot and numerical table stay available. One bit halves E; the original calculator's claim that five bits halve E was wrong. The original claim that halving the database doubles E was also reversed. All stated limits are now qualitative and explicit: statistics depend on assumptions and do not establish function.

The plot covers bit scores 20–80 and log10(E) −18 through 8; all supported control combinations remain within the plot. The accompanying `../../diagrams/week-02/search-space.svg` shows the same default bit/query assumptions with database length on the horizontal axis.

## Verification and embedding

Inline JavaScript syntax was checked with Node. A lightweight DOM harness executed actual artifact scripts and button handlers: scan completion/repeats/overlaps/invalid input, incremental matrix fill and traceback, the original score-5 example, zero local scores, input resets, and default/tenfold/one-bit E-values. Numerical algorithms share `alignment-core.js`. The new static search-space SVG was parsed, rendered with `rsvg-convert`, and visually inspected. Browser UI verification remains subject to the task's existing approval boundary.

Artifact IDs: `week2-brute-force`, `week2-smith-waterman`, `week2-evalue-explorer`. Embedding uses the existing `{type: 'artifact-resize', height}` message; the parent matches the sending iframe via `event.source`. All artifacts also work as standalone pages.
