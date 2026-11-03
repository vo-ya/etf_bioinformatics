"""Exercise the delivered assembly homework and independent small-case oracles."""

import contextlib
import importlib.util
import io
import itertools
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PRACTICAL = ROOT / "practicals" / "week-03"


class WeekThreeDeliveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("week03_builder", PRACTICAL / "build_notebook.py")
        cls.builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.builder)
        cls.reference = cls.builder.reference_namespace()

    def test_instructor_cells_execute_from_fresh_namespace_and_match_key(self):
        namespace = {}
        notebook = json.loads((PRACTICAL / "solutions.ipynb").read_text())
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            for cell in notebook["cells"]:
                if cell["cell_type"] == "code":
                    exec(compile(cell["source"], "solutions.ipynb", "exec"), namespace)
        expected = json.loads((PRACTICAL / "expected_results.json").read_text())
        self.assertEqual(self.builder.reference_results(namespace), expected)
        self.assertIn("Homework 03 setup ready", output.getvalue())
        self.assertEqual(namespace["observed_counts"],
                         {"ATG": 1, "TGA": 1, "GAC": 2, "ACC": 1, "CCT": 1})
        self.assertEqual(namespace["spelled"], "ATGACCT")
        self.assertEqual(namespace["length_results"], [
            {"contigs": 3, "total": 20, "N50": 7, "L50": 2},
            {"contigs": 2, "total": 20, "N50": 12, "L50": 1}])
        self.assertEqual(len(namespace["repeat_graph"]["nodes"]), 5)
        self.assertEqual(len(namespace["repeat_graph"]["edges"]), 6)
        self.assertEqual(namespace["repeat_counts"][0], namespace["repeat_counts"][1])
        self.assertEqual(namespace["added_kmers"], ["ATC", "GAT", "TCT"])

    def test_count_boundaries_graph_support_and_supplied_path_invariants(self):
        count = self.reference["kmer_counts"]
        graph = self.reference["build_kmer_graph"]
        spell = self.reference["spell_path"]
        self.assertEqual(count(["AT", "GAC"], 3), {"GAC": 1})
        reads = ["ATGAC", "GACCT", "ATGAC", "AA", ""]
        for k in (1, 2, 3, 4, 6):
            counts = count(reads, k)
            self.assertEqual(sum(counts.values()), sum(max(0, len(read) - k + 1) for read in reads))
            if k >= 2:
                observed = graph(counts)
                self.assertEqual(len(observed["edges"]), len(counts))
                self.assertEqual(sum(edge["support"] for edge in observed["edges"]), sum(counts.values()))
                for edge in observed["edges"]:
                    self.assertEqual(edge["source"][1:], edge["target"][:-1])
                    self.assertEqual(edge["source"] + edge["target"][-1], edge["kmer"])
        for size in range(2, 6):
            for letters in itertools.product("AC", repeat=size):
                sequence = "".join(letters)
                for width in range(1, size):
                    path = [sequence[start:start + width] for start in range(size - width + 1)]
                    self.assertEqual(spell(path), sequence)

    def test_n50_matches_independent_base_weighted_median(self):
        for number in range(1, 4):
            for lengths in itertools.product(range(1, 5), repeat=number):
                # Give each base the length of its own contig, then select the
                # halfway base in descending order. This avoids a prefix-sum oracle.
                per_base_lengths = sorted((length for length in lengths for _ in range(length)), reverse=True)
                expected = per_base_lengths[(len(per_base_lengths) - 1) // 2]
                original = list(lengths)
                self.assertEqual(self.reference["n50"](original), expected)
                self.assertEqual(original, list(lengths))
        self.assertEqual(self.reference["assembly_summary"]([]),
                         {"contigs": 0, "total": 0, "N50": 0, "L50": 0})

    def test_reproducible_packaging_colab_setup_and_separate_reference(self):
        for solution, filename in ((False, "exercise.ipynb"), (True, "solutions.ipynb")):
            notebook = json.loads((PRACTICAL / filename).read_text())
            self.assertEqual(self.builder.build(solution, self.reference), notebook)
            self.assertEqual(notebook["metadata"]["colab"]["provenance"], [])
            self.assertTrue(notebook["metadata"]["colab"]["toc_visible"])
            self.assertEqual(len({cell["id"] for cell in notebook["cells"]}), len(notebook["cells"]))
            code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
            self.assertEqual(code_cells[0]["metadata"]["tags"], ["setup"])
            self.assertEqual(code_cells[0]["metadata"]["cellView"], "form")
            self.assertTrue(code_cells[0]["source"].startswith("#@title"))
        cells = self.builder.build()["cells"]
        references = [cell for cell in cells if cell["metadata"].get("tags") == ["reference-solution"]]
        student = "\n".join(cell["source"] for cell in cells)
        visible_source = "\n".join(cell["source"] for cell in cells if cell not in references)
        self.assertEqual(len(references), 4)
        self.assertIn("NotImplementedError", student)
        self.assertNotIn("## Instructor answer key", student)
        for reference in (self.builder.COUNTS_SOLUTION, self.builder.GRAPH_SOLUTION,
                          self.builder.PATH_SOLUTION, self.builder.N50_SOLUTION):
            self.assertNotIn(reference.strip(), visible_source)
            self.assertTrue(any(reference.strip() in cell["source"] for cell in references))

    def test_colab_student_attempt_and_reveal_workflow_in_all_three_weeks(self):
        original_import = __import__

        def without_optional_plotting(name, *args, **kwargs):
            if name == "matplotlib" or name.startswith("matplotlib."):
                raise ImportError("Exercise must support the documented table fallback")
            return original_import(name, *args, **kwargs)

        for week, reference_count in ((1, 4), (2, 3), (3, 4)):
            with self.subTest(week=week):
                notebook = json.loads((ROOT / "practicals" / f"week-{week:02d}" / "exercise.ipynb").read_text())
                namespace, pending_check, failures, revealed = {}, None, 0, 0
                with patch("builtins.__import__", side_effect=without_optional_plotting), contextlib.redirect_stdout(io.StringIO()):
                    for cell in notebook["cells"]:
                        if cell["cell_type"] != "code":
                            continue
                        if cell["metadata"].get("tags") == ["reference-solution"]:
                            self.assertIsNotNone(pending_check, "The attempt/check must precede its reference")
                            self.assertEqual(cell["metadata"]["cellView"], "form")
                            self.assertTrue(cell["metadata"]["jupyter"]["source_hidden"])
                            self.assertTrue(cell["source"].startswith("#@title"))
                            exec(cell["source"], namespace)
                            exec(pending_check, namespace)  # learner reruns the check above
                            pending_check = None
                            revealed += 1
                        else:
                            self.assertIsNone(pending_check)
                            try:
                                exec(cell["source"], namespace)
                            except NotImplementedError:
                                pending_check = cell["source"]
                                failures += 1
                self.assertIsNone(pending_check)
                self.assertEqual(failures, reference_count)
                self.assertEqual(revealed, reference_count)


if __name__ == "__main__":
    unittest.main()
