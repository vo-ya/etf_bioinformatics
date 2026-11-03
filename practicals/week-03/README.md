# Homework 03 — Reconstructing a sequence from fragments

Complete **after Week 3, before Week 4**. This **60–90-minute homework** follows
the **180-minute class**: about 50 minutes of core notebook work plus 10–40
minutes for setup, debugging, and interpretation. The optional support-filter
comparison takes about 10 additional minutes.

Use [exercise.ipynb](exercise.ipynb) with students and
[solutions.ipynb](solutions.ipynb) for instructor review. Each file works alone
when uploaded to Colab or opened in an existing Jupyter environment with
Python 3.9 or later. Standard library only: no installs, plotting packages,
external files, data downloads, or network requests.

The notebook continues the class's assembly story. Students implement four
short functions: count k-mers **within separate reads**, build a directed
graph, spell a **supplied ordered node path**, and calculate N50. No path-search
or Eulerian traversal implementation is required. Supplied observations let
students interpret repeats, disconnected evidence, and an added read without
attributing those patterns to a known biological cause.

| Step | Minutes | Student work |
|---|---:|---|
| Predict overlaps | 5 | Relate separate read windows to sampling support |
| Count k-mers | 10 | Include overlapping windows; preserve read boundaries |
| Build graph | 10 | Link prefix to suffix; keep counts as support weights |
| Spell supplied path | 10 | Add new letters once; inspect ambiguous observations |
| Calculate and interpret N50 | 15 | Use cumulative bases; compare N50/L50/total and limits |
| **Core work** | **50** | Plus setup, debugging, and written interpretation |

Submit the completed notebook with the initial prediction, k-mer counts,
printed graph/path, length summaries, and three interpretation sentences.
Beginner instructions cover upload/save/run/download, recovery after a fresh
runtime, and expandable hints. Each exercise's optional reference appears
after its checks in a Colab-compatible form: attempt the task first; running
the reference replaces that function, then rerun the checks above it.

The notebook includes worked reminders for the read-boundary and N50-denominator
examples in the 40-slide deck. These add no required coding tasks. Timing labels
are omitted from both notebook editions; the estimates above are for planning.

## Colab setup

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vo-ya/etf_bioinformatics/blob/main/practicals/week-03/exercise.ipynb)

The badge opens the published notebook from GitHub `main`. Alternatively,
download `exercise.ipynb` and use **File → Upload notebook** in Colab. Save a
working copy; use **None / CPU** acceleration. Run **0. Run first — CPU/Python
setup**, then **1. Create the deterministic teaching data**, before the tasks.
No helper upload or dataset download is needed. See the
[shared setup guide](../README.md) for the common packaging and recovery steps.

## Deterministic examples and answer key

[expected_results.json](expected_results.json) is generated from the same
functions as the instructor notebook. All sequences and length lists are
invented teaching examples, independent of the fictional cell-culture tubes.

The sequence `ATGACCT` at k=3 yields ATG, TGA, GAC, ACC, and CCT, once each.
Separately sampled reads `ATGAC` and `GACCT` instead yield:

| K-mer | Observed support | Directed edge |
|---|---:|---|
| ATG | 1 | AT → TG |
| TGA | 1 | TG → GA |
| GAC | 2 | GA → AC |
| ACC | 1 | AC → CC |
| CCT | 1 | CC → CT |

The graph has **six nodes and five distinct edges**, with observed support
totaling six windows. Its supplied node path
`AT → TG → GA → AC → CC → CT` spells `ATGACCT`.
GAC support 2 comes from overlapping read observations in this example; it is
not evidence of two genomic copies or a requirement to traverse the edge twice.
`["AT", "GAC"]` at k=3 contributes only GAC: words cannot cross read boundaries.

The graph represents **one edge per distinct observed k-mer**, weighted by its
sampling count. It is not a known genomic-multiplicity multigraph. Nodes are
sorted for display; the alphabetical edge list does not define path order.

| Observation | Deterministic result | What remains unresolved |
|---|---|---|
| `ATGATCAT` versus `ATCATGAT`, k=3 | Both have ATG/TGA/GAT/ATC/TCA/CAT once; one graph with five nodes and six edges | Which ordering is correct; a graph cycle does not prove a circular molecule |
| Same two strings, k=4 | The spectra differ; GATC appears only in the first | Larger k is not a universal solution and may reduce support with short reads |
| Separate reads `ATGA`, `CCGT` | Two components: AT→TG→GA and CC→CG→GT | Missing sequence, missing coverage, or different sources; no unsupported join |
| Add `GATCT` to the baseline reads | Adds GAT, ATC, TCT, each with support 1 | Error versus real difference versus sparse sampling |

Two ordered node walks are supplied for the repeat pair:

```text
AT → TG → GA → AT → TC → CA → AT  spells ATGATCAT
AT → TC → CA → AT → TG → GA → AT  spells ATCATGAT
```

| Contig lengths | Total | N50 | L50 | Correctness |
|---|---:|---:|---:|---|
| 8, 7, 5 | 20 | 7 | 2 | Unknown |
| 12, 8 | 20 | 12 | 1 | Unknown |

N50 is a contig length at the first cumulative-base threshold of at least 50%
of total assembled length. L50 is the number of longest contigs needed to
reach it. These are separate invented length lists, not output contigs of the
seven-base example. An incorrect join could raise N50. No correctness claim
is supported by length alone.

The optional support≥2 filter keeps only GAC and removes four genuine
substrings of the known toy sequence. Low support alone does not identify
sequencing errors; the notebook does not automatically discard singletons.

## APIs, validation, and verification

| Function | Contract |
|---|---|
| `kmer_counts(reads, k)` | Dictionary of observed counts; positive integer k; separate read windows |
| `build_kmer_graph(counts)` | `{"nodes": [...], "edges": [{"kmer", "source", "target", "support"}, ...]}`; one edge per type |
| `spell_path(path)` | DNA spelled by supplied (k−1)-mer node labels; validates local overlap, not graph membership |
| `n50(lengths)` | Integer N50; positive integer contig lengths; empty list returns 0 by convention |
| `assembly_summary(lengths)` | Supplied helper returning `contigs`, `total`, `N50`, `L50` |

DNA is uppercase A/C/G/T only. Empty read collections and reads shorter than
k contribute no windows. The graph requires uniform k-mer widths of at least
two and positive integer support. Empty graphs and paths are allowed;
nonempty path nodes must share a positive width and overlap correctly.
Invalid letters, path overlaps, counts, k values, or lengths raise errors.

Edit [build_notebook.py](build_notebook.py), then regenerate and test from the
repository root:

```sh
python3 practicals/week-03/build_notebook.py
python3 -m unittest discover -s tests -p 'test_week03_practical.py'
```

Tests execute every instructor cell, verify hand-specified examples and read
boundaries, check supplied-path reconstruction on small DNA strings, compare
N50 against an independent base-weighted median, and verify deterministic
Colab packaging. They also exercise the attempt/reveal/check workflow across
all three student notebooks.

Teaching ideas were adapted from
`bioinformatis-web/coding_exercises/lecture-03/build_notebook.py`, with the
Apache 2.0 license retained in [LICENSE.upstream.txt](LICENSE.upstream.txt).
The large random-genome exercise, automatic singleton removal, and general
contig extraction were replaced with small fixed examples and supplied paths.
N50 is treated as contiguity, not as an accuracy objective. Notebook packaging
continues Week 2 through [the shared helper](../notebook_helpers.py).
