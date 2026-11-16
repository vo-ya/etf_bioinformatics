"""Synthetic Week 5 data and supplied helpers; embedded into both notebooks."""
from collections import Counter
from math import log10
from statistics import mean


def make_reads(bases, base_q=35, map_q=60, strands=None):
    """One observation per independent invented fragment at a single site."""
    if strands is None:
        strands = ['+' if i % 2 == 0 else '-' for i in range(len(bases))]
    return [dict(base=base, base_q=base_q, map_q=map_q, strand=strand)
            for base, strand in zip(bases, strands)]


pileups = {
    'A': make_reads('AAAAAAGGGGGG'),
    'B': (make_reads('AAAAAAAA') + make_reads('GGGG', base_q=10)
          + make_reads('GG', map_q=5)),
    'C': make_reads('AAAAAA') + make_reads('GGGGGG', strands=['+'] * 6),
    'D': make_reads('AAAGGG', base_q=20, map_q=30),
}
# A, B, C, D are four independent synthetic sites: REF=A, candidate ALT=G.
positions_1based = {'A': 101, 'B': 201, 'C': 301, 'D': 401}


def retain_reads(reads, min_base_q=20, min_map_q=30):
    """Teaching thresholds, inclusive; not a general variant-filtering recipe."""
    if min_base_q < 0 or min_map_q < 0:
        raise ValueError('Quality thresholds must be nonnegative')
    return [read for read in reads
            if read['base_q'] >= min_base_q and read['map_q'] >= min_map_q]


def summarize(reads, ref='A', alt='G'):
    """Allele fraction uses ALL retained A/C/G/T observations as denominator."""
    if ref == alt or ref not in 'ACGT' or alt not in 'ACGT':
        raise ValueError('Use distinct reference and alternate DNA bases')
    if any(read['base'] not in ('A', 'C', 'G', 'T') for read in reads):
        raise ValueError('This toy accepts called A/C/G/T bases only')
    counts = Counter(read['base'] for read in reads)
    depth = len(reads)
    return dict(depth=depth, ref_count=counts[ref], alt_count=counts[alt],
                other_count=depth - counts[ref] - counts[alt],
                alt_fraction=counts[alt] / depth if depth else None,
                alt_forward=sum(r['base'] == alt and r['strand'] == '+' for r in reads),
                alt_reverse=sum(r['base'] == alt and r['strand'] == '-' for r in reads))


def genotype_log_likelihoods(ref_count, alt_count, error=0.01):
    """Binary A/G model of independent observations, not a production caller.

    Only A and G outcomes exist; errors flip between them. All observations
    have the same known error probability and correct mappings. No priors.
    """
    if any(type(n) is not int or n < 0 for n in (ref_count, alt_count)):
        raise ValueError('Counts must be nonnegative integers')
    if not 0 < error < 0.5:
        raise ValueError('Use 0 < error < 0.5')
    probabilities = {'0/0': error, '0/1': 0.5, '1/1': 1 - error}
    return {gt: ref_count * log10(1 - p) + alt_count * log10(p)
            for gt, p in probabilities.items()}


window_size = 100
window_starts = list(range(0, 1200, window_size))
control_depth = [20] * 12
sample_depth = [20, 22, 18, 20, 10, 9, 11, 10, 20, 18, 22, 20]
duplication_depth = [20, 22, 18, 20, 30, 29, 31, 30, 20, 18, 22, 20]
# These are invented MEAN depths for equal 100-bp windows, not read counts.
region_start, region_stop = 400, 800


def depth_ratio(depths, starts, start, stop):
    """Region mean / flanking mean, for supplied equal-width aligned windows."""
    if len(depths) != len(starts) or len(starts) < 3:
        raise ValueError('Supply matching depth and start lists with at least three windows')
    if any(d < 0 for d in depths):
        raise ValueError('Depths cannot be negative')
    width = starts[1] - starts[0]
    if width <= 0 or any(b - a != width for a, b in zip(starts, starts[1:])):
        raise ValueError('Windows must be ordered and equally spaced')
    if start not in starts or stop not in starts + [starts[-1] + width] or start >= stop:
        raise ValueError('Region boundaries must align with the supplied windows')
    inside = [d for s, d in zip(starts, depths) if start <= s < stop]
    outside = [d for s, d in zip(starts, depths) if not start <= s < stop]
    if not outside or mean(outside) == 0:
        raise ValueError('Need flanking windows with positive mean depth')
    return mean(inside) / mean(outside)


# Deliberately restricted to two biallelic records and one sample.
# QUAL and GQ are unknown ('.'); the GT and PASS labels are supplied examples.
vcf_text = '''##fileformat=VCFv4.3
##reference=synthetic_week05
##contig=<ID=toy,length=1200>
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic depths">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read depth">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE
 toy\t101\t.\tA\tG\t.\tPASS\t.\tGT:AD:DP\t0/1:6,6:12
 toy\t501\t.\tAT\tA\t.\tPASS\t.\tGT:AD:DP\t0/1:7,5:12
'''.replace('\n toy', '\ntoy')


def parse_toy_vcf(text):
    """A teaching parser, intentionally limited to one sample and GT/AD/DP."""
    records = []
    for line in text.splitlines():
        if not line or line.startswith('#'):
            continue
        columns = line.split('\t')
        if len(columns) != 10:
            raise ValueError('Expected ten tab-separated columns and one sample')
        chrom, pos, identifier, ref, alt, qual, filters, info, fmt, sample = columns
        if ',' in alt or not ref or not alt or any(b not in 'ACGT' for b in ref + alt):
            raise ValueError('This example parser accepts one literal DNA ALT allele only')
        names, values = fmt.split(':'), sample.split(':')
        if len(names) != len(values) or len(set(names)) != len(names):
            raise ValueError('FORMAT names must be unique and match sample values')
        fields = dict(zip(names, values))
        if not {'GT', 'AD', 'DP'} <= fields.keys():
            raise ValueError('This example requires GT, AD, and DP')
        ad = [int(value) for value in fields['AD'].split(',')]
        dp, position = int(fields['DP']), int(pos)
        if len(ad) != 2 or min(ad) < 0 or dp < sum(ad) or position < 1:
            raise ValueError('Invalid position or allele-depth fields')
        records.append(dict(chrom=chrom, pos=position, ref=ref, alt=alt,
                            gt=fields['GT'], ad=ad, dp=dp, filters=filters))
    return records
