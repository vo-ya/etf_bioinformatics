"""Build the Week 4 guided Python workshop; no network or notebook runtime needed."""

from pathlib import Path
import json
import sys
import textwrap

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from notebook_helpers import colab_url, form_cell

HERE = Path(__file__).resolve().parent

SW_IMPLEMENTATION = (HERE / "smith_waterman_simulator.py").read_text()
SW_SETTINGS = '''\
# Edit these two sequences and any of the 16 substitution scores.
sw_sequence_1 = "TTACGTAA"
sw_sequence_2 = "GGACGTCC"

#                    Columns: sequence 2
#                       A   C   G   T
sw_scoring_matrix = [
    [ 2, -1, -1, -1],  # A: sequence 1
    [-1,  2, -1, -1],  # C
    [-1, -1,  2, -1],  # G
    [-1, -1, -1,  2],  # T
]
sw_gap_score = -2        # Score for EACH gap base (linear gap model).
sw_cells_to_show = None  # None = full table; 0, 1, 2, ... reveal the fill order.
sw_inspect = None        # None = automatic; or a DP cell such as (4, 4).
'''
SW_RUN = '''\
sw_result = sw_align(sw_sequence_1, sw_sequence_2, sw_scoring_matrix, sw_gap_score)
sw_figure = sw_show(sw_result, sw_cells_to_show, sw_inspect)
'''

DATA = '''\
# Six invented blocks of ten bases; Python joins these strings.
reference = (
    "ATATATATAT"
    "GCGCGCGCGC"
    "ATGCATGCAT"
    "GGCCAAAATT"
    "CCGGAATTGC"
    "ATATGGCCGC"
)
print("Synthetic reference length:", len(reference))
'''

WINDOWS = '''\
window_size = 10
starts = []
widths = []
gc_values = []
for start in range(0, len(reference), window_size):
    window = reference[start:start + window_size]
    gc = window.count("G") + window.count("C")
    percent = 100 * gc / len(window)
    starts.append(start)
    widths.append(len(window))
    gc_values.append(percent)
print("Starts:", starts)
print("Widths:", widths)
print("GC (%):", gc_values)
'''

PLOT = '''\
# Supplied drawing code. Read the labels; the calculation is in the previous cell.
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
    print("Plotting is unavailable. Use the printed Starts, Widths, and GC (%) lists.")

if plt is not None:
    plt.figure(figsize=(10, 3))
    plt.bar(starts, gc_values, width=widths, align="edge", edgecolor="white")
    plt.xlim(0, len(reference))
    plt.ylim(0, 100)
    plt.xlabel("Position boundary (0-based; right boundary excluded)")
    plt.ylabel("GC (%)")
    plt.title("Invented DNA: GC in non-overlapping windows")
    plt.tight_layout()
    plt.show()
'''

BROWSER = '''\
# Optional supplied renderer: a preview for a project, not a required coding task.
# Each annotation is (label, start, stop). These intervals are invented.
features = [("Toy feature A", 12, 26), ("Toy feature B", 38, 54)]

def show_region(region_start, region_stop):
    if type(region_start) is not int or type(region_stop) is not int:
        raise ValueError("Region boundaries must be integers")
    if not (0 <= region_start < region_stop <= len(reference)):
        raise ValueError("Use 0 <= start < stop <= 60 for this synthetic reference")
    print("Visible DNA:", reference[region_start:region_stop])
    print("GC windows keep the boundaries calculated in Step 6; zoom only crops the view.")
    if plt is None:
        for label, start, stop in features:
            if start < region_stop and stop > region_start:
                print(label, "visible interval:", max(start, region_start), min(stop, region_stop))
        return
    figure, axes = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
    axes[0].bar(starts, gc_values, width=widths, align="edge", edgecolor="white")
    axes[0].set_ylim(0, 100)
    axes[0].set_ylabel("GC (%)")
    axes[0].set_title("Mini browser: invented DNA and invented annotations")
    for row, (label, start, stop) in enumerate(features):
        axes[1].broken_barh([(start, stop - start)], (row - 0.2, 0.4))
    axes[1].set_yticks([0, 1])
    axes[1].set_yticklabels([item[0] for item in features])
    axes[1].set_ylim(-0.5, 1.5)
    axes[1].set_xlim(region_start, region_stop)
    axes[1].set_xlabel("Position boundary (0-based; right boundary excluded)")
    figure.tight_layout()
    plt.show()

show_region(0, 60)
'''


def build(solution=False):
    cells = []

    def add(kind, source, *, tags=(), title=None):
        cell = {"cell_type": kind, "id": f"week04-{len(cells):02d}",
                "metadata": {"tags": list(tags)} if tags else {},
                "source": textwrap.dedent(source).strip() + "\n"}
        if kind == "code":
            cell.update(execution_count=None, outputs=[])
        if title:
            cell = form_cell(cell, title)
        cells.append(cell)

    def md(source):
        add("markdown", source)

    def code(source, **kwargs):
        add("code", source, **kwargs)

    md('''\
    # Week 4 — Python, one small step at a time

    **A guided in-class workshop.** Follow the instructor, one cell at a time.
    We will turn a DNA string into a picture of its G/C composition. All DNA
    and annotations are invented. This is a sequence viewer, not a gene finder.

    Each step has four actions: **predict → run → change → explain**. Working
    examples are supplied. You will edit small pieces rather than complete a
    large function. Running the untouched notebook works, but your own changes
    and explanations are the exercise.

    Keep an answer below each step. If working in pairs, take turns typing and
    explaining. You do not need to remember Python syntax before class.
    ''')
    if solution:
        md("**Instructor edition.** The same working cells appear here, with suggested answers and pacing cues. Give students `exercise.ipynb`.")
    md(f'''\
    ## Open your copy and run the first cell

    [Open in Colab]({colab_url(4, solution)}) ·
    [Colab help](https://research.google.com/colaboratory/faq.html)

    If the GitHub copy is unavailable, upload this downloaded `.ipynb` to Colab.
    Save your own copy as `week04_yourname.ipynb`. Use a Python 3 CPU runtime.
    Run a cell with its ▶ button or **Shift+Enter**. Code produces output below;
    Markdown cells hold explanations. Double-click Markdown to write an answer.

    A variable exists only after you run its assignment. Editing a cell does
    not run it. After a runtime restart, run the notebook from the top. A saved
    output may describe old code: rerun the cell before trusting that output.

    All data are included. No package installation, file download, Drive mount,
    or GPU is required. Colab normally supplies matplotlib for drawing; if it
    is unavailable, the printed numerical results still let you complete the
    exercise. Save the notebook with your outputs and explanations.
    ''')
    code('''\
    import sys
    print("Python:", sys.version.split()[0])
    print("Week 4 ready — run the next cell together")
    ''', tags=["setup"])

    md('''\
    ## 1. Store a DNA sequence and print it

    `dna` is a name for a value. The letters inside quotes form a **string**.
    `=` assigns the string to the name. `print(...)` displays a value, and
    `len(...)` counts the characters. `#` begins a comment for the reader.

    **Predict:** how many letters will Python report?
    ''')
    code('''\
    dna = "ATGCGCAT"
    print(dna)
    print(len(dna))
    ''')
    md('''\
    **Check:** the output is `ATGCGCAT`, then `8`.
    **Change:** add one A inside the quotes, rerun, and check that the length is 9.
    Restore `ATGCGCAT` and rerun before continuing.

    **My observation:** I changed … ; Python printed … ; `len` measures … .
    ''')

    md('''\
    ## 2. Select letters by position

    Python starts at position 0. Here is the eight-letter example:

    ```text
    index: 0 1 2 3 4 5 6 7
    base:  A T G C G C A T
    ```

    `dna[0]` selects one letter. `dna[2:6]` selects positions 2, 3, 4, and 5:
    include the start and exclude the stop. There are `6 - 2 = 4` letters.
    **Predict both outputs before running.**
    ''')
    code('''\
    dna = "ATGCGCAT"  # Restore our shared example.
    print(dna[0])
    print(dna[2:6])
    ''')
    md('''\
    **Check:** `A`, then `GCGC`. **Change:** select the first four letters by
    replacing `2:6` with `0:4`. Predict and then check `ATGC`.

    **My explanation:** the slice includes index … and excludes index … .
    ''')

    md('''\
    ## 3. Calculate GC percentage

    GC percentage is the fraction of letters that are G or C, multiplied by
    100. For this sequence, count 2 Gs and 2 Cs: `100 × (2 + 2) / 8 = 50%`.
    `dna.count("G")` counts exact uppercase G characters. `+` adds counts,
    `*` multiplies, and `/` divides. Our inputs are nonempty uppercase A/C/G/T
    strings. Lowercase letters and N would need an explicit handling rule.
    ''')
    code('''\
    dna = "ATGCGCAT"
    g_count = dna.count("G")
    c_count = dna.count("C")
    gc_percent = 100 * (g_count + c_count) / len(dna)
    print("G:", g_count, "C:", c_count)
    print("GC (%):", gc_percent)
    ''')
    md('''\
    **Change:** use `ATATGCAT` in this cell. Calculate the new result by hand,
    then rerun: `100 × 2 / 8 = 25%`. Restore the original string afterward.
    GC composition alone cannot tell you that a segment is a gene or is active.

    **My calculation:** … Gs + … Cs out of … bases gives … %.
    ''')

    md('''\
    ## 4. Repeat a simple operation with a loop

    A **list** holds several values inside square brackets. A `for` loop takes
    them one at a time. The colon introduces the loop body. The indented line
    runs once for each value. `fragment` is the name of the current value.

    **Predict:** how many lines will appear, and in what order?
    ''')
    code('''\
    fragments = ["ATAT", "GCGC", "ATGC"]
    for fragment in fragments:
        print(fragment, len(fragment))
    ''')
    md('''\
    **Check:** `ATAT 4`, `GCGC 4`, `ATGC 4`.
    **Write:** inside the loop, add `print(fragment.count("G"))` on a new
    indented line. The additional counts should be 0, 2, 1.
    Do not put that line after the loop without indentation: then it runs only
    once, with the final fragment. Use four spaces for each loop-body line.

    **My explanation:** `fragment` changes from … to … to … .
    ''')
    if solution:
        md("Instructor: type the extra print line live. Ask students to point at the colon and the two equally indented lines. Pause here if they cannot explain which lines repeat.")

    md('''\
    ## 5. Walk along a longer DNA string

    Now use a new 60-base synthetic reference. No connection to a measured
    organism or to the fictional cultures is implied. The following cell
    supplies the DNA; you only need to run it.
    ''')
    code(DATA, tags=["data"])
    md('''\
    `range(0, 60, 10)` produces 0, 10, 20, 30, 40, 50. Its arguments are start,
    stop (excluded), and step. At each start we take ten letters with a slice.
    First follow just the iteration where `start` is 10.
    ''')
    code('''\
    for start in range(0, len(reference), 10):
        window = reference[start:start + 10]
        print(start, window)
    ''')
    md('''\
    **Check:** the first two rows are `0 ATATATATAT` and `10 GCGCGCGCGC`.
    **Change:** use 20 in **both** places where 10 appears. Predict three
    windows, then run. Restore both 10s afterward. Changing only the range step
    to 20 would skip every other ten-base block.

    **My trace:** when `start = 10`, the slice is `reference[10:20]` and contains … .
    ''')

    md('''\
    ## 6. Save one result for each window

    We combine the calculation from Step 3 with the loop from Step 5. `[]`
    starts an empty list; `.append(value)` puts one value at its end. The
    lists keep the left boundary, actual width, and GC percentage for each bar.
    Read the loop one line at a time with the instructor.

    **Predict:** the first two windows should give 0% and 100%. The left
    boundaries are 0 and 10. The next code cell resets the lists each time,
    so rerunning it will not duplicate the results.
    ''')
    code(WINDOWS, tags=["window-calculation"])
    md('''\
    **Check at size 10:** starts `[0, 10, 20, 30, 40, 50]`; widths all 10;
    percentages `[0, 100, 40, 40, 60, 60]`. Python may display decimal `.0`.

    **Change:** set `window_size = 20`. Predict `[50, 40, 60]`, then rerun.
    Return to 10 before the next step. Use positive integer sizes.
    For a size that does not divide 60, the last window is shorter: division by
    `len(window)` uses its actual number of bases, not the requested size.

    **My explanation:** the first twenty-base window has … G/C bases out of … .
    ''')

    md('''\
    ## 7. Draw the results

    The drawing code is supplied. A bar begins at `starts`, extends over
    `widths` bases, and reaches the percentage in `gc_values`. The vertical
    scale stays at 0–100 so different settings can be compared.
    `import` loads a library; here matplotlib draws the figure.

    **Run** the next cell. **Change** `window_size` to 20 in Step 6, rerun
    Step 6, then rerun this plot. Changing the number without rerunning the
    calculation leaves the old lists in memory.
    ''')
    code(PLOT, tags=["plot"])
    md('''\
    **Explain:** why does the first 20-base bar have height 50%, although its
    two ten-base halves are 0% and 100%? Which detail disappears in the bigger
    window? A bar averages the letters in an interval; it does not display
    each base or measure gene activity.

    **My answer:** …

    Restore size 10 and rerun the calculation and plot. Save your notebook.
    You have completed the core programming exercise.
    ''')

    md('''\
    ## When something goes wrong

    Read the final line of the error, then the highlighted line in your cell.
    Change one thing and rerun. These are examples to discuss, not cells you
    need to execute:

    | Symptom | Likely cause | Next action |
    |---|---|---|
    | `NameError: name 'reference' is not defined` | Data cell has not run in this runtime | Run Step 5 data, then the calculation |
    | `NameError` for `dna = ATGC`, or `SyntaxError` for an unfinished quote | DNA text needs matching quotes | Use `dna = "ATGC"` |
    | `IndentationError` after `for` | Python cannot find an indented body | Put four spaces before each line inside the loop |
    | `IndexError` for `dna[8]` on eight letters | Valid indexes are 0–7 | Use `dna[7]` for the last letter |
    | `ZeroDivisionError` | An empty sequence has length zero | Restore a nonempty input; do not report an empty sequence as 0% GC |
    | Plot did not change | An earlier cell was edited but not rerun | Rerun calculation, then plot |

    **Pair debugging task:** one person explains why `range(0, 60, 0)` cannot
    advance; the other repairs it to use step 10. The error is `ValueError`.
    ''')

    md('''\
    ## Project preview — A tiny genome browser

    A browser places different tracks on the same coordinate axis. Here the
    first track is your GC calculation. The second uses two **invented feature
    annotations**, A at `[12,26)` and B at `[38,54)`. The brackets mean start
    included, stop excluded. These annotations are supplied independently;
    GC does not predict them. No strand, exon structure, or real gene identity
    is represented.

    This optional code is already complete. Run it after Step 7. A **function**
    is a named set of instructions: `def` defines `show_region`; the final line
    calls it with start 0 and stop 60. You need only change its two arguments.
    ''')
    code(BROWSER, tags=["optional", "browser-preview"], title="Optional supplied mini-browser renderer")
    md('''\
    **Optional change:** call `show_region(10, 40)`. Feature A is fully in view;
    feature B is visible only from 38 to 40. Its annotation still ends at 54.
    Zoom crops already calculated GC bars; it does not recompute their windows.

    This is a classroom starting point. The six-week browser project adds
    file loading, region navigation, validation, automated tests, and an
    analysis of one documented reference region. Its full scope is in the
    Week 4 project menu. See the [UCSC user guide](https://genome.ucsc.edu/goldenPath/help/hgTracksHelp.html)
    for a real example and the [BED coordinate definition](https://genome.ucsc.edu/FAQ/FAQformat.html#format1)
    for start-inclusive, stop-exclusive intervals. Browser search boxes may
    display 1-based positions; label your own convention explicitly.
    ''')

    md('''\
    ## After class — Consolidate and choose your project scope

    Allow **60–90 minutes separately from class**: 10–15 to rerun and repair
    your notebook, 25–35 for the transfer task, and 25–40 for personal project
    planning. The planning time counts toward the project budget below;
    these notes are not a separate proposal submission.

    **Transfer task:** in a new code cell, use `practice_dna = "GGCCATATGC"`.
    Write three lines: assign that string, calculate its GC percentage into
    `practice_gc`, and print it. Then modify the calculation to use only
    `practice_dna[0:4]`. Check by counting the letters on paper. Explain why
    the denominator must also change for that slice. If stuck, copy Step 3 and
    change one line at a time. Add your code cell below this paragraph.

    **Final project: 30% of the final grade.** Choose either a research project
    or a coding project and complete it within **six weeks**, with approximately **four hours
    per week (24 hours total)**. This includes reading, implementation or
    analysis, testing, writing, and preparing the final explanation. Organize
    your own time: there are no weekly milestones or interim submissions.
    Follow the instructor's calendar deadline and submission instructions.

    Coding projects assume **intermediate Python** and require functions,
    file input, validation, tests, and a documented analysis or visualization.
    The supplied workshop alone is not a complete project. Research projects
    compare published evidence and include a worked example, with a report
    and presentation as the final deliverables; no programming is required.
    Research and coding are separate choices.

    **Two full research examples:** compare sequencing mechanisms for a
    defined task, or explain repeat ambiguity using a published assembly case.

    **Two full coding examples:** build a genome-region browser, or build an
    LLM bioinformatics question-answering tool that retrieves short source
    passages and checks answer support. The LLM project uses one model,
    10–15 passages, and 12 questions, including held-out questions and cases
    where the collection does not contain an answer. It is an implementation
    and evaluation task; no model training is required.

    The Week 4 page also lists ten one-line alternatives, including research
    on LLM evaluation and a coding project that extracts study fields from
    abstracts. Choose one project, using its type's final deliverables and
    the 24-hour budget; the additional ideas are not extra assignments.
    See the page for the full briefs and final deliverables.

    **Personal planning notes:** record your route, one question, the intended
    reader/user, sources or data, the complete core deliverable, a way to check
    it, and a limitation. Identify which optional features you will leave out.
    No separate planning document needs to be submitted.

    Save the notebook with your edits, visible outputs, explanations, and
    personal planning notes. Restart the runtime and run the core cells in order
    to confirm your notebook no longer depends on old variables. The optional
    preview can be skipped. Follow the instructor's instructions for saving
    workshop work; the complete project is submitted after six weeks.
    ''')
    code("# Add your three-line transfer task here.\n# This empty starter is intentional; no exception is raised.", tags=["transfer-task"])
    md("**My project planning notes (not a separate submission)**\n\nProject type (research or coding): …\n\nQuestion: …\n\nReader/user: …\n\nSources/data: …\n\nComplete core deliverable within 24 hours: …\n\nCheck: …\n\nLimitation and excluded extensions: …\n\nResult I checked and how: …")
    if solution:
        md('''\
        ## Instructor answers and live-coding cues

        1. Eight bases; appending A gives nine. Restore the eight-base example.
        2. Index 0 is A. Slice 2:6 is GCGC; 0:4 is ATGC.
        3. Original: 2 G + 2 C / 8 = 50%. Changed: 1 G + 1 C / 8 = 25%.
        4. Three lines before the extra print, six afterward. Added G counts: 0, 2, 1.
        5. Starts 0,10,20,30,40,50. With both literals changed to 20: 0,20,40.
        6. Size 10: GC 0,100,40,40,60,60. Size 20: 50,40,60. Each pair of
           equal-width bins contributes equally. In general, unequal widths
           require weighting by their actual base counts.
        7. Averaging the first two bins hides the low/high split. No evidence
           about transcription or gene boundaries is created by drawing it.

        Transfer: the ten-base string has 6 G/C bases, so 60%. Its first four
        letters GGCC have 4/4, or 100%. A denominator of 10 for the slice would
        incorrectly give 40%. Optional preview 10:40 clips B to 38:40.

        Suggested support: ask “Which line did you run last?” before changing
        a student's code. Have them read a slice in plain language. At Step 6,
        trace two iterations on the board before showing the full loop.
        If loops remain difficult, supply Step 6 unchanged and prioritize
        explaining one window and rerunning its plot. Functions and the
        browser renderer remain optional.
        ''')
        code('''\
        practice_dna = "GGCCATATGC"
        practice_gc = 100 * (practice_dna.count("G") + practice_dna.count("C")) / len(practice_dna)
        print(practice_gc)
        practice_slice = practice_dna[0:4]
        print(100 * (practice_slice.count("G") + practice_slice.count("C")) / len(practice_slice))
        ''', tags=["instructor-answer"])
    md('''\
    ## References

    - [Python: strings, numbers, and lists](https://docs.python.org/3/tutorial/introduction.html)
    - [Python: for loops and range](https://docs.python.org/3/tutorial/controlflow.html)
    - [Matplotlib: drawing and labeling plots](https://matplotlib.org/stable/tutorials/pyplot.html)

    Examples and teaching text were written for this course. Notebook form
    metadata uses the shared course helper, whose packaging follows the
    Apache-licensed upstream Colab form pattern; see `LICENSE.upstream.txt`.
    ''')
    md('''\
    ## Smith–Waterman simulator — Generate your own alignment examples

    This optional simulator is ready to use. It does **local alignment**:
    it finds high-scoring subsequences, so unmatched ends may be left out.
    You do not need to implement the algorithm or finish earlier exercises
    to use it. Run the cells in this section in order.

    1. Run **Load the simulator** once per runtime. All its code is embedded here.
    2. Edit **Settings**: two DNA sequences, the 4×4 substitution matrix,
       and the gap score. Run Settings, then **Calculate and display**.
    3. Optionally run the final widget cell for text fields, a score grid,
       an **Align / reset table** button, and a fill-progress slider.

    Use 1–30 bases per sequence. Lowercase and surrounding whitespace are
    normalized; internal spaces, N, gaps, and other symbols are rejected.
    Scores are integers, and the gap score must be negative. The four matrix
    rows refer to sequence 1 and the columns to sequence 2, in A/C/G/T order.
    You can change every entry; symmetry is not required. If you want a
    symmetric rule, edit both mirrored entries, such as A/G and G/A.

    The matrix here contains **substitution scores**. The **DP table** is
    calculated from them; its rows and columns are sequence-prefix lengths.
    A gap of length three costs three times the gap score. This is a linear
    model, not an affine gap-open/gap-extension model. Sequences are used in
    their supplied forward orientation; the simulator does not search the
    reverse complement automatically.
    ''')
    code(SW_IMPLEMENTATION, tags=["optional", "smith-waterman-core"],
         title="Load the simulator — supplied implementation")
    md('''\
    ### Settings — Edit the sequences and scoring matrix

    For the defaults, predict the best shared local segment before running.
    A substitution score is added for each aligned letter pair; the gap score
    is added for a column containing one gap. Set `sw_cells_to_show` to an
    integer from 0 to `len(sequence_1) * len(sequence_2)` to reveal a partial
    table, or leave it as `None` for the complete result.
    ''')
    code(SW_SETTINGS, tags=["optional", "smith-waterman-settings"])
    md('''\
    ### Calculate and display

    With sequence 1 along the rows and sequence 2 along the columns,

    ```text
    H[i,j] = max(0,
                 H[i-1,j-1] + substitution(sequence_1[i-1], sequence_2[j-1]),
                 H[i-1,j]   + gap_score,
                 H[i,j-1]   + gap_score)
    ```

    Row 0 and column 0 start at zero. A diagonal step aligns two letters;
    an up step puts a gap in sequence 2; a left step puts a gap in sequence 1.
    Choosing zero restarts the local alignment. Cells fill left to right,
    then top to bottom. Dots mean “not filled yet,” rather than score zero.

    The inspected cell shows all four candidate values. On the complete
    table, orange arrows and bracketed text cells show traceback from the
    maximum to zero. The displayed alignment uses zero-based, stop-exclusive
    sequence intervals; DP indices instead count consumed letters.

    **Default check:** ACGT aligns with ACGT, score 8, at interval [2,6) in
    both sequences. Cell H[4,4] aligns C/C: its diagonal predecessor is 2,
    so 2 + 2 = 4 wins. This is one optimal alignment. For tied maximum cells,
    the first in row-major order is selected; tied traceback moves prefer
    diagonal, then up, then left. No positive score gives an empty local
    alignment with score zero. A high score alone does not establish a
    biological relationship or statistical significance.
    ''')
    code(SW_RUN, tags=["optional", "smith-waterman-output"])
    md('''\
    ### Optional controls — Change settings without editing code

    These controls require `ipywidgets` in your notebook environment. If they
    are unavailable, use the Settings and Calculate cells above; no installation
    is necessary for that route. Matplotlib supplies the heatmap when available,
    and the printed table, recurrence values, and alignment work without it.

    Edit the two sequence fields, score grid, or gap score, then press
    **Align / reset table** to apply them. Move **Filled cells** back to zero
    and forward to watch the table build. The full alignment is revealed only
    when all cells are filled. **Inspect row/col** chooses a cell to explain.
    After changing sequence lengths, the slider and inspection bounds reset.

    Widget edits are temporary: copy the chosen settings into the Settings
    code cell and rerun Settings and Calculate before saving an example to
    share. The printed output includes both sequences and all scores.

    **Try three experiments:** (1) change only a mismatch score and inspect a
    cell that uses it; (2) compare `ACGTT` with `ACTT`, using gap scores −1
    and −3; (3) set every substitution score to −1 and explain why the best
    local score becomes zero. Record the settings, score, and alignment for
    each. Do not compare scores from different scoring rules as if their
    numerical scales were interchangeable.

    Algorithm source: Smith and Waterman (1981),
    [Identification of common molecular subsequences](https://pubmed.ncbi.nlm.nih.gov/7265238/).
    This course implementation uses the explicitly stated linear-gap model.
    ''')
    code('sw_widget_controls = sw_controls(sw_sequence_1, sw_sequence_2, sw_scoring_matrix, sw_gap_score)',
         tags=["optional", "smith-waterman-controls"])
    filename = "solutions" if solution else "exercise"
    return {"cells": cells, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
        "colab": {"name": f"week-04-{filename}.ipynb", "provenance": [], "toc_visible": True}},
        "nbformat": 4, "nbformat_minor": 5}


def main():
    for solution, name in ((False, "exercise"), (True, "solutions")):
        (HERE / f"{name}.ipynb").write_text(json.dumps(build(solution), indent=1) + "\n")
    print("Wrote Week 4 workshop and instructor notebooks")


if __name__ == "__main__":
    main()
