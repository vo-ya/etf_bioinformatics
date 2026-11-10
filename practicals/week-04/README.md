# Week 4 guided Python workshop

This notebook is used **in class**, with a separate 60–90-minute consolidation
and personal project-planning task afterward. It introduces strings, assignment,
indexing, slicing, counts, arithmetic, loops, `range`, and lists in small steps.
Plotting is supplied; writing a function is not required. The optional
mini-browser renderer previews one possible project.

The notebook ends with an optional **Smith–Waterman dynamic-programming
simulator**. Students can edit two DNA sequences, every entry of a 4×4
substitution-score matrix, and a linear gap score. It displays the DP table,
the four candidates for a selected cell, and one optimal local alignment with
traceback and sequence intervals. Optional widgets add sequence fields, an
editable score grid, a fill-progress slider, and cell inspection. The settings
and calculation cells also work without widgets; a text table works without
matplotlib. This section can run independently of the earlier workshop cells.

Use 1–30 A/C/G/T bases and integer scores, with a negative score per gap base.
The default TTACGTAA / GGACGTCC example aligns ACGT / ACGT with score 8.
The simulator normalizes lowercase and surrounding whitespace, rejects
unsupported input, and documents deterministic tie choices. It uses linear
gaps and the supplied forward orientations. It adds no required class block.

The final project is a separate **six-week assessment worth 30% of the final
grade**, scoped for approximately **24 hours per student** (four hours per
week). Students submit the complete project at the end, with no weekly
milestones or interim submissions. Coding projects assume intermediate
Python and extend beyond the classroom examples. Research projects are a
separate choice, with a report and presentation and no programming deliverable. The project budget includes reading, development,
validation, reporting, and the final explanation. Personal planning time in
the workshop follow-up counts toward that budget.

- [Student notebook](exercise.ipynb)
- [Instructor notebook with answers](solutions.ipynb)
- [Student page: four full project examples and ten one-line ideas](../../weeks/week-04.html)
- [180-minute teaching plan](../../teaching/week-04.html)

Both editions run from an empty namespace. Student code examples are complete:
the learning tasks are small edits, predictions, explanations, and a final
three-line transfer task. Running the untouched notebook does not complete
those tasks. Unlike Weeks 1–3, this workshop has no `NotImplementedError`
stubs or reference cells that overwrite attempted functions.

All DNA and feature annotations are synthetic. The 60-base reference has
ten-base GC percentages `[0, 100, 40, 40, 60, 60]`. Twenty-base windows yield
`[50, 40, 60]`. Coordinates are zero-based with an excluded right boundary.
Features A `[12,26)` and B `[38,54)` are supplied independently of GC.

The calculation uses ordinary Python. Matplotlib draws the plots when
available, with printed data as a fallback; the lesson includes a saved plot.
No installs, analysis-time network requests, external files, or GPU are needed.
Colab itself requires internet. Download/upload the notebook if the direct
GitHub launch is not yet available. Save a copy before editing.

Edit [build_notebook.py](build_notebook.py), then regenerate:

The generator embeds [smith_waterman_simulator.py](smith_waterman_simulator.py)
into both notebooks; edit that source for simulator changes. Students do not
need the Python source file alongside the delivered notebook.

```sh
python3 practicals/week-04/build_notebook.py
python3 -m unittest discover -s tests -p 'test_week04*.py'
python3 practicals/week-04/render_preview.py
python3 scripts/check_pilot.py
```

Tests execute the student and instructor routes, check alternate window sizes
including a partial final window, rerunning without accumulating duplicate
results, plotting fallback, and shared-coordinate region bounds. Rendered
output and page layout require separate visual inspection. A local notebook
execution does not establish successful hosted Colab execution.

The simulator tests compare scores with independent exhaustive enumeration
of short alignments, rescore traceback output, and check asymmetric matrices,
ties, gaps, invalid input, partial table displays, standalone execution, and
widget callbacks. These are computational checks, not hosted Colab UI tests.

Validation on 5 November 2026: four workshop tests passed, both notebook
schemas validated, and the generated browser figure was visually inspected.
The site checker passed for 22 HTML pages, 636 local links/fragments, and 27
JavaScript syntax checks. The browser preview service was unavailable, so
the new HTML layout and hosted Colab workflow have not been visually tested.

Notebook packaging uses the course helper’s Apache-derived Colab form pattern;
the upstream license is retained in `LICENSE.upstream.txt`. Examples, exercise
text, and project briefs were authored for this course.
