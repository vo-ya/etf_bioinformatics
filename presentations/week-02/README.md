# Week 2 companion presentation

Open [index.html](index.html) directly in a browser or through the repository’s
local HTTP server. This is a 32-slide browser presentation with editable HTML,
CSS, and JavaScript. A PowerPoint/PPTX file is not included.

The central question is **Where does this sequence belong, and how much can a
match tell us?** The narrative connects Week 1 confidence estimates with
placement ambiguity, scoring, alignment objectives, and database search.
The recurring cue marks Quality, Placement, Scoring, Alignment, and Search.

The [companion lesson](../../weeks/week-02.html) contains the explanations and
four inline labs and three adapted original tools. Lab links in slide footers and notes open another tab,
so the deck stays on the current slide.

## Instructor timing

The deck and notebooks omit timing labels. The pacing guide below remains
for instructor planning; the break has no dedicated slide.

| Class block | Elapsed minutes | Slides |
|---|---:|---:|
| Homework bridge: confidence and placement | 00–15 | 1–3 |
| Exact matches, strand, and stepwise scanning | 15–50 | 4–8 |
| Mismatches, gaps, and scoring | 50–75 | 9–13 |
| Break | 75–85 | No slide |
| Global/local alignment, fill, and traceback | 85–120 | 14–21 |
| Database search, search space, and interpretation | 120–160 | 22–30 |
| Recap and homework handoff | 160–180 | 31–32 |

Slides 16, 18, and 23 explain fitting a whole read, one global DP cell,
and the cost of full-table alignment versus candidate windows. In the 35-minute
alignment block, allow 5 minutes for global/local scope, 4 for fitting, 3 for
DP moves, 5 for the worked cell, 10 for the traceback animator, 6 for the
alignment lab, and 2 for the homework connection. In the search block, the
three-minute cost calculation sits between mapping/search (2 minutes) and
seed intuition (2 minutes); the search lab (10), hit interpretation (8),
function discussion (5), and E-value explorer (10) complete the 40 minutes.

The class lasts **180 minutes**, including the ten-minute break. It includes predictions, discussion, and lab demonstrations. The
**60–90-minute Colab homework is separate**. It covers all overlapping exact
matches, aligned-pair scoring, a scaffolded global-alignment table with supplied
traceback, and three interpretation sentences. BWT/FM-index internals and a full
BLAST implementation are outside this lesson.

## Added class experiments

Three adapted upstream tools provide a ten-minute prediction → experiment →
interpretation activity each:

- Slide 6 opens the [stepwise exact scanner](../../weeks/week-02.html#scan-lab).
  Compare letter comparisons and candidate starts, with and without early exit
  after a mismatch. Continue scanning to retain every exact match.
- Slide 20 opens the [fill-and-traceback lab](../../weeks/week-02.html#traceback-lab).
  Explain one local-alignment cell, then follow one optimal traceback to zero.
  A displayed path can be one of several tied paths.
- Slide 29 opens the [E-value explorer](../../weeks/week-02.html#evalue-lab).
  Hold score and query size fixed, enlarge the synthetic effective database,
  and interpret the increased expected chance-hit count. The search-space figure
  supports this concept. No formula or universal significance cutoff is required.

All open another tab. The original four lesson labs remain linked as well.
These activities use upstream tools to expose the reasoning behind the result.
They do not run production mapping or BLAST pipelines.

Slide 28 illustrates query coverage (6/12 = 50%) and two read placements with
the same average depth (12/12 = 1×), but different reference breadth (100%
versus 33.3%). Use it within the existing hit-interpretation discussion.

## Optional CIGAR reading

Slide 20 includes a link to the [CIGAR worked example](../../weeks/week-02.html#cigar-reference), connecting traceback to a stored alignment and later pileup. It is **5–8 minutes beyond the 180-minute core**, not an additional slide or required lab. The deck remains **32 slides**. Its separate example `4=1X2=2D3=1I3=` consumes 14 query bases and 15 reference bases; I/D are relative to the reference and M does not distinguish matches from mismatches. The lesson provides a native prediction/reveal answer, selected stored fields, and a primary SAM-specification link.

## Opening the homework in Colab

Use **Open in Colab** on the last slide, save a copy, and run setup. The direct
link targets the notebook’s GitHub copy. If that copy is unavailable, download
`exercise.ipynb` from the lesson and upload it to Colab instead. The notebook
states its setup checks; use the supplied check before starting the tasks.
Colab normally needs internet and a Google sign-in.

## Presenting

- Right, Down, or Space: reveal the next part, then advance.
- Left, Up, or Shift+Space: rewind a reveal, then return to the previous slide.
- Page Down / Page Up: next / previous slide without stepping through reveals.
- Home / End: first / last slide.
- R: replay the current slide’s reveals.
- N: speaker notes and sources.
- ?: keyboard help. Escape closes help.
- **Reveal** provides the same incremental reveal by button.
- **Fullscreen** uses the browser fullscreen API when available.
- A URL fragment such as `#slide-15` opens a particular slide.

The 1280×720 slide canvas scales to the screen. Controls remain outside it.
Reveals preserve space and keep source credits visible. The live status region
announces revealed text and diagram captions. Unrevealed text stays outside
keyboard and assistive-technology navigation until revealed.

Without JavaScript, all slides and complete content appear in document order.
Use **Print**, A4 landscape, and background graphics for one 16:9 slide per page.
Printing exposes all reveal content and complete diagrams; closing print preview
restores the current slide and its reveal state. Notes and controls do not print.

## Editing and sources

Edit [index.html](index.html), [slides.css](slides.css), or [slides.js](slides.js).
Keep slide IDs unique. `data-steps` gives a slide’s reveal count; `data-reveal`
marks text reveal steps. `data-clips` and `data-captions` provide vertical-bar-
separated figure states and captions, including the initial state. Source image
width and height attributes preserve the actual SVG aspect ratio when clipping.

Six corrected source-course diagrams and the new coverage comparison come from
`diagrams/week-02/`.
See the repository’s [attribution notice](../../THIRD_PARTY_NOTICES.md).
The sliding-search and matrix figures use separate, explicitly identified source
examples. They do not replace the shared lesson examples:

- Reference `ATGCCATGACCTATGCCA`: `ATGCCA` starts at 0 and 12; `CCATGA` at 3.
- `ACGT / A-GT` scores 4 under match +2, mismatch −1, gap base −2.
  `ACGT / AGT-` scores −2.
- `TTACGTAA` versus `GGACGTCC` has optimal global score 4 and local score 8.
- `ACGTTGCA` and `ACATTACA` share no exact 4-mer; their directly aligned pair
  still has score 10 under the teaching rule.

The classroom seed search is a teaching model, not BLAST. The search-hit figure
is a synthetic protein example with 90% identity across 50% query coverage. It
fabricates no numerical E-value or bit score. E-value interpretation uses the
NCBI sources linked in slide notes. No real BLAST result is invented.

## Validation status

Checks confirm 32 slides, unique IDs, one main heading per slide, valid JavaScript
syntax, existing local files and lesson/lab anchors, and SVG dimensions matching
the source viewBoxes. Independent calculations confirm the stated placements,
scoring examples, global/local optima, and the seed-miss example.

A Node DOM stub checked reveal/rewind/replay, hidden/inert accessibility state,
aspect-ratio image fitting, print preparation/restoration, navigation, notes,
help, and form-focus handling.

Slides 16, 18, and 23 were visually checked in Chrome, including their reveals,
with forward navigation and reveal rewind checked around slide 23. The read
and reference letters on slide 16 align in the displayed sequence. Fullscreen
and print-preview appearance remain unverified; review those in the classroom
browser before projection.

Slide 28 was visually checked in Chrome, with navigation to slide 29 verified.
Its read placements, depth-bar heights, numeric depths, and mean calculations
were checked against the synthetic start positions.
