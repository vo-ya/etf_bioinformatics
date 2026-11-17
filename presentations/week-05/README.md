# Week 5 browser presentation

Open [index.html](index.html) in a browser. The deck has 40 slides, six original
SVG figures, answer reveals, speaker notes, keyboard navigation, fullscreen,
and print styling. It follows the course's existing 1280×720 browser format.
No PowerPoint file is included.

The 180-minute pacing, including a ten-minute break after slide 19, is in the
[teaching guide](../../teaching/week-05.html). Timing labels and the break are
kept out of the visible slides. The [exercise notebook](../../practicals/week-05/exercise.ipynb)
is separate 60–90-minute homework, with an optional likelihood extension.

Right/Down/Space reveals or advances; Left/Up reverses; Page Down/Page Up changes
slide directly; Home/End jumps; R replays reveals; N toggles notes; ? opens help.
Print styling reveals all answers. With JavaScript disabled, all slides appear
in document order. A fragment such as `#slide-23` opens that slide.

Edit `build_slides.py`, then run `python3 presentations/week-05/build_slides.py`.
The builder reuses the Week 3 control markup, while `slides.js` is a local copy
with the Week 5 title. `slides.css` imports the established Week 3 styling and
adds Week 5 layouts. Regenerating does not change previous decks.

Diagrams are built with `python3 diagrams/week-05/build_diagrams.py`.
The student guide, notebook, and slides share the same invented read counts,
thresholds, coverage profile, and coordinate examples. The three primary
references are linked in slide notes and the student guide. Source diagrams
from the original course were not copied.

Run `python3 scripts/check_pilot.py` for local HTML links and JavaScript syntax,
and `python3 -m unittest discover -s tests -p 'test_week05*.py'` for computational
and content-structure checks. These checks are distinct from browser rendering.

## Initial 36-slide validation — 16 November 2026

All 36 slides were rendered in headless Chrome and visually reviewed. Checks
found no content extending into the footer, missing images, or page errors.
Navigation, reveal accessibility state, notes, and help worked. The student
page had no horizontal overflow at a 390-pixel viewport. Chrome generated a
36-page print PDF; the deletion-evidence print page was visually checked.
Fullscreen and the hosted Colab UI were not tested. Seven Week 5 tests passed,
and both notebook schemas validated. The site checker passed for 25 HTML pages,
740 local links/fragments, and 28 JavaScript syntax checks.

## Live activities

Slides 12, 16, 20, 24, and 32 contain live pileup filtering, genotype likelihoods,
sequence rearrangements, coverage evidence, and a VCF index check. Predict
before changing a control. The same components appear in the student guide.
Each activity has reset controls and a static print/no-JavaScript fallback.
Sliders and selectors keep the deck from consuming their arrow keys.

The [student lesson](../../weeks/week-05.html) provides the full prose explanations
and worked calculations, with each activity placed after its related discussion.
It shares Week 3's illustrated header, sticky contents, mobile navigation,
section typography, and homework layout through the common lesson styles.
Edit that HTML for lesson text; `assets/week5-lesson.css` fits the Week 5 controls
within the shared layout without changing other weeks or the slides.
The activity builder replaces only the five `WEEK05 LAB` marker pairs in place;
keep those markers when editing so regeneration preserves the lesson structure.

Edit `labs_markup.py`, `assets/week5-core.js`, `assets/week5-interactions.js`,
and `assets/week5-interactions.css` (asset paths relative to the repository root).
Run both `python3 presentations/week-05/build_slides.py` and
`python3 presentations/week-05/build_labs.py` to regenerate their markup.
`node tests/test_week05_interactions.js` verifies model calculations, edge
cases, block conservation, and consistency with the notebook's Python data.

The interactive update passed Chrome checks for every preset, empty input,
feedback/reset behavior, slider keyboard focus, print fallback and restoration,
no-JavaScript output, and the guide at 390-pixel width. All five activities were
visually inspected. The model test also checks 1,323 count/error combinations
against direct likelihood calculations. The updated site check reports 25 HTML
pages, 748 local links/fragments, and 31 JavaScript syntax checks.

## BAM introduction

Slides 3–4 introduce SAM versus BAM, sorting and indexing, and a selected-field
SAM view of a BAM alignment. At POS=99, CIGAR=5M, SEQ=TCGAT, the G appears at
reference position 101. QUAL=DDDDD gives Q35 per base; MAPQ=60 concerns the
placement. M permits mismatches. This makes the optional Week 2 SAM/CIGAR
material available to the whole class before variant evidence is introduced.
The deck has 38 slides; the class remains 180 minutes.

The two BAM slides were visually checked in Chrome with their answers revealed.
Their coordinates, CIGAR consumption, and Phred+33 decoding were verified; all
five activities still appear at their updated slide numbers. Seven Python tests,
the interactive model checks, and the site checks pass (25 HTML pages, 749 local
links/fragments, and 31 JavaScript syntax checks).

## Mutation consequences

Slides 39–40 close the deck with silent (synonymous), missense, and nonsense
substitutions, then frameshift versus in-frame indels. The examples show mRNA
codons in the 5′→3′ direction using the standard genetic code. Notes also explain
stop-loss, splice-site, and regulatory consequences. The student guide includes
the same examples; the final teaching block includes six minutes for them within
the existing 180-minute class. Edit `build_slides.py` before regenerating.

The two closing slides were visually checked in Chromium, including the silent
answer reveal, final-slide navigation, and print layout. Both fit above their
footers, all 40 slides appear in print, and the student guide has no horizontal
overflow at 390 pixels. Seven Week 5 Python tests and the interactive model
checks passed; six BAM tests were skipped because pysam is unavailable. The
site checker passed for 25 HTML pages, 801 local links/fragments, and 31
JavaScript syntax checks.
