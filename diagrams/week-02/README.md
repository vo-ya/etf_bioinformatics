# Week 2 reused figures

These seven local SVGs adapt `bioinformatis-web` illustrations under Apache 2.0. The upstream license is in `../../third_party/bioinformatis-web-LICENSE`; each modified SVG includes its exact source path and modification notice. Embed with `width: 100%; height: auto` on a light background. No external images, scripts, or downloaded fonts are required; standard fallback fonts are specified.

| Local figure | ViewBox | Upstream source | Intended use |
|---|---|---|---|
| `alignment-context.svg` | 860 × 360 | `diagrams/lecture-02/01-alignment-problem-overview.svg` | Why read placement matters; matches, mismatches, insertions relative to a reference. Schematic rather than a coordinate example. |
| `sliding-search.svg` | 860 × 420 | `diagrams/lecture-02/02-brute-force-sliding.svg` | Exact search by trying starts in order; coordinate convention and cost. |
| `local-alignment-matrix.svg` | 860 × 540 | `diagrams/lecture-02/08-smith-waterman-matrix.svg` | A complete small local-alignment calculation and traceback. Best revealed after scoring is introduced. |
| `seed-and-extend.svg` | 860 × 420 | `diagrams/lecture-02/10-seed-and-extend-pipeline.svg` | Short words identify candidates; extension checks nearby sequence; heuristics can miss useful alignments. |
| `search-hit-evidence.svg` | 1200 × 660 | `diagrams/lecture-19/12-blast-output.svg` | Separate identity, query coverage, search statistics, and a biological claim. Rebuilt report-and-explanation composition with a fully synthetic example. |
| `search-space.svg` | 1200 × 540 | `diagrams/lecture-19/10-database-scaling.svg` | Fixed-score comparison of synthetic effective database lengths; search context changes expected chance-hit count. |
| `cigar-walkthrough.svg` | 860 × 500 | `diagrams/lecture-02/09-cigar-rle-diagram.svg` | Optional traceback-to-record example with checked aligned strings and query/reference consumption. |

## Scientific review and modifications

**Alignment context.** Removed fixed genome/run sizes, error rates and biological variation rates that were not universal or supported by the figure. Labeled lengths schematic. The insertion is explicitly relative to the reference; an alignment difference is not itself proof of biological variation.

**Sliding search.** The source claimed `TACAGA` exactly matched `GATTACAGATTACA` at zero-based position 2; the correct position is **3**. It also claimed four comparisons before exiting at position 0, although the first letters differ. The adapted four rows show starts 0, 1, 2 and 3, with **1, 1, 2 and 6 comparisons**, respectively: **10 comparisons to the first hit**. This does not claim ten comparisons for searching every possible start. The worst-case cost statement is separate. Increased the canvas height and separated the total/legend so neither is clipped.

**Local alignment.** Independently recalculated all 64 matrix entries using reference `GATTACA`, query `GCATGCA`, match **+2**, mismatch **−1**, and linear gap cost **−2 per base**. The source numbers are correct and retained. Maximum **5** occurs at row 7, column 7. The displayed traceback follows `(7,7) → (6,6) → (5,5) → (4,4) → (3,3)` where the score reaches zero. It aligns query `TGCA` to reference `TACA`, positions **4–7** in both strings using **1-based inclusive** coordinates, giving `2 − 1 + 2 + 2 = 5`. The new explanatory panel names row/column sequences and cell choices. Replaced the unexplained CIGAR field with score arithmetic and coordinates. Matrix prefix indices include the zero row/column; sequence positions are stated separately.

**Seed and extend.** Retained the original candidate-track and mini-matrix composition. Removed FM-index intervals, named indexing implementations, a fabricated MAPQ, absolute position and unverified candidate scores. The original claimed 50 bases while its CIGAR consumed 48 query bases; no such inconsistent read-length/CIGAR claim remains. The new graphic is explicitly conceptual: sketches of the query and seed words do not supply enough sequence to compute an alignment score. Candidate B is the best *tested* region, not a guaranteed globally best placement. Index internals and minimizer/chaining details are outside this week's scope.

**Search evidence.** Replaced a plausible-looking real accession and unrelated sample score/statistics with a coherent toy protein example. Full query `MKTAYIAKQRQISFVKSHFS` has **20 amino acids**. Its residues **4–13**, `AYIAKQRQIS`, align with subject residues **21–30**, `AYIAKQKQIS`. These are **10 columns with 9 exact matches and no gaps**: **90% identity** over alignment columns but **50% query coverage** over the full query. A synthetic 80-residue subject can be constructed as 20 G residues, the displayed subject segment, then 50 G residues; the remainder is not relevant to the arithmetic. The alignment is illustrative, not asserted to be a computed best local alignment or a genuine BLAST hit. All displayed coordinates are **1-based inclusive**. Explicit text coordinates keep sequence columns aligned in SVG renderers. No numerical bit score, E-value, biological annotation, or significance claim is invented. A high identity percentage over a short region does not establish the same whole-protein function or explain a phenotype.

## Verification and interpretation references

The initial five SVGs were parsed as XML, rendered using `rsvg-convert` on white, and visually inspected. The exact-match positions/comparison counts, all local-alignment matrix values and traceback endpoints, and protein identity/coverage arithmetic were checked independently with short Python calculations. No browser automation was used.

[NCBI: The statistics of sequence similarity scores](https://www.ncbi.nlm.nih.gov/BLAST/tutorial/Altschul-1.html) explains the distinction between raw score, bit score, E-value and P-value, plus scoring and search-space assumptions. E-value concerns expected chance matches at least as strong under the search model; it is neither the probability a biological claim is correct nor a missed-detection rate. Database search and mapping share computational ideas but answer different questions. A seed search can trade sensitivity for speed; failure to report a hit is not evidence that no related sequence exists.

The parent lesson and interactive tools use additional shared toy sequences. These static worked examples retain their own clearly labeled sequences; their numerical results should not be mixed across examples.

## Added search-space figure for the 180-minute lesson

`search-space.svg` (1200 × 540) adapts `diagrams/lecture-19/10-database-scaling.svg`. It retains the log-log plot and bottom interpretation strip, using the same **40-bit score / 100-residue effective query** as the reused calculator. Horizontal values are **synthetic effective protein-database lengths** from 10⁶ to 10¹⁰ amino-acid residues. The vertical axis is **expected chance-alignment count E**, from 10⁻⁵ to 10¹, with larger values upward. At n = 10⁶, E ≈ 9.094947 × 10⁻⁵; at n = 10⁷, E ≈ 9.094947 × 10⁻⁴. All curve and annotation positions were regenerated from `E = 100 × n × 2**(-40)`.

The source figure's vertical-axis labels disagreed with its ascending curve, its top point was clipped, and its numerical callouts disagreed with the stated formula. Those errors were corrected. Named real-database sizes and a universal significance threshold were removed. Effective-length and model assumptions replace raw-current-database claims. The figure was rendered and visually inspected; it contains no external assets. Its modification notice and the retained upstream Apache license cover the reuse.

## Optional CIGAR walkthrough

`cigar-walkthrough.svg` (**860 × 500**, aspect 1.72) adapts original `diagrams/lecture-02/09-cigar-rle-diagram.svg` under the same Apache 2.0 attribution. It preserves the original 16 operation boxes, seven run brackets, boxed CIGAR and side-panel composition; added checked sequence rows, consumed-base totals, explicit forward/coordinate scope and a new explanatory inset. Standard system font fallbacks replace any need for downloaded fonts. This optional figure is linked from the lesson’s `#cigar-reference` extension rather than added as a required presentation slide.

Reference alignment `ACGTACCGTTAC-GTA` and query `ACGTGCC--TACGGTA` give operations `====X==DD===I===`, encoded as `4=1X2=2D3=1I3=`. Removing gaps gives reference `ACGTACCGTTACGTA` (15 bases) and query `ACGTGCCTACGGTA` (14 bases). There are 16 alignment columns. A forward alignment beginning at one-based SAM POS 101 spans reference positions 101–115 inclusive (Python slice `[100:115]`). D consumes only reference; I consumes only query; both = and X consume both. M can encode either match or mismatch. This example has no clipping and is not a complete SAM parser.

The original operation/run arithmetic was already consistent; no correction to that arithmetic was necessary. Sequence rows and consumption/coordinate claims were checked independently against the [SAM specification, section 1.4](https://samtools.github.io/hts-specs/SAMv1.pdf). The added SVG was parsed, rendered locally with `rsvg-convert`, and visually inspected. Lesson text contains the same alignment and a per-run consumption table as accessible alternatives. The optional 5–8-minute reading is outside the core 180-minute lesson.

## Query coverage and average read depth

`coverage-comparison.svg` is an original diagram for slide 28. Its top example
shows one aligned region covering 6 of 12 query bases (50%). Below, three
four-base reads have starts [0, 4, 8] or [0, 0, 0] on a 12-base reference.
Both arrangements have mean depth 1×; reference breadth is 100% or 33.3%.
The depth bars and numbers include all 12 positions. Query and reference
examples are separate synthetic inputs. Definitions follow the Illumina
coverage reference linked in the lesson and notes; placements also match the
Week 3 teaching example.
