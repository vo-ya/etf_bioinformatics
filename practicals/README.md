# Colab homework setup

Each week has a standalone student `exercise.ipynb` and a complete instructor
`solutions.ipynb`. Uploading one notebook is enough: no Python helper file,
dataset download, Drive mounting, package installation, or paid accelerator
is required. Homework follows each lecture; extensions are optional.

| Week | Student notebook | Instructor notebook |
|---|---|---|
| 1 | [FASTQ and confidence](week-01/exercise.ipynb) | [Reference](week-01/solutions.ipynb) |

## Open, run, and save

The Open in Colab badges use
`https://colab.research.google.com/github/vo-ya/etf_bioinformatics/blob/main/practicals/week-NN/exercise.ipynb`.
Week 1 is published on GitHub `main`. Alternatively, download the notebook
and use Colab's **File → Upload notebook**. An existing local Jupyter environment also works.

1. Save your own copy and use a **None / CPU** hardware accelerator setting.
2. Run **0. Run first — CPU/Python setup**. It checks Python 3.9 or later and
   explains that the code needs no installs or GPU.
3. Run **1. Create the deterministic teaching data** in Step 1. Week 1 uses
   a fixed simulation seed.
4. Attempt each exercise, rerun its function definition, and run its checks.
5. If needed, reveal the optional reference **after the check cell**. Running
   that form replaces the function definition; rerun the checks above it.
6. Preserve outputs, write your interpretation, save, and download the `.ipynb`.
   After a runtime restart, rerun setup/data and your completed code from the top.

The analysis code has no network requests. Colab itself and the badge image
need internet access. Week 1 optionally plots with matplotlib; its numerical
table works if plotting is unavailable.
See the [official Colab FAQ](https://research.google.com/colaboratory/faq.html)
for upload, storage, download, and CPU runtime settings.

## Reference cells and generator conventions

The original course's form mechanism is preserved: **both** a first-line
`#@title` comment and `metadata.cellView = "form"` are present. Reference
cells also carry `metadata.jupyter.source_hidden = true` for JupyterLab.
Jupyter's source-hidden flag alone is not sufficient for Colab. These forms
are learning aids, not a way to secure or withhold answer source code.

Reference functions are placed after their task's checks, with an attempt-first
warning. Student TODOs remain editable and raise `NotImplementedError` until
implemented. Running every cell after finishing the notebook also executes
reference functions; it does not show that the student implemented them unaided.
The separate instructor edition contains completed functions and interpretation
keys, making all cells executable from a fresh Python process.

[notebook_helpers.py](notebook_helpers.py) adds badges, `metadata.colab` name/
provenance/table-of-contents fields, CPU setup, data forms, and reference forms.
Only generators import it; the delivered notebooks contain all required code.
This helper follows the Apache-licensed upstream
`bioinformatis-web/coding_exercises/apply_colab_form.py` pattern. Copies of the
upstream license are retained in each week directory.

Regenerate and check from the repository root:

```sh
python3 practicals/week-01/build_notebook.py
python3 -m unittest discover -s tests -p 'test_week01_practical.py'
```

Builds are deterministic. Tests execute complete instructor notebooks from
empty namespaces, test student attempt → reveal → rerun-check workflows,
validate form packaging, and check the computational results independently.
