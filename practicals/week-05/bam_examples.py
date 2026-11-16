"""Build a tiny real BAM for teaching; this source is embedded in each notebook."""
from pathlib import Path
from collections import Counter
import tempfile
import pysam


def create_bam_example():
    """Use a fresh temporary directory so no existing student file is replaced."""
    work_dir = Path(tempfile.mkdtemp(prefix='week05_bam_'))
    letters = list('ACGT' * 50)
    letters[98:103] = 'TCAAT'
    reference = ''.join(letters)
    fasta_path = work_dir / 'toy.fa'
    fasta_path.write_text('>toy\n' + reference + '\n')
    pysam.faidx(str(fasta_path))
    header = {'HD': {'VN': '1.6', 'SO': 'unsorted'},
              'SQ': [{'SN': 'toy', 'LN': len(reference)}],
              'RG': [{'ID': 'class', 'SM': 'synthetic'}]}
    records = []

    def record(name, start, sequence, cigar, flag=0, mq=60, quality=35):
        read = pysam.AlignedSegment()
        read.query_name = name
        read.query_sequence = sequence  # Already in alignment/reference orientation.
        read.flag = flag
        read.reference_id = 0 if start is not None else -1
        read.reference_start = start if start is not None else -1
        read.mapping_quality = mq
        read.cigarstring = cigar
        read.query_qualities = pysam.qualitystring_to_array(chr(quality + 33) * len(sequence))
        read.set_tag('RG', 'class')
        records.append(read)
        return read

    for base in ('A', 'G'):
        for i in range(6):
            record(f'{base}_{i+1:02}', 98, 'TC' + base + 'AT', '5M', flag=16 if i % 2 else 0)
    for i in range(3):
        record(f'low_base_G_{i+1}', 98, 'TCGAT', '5M', quality=10)
    for i in range(2):
        record(f'low_map_G_{i+1}', 98, 'TCGAT', '5M', mq=5)
    for name, flag in [('duplicate_G', 1024), ('secondary_G', 256),
                       ('supplementary_G', 2048), ('qc_fail_G', 512)]:
        record(name, 98, 'TCGAT', '5M', flag=flag)

    record('insertion', 130, reference[130:134] + 'GG' + reference[134:138], '4M2I4M')
    record('deletion', 145, reference[145:149] + reference[151:155], '4M2D4M')
    record('soft_clip', 165, 'GG' + reference[165:171], '2S6M')
    record('ref_skip', 175, reference[175:178] + reference[182:185], '3M4N3M')
    left = record('pair_01', 20, reference[20:40], '20M', flag=99)
    right = record('pair_01', 60, reference[60:80], '20M', flag=147)
    left.next_reference_id = right.next_reference_id = 0
    left.next_reference_start, right.next_reference_start = 60, 20
    left.template_length, right.template_length = 60, -60
    record('unmapped', None, 'AACCGG', None, flag=4, mq=0)

    # Deliberately reverse record order: BAM encoding itself does not imply sorting.
    unsorted_path = work_dir / 'toy.unsorted.bam'
    with pysam.AlignmentFile(str(unsorted_path), 'wb', header=header) as bam:
        for read in reversed(records):
            bam.write(read)
    bam_path = work_dir / 'toy.sorted.bam'
    pysam.sort('-o', str(bam_path), str(unsorted_path))
    pysam.index(str(bam_path))
    return work_dir, fasta_path, bam_path


def keep_alignment(read, min_mapq=30):
    """Teaching policy; duplicate and other flags are supplied, not inferred here."""
    return (not read.is_unmapped and not read.is_secondary and not read.is_supplementary
            and not read.is_duplicate and not read.is_qcfail
            and read.mapping_quality != 255 and read.mapping_quality >= min_mapq)


def count_site(bam_path, position0, min_baseq=20, min_mapq=30, filter_flags=True):
    """Count bases at a zero-based coordinate with all teaching filters explicit."""
    counts = Counter()
    deletions = skips = 0
    with pysam.AlignmentFile(str(bam_path), 'rb') as bam:
        if not 0 <= position0 < bam.get_reference_length('toy'):
            raise ValueError('Choose a zero-based position inside contig toy')
        # Disable implicit base/flag/BAQ rules, then apply our visible policy below.
        # All toy pairs are non-overlapping. The cap exceeds this dataset's depth.
        for column in bam.pileup('toy', position0, position0 + 1, truncate=True,
                                 stepper='nofilter', min_base_quality=0,
                                 min_mapping_quality=0, compute_baq=False,
                                 ignore_overlaps=False, ignore_orphans=False,
                                 max_depth=10000):
            for observation in column.pileups:
                read = observation.alignment
                if filter_flags:
                    if not keep_alignment(read, min_mapq):
                        continue
                elif read.mapping_quality == 255 or read.mapping_quality < min_mapq:
                    continue
                # N can also have is_del set. Test reference skips first.
                if observation.is_refskip:
                    skips += 1
                    continue
                if observation.is_del:
                    deletions += 1
                    continue
                query_index = observation.query_position
                if query_index is None or read.query_qualities is None:
                    continue
                if read.query_qualities[query_index] < min_baseq:
                    continue
                base = read.query_sequence[query_index]
                if base in 'ACGT':
                    counts[base] += 1
    depth = sum(counts.values())
    return {'counts': dict(counts), 'base_depth': depth,
            'g_fraction': counts['G'] / depth if depth else None,
            'deletion_observations': deletions, 'reference_skips': skips}
