# Week 1 companion presentation

Open [index.html](index.html) directly in a browser or through the repository’s
local HTTP server. This is a 29-slide browser presentation with editable HTML,
CSS, and JavaScript. A PowerPoint/PPTX file is not included.

The central question is **How does a biological sample become information we can
trust?** A fictional case follows two tubes of cultured eukaryotic cells: one
untreated and one exposed to a changed growth condition. Slower growth in Tube B
is a teaching premise, not a measured result from a supplied dataset. The story
keeps sequence differences, expression changes, and protein behavior as possible
questions rather than assuming a DNA change explains the response.

The recurring journey cue matches the [companion lesson](../../weeks/week-01.html):
Sample, Molecules, Measurement, Reads, Interpretation. The shared prediction uses
two independent toy observations unrelated to the tubes. Both called sequences
are `ACGTACGT`. Read 1 has qualities `IIIIIIII`; Read 2 has `IIII55++`.
Numerical quality information appears before the character encoding.

Slides 9, 15, and 26 have prominent **Try it** links that open the translator,
nanopore simulation, and FASTQ inspector inside the presentation. **Back to
slide** returns to the same slide; closing an experiment resets it. A separate-tab
link is available in each activity window. Slide 23 has a live Phred slider,
with Q = −10 log₁₀(p_error) and p_error = 10^(−Q/10).

Slide 13 compares Illumina short-read NGS, Oxford Nanopore, and PacBio HiFi:
measurement principles, illustrative read lengths, paired reads, and circular
consensus. Sources are in its notes and the companion lesson.

Slides 10, 13, 18, and 27 link to the lesson’s cell-response prediction, signal
experiment, measurement chooser, and read-retention control. Each opens in a
separate tab so the deck keeps its place. Use these within the existing
activity times, then return to the deck.

## Sequencing slides

- **11:** Define DNA sequencing and distinguish physical DNA, signals, and reads.
- **12:** Prepare a library; trace adapters, optional PCR, and paired reads.
- **13:** Compare Illumina, Oxford Nanopore, and PacBio HiFi.
- **14:** Examine how a nanopore measures current and software calls bases.
- **15:** Keep DNA fixed and test how added noise changes the reported read.
- **16:** Use overlaps and context to discuss where reads belong.

## Timing

| Class block | Elapsed minutes | Slides |
|---|---:|---:|
| The case and central question | 00–15 | 1–4 |
| Biology and translation experiment | 15–60 | 5–10 |
| Sequencing introduction, preparation, sensors, and reads | 60–95 | 11–16 |
| Break | 95–105 | — |
| Interpretation and evidence comparison | 105–130 | 17–21 |
| Raw records and confidence | 130–165 | 22–27 |
| Recap and homework handoff | 165–180 | 28–29 |

The class lasts **180 minutes**, including the ten-minute break. Discussions and demonstrations occupy part of each block. The Colab notebook is
separate **60–90-minute homework**. Encoding details remain optional reference
material in the notes. Trimming implementation belongs to the homework.

## Class experiments

- **Library preparation and paired reads, 5 minutes:** slide 12 uses five minutes of the 35-minute measurement
  block. Trace added adapters and short-insert read-through, then optional PCR
  copies and two mates from the same fragment. Both mate outputs are 5′→3′ in
  opposite orientations. A 500 bp insert with two 150 bp reads can leave 200 bp
  unread; two mates are not guaranteed to be one continuous 300 bp sequence.
  Ask how many records result if three PCR copies each yield one pair: six
  records, one original fragment, one source culture, and no new biological
  replicates. Open [the preparation activity](../../weeks/week-01.html#library-prep)
  from slide 12. This is a short-read example, not a universal library protocol.
- **Translation, 10 minutes:** predict the coding DNA → RNA → protein relationship,
  then use the adapted original translator. Compare the silent-change and
  early-stop presets. The genetic-code figure supports lookup rather than
  memorization. Open [the translation lab](../../weeks/week-01.html#translation-lab)
  inside slide 9.
- **Nanopore, 10 minutes:** keep the template fixed, change noise, and compare
  signal and estimated calls in the adapted original simulation. Its currents
  and decoder are deliberately simplified. Open [the nanopore lab](../../weeks/week-01.html#nanopore-lab)
  inside slide 15.
- **Evidence, 5 minutes:** compare repeated measurements of one culture
  with independently grown cultures, then discuss a possible batch confound.
- **FASTQ, 5 minutes:** use the existing inspector for
  comparing even-confidence and weak-tail examples, alongside malformed-record
  validation. The [record lab](../../weeks/week-01.html#record-lab) remains linked from slide 26.

The activity windows retain the deck at its current position. A prediction precedes each
experiment, followed by a discussion of what the observation can establish.

## Opening the homework in Colab

Use **Open in Colab** on the last slide, save a copy, and run setup. The direct
link targets the notebook’s GitHub copy. If that copy is unavailable, download
`exercise.ipynb` from the lesson and upload it to Colab instead. The notebook
states its setup checks; use the supplied check before starting the tasks.
Colab normally needs internet and a Google sign-in.

## Presenting

- Right, Down, or Space: reveal the next part, then advance to the next slide.
- Left, Up, or Shift+Space: rewind a reveal, then return to the previous slide.
- Page Down / Page Up: skip directly to the next / previous slide.
- Home / End: first / last slide.
- R: replay the current slide’s reveals.
- N: show speaker notes and sources.
- ?: show keyboard help. Escape closes help or an activity window.
- A focused quality slider uses arrow keys without advancing the slide.
- Per-slide timing labels are omitted; the schedule remains in this guide and
  speaker notes. The homework duration remains visible. The break has no dedicated slide.
- The **Reveal** button provides the same incremental reveal without a keyboard.
- The **Fullscreen** button uses the browser fullscreen API when available.
- A URL fragment such as `#slide-19` opens a particular slide.

The 1280×720 canvas scales to the available screen. Controls sit outside it.
Text reveals reserve their space. Diagram reveals preserve the source aspect
ratio and keep the source credit visible. The live status region announces
revealed text and diagram captions. Unrevealed text stays outside keyboard and
assistive-technology navigation until revealed.

Without JavaScript, all slides, complete diagrams, and reveal text appear in
normal document order. Print also includes complete slides. Use **Print**, A4
landscape, and background graphics for one 16:9 slide per page. Speaker notes and
controls do not print. Closing print preview restores the active slide and its
reveal state.

## Editing and sources

Edit text and order in [index.html](index.html), appearance in
[slides.css](slides.css), and presentation behavior in [slides.js](slides.js).
Keep slide IDs unique. The counter adapts to the number of slide sections.

`data-steps` defines a slide’s reveal count. A text element’s `data-reveal`
selects the step when it appears. Figure `data-clips` and caption `data-captions`
contain vertical-bar-separated states, including the initial state. Source SVG
width and height attributes allow the script to fit an exact aspect-ratio image
box before clipping. Print shows complete figures and final captions.

Seven adapted course SVGs appear in the main deck, including the genetic-code
reference and the library-preparation diagram. Slide 12 now uses
`library-preparation.svg` (1100 × 560) in place of the workflow overview;
the fuller workflow remains in the student lesson. The new figure combines the
original adapter/insert design with the paired-end teaching idea, using explicit
not-to-scale drawings and no technology performance comparison. The Phred
encoding SVG is an optional reference link in slide 23’s notes. All retain relative links to
`diagrams/week-01/` and the repository’s [attribution notice](../../THIRD_PARTY_NOTICES.md).
The figures are teaching schematics. Sparse slide text carries the main point;
the lesson and notes provide further explanations and limits.

## Validation

Run `python3 scripts/check_pilot.py` for local links, fragments, duplicate IDs,
and JavaScript syntax, plus `node tests/test_week01_interactions.js` and
`node tests/test_week01_tools.js` for the existing calculation checks.

Chrome review covers the modified slide layouts, the Phred slider, embedded
translation and nanopore controls, the FASTQ inspector, and returning to the deck.
Print preview and fullscreen remain separate manual checks.
