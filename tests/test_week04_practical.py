"""Check the beginner workshop's execution, calculations, and plotted coordinates."""

import builtins
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

os.environ.setdefault("MPLCONFIGDIR", "/tmp/etf-week04-matplotlib")
ROOT = Path(__file__).resolve().parents[1]
PRACTICAL = ROOT / "practicals/week-04"
spec = importlib.util.spec_from_file_location("week04_builder", PRACTICAL / "build_notebook.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class WorkshopTests(unittest.TestCase):
    def execute(self, notebook, *, no_plot=False):
        namespace = {}
        original_import = builtins.__import__

        def controlled_import(name, *args, **kwargs):
            if no_plot and (name == "matplotlib" or name.startswith("matplotlib.")):
                raise ImportError("Test the documented table fallback")
            return original_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=controlled_import), contextlib.redirect_stdout(io.StringIO()):
            for cell in notebook["cells"]:
                if cell["cell_type"] == "code":
                    exec(cell["source"], namespace)
        return namespace

    def test_both_delivered_notebooks_are_reproducible_and_run_without_plotting(self):
        for solution, name in ((False, "exercise"), (True, "solutions")):
            with self.subTest(edition=name):
                notebook = json.loads((PRACTICAL / f"{name}.ipynb").read_text())
                self.assertEqual(notebook, builder.build(solution))
                ids = [cell["id"] for cell in notebook["cells"]]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertTrue(notebook["metadata"]["colab"]["toc_visible"])
                ns = self.execute(notebook, no_plot=True)
                self.assertEqual(len(ns["reference"]), 60)
                self.assertEqual(ns["gc_values"], [0, 100, 40, 40, 60, 60])
                self.assertIsNone(ns["plt"])
                if solution:
                    self.assertEqual(ns["practice_gc"], 60)
                else:
                    self.assertNotIn("instructor-answer", [tag for cell in notebook["cells"] for tag in cell["metadata"].get("tags", [])])
                    self.assertNotIn("practice_gc", ns)

    def test_changed_window_size_uses_actual_width_and_reruns_cleanly(self):
        ns = {}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(builder.DATA, ns)
            for size in (1, 5, 7, 10, 20, 60, 100):
                source = builder.WINDOWS.replace("window_size = 10", f"window_size = {size}")
                exec(source, ns)
                first_run = (ns["starts"][:], ns["widths"][:], ns["gc_values"][:])
                exec(source, ns)
                self.assertEqual((ns["starts"], ns["widths"], ns["gc_values"]), first_run)
                self.assertEqual(sum(ns["widths"]), 60)
                # Independent per-base grouping; no string.count or slicing.
                groups = {}
                for position, base in enumerate(ns["reference"]):
                    groups.setdefault(position // size, []).append(base in "GC")
                expected = [100 * sum(group) / len(group) for group in groups.values()]
                self.assertEqual(ns["gc_values"], expected)
                weighted_gc = sum(width * value / 100 for width, value in zip(ns["widths"], ns["gc_values"]))
                self.assertAlmostEqual(weighted_gc, 30)
                if size == 7:
                    self.assertEqual(ns["widths"][-1], 4)

    def test_region_bounds_and_touching_feature_boundaries_without_plotting(self):
        ns = self.execute(builder.build(), no_plot=True)
        for start, stop in ((-1, 10), (0, 61), (20, 10), (0, 0), (1.5, 10), (False, 10)):
            with self.assertRaises(ValueError):
                ns["show_region"](start, stop)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            ns["show_region"](10, 40)
        self.assertIn("Toy feature A visible interval: 12 26", output.getvalue())
        self.assertIn("Toy feature B visible interval: 38 40", output.getvalue())
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            ns["show_region"](26, 38)
        self.assertNotIn("visible interval:", output.getvalue())

    @unittest.skipUnless(importlib.util.find_spec("matplotlib"), "Matplotlib unavailable; fallback covered separately")
    def test_actual_plot_uses_window_widths_and_shared_coordinates(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        try:
            with patch.object(plt, "show"):
                ns = self.execute(builder.build())
                for start, stop in ((0, 60), (10, 40), (26, 38)):
                    with contextlib.redirect_stdout(io.StringIO()):
                        ns["show_region"](start, stop)
                    top, bottom = plt.gcf().axes
                    self.assertEqual(top.get_xlim(), (start, stop))
                    self.assertEqual(bottom.get_xlim(), (start, stop))
                    self.assertEqual([bar.get_x() for bar in top.patches], ns["starts"])
                    self.assertEqual([bar.get_width() for bar in top.patches], ns["widths"])
                    self.assertEqual([bar.get_height() for bar in top.patches], ns["gc_values"])
                    for collection, bounds in zip(bottom.collections, ((12, 26), (38, 54))):
                        x = collection.get_paths()[0].vertices[:, 0]
                        self.assertEqual((min(x), max(x)), bounds)
                        self.assertTrue(collection.get_clip_on())
        finally:
            plt.close("all")


if __name__ == "__main__":
    unittest.main()
