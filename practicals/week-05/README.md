# Week 5 — Variant calling and structural variants

- [Exercise notebook](exercise.ipynb)
- [Instructor answers](solutions.ipynb)
- [Student guide](../../weeks/week-05.html)
- [38-slide presentation](../../presentations/week-05/index.html)

Required work takes 60–90 minutes, separate from the 180-minute class. The
optional binary genotype-likelihood extension adds 10–15 minutes. Working
cells use short loops and editable settings; students must predict, change
inputs, and explain the outputs. Running the untouched notebook is not a
completed assignment. Instructor answers are prose, not hidden overwrites of
student functions.

In the original exercise and solution notebooks, all data and helpers are embedded. No external files, installs,
network requests, GPU, or production caller are required during execution.
Matplotlib is optional, with a printed coverage table as fallback. Hosted Colab
itself needs internet. Download/upload if the GitHub launch is unavailable.

Edit `build_notebook.py` for instructions and visible cells. Edit
`variant_examples.py` for embedded data and helpers, then rebuild both editions:

```sh
python3 practicals/week-05/build_notebook.py
python3 -m unittest discover -s tests -p 'test_week05*.py'
python3 scripts/check_pilot.py
```

The four synthetic sites share REF=A and candidate ALT=G. A has balanced 6/6
counts; B loses all six G under the illustrative Q20/MQ30 filters; C has the
same counts as A but all G on forward alignments; D is exactly on the default
thresholds. Empty sites return an undefined fraction. The coverage case has
region [400,800) with mean 10 versus flanks 20; the gain case has mean 30.
Both are compatible with alternative technical explanations until supported
by further evidence. See the notebook and teaching guide for model assumptions.

The VCF reader is intentionally restricted to one sample and literal biallelic
records with GT/AD/DP. It is not a general parser. The optional likelihood model
is binary, assumes correct mappings and independent errors, and has no priors.
Its outputs must not be used as calibrated QUAL/GQ values.

Checks execute both editions, test filter boundaries and empty data, compare
likelihoods with direct probability products, check depth ratios and VCF
coordinates, and verify deterministic regeneration. Local execution is not a
hosted Colab UI test. Colab form packaging uses the Apache-derived shared helper;
`LICENSE.upstream.txt` retains the source license.

Validation on 16 November 2026: all seven Week 5 tests passed. Both standalone
notebook editions executed with plotting and with the no-matplotlib fallback;
both notebook schemas validated. Hosted Colab controls were not browser-tested.

## Additional BAM practical

- [BAM exercise](bam_exercise.ipynb)
- [BAM instructor answers](bam_solutions.ipynb)

This separate 75–90-minute practical uses **real BAM files with pysam**. It is
additional practice, not an automatic increase to the original required homework.
Unlike the original notebook, it installs `pysam==0.24.1` if missing; that setup
requires internet. There is no genome download or external samtools executable.
Matplotlib is optional. All subsequent analysis uses locally generated data.

Students inspect headers and flags, fetch regions, decode CIGAR, count bases
with explicit pileup filters, plot base coverage, and write/index a filtered
regional BAM. A fresh temporary directory prevents overwriting existing files.
The optional final index experiment uses a separate file copy. A ZIP cell lets
students save the generated files alongside their notebook.

The synthetic BAM contains 28 alignment records (27 mapped, one unmapped) on a
200-base contig. At 1-based position 101, raw A/G counts are 6/15; after the
explicit record and base filters they are 6/6. The output regional BAM has
15 records because it applies only the record-level policy; base-Q filtering
subsequently leaves 12 observations. Deletion and N operations have no query
base at the affected reference positions.

Edit `build_bam_notebook.py` and the embedded fixture/helper source
`bam_examples.py`, then regenerate both BAM editions:

```sh
python3 practicals/week-05/build_bam_notebook.py
python3 -m pip install pysam==0.24.1
python3 -m unittest discover -s tests -p 'test_week05*.py'
```

The six BAM tests need pysam and report a skip if it is absent. They check real
BAM/index I/O, sorting, coordinates, CIGAR consumption, filtering, missing
indices, subset writing, coverage against pileup at every reference position,
and execution of both notebook editions with and without plotting.

BAM validation: tested with pysam 0.24.1 and Python 3.11.9. All 13 Week 5
Python tests pass, including six real-BAM tests. All four Week 5 notebook
schemas validate. Both BAM editions execute with and without matplotlib;
the coverage plot was rendered for visual review. Hosted Colab execution
was not tested.
