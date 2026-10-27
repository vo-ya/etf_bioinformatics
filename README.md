# Bioinformatics for Engineers

A ten-week introductory course for engineering students. **Weeks 1 and 2 are published**,
with lessons, browser presentations, interactive activities, Colab homework,
and instructor guides. Later weeks will be published separately.

## Week 1: Reading life as data

- [Student lesson](weeks/week-01.html)
- [Presentation](presentations/week-01/index.html)
- [Homework in Colab](https://colab.research.google.com/github/vo-ya/etf_bioinformatics/blob/main/practicals/week-01/exercise.ipynb)
- [Download student notebook](practicals/week-01/exercise.ipynb)
- [Instructor notebook](practicals/week-01/solutions.ipynb)
- [Teaching guide](teaching/week-01.html)

HTML files need a browser to display as course pages. Clone or download the
repository, then run this command from its root:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open [the course home page](http://127.0.0.1:8765/). The static site has no build
step; diagrams, scripts, and styles are included. Colab opens the notebook
directly from GitHub and requires internet access.

The lesson follows a fictional experiment involving two cultures of eukaryotic
cells, one growing more slowly after a change in conditions. Students distinguish
DNA sequence, RNA abundance, and protein activity before choosing a measurement.
The sequencing introduction connects physical DNA fragments, instrument signals,
and reported reads, then compares Illumina, Oxford Nanopore, and PacBio HiFi.

The presentation embeds translation, nanopore, and FASTQ activities and includes
a live Phred score control with the equation Q = −10 log₁₀(p_error).
Two identical toy reads with different quality scores connect class to homework.
These reads and the synthetic homework dataset are independent illustrations;
they do not provide experimental evidence about either fictional culture.

## Week 2: Sequence alignment and search

- [Student lesson](weeks/week-02.html)
- [32-slide presentation](presentations/week-02/index.html)
- [Homework in Colab](https://colab.research.google.com/github/vo-ya/etf_bioinformatics/blob/main/practicals/week-02/exercise.ipynb)
- [Download student notebook](practicals/week-02/exercise.ipynb)
- [Instructor notebook](practicals/week-02/solutions.ipynb)
- [Teaching guide](teaching/week-02.html)

Find every exact placement, compare gapped alignments, distinguish global,
local, and fitting objectives, and interpret sequence-search results. The deck
includes a worked dynamic-programming cell, candidate-window cost comparison,
and a graphical explanation of query coverage versus average read depth.
Seven interactive activities use small synthetic examples. Timing labels and
the break slide are omitted from the deck; instructor pacing stays in the guide.

The homework scaffolds exact search, aligned-pair scoring, and a global score
table with supplied traceback. It needs only the Python standard library.
Edit [the generator](practicals/week-02/build_notebook.py), then rebuild both
notebook editions. See the [presentation guide](presentations/week-02/README.md)
and [homework guide](practicals/week-02/README.md) for scope and verification.

```sh
python3 practicals/week-02/build_notebook.py
python3 -m unittest discover -s tests -p 'test_week02_practical.py'
node tests/test_week02_tools.js
python3 scripts/check_pilot.py
```

## Homework and authoring

The notebooks contain their own deterministic teaching dataset and need no
repository clone, Drive mount, data download, or package installation.
Matplotlib is optional; a positional table is available without it. Students
complete scaffolded Python functions and interpret quality filtering. Optional
reference cells follow the exercise checks. See [homework setup](practicals/README.md).

Edit [the notebook generator](practicals/week-01/build_notebook.py) before
rebuilding the student and instructor notebooks. Edit the presentation's
HTML/CSS/JavaScript directly; its [guide](presentations/week-01/README.md)
describes controls and slide structure. [AGENTS.md](AGENTS.md) records the course
writing rules. Instructor timing remains in the teaching guide.

## Verification

```sh
python3 practicals/week-01/build_notebook.py
python3 scripts/check_pilot.py
python3 -m unittest discover -s tests -p 'test_week01_practical.py'
node tests/test_week01_interactions.js
node tests/test_week01_tools.js
```

The structural checker verifies local HTML links, fragments, duplicate IDs, and
JavaScript syntax. Notebook tests execute the delivered instructor notebook in
a fresh namespace, check numerical results, and verify that generated outputs
match the delivered files. JavaScript tests check the interactive calculations.

Chrome review covered the sequencing slide layouts, Phred slider, embedded
translation and nanopore activities, FASTQ validation, and return to the deck.
The notebook has been executed locally; a Colab UI run, print preview, and
fullscreen remain separate manual checks.

## Sources and licences

Selected teaching ideas, tools, and illustrations derive from `bioinformatis-web`.
See [third-party notices](THIRD_PARTY_NOTICES.md), the
[tool inventory](artifacts/week-01/README.md), and the
[figure inventory](diagrams/week-01/README.md). Adapted Apache 2.0 material retains
its source notices and [upstream licence](third_party/bioinformatis-web-LICENSE).
The repository's root licence is [GPL-3.0](LICENSE). Restricted upstream logos
are not included.
