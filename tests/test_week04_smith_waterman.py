"""Independent checks for the notebook's editable local-alignment simulator."""

import contextlib
import importlib.util
import io
import itertools
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

os.environ.setdefault("MPLCONFIGDIR", "/tmp/etf-week04-matplotlib")
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "practicals/week-04/smith_waterman_simulator.py"
spec = importlib.util.spec_from_file_location("sw_simulator", SOURCE)
sim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sim)
MATRIX = [[2 if i == j else -1 for j in range(4)] for i in range(4)]


def enumerate_local_scores(a, b, matrix, gap):
    """Enumerate alignment paths from every start, without a DP score table."""
    scores = {0}

    def walk(i, j, score):
        scores.add(score)
        if i < len(a) and j < len(b):
            walk(i + 1, j + 1, score + matrix["ACGT".index(a[i])]["ACGT".index(b[j])])
        if i < len(a):
            walk(i + 1, j, score + gap)
        if j < len(b):
            walk(i, j + 1, score + gap)

    for start_i in range(len(a)):
        for start_j in range(len(b)):
            walk(start_i, start_j, 0)
    return max(scores)


class SmithWatermanTests(unittest.TestCase):
    def verify_alignment(self, result):
        a, b = result["aligned_1"], result["aligned_2"]
        self.assertEqual(len(a), len(b))
        total = 0
        for x, y in zip(a, b):
            self.assertNotEqual((x, y), ("-", "-"))
            total += result["gap"] if "-" in (x, y) else result["matrix"]["ACGT".index(x)]["ACGT".index(y)]
        self.assertEqual(total, result["score"])
        for index, aligned in enumerate((a, b)):
            sequence = result[f"sequence_{index + 1}"]
            self.assertEqual(aligned.replace("-", ""), sequence[result["start"][index]:result["end"][index]])
        if result["score"]:
            self.assertEqual(result["path"][0], result["end"])
            self.assertEqual(result["path"][-1], result["start"])
            i, j = result["start"]
            self.assertEqual(result["table"][i][j], 0)
            for (i, j), (pi, pj) in zip(result["path"], result["path"][1:]):
                self.assertIn((i - pi, j - pj), ((1, 1), (1, 0), (0, 1)))
        else:
            self.assertEqual(result["path"], [])

    def test_default_worked_example_and_cell_candidates(self):
        result = sim.sw_align("TTACGTAA", "GGACGTCC", MATRIX, -2)
        self.assertEqual((result["aligned_1"], result["aligned_2"], result["score"]), ("ACGT", "ACGT", 8))
        self.assertEqual(result["start"], (2, 2))
        self.assertEqual(result["end"], (6, 6))
        self.assertEqual(sim.sw_cell(result, 4, 4), {"restart": 0, "diagonal": 4, "up": -2, "left": -2})
        self.verify_alignment(result)

    def test_exhaustive_short_examples_and_asymmetric_scores(self):
        sequences = ["".join(letters) for length in (1, 2, 3)
                     for letters in itertools.product("AC", repeat=length)]
        asymmetric = [[2, 4, -3, -3], [-5, 1, -3, -3], [-3, -3, 2, -3], [-3, -3, -3, 2]]
        for matrix, gap in ((MATRIX, -2), (MATRIX, -1), (asymmetric, -2), ([[-1] * 4 for _ in range(4)], -1)):
            for a, b in itertools.product(sequences, repeat=2):
                result = sim.sw_align(a, b, matrix, gap)
                self.assertEqual(result["score"], enumerate_local_scores(a, b, matrix, gap), (a, b, matrix, gap))
                self.verify_alignment(result)
        self.assertEqual(sim.sw_align("A", "C", asymmetric)["score"], 4)
        self.assertEqual(sim.sw_align("C", "A", asymmetric)["score"], 0)

    def test_gaps_ties_normalization_and_invalid_inputs(self):
        low_gap = sim.sw_align("ACGTT", "ACTT", MATRIX, -1)
        self.assertEqual((low_gap["aligned_1"], low_gap["aligned_2"], low_gap["score"]), ("ACGTT", "AC-TT", 7))
        high_gap = sim.sw_align("ACGTT", "ACTT", MATRIX, -3)
        self.assertEqual(high_gap["score"], 5)
        self.verify_alignment(high_gap)
        tied = sim.sw_align("aa", " a ", MATRIX)
        self.assertEqual(tied["end"], (1, 1))
        self.assertEqual(tied["sequence_1"], "AA")
        for a, b, matrix, gap in (("", "A", MATRIX, -2), ("AN", "A", MATRIX, -2),
                                  ("A C", "A", MATRIX, -2), ("A" * 31, "A", MATRIX, -2),
                                  ("A", "A", [[2]], -2), ("A", "A", [[1.5]*4]*4, -2),
                                  ("A", "A", MATRIX, 0), ("A", "A", MATRIX, -1.5)):
            with self.assertRaises(ValueError):
                sim.sw_align(a, b, matrix, gap)

    def test_partial_reveal_and_independent_notebook_section(self):
        result = sim.sw_align("AC", "AC", MATRIX)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            sim.sw_show(result, 0, plot=False)
        self.assertIn("Best score so far: 0", output.getvalue())
        self.assertIn("not been filled yet", output.getvalue())
        self.assertNotIn("Aligned 1:", output.getvalue())
        with self.assertRaises(ValueError):
            sim.sw_show(result, 5, plot=False)
        notebook = json.loads((ROOT / "practicals/week-04/exercise.ipynb").read_text())
        namespace = {}
        section = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"
                   and any(tag.startswith("smith-waterman-") for tag in cell["metadata"].get("tags", []))]
        self.assertEqual(len(section), 4)
        self.assertEqual(section[0]["metadata"]["cellView"], "form")
        with contextlib.redirect_stdout(io.StringIO()):
            for cell in section[:2]:
                exec(cell["source"], namespace)
            namespace["sw_show"] = lambda *args, **kwargs: None
            exec(section[2]["source"], namespace)
        self.assertEqual(namespace["sw_result"]["score"], 8)

    @unittest.skipUnless(importlib.util.find_spec("ipywidgets"), "Optional widgets unavailable")
    def test_widget_edits_recompute_scores_and_reset_bounds(self):
        with patch.object(sim, "sw_show", return_value=None), contextlib.redirect_stdout(io.StringIO()):
            controls = sim.sw_controls("ACGT", "ACGT", MATRIX, -2)
            controls["sequences"][0].value = "A"
            controls["sequences"][1].value = "C"
            controls["matrix"][0][1].value = 5
            controls["gap"].value = -3
            controls["run"].click()
            self.assertEqual(controls["state"]["result"]["score"], 5)
            self.assertEqual(controls["steps"].max, 1)
            self.assertEqual(controls["row"].max, 1)
            self.assertEqual(controls["column"].max, 1)
            controls["steps"].value = 0
            controls["sequences"][0].value = "N"
            controls["run"].click()
            self.assertIsNone(controls["state"]["result"])


if __name__ == "__main__":
    unittest.main()
