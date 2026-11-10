"""Render the notebook's actual browser plot for the lesson; matplotlib required."""

import contextlib
import io
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/etf-week04-matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from build_notebook import BROWSER, DATA, WINDOWS


def main():
    root = Path(__file__).resolve().parents[2]
    target = root / "diagrams/week-04/browser-preview.png"
    namespace = {"plt": plt}
    with contextlib.redirect_stdout(io.StringIO()):
        for source in (DATA, WINDOWS, BROWSER):
            exec(source, namespace)
    plt.gcf().savefig(target, dpi=150)
    plt.close("all")
    print(f"Wrote {target.relative_to(root)}")


if __name__ == "__main__":
    main()
