"""Generate the standalone Homework 01 student and instructor notebooks.

Run: python3 practicals/week-01/build_notebook.py
Adapted teaching idea: bioinformatis-web/coding_exercises/lecture-01/
build_notebook.py (Apache-2.0; see LICENSE.upstream.txt). Rewritten on
2026-10-18: shorter dataset, explicit validation, sampled truth, separate
solutions, probability summaries, and an optional plotting dependency.
This repository's license applies to the new work; upstream attribution
and its Apache-2.0 license are retained.
"""

from pathlib import Path
import json
import inspect
import textwrap
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from notebook_helpers import prepare_notebook

HERE = Path(__file__).resolve().parent

SETUP = '''\
import math
import random
from statistics import mean

def make_dataset(seed=2026, n_reads=200, read_length=80):
    """A teaching simulation, not a model fitted to a sequencing instrument."""
    rng = random.Random(seed)
    lines, truth = [], {}
    for i in range(n_reads):
        name = f"synthetic_{i:03d}"
        true_bases, calls, qualities = [], [], []
        decline_start = 40 if i % 5 == 0 else 60
        for position in range(read_length):
            q = max(5, min(41, 31 - 2 * max(0, position - decline_start)
                            + rng.choice((-2, -1, 0, 1, 2))))
            # Include legitimate '@' and '+' quality symbols in the dataset.
            if i == 0 and position == 0:
                q = 31
            if i == 0 and position == 1:
                q = 10
            # A few internal low-quality calls survive end trimming.
            if i % 40 == 1 and position == 20:
                q = 12
            true_base = rng.choice("ACGT")
            called_base = true_base
            if rng.random() < 10 ** (-q / 10):
                called_base = rng.choice([b for b in "ACGT" if b != true_base])
            true_bases.append(true_base)
            calls.append(called_base)
            qualities.append(chr(q + 33))
        truth[name] = "".join(true_bases)
        lines.extend(("@" + name, "".join(calls), "+", "".join(qualities)))
    return "\\n".join(lines) + "\\n", truth

fastq_text, synthetic_truth = make_dataset()
print("Dataset generated locally: 200 synthetic reads, 80 bases each.")
print("No download or installation is needed.")
'''

PARSER_SOLUTION = '''\
def parse_fastq(text):
    """Parse this exercise's unwrapped, Phred+33, Q0..41 FASTQ subset."""
    lines = text.splitlines()  # handles LF and CRLF without stripping qualities
    if len(lines) % 4:
        raise ValueError("Truncated record: expected groups of four lines")
    records = []
    for start in range(0, len(lines), 4):
        header, sequence, separator, quality = lines[start:start + 4]
        if not header.startswith("@") or not header[1:].strip():
            raise ValueError("Expected @ and a nonempty read identifier")
        if not separator.startswith("+"):
            raise ValueError("Expected + separator")
        if separator[1:] and separator[1:] != header[1:]:
            raise ValueError("Repeated identifier does not match header")
        if not sequence or any(base not in "ACGTN" for base in sequence):
            raise ValueError("Expected a nonempty uppercase DNA sequence")
        if len(sequence) != len(quality):
            raise ValueError("Sequence and quality lengths differ")
        if any(not 0 <= ord(symbol) - 33 <= 41 for symbol in quality):
            raise ValueError("Quality outside this exercise's Q0..41 range")
        records.append((header[1:], sequence, quality))
    return records
'''

PARSER_STARTER = '''\
def parse_fastq(text):
    """Return a list of (identifier, sequence, quality_string) tuples."""
    lines = text.splitlines()
    if len(lines) % 4:
        raise ValueError("Truncated record: expected groups of four lines")
    records = []
    for start in range(0, len(lines), 4):
        header, sequence, separator, quality = lines[start:start + 4]
        if not header.startswith("@") or not header[1:].strip():
            raise ValueError("Expected @ and a nonempty read identifier")
        if not separator.startswith("+"):
            raise ValueError("Expected + separator")
        if separator[1:] and separator[1:] != header[1:]:
            raise ValueError("Repeated identifier does not match header")
        if not sequence or any(base not in "ACGTN" for base in sequence):
            raise ValueError("Expected a nonempty uppercase DNA sequence")
        # TODO 1: reject unequal sequence / quality lengths with ValueError.
        # TODO 2: reject any quality outside Q0..41 (use ord(symbol) - 33).
        # TODO 3: append (header[1:], sequence, quality) to records.
        raise NotImplementedError("Complete the three parser tasks")
    return records
'''

PARSER_CHECKS = '''\
records = parse_fastq(fastq_text)
assert len(records) == 200
assert all(len(sequence) == 80 for _, sequence, _ in records)
# Neither @ nor + starts a new record when it occupies the quality line.
tiny = "@toy\\nAC\\n+\\n@+\\n"
assert parse_fastq(tiny) == [("toy", "AC", "@+")]
assert parse_fastq(tiny.replace("\\n", "\\r\\n")) == parse_fastq(tiny)
assert parse_fastq("@toy\\nAC\\n+toy\\n@+") == parse_fastq(tiny)
assert parse_fastq("") == []
bad_examples = {
    "truncated": "@toy\\nAC\\n+\\n",
    "wrong header": "toy\\nAC\\n+\\n@+\\n",
    "wrong separator": "@toy\\nAC\\n-\\n@+\\n",
    "unequal lengths": "@toy\\nAC\\n+\\n@\\n",
    "quality below chosen range": "@toy\\nAC\\n+\\n @\\n",
    "quality above chosen range": "@toy\\nAC\\n+\\nK@\\n",
    "mismatched repeated identifier": "@toy\\nAC\\n+other\\n@+\\n",
    "empty sequence": "@toy\\n\\n+\\n\\n",
    "blank header": "@\\nAC\\n+\\n@+\\n",
    "invalid base": "@toy\\nAX\\n+\\n@+\\n",
}
for reason, malformed in bad_examples.items():
    try:
        parse_fastq(malformed)
    except ValueError:
        pass
    else:
        raise AssertionError("Parser accepted " + reason)
print("Parsed", len(records), "reads; format checks passed.")
'''

QUALITY_SOLUTION = '''\
def phred_scores(quality):
    return [ord(symbol) - 33 for symbol in quality]

def expected_errors(quality):
    return sum(10 ** (-q / 10) for q in phred_scores(quality))
'''

QUALITY_STARTER = '''\
def phred_scores(quality):
    # TODO: return one integer Q = ord(symbol) - 33 per quality symbol.
    raise NotImplementedError("Decode Phred scores")

def expected_errors(quality):
    # TODO: convert each Q to p = 10 ** (-Q / 10), then sum p.
    raise NotImplementedError("Sum estimated error probabilities")
'''

QUALITY_CHECKS = '''\
assert phred_scores("!+5?J") == [0, 10, 20, 30, 41]
assert math.isclose(expected_errors("5?"), 0.011)
q_pair = [10, 30]
mean_q = mean(q_pair)
mean_probability = mean(10 ** (-q / 10) for q in q_pair)
print("Q10 + Q30: mean Q =", mean_q)
print("Average estimated error probability =", mean_probability)
print("Probability obtained from the average Q =", 10 ** (-mean_q / 10))
print("Expected errors, first read =", round(expected_errors(records[0][2]), 4))
'''

TOY_REVIEW = '''\
# Revisit the class prediction using the functions you just completed.
# These illustrative reads are independent of the fictional tubes.
toy_reads = [("Read 1", "ACGTACGT", "IIIIIIII"),
             ("Read 2", "ACGTACGT", "IIII55++")]
for name, sequence, quality in toy_reads:
    print(name, "sequence:", sequence, "Q scores:", phred_scores(quality),
          "expected errors:", round(expected_errors(quality), 4))
'''

POSITION_SOLUTION = '''\
def positional_mean_errors(records):
    width = max((len(quality) for _, _, quality in records), default=0)
    result = []
    for position in range(width):
        probabilities = [10 ** (-phred_scores(quality)[position] / 10)
                         for _, _, quality in records if len(quality) > position]
        result.append(mean(probabilities))
    return result
'''

POSITION_STARTER = '''\
def positional_mean_errors(records):
    width = max((len(quality) for _, _, quality in records), default=0)
    result = []
    for position in range(width):
        # Only include reads that contain this position (also works after trimming).
        scores = [phred_scores(quality)[position]
                  for _, _, quality in records if len(quality) > position]
        # TODO: append the mean of 10 ** (-q / 10) for q in scores.
        raise NotImplementedError("Average probabilities at each position")
    return result
'''

POSITION_CHECKS = '''\
profile = positional_mean_errors(records)
assert len(profile) == 80
assert math.isclose(positional_mean_errors([("a", "A", "+"),
                                          ("b", "AC", "?5")])[0], 0.0505)
print("Read position -> average estimated error probability")
for position in (0, 19, 39, 49, 59, 69, 79):
    print(f"{position + 1:2d} -> {profile[position]:.5f}")

# Optional visual: all calculations and the printed table work without matplotlib.
def plot_profile(profile):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib unavailable: use the printed position table.")
        return
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(range(1, len(profile) + 1), profile)
    ax.axhline(0.01, color="darkorange", linestyle="--", label="Q20: p = 0.01")
    ax.set(xlabel="Position within read (1-based)", xlim=(1, len(profile)),
           ylabel="Mean estimated error probability", ylim=(0, 0.35))
    ax.legend()
    fig.tight_layout()
    plt.show()

plot_profile(profile)
'''

TRIM_SOLUTION = '''\
def trim_record(record, threshold=20, min_length=50):
    name, sequence, quality = record
    end = len(quality)
    while end > 0 and ord(quality[end - 1]) - 33 < threshold:
        end -= 1
    if end < min_length:
        return None
    return name, sequence[:end], quality[:end]
'''

TRIM_STARTER = '''\
def trim_record(record, threshold=20, min_length=50):
    name, sequence, quality = record
    end = len(quality)
    # TODO: move end left while the final remaining Q is below threshold.
    # Stop at the first Q >= threshold, even if lower scores remain internally.
    # TODO: return None if end < min_length; otherwise return
    # (name, sequence[:end], quality[:end]). Preserve bases exactly.
    raise NotImplementedError("Trim a trailing low-quality suffix")
'''

TRIM_CHECKS = '''\
assert trim_record(("toy", "ACGT", "5?+!"), min_length=2) == ("toy", "AC", "5?")
assert trim_record(("toy", "ACGT", "5?+!"), min_length=3) is None
assert trim_record(("toy", "AC", "!!"), min_length=1) is None
assert trim_record(("toy", "ACG", "?+?"), min_length=1) == ("toy", "ACG", "?+?")
assert trim_record(("toy", "AC", "55"), min_length=2) == ("toy", "AC", "55")

retained = []
for record in records:
    result = trim_record(record)
    if result is not None:
        retained.append(result)

def summarize(records):
    bases = sum(len(sequence) for _, sequence, _ in records)
    expected = sum(expected_errors(quality) for _, _, quality in records)
    return {"reads": len(records), "bases": bases, "expected_errors": expected,
            "expected_errors_per_1000_bases": 1000 * expected / bases if bases else 0}

before, after = summarize(records), summarize(retained)
for label, summary in (("Before", before), ("After", after)):
    print(label, {key: round(value, 4) if isinstance(value, float) else value
                  for key, value in summary.items()})
print(f"Retained bases: {100 * after['bases'] / before['bases']:.2f}%")
print(f"Expected-error reduction: {100 * (1 - after['expected_errors'] / before['expected_errors']):.2f}%")

# Synthetic truth exists only because WE generated these data.
def observed_errors(records):
    return sum(sum(call != true for call, true in zip(sequence, synthetic_truth[name]))
               for name, sequence, _ in records)

print("Simulated observed mismatches, before / after:",
      observed_errors(records), "/", observed_errors(retained))
'''

TRIM_EXPERIMENT = '''\
# Optional comparison: pass the experimental threshold as an argument.
for threshold in (10, 20):
    experiment_retained = []
    for record in records:
        result = trim_record(record, threshold=threshold, min_length=50)
        if result is not None:
            experiment_retained.append(result)
    experiment_summary = summarize(experiment_retained)
    print(f"Q{threshold}:",
          {key: round(value, 4) if isinstance(value, float) else value
           for key, value in experiment_summary.items()})
'''


def cell(kind, source, index):
    result = {"cell_type": kind, "id": f"week01-{index:02d}", "metadata": {},
              "source": (inspect.cleandoc(source) if kind == "markdown"
                         else textwrap.dedent(source).strip()) + "\n"}
    if kind == "code":
        result.update(execution_count=None, outputs=[])
    return result


def reference_namespace():
    namespace = {}
    # Execute definitions and reference calculations to keep the answer key in sync.
    for source in (SETUP, PARSER_SOLUTION, PARSER_CHECKS, QUALITY_SOLUTION,
                   QUALITY_CHECKS, POSITION_SOLUTION, TRIM_SOLUTION, TRIM_CHECKS):
        exec(source, namespace)
    return namespace


def build(solution=False, reference=None):
    cells = []

    def md(source):
        cells.append(cell("markdown", source, len(cells)))

    def code(source):
        cells.append(cell("code", source, len(cells)))

    md("""# Homework 01 — Reading life as data

    Complete after Week 1, before Week 2

    The two class reads have identical DNA letters but different quality scores.
    Which read is more reliable? Calculate their estimated errors, then examine
    200 simulated reads to see whether trimming uncertain ends is worth the lost sequence.

    The reads are invented examples, separate from the class case about cell
    cultures. They contain no measurements of the cultures' growth or response
    to the changed condition.

    Basic Python loops, lists, slicing, and functions are enough.
    The extension is optional.

    **Submit:** this notebook with your initial prediction, the positional quality
    plot or printed table, the trimming comparison, and the three interpretation
    sentences requested in Step 5.

    Follow the Colab setup instructions below. You can also use local Jupyter
    with Python 3.9 or later. The notebook creates its own data.

    <details>
    <summary>Reading an error message</summary>

    `NotImplementedError` marks an unfinished exercise. `NameError` often means
    you skipped a cell or restarted the runtime; rerun setup and the preceding
    cells. For an `AssertionError`, compare the check's input and expected result
    with your function's output. An `IndentationError` points to the spacing at
    the start of a code line. After changing a function, run its definition again
    before running the checks. Each task has a hint and an optional reference solution.

    </details>

    The parser accepts four-line, unwrapped Phred+33/Sanger FASTQ records with
    uppercase A/C/G/T/N and qualities Q0–41. Other FASTQ variants and higher
    quality values need different validation. A FASTA record has a `>` header
    and sequence, with no per-base quality string.
    """)
    if solution:
        md("**Instructor reference edition.** All functions are completed. Run all cells to reproduce the answer key. Distribute `exercise.ipynb` to students.")
    md("""## Before you code — Continue the class prediction

    Both reads report `ACGTACGT`. Compare their quality strings below.

    | Illustrative read | Measured DNA letters | Quality string | Estimated quality at the eight positions |
    |---|---|---|---|
    | Read 1 | `ACGTACGT` | `IIIIIIII` | Q40 × 8 |
    | Read 2 | `ACGTACGT` | `IIII55++` | Q40 × 4, Q20 × 2, Q10 × 2 |

    Before running Step 1, predict which read has fewer estimated errors.
    Explain how its quality string supports your prediction. Step 3 will convert
    the quality scores to probabilities.

    Double-click the text below to record your prediction. Keep it so you can
    compare your reasoning with the calculation later.

    **My prediction and reason:** …

    Read 1 and Read 2 are labels for these examples; neither belongs to tube A or B.
    """)
    md("""## Step 1 — Inspect one measurement

    Run the supplied simulation and preview. Each record has an `@` identifier,
    a sequence, a `+` separator (optionally repeating the identifier), and one
    quality character per base. Read position is order within one read, not a
    chromosome coordinate.

    | Line | Read 1 example | What it represents |
    |---|---|---|
    | 1 | `@Read1` | Read identifier |
    | 2 | `ACGTACGT` | Eight measured DNA letters |
    | 3 | `+` | Separator |
    | 4 | `IIIIIIII` | Eight encoded confidence estimates, one per letter |

    Read 2's quality string `IIII55++` contains `+` as a quality character.
    Its **line position** distinguishes it from the separator above it.

    The simulation creates 200 reads of 80 bases. It chooses true bases
    independently, assigns qualities that decline toward the ends, and changes
    some calls according to their error probabilities. This built-in decline
    lets you test the trimming calculation; it was not measured on an instrument.

    **Think it through:** Which string is the measurement? Which string expresses the
    uncertainty? Why must their lengths agree? Is the first character `@` always
    a new header? Inspect its position before deciding.
    """)
    code(SETUP)
    code('print("\\n".join(fastq_text.splitlines()[:4]))\nprint("Sequence length:", len(fastq_text.splitlines()[1]))')
    md("""## Step 2 — Parse and reject malformed records

    Complete the three marked parser tasks. The supplied code already checks
    headers, separators, repeated identifiers, and the chosen DNA alphabet.
    Raise `ValueError` when lengths differ or a quality is outside Q0..41;
    append a `(name, sequence, quality)` tuple for each valid record.

    Use `splitlines()` to handle LF and CRLF. Do not strip individual quality
    lines or search for every `@` / `+`: those characters are valid qualities.
    A final newline is optional; an empty input has no records. Run the checks,
    then explain to yourself why one malformed example is rejected.

    <details>
    <summary>Hint: break the three TODOs into separate actions</summary>

    First compare the two string lengths with `len`. Next inspect every quality
    character: `ord` turns a character into its character-code number. Check
    the inclusive allowed range after subtracting 33. Finally add one tuple to
    the `records` list using its `append` method. These actions belong inside
    the four-line-record loop. Remove the placeholder exception after implementing them.

    </details>
    """)
    code(PARSER_SOLUTION if solution else PARSER_STARTER)
    code(PARSER_CHECKS)
    md("""## Step 3 — Decode confidence as probability

    For modern Phred+33, `Q = ord(character) - 33` and
    `p = 10 ** (-Q / 10)`. Thus Q10 estimates p=0.1; Q20 estimates p=0.01;
    Q30 estimates p=0.001. These are estimates supplied by a base caller.

    Complete `phred_scores` and `expected_errors`. Sum the per-base p values
    to obtain the **expected number of incorrect calls**, not an observed count.
    Linearity of expectation makes this sum valid without assuming independent
    errors. Its usefulness for real reads depends on quality calibration.

    **Think it through:** Why do Q10 and Q30 have mean probability 0.0505 while converting
    their mean Q20 gives 0.01? Compute probabilities before averaging them.

    <details>
    <summary>Hint: separate decoding from summarizing</summary>

    `phred_scores` returns a list with one integer for each character. Try a
    one-character input first. `expected_errors` uses that list, converts each
    score into a probability, and combines the probabilities with `sum`.
    Python uses `**` for exponentiation. A result such as 0.3 is allowed: it is
    an expected count, not a claim that a fraction of one actual base was wrong.

    </details>
    """)
    code(QUALITY_SOLUTION if solution else QUALITY_STARTER)
    code(QUALITY_CHECKS)
    md("""### Revisit your prediction

    Run the comparison below. Do the estimated error counts support your
    prediction? Both reads still report `ACGTACGT`. Their quality scores estimate
    how many calls may be wrong, but we have no true sequence for these two
    examples with which to identify the errors.
    """)
    code(TOY_REVIEW)
    md("""## Step 4 — Find where uncertainty increases

    Complete one line in `positional_mean_errors`: average estimated error
    probabilities over reads containing each position. Run the table and optional
    plot. The horizontal reference is p=0.01, corresponding to Q20.

    **Think it through:** At which positions does uncertainty rise? Why would a single
    average per read hide this pattern? Explain what this simulation can show
    about the calculation and what it cannot establish about a real sequencer.

    <details>
    <summary>Hint: the supplied loop already selects the right scores</summary>

    Each pass through the loop gives you `scores` for one read position. Convert
    those scores to probabilities before using `mean`, then append that one
    average to `result`. The first Python index is 0, while the plot labels the
    first position as 1. The printed table is a valid result if no plot appears.

    </details>
    """)
    code(POSITION_SOLUTION if solution else POSITION_STARTER)
    code(POSITION_CHECKS)
    md("""## Step 5 — Evaluate end trimming

    Complete `trim_record`. Starting at the right end, remove consecutive bases
    whose Q is **below 20**, stopping at the first Q ≥20. Apply identical slices
    to sequence and quality. Discard the read if fewer than **50 bases** remain.
    An internal low-quality base stays when a higher-quality suffix follows it.
    This simple policy is a teaching example; it does not remove adapters or
    guarantee that retained reads will align correctly.

    Run the checks and comparison. Compare retained bases, total expected errors,
    and expected errors per 1,000 retained bases. A lower total alone could simply
    mean you deleted more data. The last cell also compares with known synthetic
    truth; in normal FASTQ files that truth is unavailable.

    **Write three sentences:** (1) quantify the bases retained and estimated error
    reduction; (2) recommend whether to use this policy for this simulation and
    state one cost; (3) state one reason you need more evidence before applying
    it to a real biological analysis.

    <details>
    <summary>Hint: work backwards without changing the original strings</summary>

    `end` is the exclusive slice boundary, so the final retained character is
    at index `end - 1`. Check that `end` is positive before using that index.
    Decrease the boundary only while that character is below the threshold.
    After the loop, compare the retained length with `min_length`. Both strings
    must use the same slice boundary. The tiny test with an internal low-quality
    character checks that you are removing a suffix rather than every low score.

    </details>
    """)
    code(TRIM_SOLUTION if solution else TRIM_STARTER)
    code(TRIM_CHECKS)
    md("**Your interpretation:**\n\n1. …\n2. …\n3. …")
    md("""### Before you submit

    - Run all five core steps from the top after completing the TODOs. Their
      supplied checks should finish without errors. Keep your initial prediction
      and compare it with the toy-read quality evidence in Step 3.
    - Keep the positional QC plot **or printed table** and the before/after
      summary in the saved notebook.
    - Replace the three placeholders above with your own sentences, including
      numerical evidence, a tradeoff, and a limit of the simulation.
    - Save and download your completed `.ipynb` file. Complete this homework
      after Week 1, before Week 2.
    """)
    md("""### Optional extension — Compare Q10 and Q20

    **Additional time, optional:** run the supplied comparison cell. It calls
    `trim_record(record, threshold=threshold, min_length=50)` in a separate loop
    for each threshold. Keep `trim_record`'s default `threshold=20`: the core
    checkpoint assertions and answer key use that default. The experiment uses
    separate variables, so the original `retained`, `before`, and `after` results
    still describe the Q20 checkpoint.

    Which threshold retains more bases? Compare expected errors per 1,000 bases
    as well as total expected errors, and explain the tradeoff.
    """)
    code(TRIM_EXPERIMENT)
    if solution:
        ns = reference
        before, after = ns["before"], ns["after"]
        md(f"""## Instructor answer key and discussion

        Format: 200 reads × 80 bases = 16,000 bases. The '@+' quality pair
        decodes to Q31 and Q10. Q10/Q30 average p is 0.0505, not 0.01.

        The class toy comparison gives Read 1 (`ACGTACGT`, `IIIIIIII`)
        0.0008 expected errors and Read 2 (`ACGTACGT`, `IIII55++`) 0.2204.
        Their identical sequence strings carry different confidence evidence.
        Neither is assigned to tube A or tube B, and no treatment effect follows
        from this comparison. The slower growth in tube B is a fictional teaching
        premise, not a result of this analysis.

        | Measure | Before | After Q20 end trimming, minimum 50 |
        |---|---:|---:|
        | Reads | {before['reads']} | {after['reads']} |
        | Bases | {before['bases']} | {after['bases']} |
        | Expected errors | {before['expected_errors']:.6f} | {after['expected_errors']:.6f} |
        | Expected errors / 1,000 bases | {before['expected_errors_per_1000_bases']:.6f} | {after['expected_errors_per_1000_bases']:.6f} |
        | Simulated observed mismatches | {ns['observed_errors'](ns['records'])} | {ns['observed_errors'](ns['retained'])} |

        Example interpretation: The policy retains {100 * after['bases'] / before['bases']:.2f}%
        of bases and reduces expected errors by
        {100 * (1 - after['expected_errors'] / before['expected_errors']):.2f}%.
        It is useful for removing the deliberately poor tails in this simulation,
        at the cost of fewer and shorter reads, including the loss of whole reads.
        A real analysis needs evidence about adapter contamination, quality
        calibration, and how read loss changes mapping or biological conclusions.

        The earlier decline affects every fifth read; the plot combines two
        simulated groups. Retained reads can still contain internal Q<20 calls.
        Expected errors and observed mismatches differ because one is an estimate
        and one is a sampled outcome. Agreement in this simulation is partly
        built in by its construction and cannot validate a real base caller.

        Checkpoints: a student can identify all four lines, rejects malformed
        records, converts Q to p before summarizing, labels plot axes correctly,
        slices quality and sequence together, and states a tradeoff. If time is
        short, supply the parser checkpoint and prioritize probability interpretation
        and the final recommendation. For homework support, use a student's
        failed check and the relevant hint to locate the difficulty; the reference
        notebook is the separate instructor answer key.
        """)
    md("""## Source

    Adapted from `bioinformatis-web/coding_exercises/lecture-01/build_notebook.py`
    under the Apache License 2.0. The exercises and simulation were rewritten
    for this course. The upstream license is stored beside the generator in
    `LICENSE.upstream.txt`: https://www.apache.org/licenses/LICENSE-2.0
    """)
    notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3",
            "language": "python", "name": "python3"}, "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}
    references = [
        {"after": PARSER_CHECKS, "source": PARSER_SOLUTION, "title": "FASTQ parser"},
        {"after": QUALITY_CHECKS, "source": QUALITY_SOLUTION, "title": "Phred probabilities"},
        {"after": POSITION_CHECKS, "source": POSITION_SOLUTION, "title": "Positional quality"},
        {"after": TRIM_CHECKS, "source": TRIM_SOLUTION, "title": "End trimming"},
    ]
    return prepare_notebook(notebook, 1, solution=solution, data_source=SETUP, references=references)


def main():
    reference = reference_namespace()
    for solution, name in ((False, "exercise.ipynb"), (True, "solutions.ipynb")):
        (HERE / name).write_text(json.dumps(build(solution, reference), indent=1) + "\n")
    (HERE / "synthetic_reads.fastq").write_text(reference["fastq_text"])
    print("Wrote exercise.ipynb, solutions.ipynb, synthetic_reads.fastq")


if __name__ == "__main__":
    main()
