# Homework 01 — Reading life as data

Use [exercise.ipynb](exercise.ipynb) with students and
[solutions.ipynb](solutions.ipynb) for instructor review. Each notebook is
self-contained: upload either file alone to Colab, or open it in Jupyter.
No separate data download or package installation is required. Matplotlib is optional; the
same positional quality information is printed in a table when unavailable.

Complete this homework **after Week 1, before Week 2**. Students need basic
Python loops, lists, slicing, and functions; biology terms are introduced in
the notebook.

The homework continues the class prediction in a fictional case: cultured
eukaryotic cells in **tube A are untreated**, while **tube B has a changed
growth condition and grows more slowly** as a teaching premise. Class time
introduces the biology; homework develops the encoding and trimming details.
Its narrow question is confidence in measured DNA letters. It cannot establish
a treatment effect or explain the growth difference.

Students first predict which illustrative read gives stronger confidence and why:

| Read | Sequence | Quality string | Quality evidence |
|---|---|---|---|
| Read 1 | `ACGTACGT` | `IIIIIIII` | Q40 × 8 |
| Read 2 | `ACGTACGT` | `IIII55++` | Q40 × 4, Q20 × 2, Q10 × 2 |

Read 1 and Read 2 are **not assigned to either tube**. These toy reads and the
200-read synthetic dataset are independent illustrations, not experimental
evidence from the fictional cultures. Step 3 revisits the prediction using
the completed probability functions: expected errors are 0.0008 and 0.2204.
The larger dataset extends the same measurement-quality question.

Submit the completed notebook with the positional QC **plot or printed table**
visible, the **initial prediction**, and **three interpretation sentences**. The student notebook includes
Colab upload/save/run/download instructions, an error-recovery guide, and
expandable hints for the coding steps. Optional reference solutions follow the checks in Colab-compatible forms; attempt each task first.

| Step | Student work |
|---|---|
| Inspect records | Identify measurement, uncertainty, and line roles |
| Parse and validate | Complete three checks/actions in a scaffolded parser |
| Decode Phred | Implement Q decoding and sum expected errors |
| Positional QC | Complete probability averaging; interpret table/plot |
| Trim and recommend | Implement suffix trimming; compare loss and uncertainty |

To start in Colab, download `exercise.ipynb`, open
[Colab](https://colab.research.google.com/), sign in, and choose
**File → Upload notebook**. Save a working copy in Drive, rename it, and run
cells from the top with **▶** or **Shift+Enter**. Complete TODO functions before
running their checks. Save and download the completed `.ipynb` through the
**File** menu, keeping the outputs. The notebook has the full walkthrough;
Google's [Colab FAQ](https://research.google.com/colaboratory/faq.html) describes
upload, storage, and download. Colab needs internet access; the analysis needs
no external data or Google Drive mounting. Existing local Jupyter also works.

The parser deliberately covers only unwrapped, four-line, modern Phred+33
records with uppercase A/C/G/T/N and this exercise's Q0..41 quality range.
It accepts CRLF, an optional final newline, valid `@` / `+` quality symbols,
and an optional repeated identifier after `+`. It rejects malformed and
truncated records. This is a teaching subset, not a production FASTQ reader.

The deterministic simulation contains 200 reads of 80 bases. It generates
true bases and then samples wrong calls according to each quality estimate.
Its artificial quality decline is not evidence about a real instrument.
`sum(p)` is an expected error count, which may differ from sampled observed
mismatches. Averaging Q before converting to probability is generally wrong.

For Q20 end trimming with minimum length 50, the reference retains 160 reads
and 10,599 bases (66.24%). Estimated errors fall from 810.3563 to 12.0783
(98.51% reduction); expected errors per 1,000 bases fall from 50.6473 to 1.1396.
The known synthetic truth gives 751 and 16 observed mismatches respectively.
The instructor notebook contains the worked interpretation and limitations.

Edit [build_notebook.py](build_notebook.py), then regenerate from the repository root:

```sh
python3 practicals/week-01/build_notebook.py
python3 -m unittest discover -s tests -p 'test_week01_practical.py'
```

[synthetic_reads.fastq](synthetic_reads.fastq) is an optional exported copy for
inspection in a text editor; notebooks generate the identical data internally.
Student and instructor editions come from the same source; student notebooks
contain optional reference forms after the checks. If learners run all cells before
implementing the TODO functions, `NotImplementedError` marks the first unfinished
step. Complete the tasks in order.

The optional extension compares Q10 and Q20 by explicitly calling
`trim_record(record, threshold=threshold, min_length=50)` in a separate loop.
Keep the function's default `threshold=20` so the core checkpoint assertions
continue to test Q20; the supplied experiment preserves the core results.

Teaching ideas were adapted from
`bioinformatis-web/coding_exercises/lecture-01/build_notebook.py`, distributed
under Apache License 2.0. The implementation and explanations were rewritten
18 October 2026 for the shorter course. The upstream license is preserved in
[LICENSE.upstream.txt](LICENSE.upstream.txt).


## Shared Colab setup

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vo-ya/etf_bioinformatics/blob/main/practicals/week-01/exercise.ipynb)

The badge requires the corresponding notebook to be published on GitHub `main`.
Before publication, download `exercise.ipynb` and use **File → Upload notebook**.
Run **0. Run first — CPU/Python setup**, then **1. Create the deterministic
teaching data**, before the tasks. Use a **None / CPU** accelerator; no installs
or helper uploads are required. Each optional reference uses both `#@title`
and Colab’s `cellView: form` metadata, with a Jupyter source-hidden hint too.
Running a reference replaces that step’s function; rerun the checks above it.
The separate instructor edition remains fully completed. See the
[common setup guide](../README.md) for recovery, saving, and generator details.
