"""Generate standalone Week 3 assembly homework and a separate reference edition.

Run: python3 practicals/week-03/build_notebook.py
Standard library only. Teaching ideas adapted from bioinformatis-web lecture 03;
see README.md and the retained Apache-2.0 license. Notebook structure continues
Week 2. All DNA and contig lengths are synthetic teaching examples.
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
# Everything is supplied locally; no downloads, installs, or extra files.
TOY_SEQUENCE = "ATGACCT"
READS = ["ATGAC", "GACCT"]
K = 3
PROVIDED_PATH = ["AT", "TG", "GA", "AC", "CC", "CT"]

def validate_dna(sequence):
    if not isinstance(sequence, str):
        raise TypeError("A DNA sequence must be a string")
    if any(base not in "ACGT" for base in sequence):
        raise ValueError("This exercise accepts uppercase A/C/G/T only")

def checked_reads(reads, k):
    if type(k) is not int or k < 1:
        raise ValueError("k must be a positive integer")
    if isinstance(reads, (str, bytes)):
        raise TypeError("Pass a collection of reads, not one concatenated string")
    result = list(reads)
    for read in result:
        validate_dna(read)
    return result

def checked_kmer_counts(counts):
    if not counts:
        return None
    widths = set()
    for kmer, support in counts.items():
        validate_dna(kmer)
        widths.add(len(kmer))
        if type(support) is not int or support < 1:
            raise ValueError("Observed counts must be positive integers")
    if len(widths) != 1 or min(widths) < 2:
        raise ValueError("Graph k-mers must all have the same length, at least 2")
    return widths.pop()

def checked_path(path):
    if isinstance(path, (str, bytes)):
        raise TypeError("Pass node labels as a list, not one string")
    nodes = list(path)
    for node in nodes:
        validate_dna(node)
    if nodes and (not nodes[0] or any(len(node) != len(nodes[0]) for node in nodes)):
        raise ValueError("Path nodes must be nonempty strings of equal length")
    for left, right in zip(nodes, nodes[1:]):
        if left[1:] != right[:-1]:
            raise ValueError("Adjacent node labels do not overlap correctly")
    return nodes

def checked_lengths(lengths):
    if isinstance(lengths, (str, bytes)):
        raise TypeError("Pass contig lengths as a collection of integers")
    values = list(lengths)
    if any(type(length) is not int or length <= 0 for length in values):
        raise ValueError("Contig lengths must be positive integers")
    return values

print("Invented sequence for the first example:", TOY_SEQUENCE)
print("Separately sampled overlapping reads:", READS)
print("k =", K, "; graph nodes have length", K - 1)
print("Provided ordered node path:", " -> ".join(PROVIDED_PATH))
'''

COUNTS_SOLUTION = '''\
def kmer_counts(reads, k):
    """Count length-k windows independently within each read."""
    reads = checked_reads(reads, k)
    counts = {}
    for read in reads:
        for start in range(len(read) - k + 1):
            kmer = read[start:start + k]
            counts[kmer] = counts.get(kmer, 0) + 1
    return counts
'''

COUNTS_STARTER = '''\
def kmer_counts(reads, k):
    """Count length-k windows independently within each read."""
    reads = checked_reads(reads, k)
    counts = {}
    # TODO: loop over reads, then every valid start within that read.
    # Increment the dictionary count of read[start:start + k].
    # Include the final valid start and overlapping windows.
    raise NotImplementedError("Count windows without joining the reads")
    return counts
'''

COUNTS_CHECKS = '''\
assert kmer_counts([TOY_SEQUENCE], 3) == {"ATG": 1, "TGA": 1, "GAC": 1, "ACC": 1, "CCT": 1}
assert kmer_counts(READS, 3) == {"ATG": 1, "TGA": 1, "GAC": 2, "ACC": 1, "CCT": 1}
assert kmer_counts(["AAAAA"], 3) == {"AAA": 3}
assert kmer_counts(["AT", "GAC"], 3) == {"GAC": 1}  # no ATG/TGA crossing a read boundary
assert kmer_counts(["AC"], 3) == {}
assert kmer_counts([], 3) == {}
assert kmer_counts([""], 3) == {}
assert kmer_counts(["AC"], 1) == {"A": 1, "C": 1}
for bad_reads, bad_k in ((["AC"], 0), (["AC"], 1.5), (["ac"], 2), (["AN"], 2)):
    try:
        kmer_counts(bad_reads, bad_k)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected invalid k or unsupported DNA to be rejected")

observed_counts = kmer_counts(READS, K)
for kmer, count in observed_counts.items():
    print(kmer, "observed", count, "time(s)")
print("Per-read boundary and counting checks passed.")
'''

GRAPH_SOLUTION = '''\
def build_kmer_graph(counts):
    """One directed edge per distinct k-mer, weighted by observed support."""
    checked_kmer_counts(counts)
    nodes, edges = set(), []
    for kmer in sorted(counts):
        source, target = kmer[:-1], kmer[1:]
        nodes.update((source, target))
        edges.append({"kmer": kmer, "source": source,
                      "target": target, "support": counts[kmer]})
    return {"nodes": sorted(nodes), "edges": edges}
'''

GRAPH_STARTER = '''\
def build_kmer_graph(counts):
    """One directed edge per distinct k-mer, weighted by observed support."""
    checked_kmer_counts(counts)
    nodes, edges = set(), []
    for kmer in sorted(counts):
        # TODO: source is the prefix without the last letter;
        # target is the suffix without the first letter.
        # Add both node labels to nodes with nodes.update((source, target)).
        # Append {"kmer": kmer, "source": source, "target": target,
        #         "support": counts[kmer]} to edges.
        raise NotImplementedError("Connect each k-mer's prefix to its suffix")
    return {"nodes": sorted(nodes), "edges": edges}
'''

GRAPH_CHECKS = '''\
graph = build_kmer_graph(observed_counts)
assert graph["nodes"] == ["AC", "AT", "CC", "CT", "GA", "TG"]
assert len(graph["edges"]) == 5
assert next(edge for edge in graph["edges"] if edge["kmer"] == "GAC") == {
    "kmer": "GAC", "source": "GA", "target": "AC", "support": 2}
assert build_kmer_graph({}) == {"nodes": [], "edges": []}
assert build_kmer_graph({"AAA": 3}) == {
    "nodes": ["AA"], "edges": [{"kmer": "AAA", "source": "AA", "target": "AA", "support": 3}]}
for malformed in ({"A": 1}, {"AT": 1, "TGA": 1}, {"ATG": 0}, {"ATN": 1}):
    try:
        build_kmer_graph(malformed)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected invalid graph counts to be rejected")

def show_graph(graph):
    print("source -> target | k-mer | observed support")
    for edge in graph["edges"]:
        print(f"{edge['source']:>3} -> {edge['target']:<3} | {edge['kmer']} | {edge['support']}")

show_graph(graph)
print("Graph checks passed; edges above are alphabetically listed, not an assembly order.")
'''

PATH_SOLUTION = '''\
def spell_path(path):
    """Spell a supplied overlapping node path; do not search for a path."""
    nodes = checked_path(path)
    if not nodes:
        return ""
    sequence = nodes[0]
    for node in nodes[1:]:
        sequence += node[-1]
    return sequence
'''

PATH_STARTER = '''\
def spell_path(path):
    """Spell a supplied overlapping node path; do not search for a path."""
    nodes = checked_path(path)
    if not nodes:
        return ""
    # TODO: begin with the complete first node, then append only the
    # final letter of each remaining node. Overlaps must not be repeated.
    raise NotImplementedError("Spell the supplied path")
'''

PATH_CHECKS = '''\
assert spell_path(PROVIDED_PATH) == "ATGACCT"
assert spell_path(["AT"]) == "AT"
assert spell_path([]) == ""
assert spell_path(["AA", "AA", "AA"]) == "AAAA"
for bad_path in (["AT", "CC"], ["AT", "T"], [""], ["AN"]):
    try:
        spell_path(bad_path)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected malformed node path to be rejected")

# Supplied verification: each ordered pair in this example is an observed edge.
observed_pairs = {(edge["source"], edge["target"]) for edge in graph["edges"]}
assert all(pair in observed_pairs for pair in zip(PROVIDED_PATH, PROVIDED_PATH[1:]))
spelled = spell_path(PROVIDED_PATH)
print(" -> ".join(PROVIDED_PATH), "spells", spelled)
print("Path-spelling checks passed.")
'''

OBSERVATIONS = '''\
# Supplied: compare evidence patterns; no traversal algorithm is required.
repeat_sequences = ["ATGATCAT", "ATCATGAT"]
repeat_paths = [["AT", "TG", "GA", "AT", "TC", "CA", "AT"],
                ["AT", "TC", "CA", "AT", "TG", "GA", "AT"]]
repeat_counts = [kmer_counts([sequence], 3) for sequence in repeat_sequences]
assert repeat_counts[0] == repeat_counts[1]
assert all(count == 1 for count in repeat_counts[0].values())
repeat_graph = build_kmer_graph(repeat_counts[0])
assert [spell_path(path) for path in repeat_paths] == repeat_sequences
repeat_four = [kmer_counts([sequence], 4) for sequence in repeat_sequences]
assert "GATC" in repeat_four[0] and "GATC" not in repeat_four[1]
print("Two supplied walks spell:", [spell_path(path) for path in repeat_paths])
print("Their 3-mer counts agree:", repeat_counts[0] == repeat_counts[1])
print("GATC occurs only in the first invented sequence; 4-mer tables differ.")

disconnected_reads = ["ATGA", "CCGT"]
disconnected_graph = build_kmer_graph(kmer_counts(disconnected_reads, 3))
print("Disconnected observations:")
show_graph(disconnected_graph)

changed_reads = READS + ["GATCT"]
changed_counts = kmer_counts(changed_reads, 3)
changed_graph = build_kmer_graph(changed_counts)
added_kmers = sorted(set(changed_counts) - set(observed_counts))
assert added_kmers == ["ATC", "GAT", "TCT"]
print("Adding synthetic read GATCT introduces these k-mer types:", added_kmers)
print("Their support:", {kmer: changed_counts[kmer] for kmer in added_kmers})
print("This observation alone does not identify an error or a real difference.")
'''

N50_SOLUTION = '''\
def n50(lengths):
    """Length of the contig that reaches at least half the total assembled bases."""
    values = checked_lengths(lengths)
    if not values:
        return 0  # Explicit empty-assembly convention for this notebook.
    total, cumulative = sum(values), 0
    for length in sorted(values, reverse=True):
        cumulative += length
        if 2 * cumulative >= total:
            return length
'''

N50_STARTER = '''\
def n50(lengths):
    """Length of the contig that reaches at least half the total assembled bases."""
    values = checked_lengths(lengths)
    if not values:
        return 0  # Explicit empty-assembly convention for this notebook.
    # TODO: sort largest first, add lengths cumulatively, and return the
    # current length at the first point where at least half the bases are covered.
    # Compare 2 * cumulative with total to avoid rounding the halfway point.
    raise NotImplementedError("Find the length at the halfway point in bases")
'''

N50_CHECKS = '''\
assert n50([8, 7, 5]) == 7
assert n50([12, 8]) == 12
assert n50([5, 8, 7]) == 7  # input ordering must not matter
assert n50([10, 10]) == 10  # reaching exactly half is sufficient
assert n50([5, 5, 5]) == 5
assert n50([9]) == 9
assert n50([]) == 0
for invalid_lengths in ([0], [-1, 8], [3.5], [True]):
    try:
        n50(invalid_lengths)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected invalid contig lengths to be rejected")

# Supplied: L50 counts how many longest contigs are needed to reach halfway.
def assembly_summary(lengths):
    values = checked_lengths(lengths)
    total = sum(values)
    l50, cumulative = 0, 0
    for length in sorted(values, reverse=True):
        l50 += 1
        cumulative += length
        if 2 * cumulative >= total:
            break
    return {"contigs": len(values), "total": total, "N50": n50(values), "L50": l50}

length_examples = [[8, 7, 5], [12, 8]]
length_results = [assembly_summary(lengths) for lengths in length_examples]
assert length_results == [{"contigs": 3, "total": 20, "N50": 7, "L50": 2},
                          {"contigs": 2, "total": 20, "N50": 12, "L50": 1}]
for lengths, summary in zip(length_examples, length_results):
    print(lengths, "->", summary)
print("Length statistics describe continuity; correctness is still unknown.")
'''

OPTIONAL = '''\
# Optional support cutoff: run only if you want the additional comparison.
supported_twice = {kmer: count for kmer, count in observed_counts.items() if count >= 2}
filtered_graph = build_kmer_graph(supported_twice)
print("Observed at least twice:", supported_twice)
show_graph(filtered_graph)
print("Dropped types:", sorted(set(observed_counts) - set(supported_twice)))
print("In our known toy sequence, every dropped type was a genuine substring.")
'''


def reference_namespace():
    namespace = {}
    with contextlib.redirect_stdout(io.StringIO()):
        for source in (SETUP, COUNTS_SOLUTION, COUNTS_CHECKS, GRAPH_SOLUTION,
                       GRAPH_CHECKS, PATH_SOLUTION, PATH_CHECKS, OBSERVATIONS,
                       N50_SOLUTION, N50_CHECKS, OPTIONAL):
            exec(source, namespace)
    return namespace


def reference_results(namespace):
    return {
        "toy_sequence": namespace["TOY_SEQUENCE"], "k": namespace["K"],
        "reads": namespace["READS"], "observed_counts": namespace["observed_counts"],
        "graph": namespace["graph"], "provided_node_path": namespace["PROVIDED_PATH"],
        "spelled_sequence": namespace["spelled"],
        "repeat": {"sequences": namespace["repeat_sequences"],
                   "node_paths": namespace["repeat_paths"],
                   "counts_k3": namespace["repeat_counts"],
                   "counts_k4": namespace["repeat_four"], "graph": namespace["repeat_graph"]},
        "disconnected": {"reads": namespace["disconnected_reads"],
                         "graph": namespace["disconnected_graph"]},
        "changed_observation": {"reads": namespace["changed_reads"],
                                "added_kmers": namespace["added_kmers"],
                                "counts": namespace["changed_counts"],
                                "graph": namespace["changed_graph"]},
        "lengths": [{"input": lengths, **summary} for lengths, summary in
                    zip(namespace["length_examples"], namespace["length_results"])],
        "optional_support_filter": namespace["supported_twice"],
    }


def build(solution=False, reference=None):
    cells = []

    def add(kind, source):
        result = {"cell_type": kind, "id": f"week03-{len(cells):02d}", "metadata": {},
                  "source": (inspect.cleandoc(source) if kind == "markdown"
                             else textwrap.dedent(source).strip()) + "\n"}
        if kind == "code":
            result.update(execution_count=None, outputs=[])
        cells.append(result)

    def md(source):
        add("markdown", source)

    def code(source):
        add("code", source)

    md("""# Homework 03 — Reconstructing a sequence from fragments

    Complete after Week 3, before Week 4

    How can overlapping reads help reconstruct a longer sequence? Count the
    short words in two reads and use them to build a de Bruijn graph. Then spell
    a supplied path and compare two paths that fit the same short-word counts.
    The final task calculates N50 from contig lengths.

    All sequences and lengths are invented examples, separate from the class
    cell cultures. The path is supplied; your code will not have to search for one.

    You will write four short functions using Python loops, dictionaries, sets,
    slicing, and `sorted`. The support-filtering exercise is optional.

    **Submit:** this notebook with your initial prediction, k-mer counts, printed
    graph and path, both length summaries, and the three interpretation sentences
    requested in Step 5.

    Follow the Colab setup instructions below, or use local Jupyter with
    Python 3.9 or later. All data are included.

    <details>
    <summary>Reading an error message</summary>

    `NotImplementedError` marks an unfinished task. `NameError` often means you
    skipped a cell or restarted the runtime; rerun setup and the preceding cells.
    For an `AssertionError`, compare the check's input and expected result with
    your function's output. After editing a function, run its definition again
    before its checks. The expandable hints suggest where to start.

    </details>
    """)
    if solution:
        md("**Instructor reference edition.** Functions are completed. Run all cells to reproduce the answer key. Give students `exercise.ipynb`.")

    md("""## Step 1 — Predict the overlaps

    Our first invented sequence is `ATGACCT`. With k=3 its successive words are
    `ATG`, `TGA`, `GAC`, `ACC`, and `CCT`. A **k-mer** is a substring of k letters;
    windows overlap and advance one letter at a time.

    Now inspect the separate reads `ATGAC` and `GACCT`.

    **My prediction:** The k-mer … occurs in both reads. That observation means
    … ; it does / does not tell us how many copies it has in a genome, because … .

    | Object | Meaning in this homework |
    |---|---|
    | Read | One observed fragment, with its own boundaries |
    | K-mer support | Number of times that word was observed across read windows |
    | Node | A (k−1)-letter prefix or suffix |
    | Directed edge | One distinct observed k-mer linking its prefix to its suffix |
    | Contig | A contiguous sequence reconstructed from assembly evidence |

    **Keep read boundaries.** The last bases of one read and the first bases
    of another are not known to be neighbors. Concatenating reads would invent
    unsupported words. Pooled counts reflect sampling, repeats, and potentially
    errors; observed support is not automatically genomic copy number.

    Scope: uppercase A/C/G/T only. Empty read collections or reads shorter than
    k contribute no windows. Counting accepts positive integer k; graph building
    requires k≥2 and a single k-mer width. Invalid characters are rejected.
    """)
    code(SETUP)

    md("""## Step 2 — Count within each read

    Complete `kmer_counts(reads, k)` to return a dictionary from word to observed
    count. Include overlapping windows and the final possible start. The
    supplied validation checks k and the alphabet; no sequence is silently cleaned.

    Run the checks. Compare the table from the reads with the words in the known
    toy sequence. Why is GAC seen twice even though it occurs once in that sequence?

    <details>
    <summary>Hint: two nested loops and one dictionary update</summary>

    Use an outer loop over individual reads. A length-k window can start at
    `len(read) - k`, inclusive, so remember that `range` excludes its stop value.
    Use `counts.get(word, 0)` when a word might not yet be in the dictionary.
    Reset the window positions for each read; never join the strings first.
    For `ATGAC` and `GACCT`, count six windows in total. Concatenating the
    records would invent `ACG` and `CGA` across their boundary.

    </details>
    """)
    code(COUNTS_SOLUTION if solution else COUNTS_STARTER)
    code(COUNTS_CHECKS)

    md("""## Step 3 — Make a directed k-mer graph

    For a k-mer `GAC`, its first k−1 letters are `GA`, and its last k−1 letters
    are `AC`. Add the edge **GA → AC**. These are directed edges: reversing
    the arrow changes the relationship.

    Complete `build_kmer_graph(counts)`. Collect node labels in a set and keep
    **one edge per distinct k-mer**, with its observed count in `support`.
    GAC has support 2 because both reads cover the same occurrence in `ATGACCT`.
    The count records repeated sampling. It does not tell the traversal to add
    another genomic copy of GAC.

    The function returns a dictionary with sorted `nodes` and a list of edge
    dictionaries (`kmer`, `source`, `target`, `support`). The printed edge list is alphabetical. A path must instead follow each
    edge's source and target. Include terminal
    nodes even when they have no outgoing edge. An empty input gives an empty graph.

    <details>
    <summary>Hint: split the word without changing its letters</summary>

    `word[:-1]` omits the last letter; `word[1:]` omits the first. Use these
    slices for the two node labels. Add both to `nodes` and append one edge
    dictionary. A count of 3 still creates one edge entry with support 3.
    The provided `sorted` calls keep displays deterministic.

    </details>
    """)
    code(GRAPH_SOLUTION if solution else GRAPH_STARTER)
    code(GRAPH_CHECKS)

    md("""## Step 4 — Spell a supplied path; inspect ambiguity

    The class provides this ordered path of two-letter nodes:

    ```text
    AT → TG → GA → AC → CC → CT
    ```

    Complete `spell_path(path)`: keep the whole first node, then add only the
    final letter of each next node. This uses the shared letters once. The
    result is conditional on the supplied path; your function does not search
    the graph or decide that this is the only possible assembly.

    The supplied validator checks equal nonempty node widths, DNA letters,
    and local overlap. It does not verify that edges occur in a particular
    dataset; a separate supplied check confirms that for this example. Empty
    paths return an empty string. A single node spells itself.

    <details>
    <summary>Hint: keep the first node, then append one new letter at a time</summary>

    Start your string with `nodes[0]`. Loop over the remaining nodes and add
    the last character of each. Appending each complete node would duplicate
    the shared overlap. For 2-letter nodes, each additional node extends the
    spelled string by exactly one base.

    </details>
    """)
    code(PATH_SOLUTION if solution else PATH_STARTER)
    code(PATH_CHECKS)
    md("""### Supplied observations — What does the graph leave unresolved?

    Run the next cell and inspect three cases:

    - **Repeated context:** `ATGATCAT` and `ATCATGAT` have the same six 3-mers,
      each observed once. Two supplied walks around the branches at AT spell
      different strings. This graph alone cannot choose their order. A cycle
      in a k-mer graph does not prove the DNA molecule is circular. The longer
      word `GATC` distinguishes this particular pair; using larger k is not
      guaranteed to resolve every real assembly and can lose support in short reads.
    - **Disconnected observations:** reads `ATGA` and `CCGT` form two separate
      graph components at k=3. These data do not supply a connecting path.
      Missing coverage is one possible explanation; disconnected components
      alone do not prove two organisms or two chromosomes.
    - **An added read:** adding `GATCT` introduces GAT, ATC, and TCT, each with
      support 1. The graph changes, but low support alone cannot decide whether
      this is an error, a real difference, or sparse sampling. Base qualities,
      repeated observations, and appropriate biological context would help.

    Both paths in the first case are already supplied. No Eulerian-path
    implementation is part of this homework.
    """)
    code(OBSERVATIONS)

    md("""## Step 5 — Calculate N50 and interpret it

    N50 summarizes **contiguity**, not sequence correctness. Sort contig lengths
    from largest to smallest and add bases until you reach at least half of
    the total assembled length. The length of the contig where you cross that
    threshold is N50; the number of contigs used is L50.

    | Lengths, largest first | Cumulative bases | Half of total | N50 | L50 |
    |---|---|---:|---:|---:|
    | 8, 7, 5 | 8, 15, 20 | 10 | 7 | 2 |

    N50 is neither the median contig length nor half of the longest contig.
    The threshold counts **bases**, not the number of contigs. Reaching exactly
    half is sufficient. Complete `n50(lengths)`; the supplied summary helper
    also reports L50 and total bases. For an empty assembly this notebook
    explicitly returns N50=0 and L50=0; zero or negative contig lengths are rejected.

    Compare `[8, 7, 5]` with `[12, 8]`. Both total 20, but the second has higher
    N50. Their lengths alone do not establish which sequences are correct:
    an incorrect join could increase N50. These are separate invented length
    lists, not contigs automatically assembled from our seven-base example.

    <details>
    <summary>Class example: losing sequence can increase N50</summary>

    Removing the five-base contig from `[8, 7, 5]` leaves `[8, 7]`. The total
    falls from 20 to 15 and its halfway threshold from 10 to 7.5. N50 rises
    from 7 to 8, although neither remaining contig grew. If the removed contig
    represented genuine distinct target sequence, completeness decreased.
    Always read N50 together with total length and evidence about the sequences.

    </details>

    <details>
    <summary>Hint: return a length at the first threshold crossing</summary>

    Use `sorted(values, reverse=True)`. Keep a cumulative sum, adding one length
    per iteration. At the first point where `2 * cumulative >= total`, return
    that current length. This integer comparison works for odd totals too.
    Return the contig length rather than the cumulative sum or the contig count.

    </details>

    **Write three sentences:** (1) use GAC support and the two repeat walks to
    explain one sampling issue and one assembly ambiguity; (2) state the N50,
    L50, and total for both length lists and explain what they measure;
    (3) identify a conclusion about errors, genomic structure, or correctness
    that these observations cannot establish, and name evidence you would seek.
    """)
    code(N50_SOLUTION if solution else N50_STARTER)
    code(N50_CHECKS)
    md("**Your interpretation:**\n\n1. …\n2. …\n3. …")
    md("""### Before you submit

    - Complete the four functions and run all core cells from the top without
      failed checks. Keep your initial prediction and outputs.
    - Preserve the k-mer counts, printed graph, spelled path, ambiguity
      observations, and both length summaries in the saved notebook.
    - Replace all three interpretation placeholders with your own sentences.
    - Save and download your completed `.ipynb` after Week 3, before Week 4.
    """)
    md("""## Optional extension — What does a support cutoff erase?

    Run the supplied cell to keep only
    words observed at least twice in the original overlapping reads.
    Predict how many graph edges will remain before running it.

    What genuine toy-sequence words disappear? Why would automatically labelling
    every singleton an error be unjustified? Compare the discarded words with `ATGACCT`: you know they belong to this
    target. In real reads, their origin would need investigation. The filtering
    cell uses separate variables, so you can still inspect the original graph.
    """)
    code(OPTIONAL)
    if solution:
        md("""## Instructor answer key

        The single sequence `ATGACCT` contributes five distinct 3-mers once each:
        ATG, TGA, GAC, ACC, CCT. Across reads `ATGAC` and `GACCT`, GAC has support
        2 and all other types support 1. There are six 2-mer nodes and five
        distinct directed edges. The supplied path AT→TG→GA→AC→CC→CT spells ATGACCT.
        Support 2 reflects overlapping observations here, not two genomic copies.

        `ATGATCAT` and `ATCATGAT` each contribute ATG, TGA, GAT, ATC, TCA, and CAT
        once at k=3. The common graph has five nodes and six edge types; two
        supplied node walks spell the two strings. Their k=4 counts differ,
        and GATC occurs only in the first. A graph cycle is not proof of a
        circular molecule or enough evidence to choose an ordering.

        `ATGA` and `CCGT` contribute ATG, TGA, CCG, and CGT: two disconnected
        components, AT→TG→GA and CC→CG→GT. A connecting sequence is not supplied
        by these data. Adding GATCT contributes new types GAT, ATC, and TCT
        with support 1; their cause is unresolved.

        | Contig lengths | Total | N50 | L50 | Correctness |
        |---|---:|---:|---:|---|
        | 8, 7, 5 | 20 | 7 | 2 | Unknown |
        | 12, 8 | 20 | 12 | 1 | Unknown |

        Example interpretation: GAC support 2 comes from overlapping sampled
        reads rather than two genomic copies, while the two repeat strings share
        one 3-mer graph that cannot choose their ordering. Both length lists
        total 20 bases, with N50/L50 of 7/2 and 12/1 respectively, describing
        contiguity. Higher N50 does not prove correctness, so I would inspect
        read support spanning joins and independent sequence evidence.

        Optional support cutoff: only GAC with count 2 remains (one edge GA→AC).
        The discarded ATG, TGA, ACC, and CCT are genuine substrings of our known
        toy sequence. No threshold based only on these counts can label their
        absence as evidence of sequencing errors.

        Checkpoints: no cross-read words; overlapping windows retained; graph
        support kept distinct from genomic multiplicity; supplied-path spelling
        preserves overlap once; N50 uses cumulative bases; conclusions remain
        limited to the available evidence.
        """)
    md("""## Source

    Adapted from `bioinformatis-web/coding_exercises/lecture-03/build_notebook.py`
    under the Apache License 2.0. The exercises were rewritten for this course.
    The upstream license is stored beside the generator in `LICENSE.upstream.txt`.
    """)
    notebook = {"cells": cells, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
    references = [
        {"after": COUNTS_CHECKS, "source": COUNTS_SOLUTION, "title": "K-mer counts"},
        {"after": GRAPH_CHECKS, "source": GRAPH_SOLUTION, "title": "Directed graph"},
        {"after": PATH_CHECKS, "source": PATH_SOLUTION, "title": "Supplied path spelling"},
        {"after": N50_CHECKS, "source": N50_SOLUTION, "title": "N50"},
    ]
    return prepare_notebook(notebook, 3, solution=solution, data_source=SETUP, references=references)


def main():
    namespace = reference_namespace()
    for solution, filename in ((False, "exercise.ipynb"), (True, "solutions.ipynb")):
        (HERE / filename).write_text(json.dumps(build(solution, namespace), indent=1) + "\n")
    (HERE / "expected_results.json").write_text(
        json.dumps(reference_results(namespace), indent=2) + "\n")
    print("Wrote Week 3 exercise.ipynb, solutions.ipynb, expected_results.json")


if __name__ == "__main__":
    main()
