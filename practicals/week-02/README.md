# Homework 02 — Where does this sequence belong?

**Where does this sequence belong—and how much can a match tell us?**

Complete after Week 2, before Week 3. This **60–90-minute homework** follows
the 180-minute interactive class: about 50 minutes of core notebook work plus
10–40 minutes for setup, debugging, and interpretation. The optional
reverse-complement extension takes about 10 additional minutes.

Use [exercise.ipynb](exercise.ipynb) with students and
[solutions.ipynb](solutions.ipynb) for instructor review. Both work when
uploaded alone to Colab or opened in an existing Jupyter environment with
Python 3.9 or later. **Standard library only:** no installs, data files,
network requests, plotting libraries, or live BLAST calls. All sequences are
synthetic teaching examples, independent of the fictional cell-culture tubes.

The story continues Week 1: confidence in a read's letters does not tell us
where it belongs. Students first predict locations, find **all** exact matches,
then score short comparisons with substitutions and gaps. They implement three
functions; memory allocation, validation scaffolds, loops for the DP interior,
traceback, and comparison displays are provided. Required Python: loops,
lists, indexing/slicing, functions, `zip`, and `max`.

| Step | Minutes | Student work |
|---|---:|---|
| Predict locations | 5 | Record a prediction; interpret zero-based starts |
| Search every window | 10 | Return all exact hits, including overlaps |
| Score aligned strings | 10 | Add explicit match, mismatch, and gap scores |
| Build a global score table | 17 | Fill boundaries and three-choice recurrence; run supplied traceback |
| Compare and interpret | 8 | Compare fragment alignments; write three sentences |
| **Core notebook work** | **50** | Plus setup, debugging, and interpretation |

Submit the completed notebook with the initial prediction, exact-match starts,
small DP table, printed fragment alignments, and three interpretation sentences.
The notebook includes Colab upload/save/run/download instructions,
an error-recovery guide, and expandable hints. The student edition includes
optional reference forms after each task’s check cell; attempt the task first. Its placeholder exceptions mark unfinished tasks;
complete them in order before running all core cells.

To start, open [Colab](https://colab.research.google.com/), sign in, choose
**File → Upload notebook**, and upload `exercise.ipynb`. Save your working
copy in Drive and run cells from the top with **▶** or **Shift+Enter**. Save
and download a completed `.ipynb` with outputs through the **File** menu.
Colab needs internet access; the analysis needs no data connection or Drive
mounting. The [official Colab FAQ](https://research.google.com/colaboratory/faq.html)
describes upload, storage, and download.

## Scope and interpretation

The reference is `ATGCCATGACCTATGCCA`, just **18 invented bases**. Coordinates
are zero-based starts in the displayed forward reference. The required search
uses the forward orientation only; the optional task introduces reverse
complementation. The DNA alphabet is uppercase A/C/G/T. An empty exact-search
query raises `ValueError`; an empty reference with a nonempty query has no hits.

The score rule is **match +2, mismatch −1, each gap column −2**. Gap penalties
are linear: two gap columns cost −4. Aligned strings must have equal lengths,
contain only uppercase A/C/G/T/`-`, and have no double-gap columns. Empty
aligned strings score 0. Global alignment includes every letter of both raw
strings, so its boundaries penalize unmatched prefixes. Empty raw strings are
valid boundary cases.

`D[i][j]` is the best score for `reference[:i]` against `read[:j]`. Its three
choices pair two letters, pair a reference letter with a gap in the read, or
pair a gap in the reference with a read letter. Supplied traceback chooses
**diagonal > up > left** when optimal scores tie. Other alignments can have the
same optimum. The complete table uses O(mn) time and O(mn) memory.

The global comparisons use **short whole fragments**, not the whole 18-base
reference for mapping each short read. Mapping needs candidate/subsequence
search and appropriate alignment choices. Scores are not probabilities,
mapping qualities, statistical significance, or BLAST E-values. Exact matches
and optimal alignments alone do not establish mutations, gene function, or
treatment effects. A unique hit in this tiny reference does not imply a unique
hit in a whole genome.

## Deterministic answer key

[expected_results.json](expected_results.json) is generated from the same
reference functions as the instructor notebook.

| Query in the 18-base reference | All exact starts |
|---|---|
| `ATGCCA` | `[0, 12]` |
| `CCATGA` | `[3]` |
| `ATGCTA` | `[]` |

Overlap check: `AAA` in `AAAAA` returns `[0, 1, 2]`.

| Case | Aligned reference | Aligned read | Score |
|---|---|---|---:|
| Exact | `ATGCCA` | `ATGCCA` | 12 |
| Substitution | `ATGCCA` | `ATGCTA` | 9 |
| Deletion relative to reference | `ATGCCA` | `ATG-CA` | 8 |
| Insertion relative to reference | `ATG-CCA` | `ATGACCA` | 10 |
| All mismatches | `AAAA` | `TTTT` | −4 |

The `AC` / `AG` table is `[[0, -2, -4], [-2, 2, 0], [-4, 0, 1]]`.
Step 4 explains the first interior cell and asks students to predict the final
cell: diagonal `2 - 1 = 1`, above `0 - 2 = -2`, left `0 - 2 = -2`.
Step 5 distinguishes whole-fragment global alignment from fitting a whole read
inside a reference. Its expandable self-check compares 450 billion interior
cells for a hypothetical 150-by-3-billion full table with 45,000 for one
150-by-300 candidate window. No large table is allocated. The self-check adds
no required function or submitted answer; the five-step timing remains unchanged.
For `AA` / `A`, the tie rule returns `AA` / `-A`, score 0;
`AA` / `A-` is equally optimal. The manual `ACGT` / `A-GT` alignment scores 4,
while `ACGT` / `AGT-` scores −2.

Optional orientation check: `TCATGG` has no forward exact match; its reverse
complement `CCATGA` has start `[3]`. Report orientation labels separately;
palindromic queries can match both orientations at the same locus.

## Source and verification

Edit [build_notebook.py](build_notebook.py), then run from the repository root:

```sh
python3 practicals/week-02/build_notebook.py
python3 -m unittest discover -s tests -p 'test_week02_practical.py'
```

The tests execute every delivered instructor cell, check notebook/generator
consistency and student/reference form packaging, and compare the DP score against
an independent exhaustive enumeration of all legal alignments for small inputs.
Boundary cases, malformed alignments, overlapping hits, sequence preservation,
and deterministic ties are covered.

The public notebook APIs are:

| Function | Return value |
|---|---|
| `find_all(reference, query)` | List of every forward exact start |
| `score_alignment(aligned_reference, aligned_read)` | Integer score |
| `nw_table(reference, read)` | List of rows containing integer prefix scores |
| `traceback_global(reference, read, table)` | `(aligned_reference, aligned_read)`; supplied |
| `global_alignment(reference, read)` | `(aligned_reference, aligned_read, optimal_score)`; supplied |
| `reverse_complement(sequence)` | Reversed complementary DNA string; optional |

Curriculum themes draw from `bioinformatis-web/coding_exercises/lecture-02/`
and `lecture-19/`; code and tasks were written for this shorter homework.
Standalone packaging and beginner instructions continue Week 1. The upstream
course's Apache 2.0 license is retained in
[LICENSE.upstream.txt](LICENSE.upstream.txt).


## Shared Colab setup

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vo-ya/etf_bioinformatics/blob/main/practicals/week-02/exercise.ipynb)

The badge requires the corresponding notebook to be published on GitHub `main`.
Before publication, download `exercise.ipynb` and use **File → Upload notebook**.
Run **0. Run first — CPU/Python setup**, then **1. Create the deterministic
teaching data**, before the tasks. Use a **None / CPU** accelerator; no installs
or helper uploads are required. Each optional reference uses both `#@title`
and Colab’s `cellView: form` metadata, with a Jupyter source-hidden hint too.
Running a reference replaces that step’s function; rerun the checks above it.
The separate instructor edition remains fully completed. See the
[common setup guide](../README.md) for recovery, saving, and generator details.
