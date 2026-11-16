"""Generate standalone Week 5 exercise and instructor notebooks."""
from pathlib import Path
import json
import sys
import textwrap
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from notebook_helpers import colab_url, form_cell
HERE = Path(__file__).resolve().parent
CORE = (HERE / 'variant_examples.py').read_text()

COUNT = '''\
site = 'A'  # Change to B, C, or D after predicting the result.
reads = pileups[site]
ref_count = 0
alt_count = 0
for read in reads:
    if read['base'] == 'A':
        ref_count += 1
    elif read['base'] == 'G':
        alt_count += 1

depth = len(reads)
alt_fraction = alt_count / depth if depth else None
print('Site:', site, 'position (1-based):', positions_1based[site])
print('Reference A:', ref_count, 'alternate G:', alt_count)
print('Depth:', depth, 'G fraction:', alt_fraction)
'''
FILTER = '''\
min_base_q = 20  # Inclusive: retain Q >= 20.
min_map_q = 30   # Independent check of mapping confidence.
filtered = {}
for site_name, observations in pileups.items():
    kept = retain_reads(observations, min_base_q, min_map_q)
    filtered[site_name] = kept
    before = summarize(observations)
    after = summarize(kept)
    print(site_name, 'raw:', before['depth'], before['alt_fraction'],
          'retained:', after['depth'], after['alt_fraction'])
'''
STRANDS = '''\
for site_name in ('A', 'C'):
    result = summarize(filtered[site_name])
    print(site_name, 'G fraction:', result['alt_fraction'],
          'G forward:', result['alt_forward'], 'G reverse:', result['alt_reverse'])
'''
COVERAGE = '''\
depths = sample_depth  # Try duplication_depth after the first calculation.
inside = []
flanks = []
for start, value in zip(window_starts, depths):
    if region_start <= start < region_stop:
        inside.append(value)
    else:
        flanks.append(value)

region_mean = sum(inside) / len(inside)
flank_mean = sum(flanks) / len(flanks)
ratio = region_mean / flank_mean
print('Region [start, stop):', (region_start, region_stop))
print('Region mean:', region_mean, 'flank mean:', flank_mean, 'ratio:', ratio)
print('Control ratio:', depth_ratio(control_depth, window_starts, region_start, region_stop))
'''
PLOT = '''\
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
    print('Plot unavailable. Compare the printed window table below.')
for start, value, control in zip(window_starts, depths, control_depth):
    print(f'[{start:4}, {start + window_size:4}): sample {value:2}, control {control:2}')
if plt is not None:
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.bar(window_starts, depths, width=window_size, align='edge',
           color='#147d87', edgecolor='white', label='Sample: mean depth')
    ax.step(window_starts + [1200], control_depth + [control_depth[-1]],
            where='post', color='#ad4936', label='Control: mean depth')
    ax.axvspan(region_start, region_stop, color='#d89c42', alpha=0.15)
    ax.set(xlim=(0, 1200), ylim=(0, max(depths + control_depth) + 5),
           xlabel='Reference position (0-based boundaries)', ylabel='Mean depth',
           title='Synthetic coverage: inspect [400, 800)')
    ax.legend()
    fig.tight_layout()
    plt.show()
'''
VCF = '''\
records = parse_toy_vcf(vcf_text)
for record in records:
    print(record)
first = records[0]
print('First record, 0-based Python index:', first['pos'] - 1)
print('First record, read G fraction:', first['ad'][1] / sum(first['ad']))
'''
LIKELIHOOD = '''\
ref_observations = 6
alt_observations = 6
error_probability = 0.01
scores = genotype_log_likelihoods(ref_observations, alt_observations, error_probability)
best = max(scores.values())
for genotype, score in scores.items():
    print(genotype, 'log10 likelihood:', round(score, 3),
          'relative likelihood:', round(10 ** (score - best), 8))
if ref_observations + alt_observations == 0:
    print('No observations: all genotypes tie. Do not call a genotype.')
else:
    print('Best under this model:', [gt for gt, score in scores.items() if score == best])
'''


def build(solution=False):
    cells = []
    def md(source):
        cells.append(dict(cell_type='markdown', id=f'w05-{len(cells):02}', metadata={},
                          source=textwrap.dedent(source).strip() + '\n'))
    def code(source, tag, title=None):
        cell = dict(cell_type='code', id=f'w05-{len(cells):02}', metadata={'tags': [tag]},
                    source=textwrap.dedent(source).strip() + '\n', execution_count=None, outputs=[])
        cells.append(form_cell(cell, title) if title else cell)
    def answer(text):
        if solution:
            md('**Instructor answer.** ' + text)
        else:
            md('**Your explanation:** Replace this sentence with your prediction, observed result, and interpretation.')
    md('''
    # Week 5 — Variant calling and structural variants

    Which differences from a reference are supported by the reads?
    Inspect four invented A→G candidate sites, then investigate a region with reduced depth.
    All data are synthetic. No biological or clinical conclusion concerns a real person.

    **Required work: 60–90 minutes**, separate from class: setup 5–10; count alleles 10;
    quality filters 15; strand evidence 10; coverage 15–20; VCF and conclusions 10–15.
    The optional likelihood extension takes another 10–15 minutes.

    Code cells already run. Your work is to predict outputs, make the requested edits,
    and explain what changes. Running all cells unchanged is not a completed exercise.
    Work through the required tasks before the optional extension.
    ''')
    md(f'''
    ## Open, save, and run

    [Open this notebook in Colab]({colab_url(5, solution)}) ·
    [Week 5 slides](https://vo-ya.github.io/etf_bioinformatics/presentations/week-05/)

    Save a copy in Drive or download the notebook and upload it to Colab.
    Use ordinary Python 3 on a CPU. All data and helpers are embedded: no dataset
    download, repository clone, package installation, or GPU is needed.
    Matplotlib is optional; the supplied plot cell prints the same values if unavailable.
    Run the two setup cells, then work downwards. After restarting the runtime,
    run setup and your preceding cells again. Save code, outputs, and written answers.
    ''')
    code('''import sys
assert sys.version_info >= (3, 9), 'Use Python 3.9 or later'
print('Week 5 setup ready; all observations are synthetic')''', 'setup')
    code(CORE, 'data', 'Load synthetic data and supplied helpers — run once per runtime')
    md('''
    ## 1. Count observations at one site

    A pileup collects aligned observations at a reference position. Each dictionary has
    `base`, `base_q` (confidence in the reported letter), `map_q` (mapping confidence),
    and `strand` (`+` or `-`, the alignment orientation). Bases are already expressed
    in reference orientation. We invented independent fragments: no PCR duplicates
    or overlapping mates are counted twice here.

    Site A has six A and six G observations. REF=A and candidate ALT=G.
    Predict its alternate-read fraction: **G observations / all retained observations**.
    Run the cell, then change `site` to `'B'`. Record its fraction before any filtering.
    A read fraction describes observations; it is not a genotype or a population allele frequency.
    ''')
    code(COUNT, 'count')
    answer('A: 6/12 = 0.5. B: 6/14 ≈ 0.429. Both denominators include all observed bases at that site. Neither fraction establishes which genotype produced the reads.')
    md('''
    ## 2. Change quality filters and keep track of the denominator

    Our illustrative rule keeps a read only if **both** base Q ≥ 20 and mapping Q ≥ 30.
    These are teaching settings, not universal recommended cutoffs. Mapping Q=255,
    which can mean unavailable in alignment files, is not present in this dataset.

    Predict which G observations at B survive. Run the cell. Then change only
    `min_base_q` to 30 and rerun. What happens to D? Try 40, then restore 20
    and rerun before continuing. Explain why an empty site returns `None` rather than zero.
    A real workflow also examines alignment context, duplicates, and other biases.
    ''')
    code(FILTER, 'filter')
    answer('At defaults A retains 12 (G fraction 0.5); B retains eight A (0.0); C retains 12 (0.5); D retains six (0.5). B loses four low-base-Q G and two low-map-Q G. At base Q≥30, D has no observations; its fraction is undefined, not evidence for 0/0. At Q≥40 all sites are empty. Restore Q≥20.')
    md('''
    ## 3. Equal fractions can conceal different evidence

    Compare A and C after restoring the default filters. Predict the strand counts,
    then run the cell. Both sites have six A and six G, but is G supported on both
    alignment orientations? Suggest one next observation that would help investigate C.
    Strand imbalance in this small toy is a reason to inspect the site, not proof of an artifact.
    ''')
    code(STRANDS, 'strands')
    answer('A has three G on each strand; C has six forward G and zero reverse G. Inspect read starts, positions within reads, local alignment, and independent molecules on the reverse strand. A simple fraction alone misses this distinction; six one-strand observations can also occur by chance.')
    md('''
    ## 4. Plot a candidate copy-number loss

    Each entry is an invented **mean depth in a 100-base window**. Python boundaries
    are zero-based and stop-exclusive: `[400,800)` contains four windows and 400 bases.
    A and B in the pileup task are separate examples from these coverage windows.

    Calculate mean depth inside the region divided by mean depth in the flanks.
    The matched synthetic control has depth 20 everywhere; assume equal library depth
    and comparable mappability for the initial comparison. Predict the ratio, then run
    both cells. The plot highlights the region; it does not estimate breakpoints.
    ''')
    code(COVERAGE, 'coverage')
    code(PLOT, 'plot', 'Draw coverage — supplied plotting code')
    md('''
    Change `depths = sample_depth` to `depths = duplication_depth` in the calculation
    cell, rerun it and the plot, and record the new ratio. Restore `sample_depth` afterward.
    For an ideal diploid baseline, what copy-number changes are compatible with these ratios?

    Now compare two explanations for the original 0.5 ratio:
    **(a)** one copy is deleted; **(b)** both copies exist but half the reads fail to map.
    The displayed depth values could be identical. Which extra evidence could distinguish them?
    ''')
    answer('Loss example: region mean 10, flank mean 20, ratio 0.5; duplication: 30/20=1.5. Under uniform sampling of a diploid baseline these are compatible with one or three copies respectively. GC bias, mapping loss, mixtures, and depth normalization can change those expectations. Seek independent reads or a contig spanning a new junction, supporting paired-read geometry, and a mappability check; depth alone cannot choose deletion over mapping loss.')
    md('''
    ## 5. Read two VCF records

    VCF separates the reference allele (`REF`), alternate allele (`ALT`), and sample
    genotype (`GT`). `0/1` means one reference and one first-alternate allele in this
    diploid example; `/` does not give phase. `AD` lists reference then alternate read
    depths; `DP` is sample depth. Real caller definitions can make DP differ from sum(AD).
    Our two records happen to have equal values. QUAL is unknown (`.`); supplied GT
    and PASS fields are examples, not results computed by the simple filters above.

    Print the embedded VCF and run the supplied restricted parser. It only accepts
    this lesson's one-sample, literal biallelic records, not general VCF files.
    ''')
    code('print(vcf_text)\n' + VCF, 'vcf')
    md('''
    1. Translate the first record into a sentence: locus, alleles, genotype, and read fraction.
    2. VCF POS is **1-based**. Which Python index corresponds to POS=101?
    3. In the second record, POS=501, REF=`AT`, ALT=`A`. Which base is deleted?
       Why is the A included? Is this a 400-base structural deletion?
    4. Does PASS establish a biological effect? Explain what additional context annotation needs.
    ''')
    answer('First: toy:101 A→G, unphased 0/1, AD=6,6, read G fraction 0.5; Python index 100. Second: the T at 1-based position 502 is deleted; A at 501 anchors the indel. It is a separate one-base deletion, not the coverage example. PASS means the record passed the filters applied by its producer. Functional interpretation needs transcript, consequence, and supporting biological evidence; it is not established by PASS.')
    md('''
    ## Finish the required exercise

    Save the notebook with your edited outputs and answers. Write three final sentences:
    - Why does filtering change the evidence at site B?
    - Why do A and C need different follow-up despite equal G fractions?
    - What observation would strengthen the candidate structural deletion beyond reduced depth?

    Check that your explanations distinguish an observed count, an inferred genotype,
    and a possible functional effect. No production variant caller is implemented here.
    ''')
    md('''
    ## Optional — Compare genotype likelihoods

    Use a deliberately simplified binary A/G model: each observation independently
    comes from one of two equally sampled chromosome copies. Errors flip A↔G with
    probability e=0.01; mappings are correct. Thus P(G|0/0)=e, P(G|0/1)=0.5,
    and P(G|1/1)=1−e. There are no other bases, strand effects, or genotype priors.

    For r A observations and a G observations:
    **log10 L = r log10(1−p) + a log10(p)**.
    This is the likelihood of the observed sequence of bases; a binomial count
    coefficient would be common to all genotypes and would not change the ranking.
    Relative likelihoods below divide by the best likelihood; they are not posterior
    probabilities and must not be reported as a calibrated QUAL or GQ.

    Compare (r,a)=(6,6), (8,0), (1,1), and (0,0). Why does the last case give no call?
    Why does this model give identical results for A and C?
    ''')
    code(LIKELIHOOD, 'optional-likelihood')
    answer('6/6 favors 0/1, with log10 L≈−3.612 versus −12.026 for either homozygote. 8/0 favors 0/0. 1/1 favors 0/1 but supplies much less evidence. 0/0 observations give equal likelihoods and no information. A and C tie because the model uses only counts and ignores strand and mapping context.')
    md('''
    ## Sources and scope

    - [VCF specification](https://samtools.github.io/hts-specs/VCFv4.5.pdf)
    - [GATK: interpreting VCF records](https://gatk.broadinstitute.org/hc/en-us/articles/360035531692-VCF-Variant-Call-Format)
    - [GATK: structural-variant evidence](https://gatk.broadinstitute.org/hc/en-us/articles/9022476791323-Structural-Variants)

    Data, diagrams, and worked calculations are authored for this course.
    Colab form packaging uses the shared Apache-derived course helper; its license
    is retained in the repository's Week 5 practical directory.
    ''')
    return dict(nbformat=4, nbformat_minor=5, cells=cells,
                metadata={'kernelspec': {'display_name':'Python 3','language':'python','name':'python3'},
                          'language_info': {'name':'python','version':'3.10'},
                          'colab': {'name':f'week-05-{"solutions" if solution else "exercise"}.ipynb',
                                    'provenance':[], 'toc_visible':True}})


if __name__ == '__main__':
    for solution, name in ((False,'exercise'),(True,'solutions')):
        (HERE / f'{name}.ipynb').write_text(json.dumps(build(solution), indent=1, ensure_ascii=False) + '\n')
    print('Wrote Week 5 exercise and instructor notebooks')
