# Week 3 assembly demonstrations

The three local HTML tools adapt the original `bioinformatis-web` Week 3 interactives, retaining their panel layouts, palette, native SVG plots and calculation/graph behaviours. They use only local `assembly-core.js`, `../_shared/artifact-theme.css` and `../_shared/resize.js`. No remote fonts, libraries or services are required. Modified files carry source and Apache 2.0 notices; the retained license is `../../third_party/bioinformatis-web-LICENSE`.

| Local tool | Original source | Parent lesson anchor |
|---|---|---|
| `01-coverage-simulator.html` | `artifacts/lecture-03/01-coverage-simulator.html` | `#coverage-lab` |
| `02-debruijn-builder.html` | `artifacts/lecture-03/03-debruijn-builder.html`, with traversal teaching idea from `04-eulerian-path.html` | `#graph-lab` |
| `03-n50-calculator.html` | `artifacts/lecture-03/06-n50-calculator.html` | `#n50-lab` |

## Coverage: depth and breadth

The default chosen arrangement has genome length **G=12**, read length **L=4**, and **N=3** reads at starts **[0,4,8]**. Every position has depth 1, so mean depth is **1×** and breadth **100%**. The clustered preset uses **[0,0,0]**: four positions have depth 3 and eight have depth zero. Mean depth remains **1×**, while breadth is **4/12 = 33.3%**. Both arrangements contain **12 measured bases**. Coordinates are zero-based read starts, with interval ends excluded.

Random draws use a deterministic seeded LCG and choose each integer start independently and uniformly from **0 through G−L**, with replacement. This is a finite **linear** genome, not a circular model. End bases have fewer covering start positions. The mean depth is exactly N×L/G because full-length reads remain inside the reference. The core computes the exact model expectation of uncovered positions by summing `(1 − coveringStarts / possibleStarts)**N` over positions. The UI does not claim that a Poisson curve exactly describes all positions. Chosen presets are labeled as such, rather than presented as random data.

The display provides read intervals, per-position depth, mean, covered breadth, uncovered positions, and an accessible numerical depth table. At most forty intervals are drawn, while calculations use every read. UI limits are G=8–120, N=0–80 and integer L=1–G. No biological bias or sequencing error is simulated.

## Graph: structure, support and traversal

The default single input sequence **ATGACCT**, k=3, produces five windows and five distinct edges. The button **Single sequence: ATGACCT** restores it. Next choose **Overlapping reads: ATGAC / GACCT**: those two reads produce **six observed k-mer instances** but **five distinct k-mer types**:

| k-mer edge | Prefix → suffix | Observation support |
|---|---|---:|
| ATG | AT → TG | 1 |
| TGA | TG → GA | 1 |
| GAC | GA → AC | 2 |
| ACC | AC → CC | 1 |
| CCT | CC → CT | 1 |

The unique-edge graph merges repeated types and labels their observed support. Starting at **AT**, the ordered five-edge traversal spells **ATGACCT**. The first node contributes k−1 bases, then each edge adds its final base. This restricted example assumes exact, forward, error-free observations and a unit traversal of each unique edge; it is not a general genome reconstruction rule.

An explicit **occurrence multigraph** mode makes every read-observed k-mer instance a separate edge (`GAC#1` and `GAC#2` are different IDs). The baseline therefore has six displayed edges in that mode. Coverage-derived observations are not genomic copy numbers; the resulting occurrence graph need not have one edge-covering walk. This distinction is stated alongside the graph and in the assumptions panel.

Traversal buttons offer only unused outgoing edges from the current node. The shortcut step button is enabled only when exactly one choice exists. Wrong-direction, missing or already-used edge IDs are rejected by the core API. A route is declared complete only after it uses all displayed edges; a dead end with unused edges is reported separately. No hidden algorithm chooses an arbitrary biological answer.

The repeat preset contains the six 3-mer observations **ATG,TGA,GAT,ATC,TCA,CAT**, once each. Starting at AT, two complete orders spell **ATGATCAT** and **ATCATGAT**. Both have the same k=3 multiset. Their k=4 multisets differ; the longer observation **GATC** occurs only in the first. A graph cycle does not prove a circular molecule. The disconnected preset **ATGA / CCGT** has two components; a traversal in one cannot consume edges in the other.

Reads are decomposed separately, never joined across read boundaries. Uppercase A/C/G/T input is required; invalid bases are rejected instead of silently deleted. The visual interface accepts k=2–6, at most twelve nodes and twenty displayed edges. The core supports k through twelve for small calculation checks. The edge table and button controls provide the graph information without relying on SVG color or pointer interactions.

## N50 and L50

Default assembly A lengths **[8,7,5]** give total **20**, cumulative lengths **[8,15,20]**, half-total threshold **10**, **N50=7** and **L50=2**. Assembly B **[12,8]** also totals **20**, but **N50=12**, **L50=1**. These are continuity summaries; sequence correctness, completeness and misjoins remain unknown.

The original comparison-card and plotting layout is retained with a cumulative-length plot and explicit sorted-length table. No assumed true genome denominator is used. Invalid, fractional, nonpositive or nonnumeric tokens reject the calculation; no subset is silently accepted. The core returns `null` N50/L50 for an empty list, while the UI asks for nonempty input. NG50 is outside this introductory calculator.

## Core API and verification

The public API is `Week3Assembly` in a browser, or CommonJS `require('./assembly-core.js')`:

- `coverageFromStarts(genomeLength, readLength, starts)` returns per-base depth, mean, covered/uncovered counts and breadth as a fraction.
- `simulateCoverage({genomeLength,readLength,readCount,seed})` adds reproducible uniform-start sampling and the exact expected uncovered count for this finite model.
- `buildDeBruijn(reads,k,{occurrenceEdges:false})` returns nodes, displayed edges, per-type counts, representation, distinct-type count and total observation count.
- `startTraversal(graph,node)`, `availableEdges(graph,state)` and `stepTraversal(graph,state,edgeId)` create and advance immutable traversal states. An edge has `id`, `kmer`, `from`, `to`, `support`, `observedSupport` and occurrence metadata.
- `parseLengths(text)` validates user-entered lengths; `assemblyStats(lengths)` returns sorted lengths, total, count, N50, L50, cumulative sums, threshold and largest contig.

Run `node tests/test_week03_tools.js` from the repository root. Tests compare finite-boundary coverage expectation against exhaustive tiny sampling, verify depth/mean/breadth invariants, distinguish support from occurrence edges, validate both repeat walks and disconnected stops, and compare N50 to independent base weighting over many small length triples. A temporary DOM harness additionally exercised the actual HTML control handlers for presets, random draws, invalid inputs, both traversal orders, edge-model changes and calculator results. Inline JavaScript, IDs, labels and local dependency paths were checked. The repeat graph generated by the HTML tool was rendered and visually inspected; no browser UI automation was used.

Artifact IDs are `week3-coverage-simulator`, `week3-debruijn-builder`, and `week3-n50-calculator`. Iframes report `{type:'artifact-resize',height}` through the existing resize mechanism. Parent pages must identify the iframe using `event.source`.
