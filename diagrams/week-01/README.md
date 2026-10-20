# Week 1 figure reuse and review

These local SVGs are adapted from `bioinformatis-web`, under its Apache 2.0 license. They have no external assets or required web fonts. `viewBox` dimensions determine aspect ratio; embed at `width: 100%; height: auto` on a light background. Each carries a title, description and source/modification notice. A lesson or slide should supply a short contextual caption and suitable alt text.

| Local SVG | ViewBox | Teaching context | Adaptation and correction |
|---|---|---|---|
| `cell-organelles.svg` | 860 × 480 | Cell → nucleus → DNA; ribosomes make protein | Scoped the mitochondrial genome size to humans, clarified that the nucleus houses most cellular DNA, removed the CPU analogy. Depicts an animal eukaryotic cell, not all cells. |
| `dna-double-helix.svg` | 860 × 470 | Complementarity and strand direction | Separated the two upper ends and supplied the missing 3′ label; clarified B-DNA geometry and that the ladder is illustrative. |
| `central-dogma.svg` | 970 × 400 | DNA → RNA → protein | Added an explicit eukaryotic protein-coding scope and reminder that many RNAs are not translated. Matched lesson colors: DNA teal, RNA blue, protein ochre with pale circles; neutral process arrows and updated exon/intron legend preserve structural distinctions. |
| `analysis-pipeline.svg` | 1100 × 280 | Where week 1 fits in the course | Updated coverage brackets to include QC, qualified PCR as optional, and made clear that variant detection is one example workflow. |
| `nanopore-signal.svg` | 980 × 400 | A physical signal becomes inferred sequence | Corrected highlighted bases to match ACAGA at 96 pA; made repeated GATTA contexts consistent; replaced universal five-base and perfectly flat homopolymer claims with explicit schematic/noise qualifications; enlarged the motor label and shortened callouts. |
| `fastq-anatomy.svg` | 1040 × 420 | Four lines, aligned sequence and quality, Q40 decoding | Original position-14 zoom paired G with I although quality position 14 was F. Adjusted the quality string, preserving 27 bases and 27 quality characters. Widened canvas to prevent clipped annotations; separated the negative exponent from the base; described accuracy as estimated. |
| `basecalling-signal.svg` | 1200 × 500 | Physical fluorescence → base call → uncertainty | Explicitly labeled synthetic four-channel schematic; modern instruments can encode bases differently. Moved the footer above the lower edge. |
| `phred-encoding.svg` | 1200 × 600 | Q, p(error), encoded character and changing uncertainty | Replaced the Unicode minus in the quality row with ASCII hyphen (Q12). Corrected tick locations for positions 5, 10, 15 and 20. Qualified accuracy as estimated and made bin bounds precise. |

All eight were parsed as XML, rendered with `rsvg-convert`, and visually inspected after the modifications. PNG previews are verification outputs rather than required website dependencies.

Scientific context used in the review:

- [Oxford Nanopore: basecalling](https://nanoporetech.com/platform/technology/basecalling) and [official k-mer models](https://github.com/nanoporetech/kmer_models): measured current is interpreted computationally; models depend on sequencing conditions.
- [Illumina: two-channel SBS](https://www.illumina.com/science/technology/next-generation-sequencing/sequencing-technology/2-channel-sbs.html): four-channel diagrams are useful teaching models but do not describe every instrument.
- [NHGRI: mitochondrial DNA](https://www.genome.gov/genetics-glossary/Mitochondrial-DNA) and [human mitochondrial reference NC_012920.1](https://www.ncbi.nlm.nih.gov/nuccore/NC_012920.1): mitochondrial DNA is distinct from nuclear DNA; the human reference is approximately 16.6 kb.


## Additional introductory figure: genetic code

| Local SVG | ViewBox | Teaching context | Adaptation and correction |
|---|---|---|---|
| `genetic-code.svg` | 720 × 580 | Read RNA codons 5′→3′; synonymous codons, AUG/Met, and stop signals | Adapted from `bioinformatis-web/diagrams/lecture-01/04-genetic-code-table.svg`. Replaced low-contrast white stop squares with visible red asterisks; moved the AUG legend onto its own line; added room for an explicit stop/direction/scope footer and a light background; uses local font fallbacks and retains Apache provenance. |

All 64 displayed codon-to-amino-acid assignments were checked against the
[NCBI standard code](https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi#SG1),
including 61 amino-acid codons and the three stop signals UAA/UAG/UGA. AUG
encodes Met and commonly initiates translation; the figure does not claim that
AUG always initiates or that the standard code is universal. The SVG was parsed
as XML, rendered with `rsvg-convert`, and visually inspected after adaptation.
The corresponding interactive is `artifacts/week-01/03-central-dogma.html`.

## Library preparation and paired reads

| Local SVG | ViewBox | Teaching context | Adaptation and correction |
|---|---|---|---|
| `library-preparation.svg` | 1100 × 560 | Added adapters, optional PCR copies, and two mates from one fragment | Adapts the adapter/insert layout from `bioinformatis-web/diagrams/lecture-01/09-adapter-structure.svg` and the paired-end teaching idea from `diagrams/lecture-03/03-read-types.svg`. Uses generic adapter blocks, an explicit short-insert read-through example, and a PCR origin diagram. Both mate outputs are 5′→3′ in opposite orientations; the 500 bp insert / 2×150 bp example leaves a 200 bp unread middle. |

The figure is explicitly **not to scale**. It omits the original read-types
figure's inconsistent common-scale claim and dated instrument-accuracy labels.
It does not imply that PCR is required, that mates are independent biological
replicates, or that two mates guarantee one continuous sequence. The main lesson
uses Mate 1/Mate 2 here to distinguish this layout from the later independent
Read 1/Read 2 confidence examples.

The SVG retains Apache provenance for both source illustrations. It was parsed
as XML, rendered with `rsvg-convert`, and visually inspected on its light
background. The lesson anchor is `#library-prep`; presentation slide 12 uses
this figure after the sequencing introduction in the 29-slide deck. The class
schedule remains 180 minutes.

Scientific review used [Illumina's paired-end explanation](https://www.illumina.com/science/technology/next-generation-sequencing/plan-experiments/paired-end-vs-single-read.html),
[adapter read-through guidance](https://support.illumina.com/ko-kr/bulletins/2016/04/adapter-trimming-why-are-adapter-sequences-trimmed-from-only-the--ends-of-reads.html),
and [EMBL-EBI's discussion of technical and biological replication](https://www.ebi.ac.uk/training/online/courses/functional-genomics-ii-common-technologies-and-data-analysis-methods/rna-sequencing/performing-a-rna-seq-experiment/design-considerations/number-of-replicates/).
