# Week 3 companion presentation

Open [index.html](index.html) directly in a browser or through the repository’s
local HTTP server. This is a 40-slide browser presentation with editable HTML,
CSS, and JavaScript. A PowerPoint/PPTX file is not included.

The central question is **What can short fragments support, and what remains
ambiguous?** The narrative connects read placement with de novo assembly,
sampling, overlaps, short-word graphs, and evaluation. The recurring cue marks
Reads, Coverage, Overlaps, Graphs, and Evidence.

The [companion lesson](../../weeks/week-03.html) contains three adapted original
tools, two inline investigations, and a staged branch-evidence discussion. Links in slide footers and notes open
another tab so the deck keeps its place.

## Instructor pacing

| Class block | Elapsed minutes | Slides |
|---|---:|---:|
| Mapping and assembly bridge | 00–15 | 1–3 |
| Coverage, sampling, and read length | 15–40 | 4–9 |
| Suffix-prefix overlaps and candidate checks | 40–75 | 10–15 |
| Break | 75–85 | No slide |
| k-mers, graph construction, and traversal | 85–125 | 16–27 |
| Repeats, data limits, and evaluation | 125–160 | 28–38 |
| Recap and homework handoff | 160–180 | 39–40 |

The class lasts **180 minutes**, including the ten-minute break. Its pauses
include predictions, discussion, and demonstrations. The **60–90-minute Colab
homework is separate**: about fifty minutes of core work plus ten to forty
minutes for setup and interpretation. It covers k-mer counts, a graph,
spelling a supplied node path, and N50.

The deck and its speaker notes have no timing labels or break slide.
The allocation above is an instructor reference; pause at a suitable transition.

## Investigations

- Slide 7 opens the [coverage lab](../../weeks/week-03.html#coverage-lab).
  Compare equal mean depth with different coverage breadth and sampling gaps.
- Slide 14 opens the [overlap lab](../../weeks/week-03.html#overlap-lab).
  Merge a clear suffix-prefix match, then preview tied local choices.
- Slide 23 opens the [graph lab](../../weeks/week-03.html#graph-lab).
  Extract short words, identify prefix/suffix nodes, and explain a path.
- Slide 29 opens the [repeat lab](../../weeks/week-03.html#repeat-lab).
  Compare two candidates with the same 3-mer inventory, then add longer context.
- Slide 30 opens the [branch evidence exercise](../../weeks/week-03.html#branch-lab).
  Compare the 12:3 read-record
  counts with contrasting follow-up evidence, then state the reconstruction goal.
- Slide 35 opens the [N50 lab](../../weeks/week-03.html#n50-lab).
  Calculate a contiguity summary and separate it from correctness evidence.

The core examples explicitly begin with forward, error-free reads. Missing
sampling, sequencing errors, repeats, and experimental uncertainty enter the
interpretation. A toy traversal is not a production genome assembly.

## Opening the homework in Colab

Use **Open in Colab** on slide 40, save a copy, and run setup. The direct link
points to the GitHub notebook. If the GitHub copy is unavailable, download
`exercise.ipynb` from the lesson and upload it to Colab instead. Use the supplied
setup check before beginning the tasks. Colab normally needs internet and a
Google sign-in; prepared local Jupyter is another option.

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
- A URL fragment such as `#slide-17` opens a particular slide.

The 1280×720 canvas scales to the screen. Controls stay outside it. Reveals keep
space reserved and leave source credits visible. The live status region
announces revealed text and diagram captions. Unrevealed text stays outside
keyboard and assistive-technology navigation until revealed.

Without JavaScript, all slides and complete content appear in document order.
Use **Print**, A4 landscape, and background graphics for one 16:9 slide per page.
Printing exposes all reveal content and complete diagrams; closing print preview
restores the current slide and reveal state. Notes and controls do not print.

## Editing and sources

Edit [index.html](index.html), [slides.css](slides.css), or [slides.js](slides.js).
Keep slide IDs unique. `data-steps` gives each slide’s reveal count, while
`data-reveal` marks text steps. `data-clips` and `data-captions` hold vertical-bar-
separated figure states and captions, including the initial state. SVG width and
height attributes preserve the source aspect ratio during diagram reveals.

Seven adapted teaching figures are reused from `diagrams/week-03/`.
Four additional original SVGs show per-position depth, fragment order, k-dependent
connectivity, and contigs versus scaffolds. See the repository’s [attribution notice](../../THIRD_PARTY_NOTICES.md). Notes
also link to the Velvet paper and NCBI assembly-statistics documentation.

The shared toy results are:

- Three length-4 reads across a length-12 target give 1× mean depth. Starts
  `[0,4,8]` cover 100% of positions; `[0,0,0]` cover one third.
- Reads `ATGAC` and `GACCT` overlap by `GAC`, length 3, and merge as `ATGACCT`.
  In the separate ambiguous set `ATGA,TGAC,TGAT`, two next joins tie at 3.
- `ATGACCT` has 3-mers `ATG,TGA,GAC,ACC,CCT`, with 2-mer node path
  `AT → TG → GA → AC → CC → CT`.
- The two reads contribute six observed 3-mer instances, including `GAC` twice.
  That support count does not establish two genomic copies.
- `ATGATCAT` and `ATCATGAT` have the same six 3-mers once each. Only the first
  contains `GATC`; their 4-mer inventories differ.
- The branch paths `AT→TG→GA→AA` and `AT→TC→CA→AA` spell `ATGAA` and
  `ATCAA`. Their toy 12:3 support counts are whole-path read records; molecular
  independence is initially unknown. The exercise supplies alternative evidence
  follow-ups, with no automatic majority or minority decision rule.
- Lengths `[8,7,5]` give total 20, N50 7, and L50 2. Lengths `[12,8]` also total
  20, with N50 12 and L50 1. Correctness is unknown from lengths alone.

## Validation status

Checks confirm 40 contiguous slide IDs, matching folios and ARIA labels, one main
heading per slide, valid JavaScript syntax, existing local files and lesson/lab
anchors, and exact source SVG aspect ratios. Independent calculations confirm
the coverage presets, overlap and k-mer examples, supplied path, repeat inventory,
and N50/L50 values. Additional checks cover the mixed-depth profile,
read-boundary artifacts, candidate substrings, k=4 versus k=5 connectivity,
the middle-base substitution, and N50 after removing a contig.

A Node DOM stub checked every reveal state, navigation, accessible hidden/inert
content, source-ratio image fitting, print preparation/restoration, notes, help,
and form-focus handling. These checks do not establish rendered appearance.

Chrome review covered navigation and reveals across all 40 slides, image
loading, and content bounds against the slide canvas and footer. Screenshots
were inspected for the twelve new slides, including their revealed answers.
Fullscreen and print preview were not tested during this revision.
