"""Exercise real BAM I/O, coordinate semantics, and the delivered notebook."""
import builtins
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'practicals/week-05'
HAVE_PYSAM=importlib.util.find_spec('pysam') is not None

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module
builder=load('week05_bam_builder',HERE/'build_bam_notebook.py')
if HAVE_PYSAM:
    import pysam
    model=load('week05_bam_model',HERE/'bam_examples.py')

@unittest.skipUnless(HAVE_PYSAM,'Install pysam==0.24.1 to test the real BAM practical')
class BamPracticalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory,cls.fasta,cls.bam=model.create_bam_example()

    def test_real_files_header_sort_and_index(self):
        self.assertEqual(pysam.quickcheck(str(self.bam)), '')
        with pysam.AlignmentFile(str(self.bam),'rb') as bam:
            self.assertTrue(bam.has_index())
            self.assertEqual(bam.references,('toy',));self.assertEqual(bam.lengths,(200,))
            self.assertEqual(bam.header.to_dict()['HD']['SO'],'coordinate')
            records=list(bam.fetch(until_eof=True))
        self.assertEqual(len(records),28)
        self.assertEqual(sum(r.is_unmapped for r in records),1)
        self.assertEqual(len({r.query_name for r in records}),27)
        starts=[r.reference_start for r in records if not r.is_unmapped]
        self.assertEqual(starts,sorted(starts))
        with pysam.FastaFile(str(self.fasta)) as ref:
            self.assertEqual(ref.fetch('toy',98,103),'TCAAT')

    def test_region_fetch_does_not_count_bases_and_cigar_consumption(self):
        with pysam.AlignmentFile(str(self.bam),'rb') as bam:
            self.assertEqual(len(list(bam.fetch('toy',100,101))),21)
            self.assertEqual(list(bam.fetch('toy',103,104)),[])
            overlapping=list(bam.fetch('toy',149,150))
            self.assertEqual([r.query_name for r in overlapping],['deletion'])
            self.assertIn((None,149),overlapping[0].get_aligned_pairs())
        with pysam.AlignmentFile(str(self.bam),'rb') as bam:
            records={r.query_name:r for r in bam.fetch()}
        for name,length,span in [('insertion',10,8),('deletion',8,10),('soft_clip',8,6),('ref_skip',6,10)]:
            r=records[name];self.assertEqual(r.query_length,length);self.assertEqual(r.reference_end-r.reference_start,span)
        self.assertEqual(records['G_02'].query_sequence,'TCGAT')
        self.assertEqual(records['G_02'].get_forward_sequence(),'ATCGA')

    def test_pileup_filters_empty_data_deletions_and_skips(self):
        cases=[({}, {'A':6,'G':6}),({'min_baseq':0},{'A':6,'G':9}),
               ({'min_mapq':0},{'A':6,'G':8}),
               ({'min_baseq':0,'min_mapq':0,'filter_flags':False},{'A':6,'G':15}),
               ({'min_baseq':40},{})]
        for settings,counts in cases:
            result=model.count_site(self.bam,100,**settings)
            self.assertEqual(result['counts'],counts)
            total=sum(counts.values());self.assertEqual(result['base_depth'],total)
            self.assertEqual(result['g_fraction'],counts.get('G',0)/total if total else None)
        deleted=model.count_site(self.bam,149)
        skipped=model.count_site(self.bam,178)
        self.assertEqual(deleted['deletion_observations'],1)
        self.assertEqual(deleted['base_depth'],0)
        self.assertEqual(skipped['reference_skips'],1)
        self.assertEqual(skipped['deletion_observations'],0)
        self.assertEqual(model.count_site(self.bam,190)['g_fraction'],None)

    def test_coverage_agrees_with_pileup_at_each_reference_position(self):
        with pysam.AlignmentFile(str(self.bam),'rb') as bam:
            arrays=bam.count_coverage('toy',0,200,quality_threshold=20,
                                     read_callback=lambda r:model.keep_alignment(r,30))
        depths=[sum(x) for x in zip(*arrays)]
        self.assertEqual(len(depths),200)
        for pos in range(200):
            self.assertEqual(depths[pos],model.count_site(self.bam,pos)['base_depth'])
        self.assertEqual(depths[100],12);self.assertEqual(depths[149:151],[0,0])
        self.assertEqual(depths[178:182],[0]*4)

    def test_no_index_and_written_subset(self):
        import shutil
        copied=self.directory/'test-no-index.bam';shutil.copyfile(self.bam,copied)
        with pysam.AlignmentFile(str(copied),'rb') as bam:
            self.assertFalse(bam.has_index())
            self.assertEqual(len(list(bam.fetch(until_eof=True))),28)
        with pysam.AlignmentFile(str(copied),'rb') as bam:
            with self.assertRaises(ValueError):list(bam.fetch('toy',100,101))
        output=self.directory/'test-subset.bam'
        with pysam.AlignmentFile(str(self.bam),'rb') as source:
            with pysam.AlignmentFile(str(output),'wb',template=source) as target:
                for read in source.fetch('toy',90,110):
                    if model.keep_alignment(read):target.write(read)
        pysam.index(str(output))
        with pysam.AlignmentFile(str(output),'rb') as bam:
            self.assertEqual(len(list(bam.fetch('toy',100,101))),15)
        self.assertEqual(model.count_site(output,100)['counts'],{'A':6,'G':6})

    def test_both_notebook_editions_execute_and_regenerate(self):
        original_import=builtins.__import__
        def no_plot(name,*args,**kwargs):
            if name=='matplotlib' or name.startswith('matplotlib.'):raise ImportError('Test plot fallback')
            return original_import(name,*args,**kwargs)
        for solution,name in [(False,'bam_exercise'),(True,'bam_solutions')]:
            notebook=json.loads((HERE/f'{name}.ipynb').read_text())
            self.assertEqual(notebook,builder.build(solution))
            ids=[c['id'] for c in notebook['cells']];self.assertEqual(len(ids),len(set(ids)))
            for plotting in [False,True]:
                namespace={}
                with patch('builtins.__import__',side_effect=original_import if plotting else no_plot),contextlib.redirect_stdout(io.StringIO()):
                    for cell in notebook['cells']:
                        if cell['cell_type']=='code':exec(cell['source'],namespace)
                self.assertEqual(namespace['written'],15)
                self.assertEqual(namespace['filtered_site']['counts'],{'A':6,'G':6})
                self.assertTrue(namespace['archive_path'].exists())
                self.assertEqual(namespace['base_depth'][100-90],12)
                if not plotting:self.assertIsNone(namespace['plt'])
        # Exercise and instructor have identical executable code.
        student=[c['source'] for c in builder.build(False)['cells'] if c['cell_type']=='code']
        instructor=[c['source'] for c in builder.build(True)['cells'] if c['cell_type']=='code']
        self.assertEqual(student,instructor)

if __name__=='__main__':unittest.main()
