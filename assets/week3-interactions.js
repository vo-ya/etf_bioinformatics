/* Week 3: exact overlaps and a finite ambiguity experiment. All data are synthetic. */
(function (root) {
  'use strict';
  function dna(value) {
    if (typeof value !== 'string' || !/^[ACGT]+$/.test(value)) throw new Error('Use nonempty uppercase A/C/G/T sequences.');
    return value;
  }
  function overlap(left, right) {
    dna(left); dna(right);
    for (let n = Math.min(left.length, right.length); n > 0; n--) {
      if (left.slice(-n) === right.slice(0, n)) return n;
    }
    return 0;
  }
  function join(left, right, minimum) {
    if (!Number.isInteger(minimum) || minimum < 1) throw new Error('The minimum overlap must be a positive integer.');
    const size = overlap(left, right);
    if (size < minimum) throw new Error('These fragments do not meet the minimum exact overlap.');
    return {size, sequence: left + right.slice(size)};
  }
  function spectrum(sequence, k) {
    dna(sequence);
    if (!Number.isInteger(k) || k < 1 || k > sequence.length) throw new Error('Choose a valid word length.');
    const counts = {};
    for (let i = 0; i <= sequence.length - k; i++) {
      const word = sequence.slice(i, i + k);
      counts[word] = (counts[word] || 0) + 1;
    }
    return counts;
  }
  const candidates = ['ATGATCAT', 'ATCATGAT'];
  function compareCandidates(k, extraRead = '') {
    if (extraRead) dna(extraRead);
    const counts = candidates.map(sequence => spectrum(sequence, k));
    const words = [...new Set(counts.flatMap(Object.keys))].sort();
    return {counts, words, same: words.every(word => (counts[0][word] || 0) === (counts[1][word] || 0)),
      supported: candidates.map(sequence => !extraRead || sequence.includes(extraRead))};
  }
  const api = {overlap, join, spectrum, compareCandidates, candidates};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof document === 'undefined') return;
  root.Week3Interactions = api;
  const $ = id => document.getElementById(id);
  let fragments = [], history = [];
  function renderOverlaps() {
    const selected = Number($('overlap-from').value) || 0;
    $('overlap-from').replaceChildren();
    fragments.forEach((fragment, i) => {
      const option = document.createElement('option');
      option.value = i; option.textContent = `${i + 1}: ${fragment}`;
      $('overlap-from').append(option);
    });
    $('overlap-from').value = String(Math.min(selected, Math.max(0, fragments.length - 1)));
    const from = Number($('overlap-from').value), min = Number($('overlap-min').value);
    $('overlap-min-value').textContent = min;
    $('overlap-fragments').textContent = fragments.map((s, i) => `${i + 1}: ${s}`).join('\n') || 'Load valid fragments to begin.';
    $('overlap-options').replaceChildren();
    const choices = fragments.map((sequence, to) => ({to, size: to === from ? 0 : overlap(fragments[from], sequence)}))
      .filter(choice => choice.size >= min).sort((a, b) => b.size - a.size || a.to - b.to);
    choices.forEach(choice => {
      const button = document.createElement('button'); button.type = 'button'; button.className = 'button';
      button.textContent = `Join ${from + 1} → ${choice.to + 1} · ${choice.size} bases`;
      button.addEventListener('click', () => {
        const left = fragments[from], right = fragments[choice.to], result = join(left, right, min);
        history.push(`${left} + ${right}: overlap ${result.size} → ${result.sequence}`);
        fragments = fragments.filter((_, i) => i !== from && i !== choice.to);
        fragments.unshift(result.sequence); $('overlap-from').value = '0'; renderOverlaps();
      });
      $('overlap-options').append(button);
    });
    const ties = choices.length && choices.filter(choice => choice.size === choices[0].size).length;
    $('overlap-result').textContent = fragments.length === 1
      ? 'One joined string remains. It is compatible with these merges; that alone does not establish the original genome.'
      : !fragments.length ? 'No active fragments.' : !choices.length
        ? 'No outgoing join meets this threshold. Try another starting fragment or inspect what evidence is missing.'
        : ties > 1 ? `${ties} choices tie for the longest outgoing overlap. Choose a hypothesis and inspect the consequence.`
          : `${choices.length} outgoing join(s) meet the threshold. Predict the result before choosing.`;
    $('overlap-history').textContent = history.join('\n') || 'No joins yet.';
  }
  function loadReads() {
    try {
      const reads = $('overlap-input').value.trim().split(/\r?\n/).map(s => s.trim());
      if (reads.length < 2 || reads.length > 6) throw new Error('Enter 2–6 fragments, one per line.');
      reads.forEach(s => {dna(s); if (s.length > 30) throw new Error('Keep each input fragment at 30 bases or fewer.');});
      fragments = reads; history = []; $('overlap-error').textContent = '';
      $('overlap-input').setAttribute('aria-invalid', 'false'); $('overlap-from').value = '0';
    } catch (error) {
      fragments = []; history = []; $('overlap-error').textContent = error.message;
      $('overlap-input').setAttribute('aria-invalid', 'true');
    }
    renderOverlaps();
  }
  if ($('overlap-form')) {
    $('overlap-controls').disabled = false;
    $('overlap-form').addEventListener('submit', event => {event.preventDefault(); loadReads();});
    $('overlap-from').addEventListener('change', renderOverlaps);
    $('overlap-min').addEventListener('input', renderOverlaps);
    document.querySelectorAll('[data-overlap-preset]').forEach(button => button.addEventListener('click', () => {
      $('overlap-input').value = button.dataset.overlapPreset === 'simple' ? 'ATGAC\nGACCT' : 'ATGA\nTGAC\nTGAT';
      $('overlap-min').value = '3'; loadReads();
    }));
    loadReads();
  }
  function renderRepeat() {
    const k = Number($('repeat-k').value), extra = $('repeat-long').checked ? 'GATC' : '';
    const state = compareCandidates(k, extra);
    $('repeat-k-value').textContent = k;
    $('repeat-counts').replaceChildren();
    state.words.forEach(word => {
      const row = document.createElement('tr');
      [word, state.counts[0][word] || 0, state.counts[1][word] || 0].forEach((value, index) => {
        const cell = document.createElement(index ? 'td' : 'th');
        if (!index) cell.scope = 'row'; cell.textContent = value; row.append(cell);
      });
      $('repeat-counts').append(row);
    });
    $('repeat-result').textContent = state.same
      ? `The complete ${k}-mer inventories, including counts, are identical. This evidence cannot choose between these two strings.`
      : `The complete ${k}-mer inventories differ. In this ideal experiment, observing these longer words can distinguish the two strings.`;
    $('repeat-evidence').textContent = extra
      ? 'The extra forward read GATC occurs at zero-based start 2 in candidate A and nowhere in candidate B. Assuming it is correctly measured from this target, it supports A over B. Other possible genomes have not been excluded.'
      : 'No longer read supplied. These are two candidate strings; the experiment does not enumerate every possible reconstruction.';
  }
  if ($('repeat-controls')) {
    $('repeat-controls').disabled = false;
    $('repeat-k').addEventListener('input', renderRepeat);
    $('repeat-long').addEventListener('change', renderRepeat); renderRepeat();
  }
})(typeof globalThis !== 'undefined' ? globalThis : this);
