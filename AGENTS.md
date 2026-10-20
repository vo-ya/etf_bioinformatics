# Course writing

For new or revised educational prose in this repository, apply the
`course-material-writing` skill. Use `clear-prose` for a general editorial pass.
The local skills are installed at:

- `/Users/vojislavvarjacic/.codex/skills/course-material-writing/SKILL.md`
- `/Users/vojislavvarjacic/.codex/skills/clear-prose/SKILL.md`

If these skills are unavailable in another checkout environment, follow the
rules below directly. These rules apply to course prose, not unrelated code work.

## Editorial rules

- Name concrete subjects in headings and explain the example's mechanism or calculation.
- Replace generic statements about evidence with the particular unresolved question and a useful next observation.
- Combine repeated disclaimers, but preserve scientific assumptions and distinctions that affect an answer.
- Keep technical terms consistent. Retain teaching questions, useful lists, and explicit misconception corrections.
- Keep editing history and review commentary out of student material and speaker notes. Retain source attribution.
- Treat the article's patterns as prompts for editorial judgment; do not apply a word blacklist or claim to detect authorship.

## Course constraints

The current course has ten weeks, with 180 minutes of class per week including
a ten-minute break. Colab homework is a separate 60–90 minutes. Follow later
user changes to these constraints. Existing Weeks 1–3 have 29-slide decks;
a prose edit should preserve their schedules and required/optional distinction.

Keep lessons, slides, teaching guides, diagrams, and notebook instructions
consistent. Edit notebook generators before rebuilding their outputs. For prose
changes, verify that examples, code cells, interactive controls, links, and Colab
metadata still work as intended. Use `python3 scripts/check_pilot.py` for HTML
link and JavaScript syntax checks. Distinguish these checks from browser testing.

Source: [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
The teaching and verification rules also reflect decisions made for this course.
