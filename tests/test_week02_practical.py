"""Verify the delivered homework and compare DP with exhaustive alignments."""

import contextlib
import importlib.util
import io
import itertools
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PRACTICAL = ROOT / "practicals" / "week-02"


def all_alignments(reference, read):
    """Enumerate legal alignments, without computing prefix-optimal scores."""
    if not reference and not read:
        yield "", ""
    if reference and read:
        for tail_reference, tail_read in all_alignments(reference[1:], read[1:]):
            yield reference[0] + tail_reference, read[0] + tail_read
    if reference:
        for tail_reference, tail_read in all_alignments(reference[1:], read):
            yield reference[0] + tail_reference, "-" + tail_read
    if read:
        for tail_reference, tail_read in all_alignments(reference, read[1:]):
            yield "-" + tail_reference, read[0] + tail_read


def direct_score(aligned_reference, aligned_read):
    columns = list(zip(aligned_reference, aligned_read))
    gap_columns = sum(a == "-" or b == "-" for a, b in columns)
    matches = sum(a == b for a, b in columns)
    mismatches = len(columns) - matches - gap_columns
    return 2 * matches - mismatches - 2 * gap_columns


class WeekTwoDeliveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("week02_builder", PRACTICAL / "build_notebook.py")
        cls.builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.builder)
        cls.reference = cls.builder.reference_namespace()

    def test_delivered_instructor_notebook_executes_and_matches_answer_key(self):
        namespace = {}
        notebook = json.loads((PRACTICAL / "solutions.ipynb").read_text())
        with contextlib.redirect_stdout(io.StringIO()):
            for cell in notebook["cells"]:
                if cell["cell_type"] == "code":
                    exec(compile(cell["source"], "solutions.ipynb", "exec"), namespace)
        expected = json.loads((PRACTICAL / "expected_results.json").read_text())
        self.assertEqual(self.builder.reference_results(namespace), expected)
        self.assertEqual(namespace["find_all"]("ATGCCATGACCTATGCCA", "ATGCCA"), [0, 12])
        self.assertEqual(namespace["find_all"]("ATGCCATGACCTATGCCA", "CCATGA"), [3])
        self.assertEqual(namespace["global_alignment"]("ATGCCA", "ATGCA"),
                         ("ATGCCA", "ATG-CA", 8))
        self.assertEqual(namespace["global_alignment"]("ATGCCA", "ATGACCA"),
                         ("ATG-CCA", "ATGACCA", 10))

    def test_global_scores_agree_with_exhaustive_legal_alignments(self):
        sequences = ["".join(letters) for length in range(4)
                     for letters in itertools.product("AC", repeat=length)]
        for reference, read in itertools.product(sequences, repeat=2):
            with self.subTest(reference=reference, read=read):
                legal_alignments = list(all_alignments(reference, read))
                optimum = max(direct_score(a, b) for a, b in legal_alignments)
                aligned_reference, aligned_read, actual = self.reference["global_alignment"](reference, read)
                self.assertEqual(actual, optimum)
                self.assertIn((aligned_reference, aligned_read), legal_alignments)
                self.assertEqual(direct_score(aligned_reference, aligned_read), actual)
                self.assertEqual(aligned_reference.replace("-", ""), reference)
                self.assertEqual(aligned_read.replace("-", ""), read)

    def test_generated_files_are_current_and_student_has_no_hidden_answers(self):
        for solution, filename in ((False, "exercise.ipynb"), (True, "solutions.ipynb")):
            delivered = json.loads((PRACTICAL / filename).read_text())
            self.assertEqual(self.builder.build(solution, self.reference), delivered)
            self.assertEqual(len({cell["id"] for cell in delivered["cells"]}), len(delivered["cells"]))
            self.assertEqual(delivered["metadata"]["colab"]["provenance"], [])
            self.assertTrue(delivered["metadata"]["colab"]["toc_visible"])
            code_cells = [cell for cell in delivered["cells"] if cell["cell_type"] == "code"]
            self.assertEqual(code_cells[0]["metadata"]["tags"], ["setup"])
            for cell in delivered["cells"]:
                if cell["metadata"].get("tags") in (["setup"], ["data"], ["reference-solution"]):
                    self.assertEqual(cell["metadata"]["cellView"], "form")
                    self.assertTrue(cell["source"].startswith("#@title"))
                    if cell["metadata"].get("tags") == ["reference-solution"]:
                        self.assertTrue(cell["metadata"]["jupyter"]["source_hidden"])
                else:
                    self.assertFalse(cell["metadata"])
        student = self.builder.build()
        student_source = "\n".join(cell["source"] for cell in student["cells"])
        references = [cell for cell in student["cells"] if cell["metadata"].get("tags") == ["reference-solution"]]
        visible_source = "\n".join(cell["source"] for cell in student["cells"] if cell not in references)
        self.assertEqual(len(references), 3)
        self.assertIn("NotImplementedError", student_source)
        self.assertNotIn("## Instructor answer key", student_source)
        for source in (self.builder.TABLE_SOLUTION, self.builder.SEARCH_SOLUTION, self.builder.SCORE_SOLUTION):
            self.assertNotIn(source.strip(), visible_source)
            self.assertTrue(any(source.strip() in cell["source"] for cell in references))


if __name__ == "__main__":
    unittest.main()
