"""Generate a separate, self-contained Week 5 BAM practical and instructor copy."""
from pathlib import Path
import json
import sys
import textwrap
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from notebook_helpers import form_cell
HERE = Path(__file__).resolve().parent
CORE = (HERE / 'bam_examples.py').read_text()
SETUP = '''\
import sys
import importlib.util
import subprocess
if sys.version_info < (3, 9):
    raise RuntimeError('Use Python 3.9 or later')
if importlib.util.find_spec('pysam') is None:
    # One package download, only when pysam is missing. Uses this notebook's Python.
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pysam==0.24.1'])
import pysam
print('pysam:', pysam.__version__)
print('BAM setup ready. CPU only; no genome download.')
'''
INSPECT = '''\
with pysam.AlignmentFile(str(bam_path), 'rb') as bam:
    print('Reference names:', bam.references)
    print('Reference lengths:', bam.lengths)
    print('Sort order:', bam.header.to_dict()['HD']['SO'])
    print('Index available:', bam.has_index())
    all_records = list(bam.fetch(until_eof=True))
print('Alignment records:', len(all_records))
print('Mapped records:', sum(not r.is_unmapped for r in all_records))
print('Unmapped records:', sum(r.is_unmapped for r in all_records))
print('Unique query names:', len({r.query_name for r in all_records}))
'''
FETCH = '''\
region_start, region_stop = 100, 101  # Python: zero-based, excluded stop.
with pysam.AlignmentFile(str(bam_path), 'rb') as bam:
    overlapping = list(bam.fetch('toy', region_start, region_stop))
print('Overlapping alignment records:', len(overlapping))
for read in overlapping[:4]:
    print(read.query_name, read.reference_start, read.reference_end,
          read.cigarstring, read.mapping_quality, read.query_sequence)
print('Selected record as a full SAM TEXT line:')
print(overlapping[0].to_string() if overlapping else '(empty region)')
'''
FLAGS = '''\
flag_counts = {
    'reverse': sum(r.is_reverse for r in all_records),
    'paired': sum(r.is_paired for r in all_records),
    'duplicate': sum(r.is_duplicate for r in all_records),
    'secondary': sum(r.is_secondary for r in all_records),
    'supplementary': sum(r.is_supplementary for r in all_records),
    'QC failed': sum(r.is_qcfail for r in all_records),
}
print(flag_counts)
for read in all_records:
    if read.query_name == 'pair_01':
        print('pair_01:', 'read1=', read.is_read1, 'read2=', read.is_read2,
              'start=', read.reference_start, 'mate start=', read.next_reference_start,
              'template length=', read.template_length)
reverse_read = next(r for r in all_records if r.query_name == 'G_02')
print('Stored alignment-oriented sequence:', reverse_read.query_sequence)
print('Original read orientation:', reverse_read.get_forward_sequence())
'''
CIGAR = '''\
chosen_name = 'deletion'  # Also try insertion, soft_clip, and ref_skip.
chosen = next(r for r in all_records if r.query_name == chosen_name)
print('Name:', chosen.query_name, 'CIGAR:', chosen.cigarstring)
print('Stored query length:', chosen.query_length)
print('Reference interval:', (chosen.reference_start, chosen.reference_end))
print('Reference span:', chosen.reference_end - chosen.reference_start)
print('Pairs: (query index, reference index); None means no base on that side')
print(chosen.get_aligned_pairs())
'''
PILEUP = '''\
position0 = 100  # SAM/VCF position 101.
min_baseq, min_mapq = 20, 30
raw_site = count_site(bam_path, position0, min_baseq=0, min_mapq=0, filter_flags=False)
filtered_site = count_site(bam_path, position0, min_baseq, min_mapq)
print('Raw observations:', raw_site)
print('After our filters:', filtered_site)
'''
VISIBLE_PILEUP = '''\
# Inspect an insertion/deletion/skip without treating a missing query base as a letter.
inspect_position0 = 149  # Try 100, 133, or 178 as well.
with pysam.AlignmentFile(str(bam_path), 'rb') as bam:
    for column in bam.pileup('toy', inspect_position0, inspect_position0 + 1,
                             truncate=True, stepper='nofilter', min_base_quality=0,
                             compute_baq=False, ignore_overlaps=False,
                             ignore_orphans=False, max_depth=10000):
        for observation in column.pileups:
            read = observation.alignment
            if not keep_alignment(read):
                continue
            if observation.is_refskip:
                label = 'reference skip (N): no query base'
            elif observation.is_del:
                label = 'deletion (D): no query base'
            else:
                label = read.query_sequence[observation.query_position]
            print(column.reference_pos, read.query_name, label,
                  'insertion/deletion length AFTER this base:', observation.indel)
'''
COVERAGE = '''\
plot_start, plot_stop = 90, 185
with pysam.AlignmentFile(str(bam_path), 'rb') as bam:
    acgt = bam.count_coverage('toy', plot_start, plot_stop, quality_threshold=20,
                             read_callback=lambda read: keep_alignment(read, 30))
base_depth = [sum(values) for values in zip(*acgt)]
print('Every position is included, including zero-depth positions.')
for position in [90, 100, 130, 149, 150, 151, 178, 182]:
    print(position, base_depth[position - plot_start])
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
    print(list(zip(range(plot_start, plot_stop), base_depth)))
if plt is not None:
    figure, ax = plt.subplots(figsize=(10, 3.5))
    ax.step(range(plot_start, plot_stop), base_depth, where='mid', color='#0d7377')
    ax.set(xlabel='Reference position (0-based)', ylabel='Retained A/C/G/T observations',
           title='Synthetic BAM: base coverage, not alignment-span coverage', ylim=(0, 14))
    ax.axvspan(149, 151, color='#ad4936', alpha=.15, label='2D example: [149,151)')
    ax.legend()
    figure.tight_layout()
    plt.show()
'''
WRITE = '''\
# This overwrites only our derived file in the fresh notebook output directory.
subset_path = work_dir / 'candidate.filtered.bam'
written = 0
with pysam.AlignmentFile(str(bam_path), 'rb') as source:
    with pysam.AlignmentFile(str(subset_path), 'wb', template=source) as output:
        for read in source.fetch('toy', 90, 110):
            if keep_alignment(read, 30):
                output.write(read)
                written += 1
# A subset selected in coordinate order remains coordinate-sorted.
# Close the writer BEFORE making an index or reopening the file.
pysam.index(str(subset_path))
with pysam.AlignmentFile(str(subset_path), 'rb') as subset:
    assert subset.has_index()
    print('Records written:', written, 'records fetched:', len(list(subset.fetch('toy', 100, 101))))
print('Subset evidence with base Q >= 20:', count_site(subset_path, 100))
print('BAM:', subset_path)
print('Index:', str(subset_path) + '.bai')
'''

def build(solution=False):
    cells=[]
    def md(source):
        cells.append(dict(cell_type='markdown', id=f'w05-bam-{len(cells):02}',metadata={},source=textwrap.dedent(source).strip()+'\n'))
    def code(source, tag, title=None):
        cell=dict(cell_type='code',id=f'w05-bam-{len(cells):02}',metadata={'tags':[tag]},source=textwrap.dedent(source).strip()+'\n',execution_count=None,outputs=[])
        cells.append(form_cell(cell,title) if title else cell)
    def answer(text):
        md('**Instructor answer.** '+text if solution else '**Your explanation:** Record your prediction, the changed output, and what it means.')
    filename='bam_solutions' if solution else 'bam_exercise'
    md('''
    # Week 5 additional practical — Working with BAM files in Python

    Open, query, inspect, and write a real BAM using **pysam**. You will build a tiny
    synthetic dataset locally, then connect its alignment records to the pileups
    used in the Week 5 lecture. No real genome or personal sequencing data are used.

    This is **additional practice**, separate from the original Week 5 notebook.
    Allow about 75–90 minutes: setup 5–10, headers/regions 15, flags/CIGAR 20,
    pileup/coverage 20–25, writing/interpretation 15–20. It does not automatically
    add to the original required homework; your instructor will specify its use.
    The optional index experiment takes additional time.

    Cells run as supplied. Predict, make the requested edits, and write explanations.
    Running all cells unchanged does not complete the tasks.
    ''')
    md(f'''
    ## 0. Install once, then create your own tiny dataset

    [Open this notebook in Colab](https://colab.research.google.com/github/vo-ya/etf_bioinformatics/blob/main/practicals/week-05/{filename}.ipynb)

    Save a copy in Drive, or download this file and upload it to Colab. Use Python 3
    and a CPU. This notebook needs **pysam**; the next cell installs version 0.24.1
    only if the package is missing. Installation requires internet. It prints the
    installed version; record it when sharing results. No external samtools executable
    is required: pysam exposes the sorting/indexing commands used here.

    After installation, all data generation and analysis are local. The supplied
    builder creates FASTA, BAM, and index files in a fresh temporary directory and
    prints its path. It does not overwrite your existing files. A runtime reset can
    remove temporary files: rerun setup and then the following cells in order.
    If installation is unavailable, use a prepared environment with pysam installed.
    ''')
    code(SETUP,'bam-setup')
    code(CORE,'bam-helpers','Load the supplied BAM builder and counting helpers')
    code('''work_dir, fasta_path, bam_path = create_bam_example()
print('Output directory:', work_dir)
for path in sorted(work_dir.iterdir()):
    print(path.name, path.stat().st_size, 'bytes')''','bam-create')
    md('''
    The builder writes an intentionally unsorted BAM, then calls `pysam.sort` and
    `pysam.index`. A `.bam.bai` is an index, not another set of reads. Sorting and
    indexing change access to records; neither operation calls variants. A FASTA
    index (`.fai`) is different from a BAM index.

    The 200-base contig is named **toy**. At 1-based position 101, six good A and six
    good G observations are supplemented by three low-base-Q G, two low-map-Q G,
    and four G records with different flags. Other regions contain an insertion,
    deletion, soft clip, reference skip, and one paired fragment. There is also an
    unmapped record. These short reads illustrate fields, not realistic unique mappings.
    Flags and mapping qualities are assigned for teaching, not inferred by an aligner.
    Some secondary/supplementary records' primary counterparts are deliberately absent.
    ''')
    md('''
    ## 1. Read the header and count records

    `AlignmentFile(..., 'rb')` opens compressed BAM for reading; `with` closes it
    even if the cell raises an error. Inspect the reference names, lengths, and sort
    order. `fetch(until_eof=True)` reads from the current file position through the
    remaining records, including unmapped records. We reopen the file for each task
    so a previous iterator cannot leave us at the end.

    Predict whether the number of records equals the number of distinct query names.
    Run the cell. Explain the difference; do not interpret either value as a general
    count of independent molecules. Keeping a whole file in `all_records` is convenient
    for 28 records; stream large BAM files instead.
    ''')
    code(INSPECT,'bam-inspect')
    answer('There are 28 records: 27 mapped and one unmapped. There are 27 query names because both mates use pair_01. Real files may have additional primary, secondary, and supplementary records per read; duplicate flags concern molecular redundancy, not simply duplicate names.')
    md('''
    ## 2. Fetch a region: a row view of the alignments

    With numeric arguments, `fetch('toy', start, stop)` uses **zero-based,
    start-inclusive, stop-exclusive** coordinates. SAM text POS is 1-based:
    `reference_start=98` is SAM POS=99. Query `[100,101)` for SAM position 101.
    The index lets pysam retrieve overlapping alignments efficiently.

    Predict the number of returned records. Run the cell, then try `[103,104)`.
    Why does a read ending at 103 (excluded) not overlap a region starting at 103?
    Restore `[100,101)` afterward. The printed SAM line is a readable representation
    of a BAM record, not a view of raw binary bytes.
    ''')
    code(FETCH,'bam-fetch')
    answer('All 21 candidate-site records overlap [100,101); fetch itself has not applied our quality/flag policy. Their interval is [98,103), so [103,104) returns zero. The first base of the requested region need not be a read start.')
    md('''
    ## 3. Flags, mates, and stored orientation

    Use the boolean properties rather than memorizing bit arithmetic. Flag categories
    can overlap: a reverse-oriented mate is both paired and reverse, for example.
    Find the two records for `pair_01`. Predict the mate coordinates and the sign of
    their template lengths, then inspect the output.

    Reverse-aligned SEQ is stored in alignment orientation. `get_forward_sequence()`
    restores the original read orientation. Do not reverse-complement the stored
    sequence again when extracting bases for a reference-coordinate pileup.
    ''')
    code(FLAGS,'bam-flags')
    answer('Two records are paired; seven mapped records are reverse-oriented (six short reads and the second mate). There is one record in each duplicate/secondary/supplementary/QC-fail category. Mate starts are 60 and 20; outer fragment [20,80) has length 60, recorded as +60 and −60. Stored G_02 is TCGAT; its original orientation is ATCGA.')
    md('''
    ## 4. CIGAR determines which coordinates a read consumes

    Try `deletion`, `insertion`, `soft_clip`, and `ref_skip` in the cell. Before each
    run, predict the stored query length and reference span. M consumes both sides
    and allows a match or mismatch; I consumes only query; D and N consume only
    reference; S consumes stored query but is not aligned to reference.

    `get_aligned_pairs()` exposes query/reference index pairs. An insertion or soft
    clip has no reference coordinate for those query bases. A deletion or reference
    skip has no query base at those reference coordinates. **N is a reference skip,
    not a synonym for a DNA deletion**; spliced RNA alignments commonly use N.
    Our N record is an artificial API example, not structural-variant evidence.
    ''')
    code(CIGAR,'bam-cigar')
    answer('4M2D4M: query length 8, reference span 10, deleted reference indices 149–150. 4M2I4M: query 10, span 8, inserted GG after index 133. 2S6M: stored query 8, aligned reference span 6. 3M4N3M: query 6, span 10, skipped reference indices 178–181. None must not be used as a Python base index.')
    md('''
    ## 5. Pileup: a column view, with explicit filtering

    A region fetch returns records; `pileup` organizes them by reference position.
    Our supplied `count_site` function disables the pileup engine's implicit filters
    and then applies a visible teaching policy: exclude unmapped, secondary,
    supplementary, duplicate, and QC-failed alignments; require mapping Q ≥ 30
    and base Q ≥ 20. MAPQ 255 (unavailable) is excluded. These are example settings,
    not a universal variant-calling recipe. Supplementary alignments may be useful
    for SV analysis; their exclusion here is specific to this simple SNV count.

    Predict the raw and filtered A/G counts. Run the cell. Lower **only** base Q to 0,
    then restore 20 and lower **only** mapping Q to 0. Finally try base Q40.
    Record how the numerator and denominator change, then restore defaults.
    The helper has a depth cap of 10,000 (well above this dataset), disables BAQ,
    and does not collapse overlapping mates; the single toy pair does not overlap.
    Those choices must be reviewed for real datasets.
    ''')
    code(PILEUP,'bam-pileup')
    answer('Raw: A=6, G=15, depth=21, G fraction=15/21. Default: A=6, G=6, depth=12, fraction=0.5. Only base-Q threshold lowered: A=6, G=9, depth=15, fraction=0.6. Only map-Q threshold lowered: A=6, G=8, depth=14, fraction=8/14. At base Q40 no base survives, so the fraction is None.')
    md('''
    Inspect the short loop below at reference index 149. Then try 178 and 133.
    Why must the code check `is_refskip` and `is_del` before reading `query_position`?
    For the insertion, `indel=2` is reported at the preceding aligned base; inserted
    bases do not occupy separate reference columns. A pileup column object is tied
    to its iterator: copy values you need while iterating, rather than storing it
    for later use after closing the file.
    ''')
    code(VISIBLE_PILEUP,'bam-pileup-details')
    answer('At 149 the deletion has no query base; at 178 the N operation skips reference sequence. Both give query_position=None. Check skips first because a skipped reference position can also be flagged as a deletion-like absence by the pileup engine. At 133, indel=2 identifies the two query bases inserted after that column.')
    md('''
    ## 6. Plot base coverage, including positions with no observations

    `count_coverage` returns four arrays in A/C/G/T order. Summing them counts retained
    bases, not merely alignments whose reference spans overlap a position. We pass
    both a base-quality threshold and our read callback so the policy matches the
    preceding analysis. The arrays include zeros for uncovered positions.

    Predict the depth at index 100 and at deletion indices 149–150. Run the cell.
    Explain why fetching a record overlapping index 149 does not give base coverage
    of one there. The plot has a text fallback if matplotlib is unavailable.
    ''')
    code(COVERAGE,'bam-coverage','Plot retained base coverage — supplied drawing code')
    answer('Index 100 has depth 12. Indices 149 and 150 have zero A/C/G/T observations even though the deletion alignment spans them. Index 151 has depth one; the reference skip at 178 has zero and alignment resumes by 182. A deletion is an alignment event, not an A/C/G/T base. This sparse teaching profile cannot estimate sample copy number.')
    md('''
    ## 7. Write and index a filtered regional BAM

    Extract alignments overlapping `[90,110)` that pass the record-level flag and
    mapping-quality policy. Reuse the input header with `template=source`. The
    subset stays in coordinate order, so it can be indexed after the writer closes.

    Predict how many records are written. Why will the output contain more records
    than the default count of retained bases at position 101? This step applies no
    per-base quality filter: low-quality bases remain attached to retained records.
    ''')
    code(WRITE,'bam-write')
    answer('Fifteen records are written: twelve good observations plus three low-base-Q G records. Four flagged records and two low-MAPQ G records are excluded. Base-quality filtering at a site removes observations, not necessarily their entire records. Querying the new file with Q20 gives A=6, G=6 again.')
    md('''
    ## Save your results

    Save this notebook with outputs and explanations. The temporary directory contains
    your synthetic BAM, its index, reference, and filtered subset. For region access,
    keep a BAM and its `.bai` together. The next optional cell bundles the output
    directory into a ZIP next to it. In Colab's Files panel, open the printed folder
    path and download the ZIP; downloading the notebook alone does not include these files.
    ''')
    code('''import shutil
archive_path = Path(shutil.make_archive(str(work_dir) + '_results', 'zip', root_dir=work_dir))
print('Optional data download:', archive_path)''','bam-archive')
    md('''
    ## Optional — Why region access needs an index

    The cell makes a **copy** of the sorted BAM under a new name without copying its
    index. A sequential scan still works, but a coordinate query should fail. Run it,
    then explain which operation requires indexed access. The original BAM is intact.
    ''')
    code('''no_index_path = work_dir / 'copy_without_index.bam'
shutil.copyfile(bam_path, no_index_path)
with pysam.AlignmentFile(str(no_index_path), 'rb', index_filename=None) as bam:
    print('Index available:', bam.has_index())
    print('Sequential records:', sum(1 for _ in bam.fetch(until_eof=True)))
with pysam.AlignmentFile(str(no_index_path), 'rb') as bam:
    try:
        list(bam.fetch('toy', 100, 101))
    except ValueError as error:
        print('Expected regional-query failure:', error)''','bam-optional-index')
    answer('A sequential scan can read stored records without an index. A coordinate-based fetch requires an index to locate compressed file blocks efficiently. The copy remains sorted but is not indexed; sorting and indexing are separate steps.')
    md('''
    ## Sources

    - [pysam: working with BAM files](https://pysam.readthedocs.io/en/stable/usage.html)
    - [pysam API: AlignmentFile, fetch, pileup, and count_coverage](https://pysam.readthedocs.io/en/stable/api.html)
    - [pysam installation](https://pysam.readthedocs.io/en/stable/installation.html)
    - [SAM/BAM specification](https://samtools.github.io/hts-specs/SAMv1.pdf)

    Synthetic records and exercises were authored for this course. Notebook form
    packaging uses the shared helper and its retained upstream Apache license.
    ''')
    return dict(nbformat=4,nbformat_minor=5,cells=cells,metadata={
        'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
        'language_info':{'name':'python','version':'3.11'},
        'colab':{'name':f'week-05-{filename}.ipynb','provenance':[],'toc_visible':True}})

if __name__=='__main__':
    for solution,name in [(False,'bam_exercise'),(True,'bam_solutions')]:
        (HERE/f'{name}.ipynb').write_text(json.dumps(build(solution),indent=1,ensure_ascii=False)+'\n')
    print('Wrote standalone BAM exercise and instructor notebooks')
