"""Execute the delivered instructor notebook, not a parallel implementation."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PRACTICAL = ROOT / "practicals" / "week-01"


class WeekOneDeliveryTests(unittest.TestCase):
    def test_instructor_notebook_runs_without_optional_dependencies(self):
        notebook = json.loads((PRACTICAL / "solutions.ipynb").read_text())
        namespace = {}
        output = io.StringIO()
        original_import = __import__

        def no_matplotlib(name, *args, **kwargs):
            if name == "matplotlib" or name.startswith("matplotlib."):
                raise ImportError("Exercise must support the documented table fallback")
            return original_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=no_matplotlib), contextlib.redirect_stdout(output):
            for cell in notebook["cells"]:
                if cell["cell_type"] == "code":
                    exec(compile(cell["source"], "solutions.ipynb", "exec"), namespace)

        self.assertIn("matplotlib unavailable", output.getvalue())
        self.assertEqual(namespace["before"]["bases"], 16000)
        self.assertEqual(namespace["after"]["reads"], 160)
        self.assertEqual(namespace["after"]["bases"], 10599)
        self.assertAlmostEqual(namespace["before"]["expected_errors"], 810.356335, places=5)
        self.assertAlmostEqual(namespace["after"]["expected_errors"], 12.078297, places=5)
        self.assertEqual(namespace["observed_errors"](namespace["records"]), 751)
        self.assertEqual(namespace["observed_errors"](namespace["retained"]), 16)
        self.assertEqual(namespace["fastq_text"], (PRACTICAL / "synthetic_reads.fastq").read_text())

    def test_generator_matches_delivered_notebooks_and_separates_solutions(self):
        spec = importlib.util.spec_from_file_location("week01_builder", PRACTICAL / "build_notebook.py")
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        with contextlib.redirect_stdout(io.StringIO()):
            reference = builder.reference_namespace()
        for solution, filename in ((False, "exercise.ipynb"), (True, "solutions.ipynb")):
            notebook = json.loads((PRACTICAL / filename).read_text())
            self.assertEqual(builder.build(solution, reference), notebook)
            self.assertEqual(notebook["metadata"]["colab"]["provenance"], [])
            self.assertTrue(notebook["metadata"]["colab"]["toc_visible"])
            code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
            self.assertEqual(code_cells[0]["metadata"]["tags"], ["setup"])
            for cell in notebook["cells"]:
                if cell["metadata"].get("tags") in (["setup"], ["data"], ["reference-solution"]):
                    self.assertEqual(cell["metadata"]["cellView"], "form")
                    self.assertTrue(cell["source"].startswith("#@title"))
                    if cell["metadata"].get("tags") == ["reference-solution"]:
                        self.assertTrue(cell["metadata"]["jupyter"]["source_hidden"])
                else:
                    self.assertFalse(cell["metadata"])
        student = (PRACTICAL / "exercise.ipynb").read_text()
        self.assertIn("NotImplementedError", student)
        self.assertNotIn("Instructor answer key", student)
        cells = builder.build()["cells"]
        reference_cells = [cell for cell in cells if cell["metadata"].get("tags") == ["reference-solution"]]
        self.assertEqual(len(reference_cells), 4)
        self.assertNotIn(builder.TRIM_SOLUTION.strip(), "\n".join(
            cell["source"] for cell in cells if cell not in reference_cells))
        self.assertTrue(any(builder.TRIM_SOLUTION.strip() in cell["source"] for cell in reference_cells))


if __name__ == "__main__":
    unittest.main()
