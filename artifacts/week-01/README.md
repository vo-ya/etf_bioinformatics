# Week 1 interactive inventory and source review

These activities are local HTML/JavaScript assets for the introductory
180-minute lesson. The two additions below each support a 10-minute
prediction → run → interpretation activity. They load only the shared local
`../_shared/artifact-theme.css` and `../_shared/resize.js`; external source
links are optional reading, not runtime dependencies. Both retain an Apache
source/modification notice and link to the preserved upstream license at
`third_party/bioinformatis-web-LICENSE`.

| File | Lesson anchor | Purpose |
|---|---|---|
| `01-dna-explorer.html` | Existing DNA exploration activity | Sequence representation and complementarity |
| `02-fastq-inspector.html` | Existing FASTQ activity | Measured letters and per-base confidence |
| `03-central-dogma.html` | `#translation-lab` | Coding DNA → RNA → amino-acid sequence; selected frame and stop signals |
| `04-nanopore-squiggle.html` | `#nanopore-lab` | Electrical signal → inferred letters; repeated context and noise |

## Coding DNA to amino acids

Adapted from the complete source
`bioinformatis-web/artifacts/lecture-01/02-central-dogma.html` after reviewing
its controls, genetic-code data, strand rendering, codon-table logic, and
playback implementation. The original silent sequence cleaning and timer
property assignment on an interval ID were replaced. The layout, standard-code
data, amino-acid color groups, and interactive synonymous-codon table were reused.

- Input is explicitly the **coding DNA strand, 5′→3′**. RNA matches that strand
  with T→U; the complementary template strand is described in the explanation.
- Frame +1/+2/+3 starts at DNA base 1/2/3. Incomplete trailing codons and skipped
  leading bases are visible. A frame not beginning with AUG is labelled
  hypothetical decoding, rather than a prediction of biological initiation.
- Decoding stops at the first in-frame stop. A stop adds **no amino acid**;
  downstream codons remain explicitly untranslated.
- This is a simplified decoding model. It does not model initiation, splicing,
  expression level, regulation, or protein function. AUG's initiation role is
  qualified; alternative genetic codes exist.
- Invalid input is preserved and reported, with playback disabled and stale
  output cleared. Accepted input is 3–90 uppercase A/C/G/T letters.
- Play, Pause, Step, Reset, labelled frame radios, and a speed slider support
  normal keyboard navigation. Status changes are announced using live regions.
  Reduced-motion preferences disable visual animations.

| Preset / setting | Expected result |
|---|---|
| Default `ATGGCTTTCTAA`, frame +1 | RNA `AUGGCUUUCUAA`; MAF (3 amino acids), then UAA stop |
| Synonymous `ATGGCCTTCTAA`, frame +1 | RNA `AUGGCCUUCUAA`; the same MAF, then stop |
| Early stop `ATGTAAGCTTTC`, frame +1 | M (1 amino acid), then UAA stop; downstream GCU/UUC are not decoded |
| Default, frame +2 | Hypothetical WLS, no full stop; 2 trailing bases remain |
| `ATGN`, lowercase, spaces, too short/long | Input remains unchanged; visible error and disabled playback |

The API `window.translationLab.decode(dna, frame=0)` returns RNA, complete
codons, the first stop index, the number of playback steps through that stop,
the decoded amino-acid string, and trailing-base count. The genetic-code table
is available as `window.translationLab.geneticCode` for cross-checks.

## Schematic nanopore signal

Adapted from the complete source
`bioinformatis-web/artifacts/lecture-01/05-nanopore-squiggle.html`, including
its signal map, basecaller, animation, input handling, diagram, and canvas.
The original layout and signal-to-call teaching idea were reused; the model,
context drawing, and controls were rewritten to avoid instrument-specific
claims and hidden fallback sequences.

- The five-base context, fixed movement, signal scale, and nearest-level decoder
  are **explicit teaching assumptions**, not universal nanopore properties.
  All levels and noise use arbitrary units, not real picoampere measurements.
- The original hashed level map had collisions that could produce incorrect
  toy calls even at zero noise. The replacement uses 1,024 unique invented
  levels; every isolated context is exactly recoverable at zero noise.
- Noise is reproducible. Changing noise clears the old run so results do not
  mix different settings. Repeated contexts share nominal levels; their noisy
  samples need not be flat or identical. The model does not infer real dwell
  time or run length and makes no claim about instrument accuracy.
- The highlighted context, last signal window, numeric table, and center call
  refer to the same step. Only complete windows are processed. The first and
  last two bases are outside the toy center-call coverage and stay dotted.
- Inputs shorter than five bases or containing unsupported characters remain
  visible with an error; no default DNA is silently substituted. The accepted
  range is 5–60 uppercase A/C/G/T letters.
- Native buttons/sliders support keyboard operation. Live status reports progress
  and completion, and a numeric table provides the signal values alongside the
  canvas. Playback and stepping disable correctly at the end.

For the default `GATTACAGATTACAGATTACAGA`, there are 19 complete windows.
At noise 0, the first context is `GATTA`, nominal and mean signal round to
90.792, and the toy center call is T. At noise 3, the same deterministic first
window has mean 91.680 and toy call C. These numbers are invented model outputs.
`ACGTA` has exactly one complete window; it ends with call G and disabled
Play/Step controls. In the long-A preset, consecutive `AAAAA` contexts share
one nominal level.

The API `window.nanoporeLab.windowResult(sequence, zeroBasedWindowIndex, noise)`
returns context, nominal level, eight samples, sample mean, center call, and
known simulated center truth. `nominal(kmer)` and `basecall(mean)` expose the
toy lookup for cross-checks; callers should use a valid five-base context.

## Review and verification

- Both inline scripts passed `node --check` after adaptation.
- The 64 codon assignments in the interactive and static SVG were checked
  against [NCBI's standard genetic code](https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi#SG1):
  61 amino-acid codons and three stops. The new SVG was parsed, rendered with
  `rsvg-convert`, and visually inspected on its explicit light background.
- Pure-function checks cover translation examples, first-stop termination,
  alternate frames, incomplete codons, and invalid inputs; nanopore checks
  cover all 1,024 unique levels, all zero-noise center calls, reproducible noise,
  and invalid sequence/window/noise inputs.
- Browser checks cover the default and early-stop translation, alternate-frame
  caveat, invalid input preservation, numeric signal table, keyboard stepping,
  and nanopore end-state controls. Shared local resources load correctly.
- Scientific scope was reviewed against the [Oxford Nanopore basecalling
  explanation](https://nanoporetech.com/platform/technology/basecalling) and
  [official context models](https://github.com/nanoporetech/kmer_models).

The related figure is `diagrams/week-01/genetic-code.svg` (viewBox 720 × 580),
adapted from `diagrams/lecture-01/04-genetic-code-table.svg`. See its figure
inventory for the rendering and layout corrections.
