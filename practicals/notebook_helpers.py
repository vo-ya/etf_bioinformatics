"""Standard-library Colab packaging shared by the notebook generators.

Only generators import this module. Its generated cells are standalone: students
do not need to upload this file. Colab form handling follows the upstream
bioinformatis-web/coding_exercises/apply_colab_form.py pattern (Apache-2.0),
using both #@title and metadata.cellView='form'; Jupyter metadata alone is not
sufficient. The upstream license is retained inside each week directory.
"""

from copy import deepcopy

REPOSITORY = "vo-ya/etf_bioinformatics"
BRANCH = "main"


def colab_url(week, solution=False):
    filename = "solutions.ipynb" if solution else "exercise.ipynb"
    return (f"https://colab.research.google.com/github/{REPOSITORY}/blob/"
            f"{BRANCH}/practicals/week-{week:02d}/{filename}")


def form_cell(cell, title, *, reference=False):
    """Return a Colab-compatible form cell without changing executable logic."""
    cell = deepcopy(cell)
    if cell["cell_type"] != "code":
        raise ValueError("A Colab form must be a code cell")
    source = cell["source"]
    if not source.lstrip().startswith("#@title"):
        cell["source"] = f"#@title {title}\n" + source
    cell.setdefault("metadata", {})["cellView"] = "form"
    if reference:
        cell["metadata"]["jupyter"] = {"source_hidden": True}
        cell["metadata"]["tags"] = ["reference-solution"]
    return cell


def setup_source(week):
    return f'''import sys

if sys.version_info < (3, 9):
    raise RuntimeError("Use Python 3.9 or later for this homework")

print("Homework {week:02d} setup ready")
print("Python:", sys.version.split()[0])
print("Execution: ordinary CPU Python; no accelerator or package installation needed")
print("Next: run the supplied deterministic-data cell before the exercises")
print("After a runtime restart, rerun setup, data, and completed exercises from the top")
'''


def colab_instructions(week, solution=False):
    filename = "solutions.ipynb" if solution else "exercise.ipynb"
    return f'''## Colab setup — run this before the exercises

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url(week, solution)})

Open the notebook with the badge above. If that link is unavailable, download
`{filename}` and choose **File → Upload notebook** in
[Colab](https://colab.research.google.com/). This notebook includes all the data
and code needed for the exercises.

1. Save a working copy with **File → Save a copy in Drive**, if needed, and
   rename it `homework{week:02d}_yourname.ipynb`.
2. Use **Runtime → Change runtime type** and keep the hardware accelerator
   set to **None / CPU**. A paid runtime or GPU is unnecessary.
3. Run the **0. Run first — CPU/Python setup** cell below using **▶** or
   **Shift+Enter**. Check that it prints “setup ready”. No pip install is needed.
4. Run **1. Create the deterministic teaching data** at Step 1, then work
   through the exercises in order. Repeating the data cell gives the same inputs.
5. After reconnecting to a fresh runtime, rerun setup and data, then your
   completed exercise cells. A saved notebook preserves code and outputs,
   while Python variables have to be created again.
6. Keep outputs in the notebook. Save, then use **File → Download → Download
   .ipynb** to obtain your completed copy. Open it once to check your answers.

Work cell by cell and attempt each TODO before opening its reference solution.
The reference follows the check cell. Running it replaces your function in
memory, so rerun the checks afterward. **Run all** also executes the reference
solutions; use the checks immediately after your own code to test your answers.
You can expand a form cell to inspect its code.
The [official Colab FAQ](https://research.google.com/colaboratory/faq.html)
describes upload, storage, download, and CPU runtime settings.
'''


def prepare_notebook(notebook, week, *, solution=False, data_source=None, references=()):
    """Add consistent metadata, badge/instructions, setup, and data form cells."""
    notebook = deepcopy(notebook)
    filename = "solutions" if solution else "exercise"
    notebook.setdefault("metadata", {})["colab"] = {
        "name": f"week-{week:02d}-{filename}.ipynb", "provenance": [], "toc_visible": True}
    instruction = {"cell_type": "markdown", "id": f"week{week:02d}-colab-guide",
                   "metadata": {}, "source": colab_instructions(week, solution)}
    setup = form_cell({"cell_type": "code", "id": f"week{week:02d}-cpu-setup",
                       "metadata": {"tags": ["setup"]}, "source": setup_source(week),
                       "execution_count": None, "outputs": []},
                      "0. Run first — CPU/Python setup")
    # Preserve the title/overview as the first cell, then put setup before all work.
    notebook["cells"][1:1] = [instruction, setup]
    if data_source is not None:
        matches = [index for index, cell in enumerate(notebook["cells"])
                   if cell["cell_type"] == "code" and
                   cell["source"].strip() == data_source.strip()]
        if len(matches) != 1:
            raise ValueError("Expected exactly one supplied data cell")
        index = matches[0]
        data = form_cell(notebook["cells"][index], "1. Create the deterministic teaching data")
        data["metadata"]["tags"] = ["data"]
        notebook["cells"][index] = data
    if not solution:
        for number, reference in enumerate(references, start=1):
            matches = [index for index, cell in enumerate(notebook["cells"])
                       if cell["cell_type"] == "code" and
                       cell["source"].strip() == reference["after"].strip()]
            if len(matches) != 1:
                raise ValueError("Expected exactly one check cell before a reference")
            index = matches[0] + 1
            explanation = {"cell_type": "markdown", "id": f"week{week:02d}-reference-note-{number}",
                           "metadata": {}, "source":
                           "**Try the task first.** Optional reference below: expand to inspect; "
                           "running it replaces this step's function definition(s). "
                           "Rerun the check cell above after applying it.\n"}
            cell = form_cell({"cell_type": "code", "id": f"week{week:02d}-reference-{number}",
                              "metadata": {}, "source": reference["source"].strip() + "\n",
                              "execution_count": None, "outputs": []},
                             "Reference solution — " + reference["title"] + " (attempt first)",
                             reference=True)
            notebook["cells"][index:index] = [explanation, cell]
    return notebook
