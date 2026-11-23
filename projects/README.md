# Bioinformatics project catalogue

Choose **one research project or one coding project** from the list below.
The project is worth **30% of the final grade** and is completed over
**six weeks**, with an expected investment of **about four hours per week:
24 hours total per student**. This includes reading, implementation or analysis,
checking results, writing, and preparing the final presentation or demonstration.

Organize your own time. There are **no weekly milestones, progress reports,
proposals, or interim submissions**. Submit the complete project at the end.
The instructor will announce the calendar deadline, submission location, and
whether teams are permitted.

Research projects require a comparison of published evidence and your own
explanation; **no programming deliverable is required**. Coding projects require
a working Python tool or analysis, tests, and a technical explanation; **no
separate literature-review assignment is required**. Coding assumes intermediate
Python: functions, lists and dictionaries, file input, debugging, and plotting.

[Research options](#research-projects) · [Coding options](#coding-projects) ·
[Four detailed briefs](#detailed-project-briefs) ·
[Final submission](#final-submission) ·
[Week 4 lesson](https://vo-ya.github.io/etf_bioinformatics/weeks/week-04.html)

## Research projects

| ID | Project | Question and intended work |
| --- | --- | --- |
| R1 | [Sequencing mechanisms for one task](#r1-sequencing-mechanisms-for-one-task) | Compare fluorescence and nanopore-current measurements, using two studies or benchmarks to explain their suitability for one defined sequencing task. |
| R2 | [Repeats and assembly ambiguity](#r2-repeats-and-assembly-ambiguity) | Explain a hand-worked repeat ambiguity and compare published evidence showing how a documented assembly problem was resolved. |
| R3 | Genome-browser evidence | Trace the origins of three tracks in one region and compare what their annotations and measurements support. |
| R4 | Protein-structure confidence | Compare two published examples to explain what confidence scores establish and what they leave unresolved about function. |
| R5 | Reference bias | Compare evidence from two studies showing how the chosen reference changes read placement or variant detection. |
| R6 | LLM claims and citations | Compare two published evaluations of biomedical answers and explain how they measure factual support and citation errors. |
| R7 | Evaluating biological LLMs | Compare two studies’ test sets and data-splitting methods, focusing on possible leakage and the generalization being tested. |

R1 and R2 have detailed briefs below. R3–R7 are alternatives using the same
research submission requirements: one focused question, a comparison of evidence,
and an original explanatory figure or worked example. Evaluate published findings;
you do not need to reproduce a computational pipeline or run an LLM.

## Coding projects

| ID | Project | Tool or analysis to build |
| --- | --- | --- |
| C1 | [Genome-region browser](#c1-genome-region-browser) | Load a small reference and annotations, navigate a region, and display GC and feature tracks on a shared coordinate axis. |
| C2 | [LLM question-answering with source checks](#c2-llm-question-answering-with-source-checks) | Retrieve relevant bioinformatics passages, generate answers with source IDs, and evaluate correctness, source support, and abstention. |
| C3 | DNA composition explorer | Load FASTA, compare GC windows and unknown-base handling, and export tested plots and tables. |
| C4 | Coverage simulator | Compare seeded read-sampling patterns using depth, breadth, and the longest uncovered interval. |
| C5 | Exact-match explorer | Display overlapping matches on both strands and test coordinates against hand-worked examples. |
| C6 | FASTQ quality report | Validate a small FASTQ subset and compare read retention under two quality-filtering rules. |
| C7 | LLM study-field extractor | Extract organism, method, and sample size from ten open abstracts into a table, testing against manual labels and preserving missing values. |

C1 and C2 have detailed briefs below. C3–C7 use the same coding submission
requirements: data handling, a meaningful comparison, automated checks, an exported
figure or table, and a reproducible run. A notebook interface or parameter cells
are sufficient. Reusing course code with attribution is allowed, but rerunning
the classroom example or changing its appearance alone is not a complete project.
For either LLM coding option, establish usable model access before committing to it.

## Detailed project briefs

### R1. Sequencing mechanisms for one task

**Question:** How do fluorescence and nanopore-current measurements differ, and
how do those differences matter for one chosen sequencing task?

Explain the physical signal, the base-calling step, and one source of uncertainty
for each technology. Choose one task, such as resolving a repeat or inspecting a
short sequence difference. Compare two published studies or technical benchmarks
that help answer that question.

Your evidence table should identify each study’s sample type, method and version,
reported metric, experimental conditions, and limitations. Explain when the
studies cannot be compared directly. Draw an original signal-to-sequence diagram
and work through one small uncertainty example.

Use at least six relevant sources, including two primary studies or technical
benchmark reports. Starting points are the
[Week 1 lesson](https://vo-ya.github.io/etf_bioinformatics/weeks/week-01.html),
[Illumina’s sequencing mechanism explanation](https://www.illumina.com/science/technology/next-generation-sequencing/sequencing-technology.html),
and [Oxford Nanopore’s technology explanation](https://nanoporetech.com/platform/technology).
Technology descriptions explain mechanisms; use the selected studies for
performance comparisons.

**Final result:** An illustrated 4–6-page comparative report, excluding references,
with a justified recommendation for the chosen task and an account of what remains
unresolved. Trace performance claims to their sources and distinguish raw-read
accuracy, consensus accuracy, and task-specific success.

**Scope:** Two technology families and one task. Instrument access, a market survey,
and a universal ranking of sequencers are outside the core.

### R2. Repeats and assembly ambiguity

**Question:** When do repeated sequences leave more than one reconstruction
possible, and what evidence resolved a documented example?

Construct a short repeat example with two reconstructions that share the same
short-word inventory. Show a longer observation that distinguishes them. Verify
the word counts by hand in a table, and draw your own sequence or graph diagram.

Then analyse one published assembly case. Identify the difficult sequence
structure, the observations used to resolve it, and how the authors evaluated the
result. Compare that account with a second primary study or technical analysis.
Explain why contiguity statistics alone cannot establish correctness.

Use at least six relevant sources, including two primary studies or technical
reports. Start with the
[Week 3 repeat example](https://vo-ya.github.io/etf_bioinformatics/weeks/week-03.html#repeat-lab)
and [The complete sequence of a human genome](https://doi.org/10.1126/science.abj6987).

**Final result:** An illustrated 4–6-page report, excluding references, linking the
hand-worked ambiguity to the published case, with an evidence table. Distinguish
what your toy example demonstrates from what the published experiments support.

**Scope:** One class of repeat ambiguity and one main case study. Reproducing a
whole-genome assembly pipeline is outside the core.

### C1. Genome-region browser

**Question:** How can a user inspect sequence composition and supplied annotations
within a selected reference region?

Build a Python notebook or small application that:

- Loads a small FASTA reference and a documented four-column BED subset:
  sequence ID, start, stop, and name.
- Displays an annotation track and a GC track on a shared coordinate axis, plus
  the selected DNA when the view is short.
- Supports region selection, zoom or pan, and feature-name lookup.
- Handles unknown sequence IDs, malformed records, invalid intervals, and regions
  without overlapping features with clear messages.
- Exports a labelled figure.

Keep the 60-base classroom example as a coordinate fixture. Demonstrate the final
browser on one small public reference region with matching annotations, recording
the source and assembly/version. Explain two views of that region and what their
scales allow the reader to see. Follow the
[BED coordinate definition](https://genome.ucsc.edu/FAQ/FAQformat.html#format1).

**Worked checks:** For the toy features A=[12,26) and B=[38,54), view 0:60 shows
both complete features; view 10:40 shows all of A and B’s 38:40 portion; view 26:38
shows neither. Test touching boundaries, overlapping features, invalid input,
file parsing, and matching axes. Document whether zoom crops existing GC bins or
recalculates them.

**Final result:** Runnable code, small reference/annotation fixtures, automated
tests, an exported figure, and a 2–3-page technical explanation. Include setup
instructions and a reproducible example run.

**Scope:** One reference region and two main tracks. You may reuse the supplied
renderer with attribution, but develop file loading, navigation, validation,
tests, and the documented region analysis. BAM support, extra tracks, and a
hosted website are optional extensions.

### C2. LLM question-answering with source checks

**Question:** Can a large language model answer questions from a small collection
of bioinformatics explanations and recognize when the collection lacks an answer?

Use one topic, such as sequence quality, alignment, or assembly. Load 10–15 short
passages from a local CSV or JSON file. Give each passage a stable ID and source;
use course explanations or openly licensed teaching text with attribution.

Implement keyword-based retrieval of up to three relevant passages. Pass the
question and retrieved passages to one existing LLM. Display the answer alongside
the retrieved text and cited passage IDs. Request an answer supported by those
passages or an explicit statement that the information is insufficient. Validate
that returned citation IDs exist, and export questions, retrieved IDs, answers,
and evaluation results.

**Data and evaluation:** Before tuning, write 12 questions with reference answers
and supporting passage IDs. Use four questions for development and keep eight
unchanged for evaluation, including two whose answers are absent from the
collection. Compare a retrieval-only display with the LLM answers. Report these
separately, using raw counts and denominators:

- Retrieval of the expected source.
- Answer correctness.
- Whether cited passages support the answer’s claims.
- Appropriate abstention when the passages lack an answer.

Inspect every evaluation answer and discuss at least two failures or difficult
questions. Test an empty question, an empty collection, no relevant passage, an
invalid citation ID, and a model error. A valid citation ID alone does not establish
that a claim is supported.

**Worked behavior:** Passage P01 says that ATGCGCAT contains four G/C bases out of
eight. “What is its GC percentage?” should produce 50% with P01 cited. “What
nanopore current does this sequence produce?” should produce an insufficient-
information response if no supplied passage reports a current.

Use a model that runs on available hardware or an instructor-provided endpoint.
The [Hugging Face chat-template guide](https://huggingface.co/docs/transformers/chat_templating)
and [text-generation guide](https://huggingface.co/docs/transformers/llm_tutorial)
describe one possible integration route.

**Final result:** A runnable Python notebook or small application with separate
loading, retrieval, model-call, and evaluation functions; the passages and question
set; automated tests; saved actual model outputs; an exported comparison table or
plot; and a 2–3-page report. Record the model/version, generation settings, prompt,
and run date. Saved outputs support replay of the submitted evaluation but do not
replace a working model integration.

**Scope:** One topic, one model, 10–15 passages, and 12 questions. Fine-tuning,
web crawling, a vector database, and deployment are outside the core. Comparing a
second retrieval method is an optional extension after the core works.

## Final submission

Submit the package for your chosen project type.

| Research project | Coding project |
| --- | --- |
| A focused 4–6-page report, excluding references. | Runnable Python code or a notebook and a 2–3-page technical report. |
| At least six relevant sources, including two primary studies or technical reports. | Small example data with provenance, setup/run instructions, and dependency versions. |
| An evidence table explaining source selection, differing conditions, and disagreements. | Automated tests, exported results, and a clean run that reproduces the submitted result. |
| An original explanatory figure or worked example. | Central operations organized into functions, with an explanation of the method, findings, and limitations. |
| An eight-minute research presentation, followed by questions. | An eight-minute demonstration, followed by questions. |

Slides are optional. Include source credits for reused text, code, data, and
figures. If working in an instructor-approved team, include a statement of
individual contributions. Be ready to explain a calculation, source comparison,
or design choice yourself.

Completing the core brief well is sufficient; optional extensions are not required
for full marks. The one-line alternatives use the same final requirements as the
detailed examples for their project type.
