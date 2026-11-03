# Week 3 reused illustrations

These seven SVGs adapt `bioinformatis-web/diagrams/lecture-03/` and the Chapter 3 book figures under Apache 2.0. Every file carries its source path and modification notice. The license is preserved in `../../third_party/bioinformatis-web-LICENSE`. Drawings retain the original palette and teaching compositions, with verified shared examples. Embed using `width:100%; height:auto` on a light background. SVGs have titles/descriptions and no external assets or required web fonts.

| Local SVG | ViewBox | Original source | Context and changes |
|---|---|---|---|
| `mapping-vs-assembly.svg` | 860×360 | `01-denovo-vs-resequencing.svg` | Retained the original two-panel read/reference versus reconstructed-contig composition. Simplified labels and removed tool-name lists; assembly can use read relationships without a reference and does not require literal pairwise overlap at every implementation stage. |
| `overlap-graph.svg` | 860×420 | `07-overlap-graph.svg` | Adapted the original read-list/matrix/read-node composition to ATGAC and GACCT, with a verified three-base GAC suffix-prefix overlap, reverse overlap zero, and join ATGACCT. Self-comparisons are excluded. The original five-read figure incorrectly labeled GTCCAT→CCATAG as a five-base overlap; it is four, and other nonzero overlaps were omitted without a clear threshold. The new tiny matrix states every non-self value. |
| `debruijn-graph.svg` | 860×440 | `06-debruijn-graph.svg` | Retained the original decomposition bands and six-node/five-edge chain. Shared baseline uses reads ATGAC/GACCT and k=3: nodes AT,TG,GA,AC,CC,CT; edge labels ATG,TGA,GAC,ACC,CCT. GAC×2 means two observations, not two genomic copies or two unique structural edges. |
| `repeat-ambiguity.svg` | 860×400 | `09-repeat-collapse.svg` | Rebuilt the original repeat/graph teaching composition around a fully verified pair of linear strings, ATGATCAT and ATCATGAT. The same six 3-mer observations, each once, support two AT-centred cycle orders. GATC occurs only in the first; their 4-mer multisets differ. The diagram explicitly avoids inferring a circular molecule. The original alternative mixed a linear sequence and disconnected components rather than a same-spectrum linear pair. |
| `coverage-distribution.svg` | 860×420 | `04-coverage-distribution.svg` | Replaced an unqualified observed/Poisson comparison with exact same-mean arrangements: G12,L4,N3, starts[0,4,8] versus[0,0,0], breadth100% versus33.3%, both mean1×. These chosen arrangements do not claim random sampling or a universal Poisson depth model. |
| `n50-metric.svg` | 900×490 | `11-n50-metric.svg` | Retained sorted contig bars and cumulative-length curves. A[8,7,5]→N50 7/L50 2 versus B[12,8]→N50 12/L50 1; both total20, threshold10, correctness unknown. The source's NG50 annotation was inconsistent: cumulative 10,500 crossed its 10,000 threshold at the 2,800-base third contig, not the 2,100-base fourth. The simplified introductory graphic omits NG50. |
| `branch-evidence.svg` | 1000×360 | `book/figures/ch03/f3-topology-cleanup.svg` | Adapted the parallel-path composition into a decision with no path removed. Verified k=3 paths AT→TG→GA→AA and AT→TC→CA→AA spell ATGAA and ATCAA. Invented 12:3 counts describe read records spanning a whole alternative, with molecular independence initially unknown. The source’s automatic bubble deletion and coverage-proves-truth claims were removed. The companion exercise contrasts technical and independent evidence and asks whether the target is one consensus or preserved variation. |

The original six were parsed, rendered with `rsvg-convert`, and visually inspected. The overlap spelling, graph prefix/suffix labels, duplicate support, repeat multisets and alternative walks, coverage vectors and cumulative N50 thresholds were checked independently. Graph and N50 calculations are also covered by `../../tests/test_week03_tools.js`.

The added branch-evidence SVG was parsed, rendered with `rsvg-convert`, and visually inspected. Its two paths and edge labels were independently checked. It is a schematic evidence discussion: its drawn paths have exact labels, while the read records may include measurement errors or PCR copies. The two alternative evidence follow-ups belong to the lesson, not to a measured dataset.

Scope of the original six: tiny, exact, forward, error-free examples. A consistent overlap or an edge-covering traversal is computational evidence under its stated model, not proof of a true genome. Observed k-mer support is affected by sampling depth as well as genomic multiplicity. Contiguity metrics do not establish correctness. Dated sequencing-error rates, universal graph-cleanup rules and assembler runtime claims from other original lecture figures were not imported.

## Additional original worked examples

These SVGs were drawn for this course and are not upstream adaptations:

- `coverage-worked.svg`: starts `[0,2,6]`, L=4, G=12; mean 1× and breadth 10/12.
- `coverage-order.svg`: known placements cover every base, while the separate
  reads leave their order unresolved.
- `k-connectivity.svg`: the same reads connect at k=4 but lack the bridging
  observed word `TGACC` at k=5.
- `contig-scaffold.svg`: linking evidence orders and orients continuous contigs;
  an unresolved gap has no implied length in the drawing.

Each uses a 1100×360 viewBox and is shared by the lesson and presentation.
