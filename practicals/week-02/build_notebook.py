"""Build the standalone Week 2 homework and separate instructor reference.

Run from the repository root: python3 practicals/week-02/build_notebook.py
Standard library only. Teaching scope draws on bioinformatis-web lecture 02
and lecture 19; rewritten for the shortened course, 18 October 2026. The notebook
format and beginner instructions continue Week 1. See README.md for provenance.
"""

from pathlib import Path
import contextlib
import inspect
import io
import json
import textwrap
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from notebook_helpers import prepare_notebook

HERE = Path(__file__).resolve().parent

SETUP = '''\
# All data and all computations live in this notebook. No downloads or installs.
REFERENCE = "ATGCCATGACCTATGCCA"
READS = {"repeated": "ATGCCA", "unique": "CCATGA", "changed": "ATGCTA"}
MATCH, MISMATCH, GAP = 2, -1, -2

def validate_dna(sequence, allow_empty=True):
    if not isinstance(sequence, str):
        raise TypeError("DNA must be a string")
    if not allow_empty and not sequence:
        raise ValueError("The query must contain at least one DNA letter")
    if any(base not in "ACGT" for base in sequence):
        raise ValueError("This exercise accepts uppercase A/C/G/T only")

print("Reference:", REFERENCE)
print("Index:    ", "".join(str(i // 10) if i >= 10 else " " for i in range(len(REFERENCE))))
print("          ", "".join(str(i % 10) for i in range(len(REFERENCE))))
print("Toy reads:", READS)
print("Alignment scores: match +2, mismatch -1, each gap column -2")
'''

SEARCH_SOLUTION = '''\
def find_all(reference, query):
    """Return every exact forward-strand match start, in ascending order."""
    validate_dna(reference)
    validate_dna(query, allow_empty=False)
    positions = []
    for start in range(len(reference) - len(query) + 1):
        if reference[start:start + len(query)] == query:
            positions.append(start)
    return positions
'''

SEARCH_STARTER = '''\
def find_all(reference, query):
    """Return every exact forward-strand match start, in ascending order."""
    validate_dna(reference)
    validate_dna(query, allow_empty=False)
    positions = []
    # TODO: try every possible start, including the final valid start.
    # Compare a query-length slice; append the start if it matches.
    # Advance one position at a time so overlapping matches are included.
    raise NotImplementedError("Find all exact matches")
    return positions
'''

SEARCH_CHECKS = '''\
assert find_all(REFERENCE, "ATGCCA") == [0, 12]
assert find_all(REFERENCE, "CCATGA") == [3]
assert find_all(REFERENCE, "ATGCTA") == []
assert find_all("AAAAA", "AAA") == [0, 1, 2]  # overlapping matches
assert find_all("ACGT", "GT") == [2]  # final valid start
assert find_all("AC", "ACG") == []
assert find_all("", "A") == []
assert find_all("AC", "AC") == [0]
for invalid_reference, invalid_query in (("AC", ""), ("AC", "N"), ("ac", "A")):
    try:
        find_all(invalid_reference, invalid_query)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected invalid DNA / empty query to be rejected")

exact_results = {name: find_all(REFERENCE, read) for name, read in READS.items()}
for name, positions in exact_results.items():
    print(name, READS[name], "->", positions)
print("All exact-search checks passed.")
'''

SCORE_PREFIX = '''\
def score_alignment(aligned_reference, aligned_read):
    """Score equal-length aligned strings using +2 / -1 / linear -2."""
    if len(aligned_reference) != len(aligned_read):
        raise ValueError("Aligned strings must have equal lengths")
    if any(symbol not in "ACGT-" for symbol in aligned_reference + aligned_read):
        raise ValueError("Aligned strings may contain uppercase A/C/G/T and '-' only")
    if any(a == b == "-" for a, b in zip(aligned_reference, aligned_read)):
        raise ValueError("A column cannot contain two gaps")
    total = 0
'''

SCORE_SOLUTION = SCORE_PREFIX + '''\
    for a, b in zip(aligned_reference, aligned_read):
        if a == "-" or b == "-":
            total += GAP
        elif a == b:
            total += MATCH
        else:
            total += MISMATCH
    return total
'''

SCORE_STARTER = SCORE_PREFIX + '''\
    # TODO: loop over aligned columns with zip.
    # A column containing one '-' scores GAP; identical letters score MATCH;
    # different letters score MISMATCH. Add each score to total.
    raise NotImplementedError("Score the aligned columns")
    return total
'''

SCORE_CHECKS = '''\
assert score_alignment("ACGT", "ACGT") == 8
assert score_alignment("ACGT", "ACCT") == 5
assert score_alignment("ACGT", "A-GT") == 4
assert score_alignment("ACGT", "AGT-") == -2
assert score_alignment("AC--GT", "ACCCGT") == 4  # two gap columns cost -4
assert score_alignment("", "") == 0
for bad_pair in (("AC", "A"), ("A-", "A-"), ("AN", "AC"), ("a", "A")):
    try:
        score_alignment(*bad_pair)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected malformed aligned strings to be rejected")
print("Hand-check: ACGT / A-GT ->", score_alignment("ACGT", "A-GT"))
print("Unshifted alternative: ACGT / AGT- ->", score_alignment("ACGT", "AGT-"))
print("Alignment-scoring checks passed.")
'''

TABLE_PREFIX = '''\
def nw_table(reference, read):
    """D[i][j] = best global score for reference[:i] aligned with read[:j]."""
    validate_dna(reference)
    validate_dna(read)
    m, n = len(reference), len(read)
    table = [[0] * (n + 1) for _ in range(m + 1)]
'''

TABLE_SOLUTION = TABLE_PREFIX + '''\
    for i in range(1, m + 1):
        table[i][0] = i * GAP
    for j in range(1, n + 1):
        table[0][j] = j * GAP
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            pair = MATCH if reference[i - 1] == read[j - 1] else MISMATCH
            diagonal = table[i - 1][j - 1] + pair
            up = table[i - 1][j] + GAP
            left = table[i][j - 1] + GAP
            table[i][j] = max(diagonal, up, left)
    return table
'''

TABLE_STARTER = TABLE_PREFIX + '''\
    # TODO 1: initialize the first column and first row.
    # Aligning i letters to an empty string requires i gap columns.
    # Keep table[0][0] = 0. Use GAP for the cost of each column.
    raise NotImplementedError("Initialize the global-alignment boundaries")

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            pair = MATCH if reference[i - 1] == read[j - 1] else MISMATCH
            # TODO 2: calculate diagonal, up, and left candidate scores.
            # TODO 3: store the largest candidate in table[i][j].
            raise NotImplementedError("Choose the best of three previous states")
    return table
'''

TABLE_CHECKS = '''\
assert nw_table("", "") == [[0]]
assert nw_table("AC", "") == [[0], [-2], [-4]]
assert nw_table("", "AG") == [[0, -2, -4]]
assert nw_table("AC", "AG") == [[0, -2, -4], [-2, 2, 0], [-4, 0, 1]]
assert nw_table("ACGT", "AGT")[-1][-1] == 4

def print_table(reference, read, table):
    print("      " + "".join(f"{letter:>4}" for letter in "-" + read))
    for letter, row in zip("-" + reference, table):
        print(f"{letter:>4}  " + "".join(f"{value:>4}" for value in row))

print("Rows: reference prefixes; columns: read prefixes. '-' labels empty prefix.")
print_table("AC", "AG", nw_table("AC", "AG"))
print("Score-table checks passed.")
'''

TRACEBACK = '''\
# Supplied: you implement the score table; this code recovers one optimum.
def traceback_global(reference, read, table):
    """Recover an alignment, breaking score ties diagonal > up > left."""
    i, j = len(reference), len(read)
    aligned_reference, aligned_read = [], []
    while i > 0 or j > 0:
        pair = MATCH if i > 0 and j > 0 and reference[i - 1] == read[j - 1] else MISMATCH
        if i > 0 and j > 0 and table[i][j] == table[i - 1][j - 1] + pair:
            aligned_reference.append(reference[i - 1])
            aligned_read.append(read[j - 1])
            i, j = i - 1, j - 1
        elif i > 0 and table[i][j] == table[i - 1][j] + GAP:
            aligned_reference.append(reference[i - 1])
            aligned_read.append("-")
            i -= 1
        elif j > 0 and table[i][j] == table[i][j - 1] + GAP:
            aligned_reference.append("-")
            aligned_read.append(read[j - 1])
            j -= 1
        else:
            raise ValueError("No valid traceback step; check the score table")
    return "".join(reversed(aligned_reference)), "".join(reversed(aligned_read))

def global_alignment(reference, read):
    """Return (aligned reference, aligned read, optimal score)."""
    table = nw_table(reference, read)
    aligned_reference, aligned_read = traceback_global(reference, read, table)
    return aligned_reference, aligned_read, table[-1][-1]
'''

COMPARISON = '''\
CASES = [
    ("exact", "ATGCCA", "ATGCCA"),
    ("one substitution", "ATGCCA", "ATGCTA"),
    ("one deletion relative to reference", "ATGCCA", "ATGCA"),
    ("one insertion relative to reference", "ATGCCA", "ATGACCA"),
    ("all mismatches", "AAAA", "TTTT"),
]
alignment_results = []
for label, reference_fragment, read in CASES:
    aligned_reference, aligned_read, score = global_alignment(reference_fragment, read)
    assert aligned_reference.replace("-", "") == reference_fragment
    assert aligned_read.replace("-", "") == read
    assert score_alignment(aligned_reference, aligned_read) == score
    alignment_results.append({"case": label, "reference": reference_fragment,
                              "read": read, "aligned_reference": aligned_reference,
                              "aligned_read": aligned_read, "score": score})
    print(f"{label}: score {score}")
    print("  reference", aligned_reference)
    print("  read     ", aligned_read)

assert [result["score"] for result in alignment_results] == [12, 9, 8, 10, -4]
assert global_alignment("", "AG") == ("--", "AG", -4)
assert global_alignment("AC", "") == ("AC", "--", -4)
# Two equally optimal gap placements. The supplied tie rule reports the first.
assert global_alignment("AA", "A") == ("AA", "-A", 0)
assert score_alignment("AA", "A-") == 0
print("All fragment comparisons and traceback checks passed.")
'''

OPTIONAL_SOLUTION = '''\
def reverse_complement(sequence):
    validate_dna(sequence)
    complement = {"A": "T", "T": "A", "C": "G", "G": "C"}
    return "".join(complement[base] for base in reversed(sequence))

opposite_read = "TCATGG"
assert reverse_complement(opposite_read) == "CCATGA"
assert find_all(REFERENCE, opposite_read) == []
assert find_all(REFERENCE, reverse_complement(opposite_read)) == [3]
print("Optional strand search:",
      {"forward": find_all(REFERENCE, opposite_read),
       "reverse_complement": find_all(REFERENCE, reverse_complement(opposite_read))})
'''


def reference_namespace():
    namespace = {}
    with contextlib.redirect_stdout(io.StringIO()):
        for source in (SETUP, SEARCH_SOLUTION, SEARCH_CHECKS, SCORE_SOLUTION,
                       SCORE_CHECKS, TABLE_SOLUTION, TABLE_CHECKS, TRACEBACK,
                       COMPARISON, OPTIONAL_SOLUTION):
            exec(source, namespace)
    return namespace


def reference_results(namespace):
    return {
        "reference": namespace["REFERENCE"],
        "coordinate_system": "zero-based start positions; forward strand unless labelled otherwise",
        "scoring": {"match": 2, "mismatch": -1, "gap_per_column": -2},
        "exact_matches": namespace["exact_results"],
        "overlap_example": {"reference": "AAAAA", "query": "AAA", "positions": [0, 1, 2]},
        "score_table_AC_AG": namespace["nw_table"]("AC", "AG"),
        "alignments": namespace["alignment_results"],
        "tie_example": {"reference": "AA", "read": "A", "aligned_reference": "AA",
                        "aligned_read": "-A", "score": 0,
                        "equivalent_aligned_read": "A-", "rule": "diagonal > up > left"},
        "optional_strands": {"query": "TCATGG", "reverse_complement": "CCATGA",
                             "forward_positions": [], "reverse_complement_positions": [3]},
    }


def build(solution=False, reference=None):
    cells = []

    def add(kind, source):
        result = {"cell_type": kind, "id": f"week02-{len(cells):02d}", "metadata": {},
                  "source": (inspect.cleandoc(source) if kind == "markdown"
                             else textwrap.dedent(source).strip()) + "\n"}
        if kind == "code":
            result.update(execution_count=None, outputs=[])
        cells.append(result)

    def md(source):
        add("markdown", source)

    def code(source):
        add("code", source)

    md("""# Homework 02 — Where does this sequence belong?

    Complete after Week 2, before Week 3

    A read can match several places even when its letters have high quality
    scores. Search an 18-base reference for every exact match, then compare
    short fragments that contain mismatches or gaps. You will implement the
    score table for a global alignment; the supplied traceback recovers an alignment.

    All sequences are invented examples, separate from the Week 1 cell cultures.
    A match here describes these strings; it supplies no experimental result
    about the cultures.

    You will use Python loops, lists, slicing, functions, and `max`.
    The reverse-complement exercise is optional.

    **Submit:** this notebook with your initial prediction, exact-match positions,
    score table, printed alignments, and the three interpretation sentences
    requested in Step 5.

    Follow the Colab setup instructions below, or use local Jupyter with
    Python 3.9 or later. All input sequences are included.

    <details>
    <summary>Reading an error message</summary>

    `NotImplementedError` marks an unfinished exercise. `NameError` usually means
    you skipped a cell or restarted the runtime; rerun setup and the preceding
    cells. For an `AssertionError`, compare the check's input and expected result
    with your function's output. After editing a function, run its definition
    again before its checks. Each step uses functions from the preceding steps.

    </details>
    """)
    if solution:
        md("**Instructor reference edition.** Functions are completed. Run all cells to reproduce the answer key. Distribute `exercise.ipynb` to students.")

    md("""## Step 1 — Predict where the read fits

    The class reference is `ATGCCATGACCTATGCCA`. Two reads are `ATGCCA` and
    `CCATGA`. Before calculating, mark every place each might fit.

    **My prediction:** The first read has … exact location(s), and the second
    has … . If one read fits twice, I think we can conclude … .

    In this notebook, **start coordinates are zero-based**: the first letter
    has index 0. An exact match starting at `s` occupies
    `reference[s:s + len(read)]`; the slice's right boundary is excluded.
    The search considers the displayed forward orientation only.

    | Word | Meaning here |
    |---|---|
    | Reference | The sequence we search or compare against |
    | Read/query | The sequence whose matching locations we seek |
    | Exact match | Every letter agrees in that window |
    | Alignment | A column-by-column comparison, possibly containing gaps |
    | Gap `-` | A placeholder in a comparison, not a measured DNA letter |

    The functions accept uppercase A/C/G/T. They reject N and lowercase input.
    Exact search also rejects an empty query. Global alignment accepts empty
    strings so you can test its first-row and first-column rules.
    """)
    code(SETUP)

    md("""## Step 2 — Return every exact match

    Complete `find_all`. Return **all** matching starts in ascending order,
    including overlapping matches. For example, `AAA` occurs three times in
    `AAAAA`: at starts 0, 1, and 2. Returning only the first hit would conceal
    ambiguity. A query longer than the reference has no matches.

    Run the checks and compare the result with your prediction. Can a unique
    exact match within this tiny reference guarantee uniqueness in a whole genome?

    <details>
    <summary>Hint: visit one possible start at a time</summary>

    A query of length k can start as late as `len(reference) - k`. Python's
    `range` excludes its stopping value, so account for the final valid start.
    Compare one query-length slice at each start and append the matching index.
    Advance by one, rather than by the query length, to preserve overlaps.

    </details>
    """)
    code(SEARCH_SOLUTION if solution else SEARCH_STARTER)
    code(SEARCH_CHECKS)

    md("""## Step 3 — Score an alignment

    Exact search misses reads with a substitution or a length difference.
    To compare imperfect matches, state a scoring rule first:

    | Aligned column | Score |
    |---|---:|
    | Same DNA letter | +2 |
    | Different DNA letters | −1 |
    | One letter and one gap `-` | −2 |

    This is a **linear gap penalty**: two gap columns cost −4, whether adjacent
    or separated. These are teaching scores, not probabilities or evidence that
    a specific evolutionary event happened. Changing the scoring rule can change
    the preferred alignment. Two gaps in the same column have no meaning here.

    Hand-score the comparison below, then complete `score_alignment`:

    ```text
    reference  A C G T
    read       A - G T
    ```

    Both aligned strings must have equal lengths. The supplied code already
    validates their alphabet and rejects double-gap columns. Your loop adds
    the score for each column.

    <details>
    <summary>Hint: three cases, one running total</summary>

    Use `zip` to visit paired columns. Check for a gap first, then a matching
    letter; the remaining case is a mismatch. Add the appropriate named constant
    to `total`. Return the total after the loop, not after its first column.

    </details>
    """)
    code(SCORE_SOLUTION if solution else SCORE_STARTER)
    code(SCORE_CHECKS)

    md("""## Step 4 — Find the best end-to-end score

    Guessing gap positions becomes difficult as sequences grow. **Dynamic
    programming** reuses the best answers for smaller prefixes. Here we use
    global Needleman–Wunsch alignment: every letter of both strings must appear
    in the alignment, including letters at the ends.

    `D[i][j]` stores the best score for `reference[:i]` aligned with `read[:j]`.
    Rows consume reference letters; columns consume read letters. At an interior
    cell there are exactly three ways to make the final aligned column:

    | Previous cell | Final column | Added score |
    |---|---|---|
    | ↖ `D[i-1][j-1]` | Reference letter / read letter | Match +2 or mismatch −1 |
    | ↑ `D[i-1][j]` | Reference letter / gap in read | −2 |
    | ← `D[i][j-1]` | Gap in reference / read letter | −2 |

    Add each column's score to its previous cell, then keep the **maximum**.
    Fill rows from top to bottom and columns from left to right, so the needed
    values already exist. The reference and read letters for cell `[i][j]` have
    Python indices `i-1` and `j-1`.

    **Boundaries:** `D[0][0] = 0`. Aligning i letters with an empty read requires
    i gap columns, so `D[i][0] = i × GAP`. Similarly `D[0][j] = j × GAP`.
    Starting the entire top row and left column at zero would allow free end
    gaps and solve a different problem.

    **One worked cell:** for `AC` / `AG`, the first interior cell pairs A with A.
    Its candidates are diagonal `0 + 2`, up `-2 - 2`, and left `-2 - 2`.
    The best score for those one-letter prefixes is therefore 2.

    Now consider the bottom-right cell `D[2][2]`, which aligns the complete
    prefixes `AC` and `AG`. Its diagonal neighbour is 2, and its upper and left
    neighbours are both 0. Predict the three candidate scores before opening
    the answer. Which final column does each candidate add?

    <details>
    <summary>Check the final cell</summary>

    Diagonal appends C/G: `2 - 1 = 1`. From above, append C/−:
    `0 - 2 = -2`. From the left, append −/G: `0 - 2 = -2`.
    The maximum is 1. This is the optimal global score for `AC` against `AG`.
    The boundary values `0, -2, -4` account for zero, one, or two letters
    aligned against an empty string.

    </details>

    Complete the boundary initialization and three-way recurrence in `nw_table`.
    Memory allocation, loops, and the letter-pair score are provided. The small
    table printed by the checks is your required table output.

    <details>
    <summary>Hint: separate initialization from the interior cells</summary>

    Use one loop for the first column and one for the first row, starting at 1.
    Inside the supplied nested loops, get the diagonal value and add `pair`;
    get the value above and add `GAP`; get the value to the left and add `GAP`.
    Store their `max` at the current cell. Remove both placeholder exceptions.
    The `AC` / `AG` table check helps locate a wrong boundary or index.

    </details>
    """)
    code(TABLE_SOLUTION if solution else TABLE_STARTER)
    code(TABLE_CHECKS)
    md("""### Supplied traceback — Recover one best alignment

    The bottom-right table cell is the optimal score. To recover aligned strings,
    start there and follow choices that explain the current score back to `[0][0]`.
    Reverse the collected characters at the end.

    The supplied function chooses **diagonal, then up, then left** when scores
    tie. Other tie rules may give different alignments with the same optimal
    score. For `AA` / `A`, both `AA` / `-A` and `AA` / `A-` score 0. A unique
    score does not imply a uniquely located gap.

    Run the supplied code without editing it. This small implementation uses
    O(mn) time and O(mn) memory; real searches need efficient candidate finding.
    """)
    code(TRACEBACK)

    md("""## Step 5 — Compare and interpret

    Run the supplied fragment comparisons. These are short **global** alignments
    of whole fragments. They do not map a short read to the full 18-base
    reference: that task needs substring/candidate search and appropriate
    alignment choices. A global comparison to the entire reference would also
    penalize its unmatched ends.

    To fit the **whole read** somewhere inside a longer reference, a fitting
    alignment leaves unused reference flanks unpenalized while consuming every
    read base. Local alignment may also omit read ends. Fitting is one form of
    semi-global alignment; which ends are free must be specified. The function
    you implement here remains global.

    <details>
    <summary>Self-check: alignment scope and search cost</summary>

    Before reading the answers, consider two questions from class:

    1. For reference `TTACGTAA` and read `ACGT`, which objective requires the
       complete read but leaves reference flanks free: global, local, or fitting?
    2. A hypothetical full DP comparison uses a 150-base read and a
       3,000,000,000-base reference. How many interior cells does it have?
       How many are needed for one 300-base candidate window?

    **Answers:** fitting requires the complete read and leaves the reference
    flanks free. Local selects the same region in this exact example but is
    allowed to omit read ends in other cases. The full comparison has
    `150 * 3_000_000_000 = 450_000_000_000` interior cells. One window has
    `150 * 300 = 45_000`. For `c` windows the count is `c * 45_000`, plus
    candidate discovery work. Boundary rows and columns are excluded. These
    are table-cell counts, not runtime measurements; candidate filtering may
    miss useful regions. Do not allocate either large table in this notebook.

    This self-check needs no additional function or submitted answer.

    </details>

    The labels substitution, insertion, and deletion describe differences from
    the reference fragment. They do not tell us how those differences arose.
    The scores use the chosen +2/−1/−2 rule; they are not probabilities or BLAST
    E-values. Statistical significance would require a model of chance matches
    and the size of the search space.

    **Write three sentences:** (1) state the exact locations and why the repeated
    read cannot be placed uniquely; (2) use at least two fragment scores to explain
    how mismatches/gaps affect a comparison; (3) state a biological conclusion the
    matches cannot establish and what extra evidence would be needed.
    """)
    code(COMPARISON)
    md("**Your interpretation:**\n\n1. …\n2. …\n3. …")
    md("""### Before you submit

    - Finish the TODOs in the three functions and run all core cells from the top.
      The supplied checks should complete without errors.
    - Keep your initial prediction, exact-match starts, score table, and fragment
      alignments visible in the saved notebook.
    - Replace all three interpretation placeholders with your own sentences.
    - Save and download the completed `.ipynb`. Complete after Week 2, before Week 3.
    """)

    md("""## Optional extension — Search the opposite DNA orientation

    DNA has complementary strands. To
    search the opposite orientation of a query, complement A↔T and C↔G and
    reverse the order. This is the **reverse complement**, not just a reversal.

    In a new code cell, implement `reverse_complement(sequence)` using a
    dictionary and `reversed(sequence)`. Reuse `validate_dna`.

    Try `TCATGG`. Print the exact matches of that string and of its reverse
    complement in `REFERENCE`, labelling the two orientations separately.
    Report start positions relative to the displayed forward reference.
    If a query equals its own reverse complement, the same coordinate may be
    reported in both orientation lists; do not treat it as two distinct loci.

    The core task searches only the forward orientation. A missing forward hit
    therefore cannot rule out a match on the opposite strand.
    """)
    if solution:
        code(OPTIONAL_SOLUTION)
        ns = reference
        rows = "\n".join(
            f"| {r['case']} | `{r['aligned_reference']}` | `{r['aligned_read']}` | {r['score']} |"
            for r in ns["alignment_results"])
        md("## Instructor answer key\n\n"
           "The repeated read `ATGCCA` has starts **0 and 12**; `CCATGA` has "
           "start **3**. The changed read `ATGCTA` has no exact match in the "
           "displayed forward reference. In `AAAAA`, `AAA` has starts 0, 1, and 2.\n\n"
           "The `AC` / `AG` score table is:\n\n"
           "```text\n       ∅   A   G\n   ∅   0  -2  -4\n   A  -2   2   0\n   C  -4   0   1\n```\n\n"
           "| Case | Aligned reference | Aligned read | Score |\n"
           "|---|---|---|---:|\n" + rows + "\n\n"
           "These particular strings and tie rule give the alignments above; "
           "other optimal gap placements can tie. `AA` / `A` reports `AA` / "
           "`-A` with score 0; `AA` / `A-` has the same score.\n\n"
           "Example interpretation: The repeated read fits starts 0 and 12, "
           "so exact sequence evidence alone does not choose a location; the "
           "other read fits start 3 in this tiny reference. Relative to the "
           "exact fragment's score 12, the substitution scores 9 and the deletion "
           "scores 8 under the stated penalties. These matches cannot show that "
           "a changed growth condition altered a gene's function: that would "
           "require appropriate biological measurements, replicated comparisons, "
           "and evidence linking a specific mechanism to the outcome.\n\n"
           "Optional result: `TCATGG` has no forward exact match; its reverse "
           "complement `CCATGA` matches start 3.\n\n"
           "Checkpoints: all occurrences are preserved, aligned strings are "
           "validated, global boundaries penalize unmatched prefixes, three "
           "previous states determine each interior cell, and interpretation "
           "separates matching evidence from biological conclusions.")
    md("""## Sources

    The alignment and search exercises draw on `bioinformatis-web` lectures
    02 and 19. The code and tasks were written for this course. The source
    course's Apache 2.0 license is stored beside the generator in
    `LICENSE.upstream.txt`.
    """)
    notebook = {"cells": cells, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
    references = [
        {"after": SEARCH_CHECKS, "source": SEARCH_SOLUTION, "title": "All exact matches"},
        {"after": SCORE_CHECKS, "source": SCORE_SOLUTION, "title": "Alignment scoring"},
        {"after": TABLE_CHECKS, "source": TABLE_SOLUTION, "title": "Global score table"},
    ]
    return prepare_notebook(notebook, 2, solution=solution, data_source=SETUP, references=references)


def main():
    namespace = reference_namespace()
    for solution, filename in ((False, "exercise.ipynb"), (True, "solutions.ipynb")):
        (HERE / filename).write_text(json.dumps(build(solution, namespace), indent=1) + "\n")
    (HERE / "expected_results.json").write_text(
        json.dumps(reference_results(namespace), indent=2) + "\n")
    print("Wrote Week 2 exercise.ipynb, solutions.ipynb, expected_results.json")


if __name__ == "__main__":
    main()
