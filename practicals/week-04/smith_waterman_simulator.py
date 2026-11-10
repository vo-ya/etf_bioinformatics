"""Standalone teaching simulator; embedded into both generated Week 4 notebooks."""

from numbers import Integral


def sw_align(sequence_1, sequence_2, scoring_matrix, gap_score=-2):
    """Local DNA alignment with a 4x4 A/C/G/T matrix and a linear gap score."""
    alphabet = "ACGT"
    sequences = []
    for label, sequence in (("Sequence 1", sequence_1), ("Sequence 2", sequence_2)):
        if not isinstance(sequence, str):
            raise ValueError(label + " must be text")
        sequence = sequence.strip().upper()
        if not sequence or any(base not in alphabet for base in sequence):
            raise ValueError(label + ": use nonempty A/C/G/T text, with no internal spaces or gaps")
        if len(sequence) > 30:
            raise ValueError(label + ": use at most 30 bases so the table stays readable")
        sequences.append(sequence)
    if not isinstance(scoring_matrix, (list, tuple)) or len(scoring_matrix) != 4:
        raise ValueError("Supply four matrix rows in A, C, G, T order")
    matrix = []
    for row in scoring_matrix:
        if not isinstance(row, (list, tuple)) or len(row) != 4:
            raise ValueError("Each matrix row needs four scores in A, C, G, T order")
        if any(isinstance(value, bool) or not isinstance(value, Integral) for value in row):
            raise ValueError("Use integer substitution scores")
        matrix.append([int(value) for value in row])
    if isinstance(gap_score, bool) or not isinstance(gap_score, Integral) or gap_score >= 0:
        raise ValueError("Use a negative integer gap score, for example -2")
    gap_score = int(gap_score)
    a, b = sequences
    m, n = len(a), len(b)
    scores = {(x, y): matrix[i][j] for i, x in enumerate(alphabet)
              for j, y in enumerate(alphabet)}
    table = [[0] * (n + 1) for _ in range(m + 1)]
    moves = [["stop"] * (n + 1) for _ in range(m + 1)]
    best, endpoint = 0, (0, 0)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            diagonal = table[i - 1][j - 1] + scores[a[i - 1], b[j - 1]]
            up = table[i - 1][j] + gap_score
            left = table[i][j - 1] + gap_score
            value = max(0, diagonal, up, left)
            table[i][j] = value
            if value > 0:
                # Reproducible ties: diagonal, then up, then left.
                moves[i][j] = "diagonal" if value == diagonal else "up" if value == up else "left"
            if value > best:
                best, endpoint = value, (i, j)
    i, j = endpoint
    aligned_a, aligned_b = [], []
    path = [(i, j)] if best > 0 else []
    while table[i][j] > 0:
        move = moves[i][j]
        if move == "diagonal":
            aligned_a.append(a[i - 1]); aligned_b.append(b[j - 1])
            i -= 1; j -= 1
        elif move == "up":
            aligned_a.append(a[i - 1]); aligned_b.append("-")
            i -= 1
        else:
            aligned_a.append("-"); aligned_b.append(b[j - 1])
            j -= 1
        path.append((i, j))
    return {"sequence_1": a, "sequence_2": b, "matrix": matrix, "gap": gap_score,
            "table": table, "moves": moves, "score": best, "start": (i, j),
            "end": endpoint, "path": path,
            "aligned_1": "".join(reversed(aligned_a)),
            "aligned_2": "".join(reversed(aligned_b))}


def sw_cell(result, i, j):
    """Four candidate scores at a non-boundary cell; row = sequence 1."""
    a, b, table = result["sequence_1"], result["sequence_2"], result["table"]
    if (type(i) is not int or type(j) is not int or
            not 1 <= i <= len(a) or not 1 <= j <= len(b)):
        raise ValueError("Inspect a row/column between 1 and the corresponding sequence length")
    substitution = result["matrix"]["ACGT".index(a[i - 1])]["ACGT".index(b[j - 1])]
    return {"restart": 0, "diagonal": table[i - 1][j - 1] + substitution,
            "up": table[i - 1][j] + result["gap"],
            "left": table[i][j - 1] + result["gap"]}


def sw_show(result, cells_to_show=None, inspect=None, plot=True):
    """Reveal cells in row-major order; show traceback only on the complete table."""
    a, b, table = result["sequence_1"], result["sequence_2"], result["table"]
    m, n = len(a), len(b)
    total = m * n
    if cells_to_show is None:
        cells_to_show = total
    if type(cells_to_show) is not int or not 0 <= cells_to_show <= total:
        raise ValueError("cells_to_show must be None or an integer from 0 to " + str(total))
    i, j = (min(4, m), min(4, n)) if inspect is None else inspect
    candidates = sw_cell(result, i, j)

    def visible(row, column):
        return row == 0 or column == 0 or (row - 1) * n + column <= cells_to_show

    path = set(result["path"]) if cells_to_show == total else set()
    labels_x = ["0:∅"] + [str(k) + ":" + base for k, base in enumerate(b, 1)]
    labels_y = ["0:∅"] + [str(k) + ":" + base for k, base in enumerate(a, 1)]
    print("Sequence 1 (rows):", a)
    print("Sequence 2 (columns):", b)
    print("Substitution scores: rows and columns both use A, C, G, T")
    for base, row in zip("ACGT", result["matrix"]):
        print(base, row)
    print("Gap score per gap base:", result["gap"])
    print("Filled cells:", cells_to_show, "/", total, "(boundary zeros are already initialized)")
    printed = []
    for row in range(m + 1):
        values = []
        for column in range(n + 1):
            value = str(table[row][column]) if visible(row, column) else "·"
            values.append("[" + value + "]" if (row, column) in path else value)
        printed.append(values)
    width = max(5, max(len(value) for row in printed for value in row))
    print(" " * (width + 1) + " ".join(value.rjust(width) for value in labels_x))
    for label, row in zip(labels_y, printed):
        print(label.rjust(width) + " " + " ".join(value.rjust(width) for value in row))
    print("· = not filled yet; [score] = chosen traceback, including its zero-score stop")
    if visible(i, j):
        sub = result["matrix"]["ACGT".index(a[i - 1])]["ACGT".index(b[j - 1])]
        print("Inspect H[" + str(i) + "," + str(j) + "]: pair", a[i - 1], "/", b[j - 1])
        print("  restart: 0")
        print("  diagonal:", table[i - 1][j - 1], "+", sub, "=", candidates["diagonal"])
        print("  up:", table[i - 1][j], "+", result["gap"], "=", candidates["up"])
        print("  left:", table[i][j - 1], "+", result["gap"], "=", candidates["left"])
        print("  chosen:", table[i][j], "via", result["moves"][i][j])
    else:
        print("The inspected cell has not been filled yet.")
    if cells_to_show < total:
        current_best = max(table[row][column] for row in range(m + 1)
                           for column in range(n + 1) if visible(row, column))
        print("Best score so far:", current_best, "— finish filling to reveal the alignment.")
    elif result["score"] == 0:
        print("Best local score: 0. No positive-scoring local alignment under these settings.")
    else:
        print("Best local score:", result["score"])
        print("Sequence 1 interval [start, stop):", (result["start"][0], result["end"][0]))
        print("Sequence 2 interval [start, stop):", (result["start"][1], result["end"][1]))
        print("Aligned 1:", result["aligned_1"])
        print("           " + "".join("|" if x == y else " " if "-" in (x, y) else "."
                                      for x, y in zip(result["aligned_1"], result["aligned_2"])))
        print("Aligned 2:", result["aligned_2"])
        print("Traceback (row, column), maximum to zero:", result["path"])
        print("One optimal alignment is shown; ties may allow others.")
    if not plot:
        return None
    try:
        import matplotlib.pyplot as sw_plt
    except ImportError:
        print("Matplotlib unavailable; the table and traceback above are complete.")
        return None
    picture = [[table[row][column] if visible(row, column) else float("nan")
                for column in range(n + 1)] for row in range(m + 1)]
    figure, axis = sw_plt.subplots(figsize=(max(7, (n + 1) * 0.46), max(5, (m + 1) * 0.42)))
    highest = max(1, max(table[row][column] for row in range(m + 1)
                         for column in range(n + 1) if visible(row, column)))
    axis.imshow(picture, cmap="Blues", vmin=0, vmax=highest, interpolation="nearest")
    axis.set_facecolor("#eeeeee")
    for row in range(m + 1):
        for column in range(n + 1):
            filled = visible(row, column)
            color = "white" if filled and table[row][column] > highest * 0.6 else "black"
            axis.text(column, row, str(table[row][column]) if filled else "·",
                      ha="center", va="center", fontsize=9, color=color)
    if path:
        for (row, column), (previous_row, previous_column) in zip(result["path"], result["path"][1:]):
            axis.annotate("", xy=(previous_column, previous_row), xytext=(column, row),
                          arrowprops={"arrowstyle": "->", "color": "#c45100", "lw": 2})
    axis.scatter([j], [i], s=300, marker="s", facecolors="none", edgecolors="#a00080", linewidths=2)
    axis.set_xticks(range(n + 1)); axis.set_xticklabels(labels_x)
    axis.set_yticks(range(m + 1)); axis.set_yticklabels(labels_y)
    axis.set_xlabel("Sequence 2: column j (prefix length)")
    axis.set_ylabel("Sequence 1: row i (prefix length)")
    axis.set_title("Smith–Waterman: " + str(cells_to_show) + "/" + str(total) + " cells filled")
    figure.text(0.5, 0.01, "Orange arrows: traceback to zero · Purple square: inspected cell",
                ha="center", fontsize=9)
    figure.tight_layout(rect=(0, 0.04, 1, 1))
    sw_plt.show()
    return figure


def sw_controls(sequence_1, sequence_2, scoring_matrix, gap_score):
    """Optional widgets; editable settings plus sw_show work without this interface."""
    try:
        import ipywidgets as widgets
        from IPython.display import display, clear_output
    except ImportError:
        print("Widgets unavailable. Edit the settings cell and rerun its output instead.")
        return None
    fields = [widgets.Text(value=sequence_1, description="Sequence 1:"),
              widgets.Text(value=sequence_2, description="Sequence 2:")]
    entries = [[widgets.IntText(value=value, layout=widgets.Layout(width="85px"))
                for value in row] for row in scoring_matrix]
    gap = widgets.IntText(value=gap_score, description="Gap/base:")
    run = widgets.Button(description="Align / reset table", button_style="primary")
    steps = widgets.IntSlider(value=0, min=0, max=1, description="Filled cells:", continuous_update=False)
    row_control = widgets.BoundedIntText(value=1, min=1, max=30, description="Inspect row:")
    col_control = widgets.BoundedIntText(value=1, min=1, max=30, description="Inspect col:")
    output = widgets.Output()
    state = {"result": None, "busy": False}

    def redraw(change=None):
        if state["busy"] or state["result"] is None:
            return
        with output:
            clear_output(wait=True)
            figure = sw_show(state["result"], steps.value, (row_control.value, col_control.value))
            if figure is not None:
                import matplotlib.pyplot as sw_plt
                sw_plt.close(figure)

    def calculate(button=None):
        try:
            result = sw_align(fields[0].value, fields[1].value,
                              [[entry.value for entry in row] for row in entries], gap.value)
        except ValueError as error:
            state["result"] = None
            with output:
                clear_output(wait=True)
                print("Please fix the settings:", error)
            return
        state["busy"] = True
        state["result"] = result
        steps.max = len(result["sequence_1"]) * len(result["sequence_2"])
        steps.value = steps.max
        row_control.max = len(result["sequence_1"])
        col_control.max = len(result["sequence_2"])
        row_control.value = min(4, row_control.max)
        col_control.value = min(4, col_control.max)
        state["busy"] = False
        redraw()

    run.on_click(calculate)
    for control in (steps, row_control, col_control):
        control.observe(redraw, names="value")
    header = widgets.HBox([widgets.Label("row / col", layout=widgets.Layout(width="85px"))] +
                          [widgets.Label(base, layout=widgets.Layout(width="85px")) for base in "ACGT"])
    rows = [widgets.HBox([widgets.Label(base, layout=widgets.Layout(width="85px"))] + entries[index])
            for index, base in enumerate("ACGT")]
    display(widgets.VBox(fields + [header] + rows + [gap, run, steps, row_control, col_control, output]))
    calculate()
    return {"sequences": fields, "matrix": entries, "gap": gap, "run": run,
            "steps": steps, "row": row_control, "column": col_control, "state": state}
