"""Verify the delivered Week 5 examples and their stated limits."""
import builtins
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from math import log10
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
PRACTICAL = ROOT / 'practicals/week-05'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

builder = load('week05_builder', PRACTICAL / 'build_notebook.py')
examples = load('week05_examples', PRACTICAL / 'variant_examples.py')

class Week05Tests(unittest.TestCase):
    def execute(self, notebook, no_plot=False):
        namespace = {}
        original = builtins.__import__
        def controlled_import(name, *args, **kwargs):
            if no_plot and (name == 'matplotlib' or name.startswith('matplotlib.')):
                raise ImportError('Exercise fallback')
            return original(name, *args, **kwargs)
        with patch('builtins.__import__', side_effect=controlled_import), contextlib.redirect_stdout(io.StringIO()):
            for cell in notebook['cells']:
                if cell['cell_type'] == 'code':
                    exec(cell['source'], namespace)
        return namespace

    def test_both_standalone_editions_and_regeneration(self):
        for solution, name in [(False,'exercise'), (True,'solutions')]:
            notebook = json.loads((PRACTICAL / f'{name}.ipynb').read_text())
            self.assertEqual(notebook, builder.build(solution))
            ids = [c['id'] for c in notebook['cells']]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertTrue(notebook['metadata']['colab']['toc_visible'])
            for no_plot in [True, False]:
                ns = self.execute(notebook, no_plot)
                self.assertEqual(ns['ratio'], 0.5)
                self.assertEqual(ns['records'][0]['pos'], 101)
                self.assertEqual(ns['ref_count'], 6)
                self.assertEqual(ns['alt_count'], 6)
                if no_plot:
                    self.assertIsNone(ns['plt'])
            code = [c for c in notebook['cells'] if c['cell_type']=='code']
            self.assertTrue(all(c['execution_count'] is None and c['outputs']==[] for c in code))
            for c in code:
                if c['metadata'].get('cellView') == 'form':
                    self.assertTrue(c['source'].startswith('#@title'))

    def test_filter_counts_boundaries_and_empty_sites(self):
        expected = {'A':(12,6), 'B':(8,0), 'C':(12,6), 'D':(6,3)}
        for site, reads in examples.pileups.items():
            original = [r.copy() for r in reads]
            kept = examples.retain_reads(reads)
            stats = examples.summarize(kept)
            self.assertEqual((stats['depth'], stats['alt_count']), expected[site])
            self.assertEqual(reads, original)
        self.assertAlmostEqual(examples.summarize(examples.pileups['B'])['alt_fraction'],6/14)
        self.assertEqual(examples.summarize(examples.retain_reads(examples.pileups['D'],30))['alt_fraction'],None)
        for reads in examples.pileups.values():
            self.assertEqual(examples.retain_reads(reads,40),[])
        stats = examples.summarize(examples.make_reads('AGT'))
        self.assertEqual(stats['other_count'],1)
        self.assertAlmostEqual(stats['alt_fraction'],1/3)

    def test_strand_counts_do_not_change_simple_likelihood(self):
        a,c = (examples.summarize(examples.pileups[s]) for s in ['A','C'])
        self.assertEqual((a['alt_forward'],a['alt_reverse']), (3,3))
        self.assertEqual((c['alt_forward'],c['alt_reverse']), (6,0))
        self.assertEqual(examples.genotype_log_likelihoods(a['ref_count'],a['alt_count']),
                         examples.genotype_log_likelihoods(c['ref_count'],c['alt_count']))

    def test_likelihood_matches_direct_observation_probabilities(self):
        for ref in range(8):
            for alt in range(8):
                for error in [0.01,0.1,0.25]:
                    actual = examples.genotype_log_likelihoods(ref,alt,error)
                    for gt, probability in [('0/0',error),('0/1',0.5),('1/1',1-error)]:
                        product = 1.0
                        for base in 'A'*ref+'G'*alt:
                            product *= probability if base=='G' else 1-probability
                        self.assertAlmostEqual(actual[gt],log10(product),places=12)
        self.assertEqual(set(examples.genotype_log_likelihoods(0,0).values()),{0.0})
        self.assertEqual(max(examples.genotype_log_likelihoods(8,0),key=examples.genotype_log_likelihoods(8,0).get),'0/0')
        for args in [(-1,2,.01),(1,1,0),(1,1,.5),(1.5,2,.01)]:
            with self.assertRaises(ValueError): examples.genotype_log_likelihoods(*args)

    def test_depth_ratio_alternative_and_scale_invariance(self):
        fn = lambda ds: examples.depth_ratio(ds,examples.window_starts,400,800)
        self.assertEqual(fn(examples.sample_depth),0.5)
        self.assertEqual(fn(examples.control_depth),1)
        self.assertEqual(fn(examples.duplication_depth),1.5)
        self.assertEqual(fn([d*3 for d in examples.sample_depth]),0.5)
        with self.assertRaises(ValueError): fn([0]*12)
        with self.assertRaises(ValueError): examples.depth_ratio([1,2,3],[0,100,200],0,300)
        with self.assertRaises(ValueError): examples.depth_ratio(examples.sample_depth,examples.window_starts,401,800)

    def test_vcf_coordinate_replacement_and_format_order(self):
        records=examples.parse_toy_vcf(examples.vcf_text)
        self.assertEqual(len(records),2)
        self.assertEqual(records[0]['pos']-1,100)
        self.assertEqual(records[0]['ad'],[6,6])
        # Apply the second VCF allele replacement to an independently constructed reference.
        reference = 'C'*500+'AT'+'C'*20
        r=records[1]; start=r['pos']-1
        self.assertEqual(reference[start:start+len(r['ref'])],r['ref'])
        mutated=reference[:start]+r['alt']+reference[start+len(r['ref']):]
        self.assertEqual(mutated,reference[:501]+reference[502:])
        changed=examples.vcf_text.replace('GT:AD:DP\t0/1:6,6:12','DP:GT:AD\t12:0/1:6,6')
        self.assertEqual(examples.parse_toy_vcf(changed),records)
        with self.assertRaises(ValueError): examples.parse_toy_vcf('toy 101 A G')
        with self.assertRaises(ValueError): examples.parse_toy_vcf(examples.vcf_text.replace('\tA\tG\t','\tA\tG,T\t'))

    def test_deck_structure_and_coordinate_diagram(self):
        class Parser(HTMLParser):
            def __init__(self): super().__init__(); self.slides=[]; self.images=[]
            def handle_starttag(self, tag, attrs):
                attrs=dict(attrs)
                if tag=='section' and 'slide' in attrs.get('class','').split(): self.slides.append(attrs)
                if tag=='img': self.images.append(attrs)
        parser=Parser(); parser.feed((ROOT/'presentations/week-05/index.html').read_text())
        self.assertEqual([s['id'] for s in parser.slides],[f'slide-{i:02}' for i in range(1,39)])
        for i,s in enumerate(parser.slides,1): self.assertTrue(s['aria-label'].startswith(f'Slide {i}:'))
        self.assertEqual(len(parser.images),6)
        self.assertEqual(950-250,700)
        self.assertEqual((950-250)-(800-400),300)
        self.assertEqual((400-380)+(820-800),40)
        for image in parser.images:
            import xml.etree.ElementTree as ET
            svg=ET.parse(ROOT/'presentations/week-05'/image['src']).getroot()
            self.assertEqual(svg.attrib['width'],image['width'])
            self.assertEqual(svg.attrib['height'],image['height'])

if __name__=='__main__': unittest.main()
