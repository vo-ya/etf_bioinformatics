/* Four classroom investigations; static worked examples remain available without JS. */
(() => {
  'use strict';
  const core = window.Week2Alignment;
  const byId = id => document.getElementById(id);
  const pct = value => value === null ? '—' : `${Number(value.toFixed(1))}%`;
  const matchLine = (a, b) => [...a].map((base, i) => base === b[i] ? '|' : base === '-' || b[i] === '-' ? ' ' : '.').join('');
  const format = result => `${result.reference}\n${matchLine(result.reference, result.query)}\n${result.query}`;

  const form = byId('placement-form');
  function placeRead() {
    try {
      const reference = core.dna(byId('placement-reference').value);
      const query = core.dna(byId('placement-query').value);
      const orientations = [{ strand: '+', query }];
      if (byId('placement-reverse').checked) orientations.push({ strand: '−', query: core.reverseComplement(query) });
      const hits = orientations.flatMap(orientation => core.exactMatches(reference, orientation.query)
        .map(start => ({ ...orientation, start })));
      const positions = new Set(hits.map(hit => hit.start));
      const palindrome = orientations.length === 2 && orientations[0].query === orientations[1].query;
      byId('placement-result').textContent = hits.length
        ? `${positions.size} distinct start position${positions.size === 1 ? '' : 's'}: ${[...positions].sort((a,b) => a-b).join(', ')}. ${hits.length} strand-labelled match${hits.length === 1 ? '' : 'es'}.${palindrome ? ' This query equals its reverse complement, so the strand cannot be distinguished by its sequence.' : ''}`
        : 'No exact match in the searched orientation(s). A mismatch, gap, missing reference region, or different orientation could matter; no exact match does not prove no relationship.';
      const output = document.createElement('pre');
      output.textContent = `Reference  ${reference}\n` + hits.map(hit => `${String(hit.start).padStart(3)} ${hit.strand}      ${' '.repeat(hit.start)}${hit.query}`).join('\n');
      byId('placement-output').replaceChildren(output);
    } catch (error) {
      byId('placement-result').textContent = error.message;
      byId('placement-output').textContent = 'Correct the entry, then search again.';
    }
  }
  form.querySelector('button').disabled = false;
  form.addEventListener('submit', event => { event.preventDefault(); placeRead(); });
  byId('placement-reverse').addEventListener('change', placeRead);
  document.querySelectorAll('[data-read]').forEach(button => {
    button.disabled = false;
    button.addEventListener('click', () => { byId('placement-query').value = button.dataset.read; placeRead(); });
  });
  placeRead();

  function scoreGap() {
    const position = Number(byId('gap-position').value);
    const cost = Number(byId('gap-cost').value);
    const read = 'AGT'.slice(0, position) + '-' + 'AGT'.slice(position);
    const result = core.scoreAlignment('ACGT', read, 2, -1, -cost);
    byId('gap-position-value').textContent = position;
    byId('gap-cost-value').textContent = cost;
    byId('gap-alignment').textContent = `ACGT\n${matchLine('ACGT', read)}\n${read}\nColumn scores: ${result.columns.map(v => v > 0 ? '+' + v : v).join('  ')}`;
    byId('gap-result').textContent = `Total score: ${result.score}. Match +2, mismatch −1, each gap column −${cost}.`;
    const gapped = core.scoreAlignment('A-CGT', 'AGC-T', 2, -1, -cost).score;
    byId('gap-tradeoff').textContent = `Ungapped candidate: 2. Gapped candidate: ${gapped}. ${gapped === 2 ? 'These candidates tie.' : gapped > 2 ? 'The gapped candidate scores higher.' : 'The ungapped candidate scores higher.'} A preferred candidate is an answer under this scoring model.`;
  }
  ['gap-position', 'gap-cost'].forEach(id => { byId(id).disabled = false; byId(id).addEventListener('input', scoreGap); });
  scoreGap();

  const examples = { region: ['TTACGTAA', 'GGACGTCC'], gap: ['ACGT', 'AGT'], none: ['AAA', 'CCC'] };
  let current;
  function explainCell(i, j, focus = false) {
    const { reference, query, mode, result } = current;
    const buttons = byId('alignment-matrix').querySelectorAll('button');
    buttons.forEach(button => {
      const active = Number(button.dataset.i) === i && Number(button.dataset.j) === j;
      button.tabIndex = active ? 0 : -1;
      button.setAttribute('aria-pressed', String(active));
      if (active && focus) button.focus();
    });
    let explanation;
    if (i === 0 || j === 0) explanation = mode === 'global'
      ? `Boundary cell (${i}, ${j}) = ${result.table[i][j]}. Aligning ${Math.max(i,j)} letters with an empty prefix requires that many gaps at −2 each.`
      : `Boundary cell (${i}, ${j}) = 0. Local alignment may start within the sequences, so these boundaries do not accumulate end-gap costs.`;
    else {
      const diagonal = result.table[i-1][j-1] + (reference[i-1] === query[j-1] ? 2 : -1);
      const above = result.table[i-1][j] - 2, left = result.table[i][j-1] - 2;
      explanation = `Cell (${i}, ${j}), reference ${reference[i-1]} / query ${query[j-1]}: diagonal ${diagonal}, above ${above}, left ${left}${mode === 'local' ? ', restart 0' : ''}. Maximum = ${result.table[i][j]}.`;
    }
    byId('cell-explanation').textContent = explanation;
  }
  function alignSequences() {
    const [reference, query] = examples[byId('alignment-example').value];
    const mode = byId('alignment-mode').value;
    const result = core.align(reference, query, mode);
    current = { reference, query, mode, result };
    byId('alignment-output').textContent = result.reference ? format(result) : '(No positive-scoring local alignment)';
    byId('alignment-result').textContent = `${mode === 'global' ? 'Global' : 'Local'} score ${result.score}; identity ${pct(result.identity)}; query coverage ${pct(result.queryCoverage)}. Reference [${result.start[0]}, ${result.end[0]}), query [${result.start[1]}, ${result.end[1]}): zero-based, end excluded. One optimum shown; ties are possible.`;
    const path = new Set(result.path.map(point => point.join(',')));
    // All interpolated symbols are fixed DNA examples or computed numbers.
    let table = '<table class="dp-table"><caption>Query prefixes across columns; reference prefixes down rows. Use arrow keys between cells.</caption><thead><tr><th scope="col">Ref / query</th>';
    for (const base of ['∅', ...query]) table += `<th scope="col">${base}</th>`;
    table += '</tr></thead><tbody>';
    result.table.forEach((row, i) => {
      table += `<tr><th scope="row">${i === 0 ? '∅' : reference[i-1]}</th>`;
      row.forEach((value, j) => {
        const onPath = path.has(`${i},${j}`);
        table += `<td><button type="button" data-i="${i}" data-j="${j}" tabindex="-1" aria-pressed="false" aria-label="Row ${i}, column ${j}, score ${value}${onPath ? ', traceback' : ''}" class="${onPath ? 'trace-cell' : ''}">${value}${onPath ? '<span aria-hidden="true"> ·</span>' : ''}</button></td>`;
      });
      table += '</tr>';
    });
    byId('alignment-matrix').innerHTML = table + '</tbody></table>';
    explainCell(Math.min(1, reference.length), Math.min(1, query.length));
  }
  ['alignment-example', 'alignment-mode'].forEach(id => { byId(id).disabled = false; byId(id).addEventListener('change', alignSequences); });
  byId('alignment-matrix').addEventListener('click', event => {
    const button = event.target.closest('button[data-i]');
    if (button) explainCell(Number(button.dataset.i), Number(button.dataset.j));
  });
  byId('alignment-matrix').addEventListener('keydown', event => {
    const button = event.target.closest('button[data-i]');
    if (!button) return;
    let i = Number(button.dataset.i), j = Number(button.dataset.j);
    if (event.key === 'ArrowLeft') j--; else if (event.key === 'ArrowRight') j++;
    else if (event.key === 'ArrowUp') i--; else if (event.key === 'ArrowDown') i++;
    else return;
    event.preventDefault();
    explainCell(Math.max(0, Math.min(current.reference.length, i)), Math.max(0, Math.min(current.query.length, j)), true);
  });
  alignSequences();

  const searchQuery = 'ACGTTGCA';
  const database = [
    { name: 'Exact', sequence: 'ACGTTGCA' }, { name: 'Near', sequence: 'ACGTCGCA' },
    { name: 'Interrupted', sequence: 'ACATTACA' }, { name: 'Short region', sequence: 'GGGACGTTTT' },
    { name: 'Repeated T', sequence: 'TTTTTTTT' }
  ];
  function search() {
    const k = Number(byId('seed-length').value), audit = byId('search-audit').checked;
    byId('seed-length-value').textContent = k;
    const results = database.map(candidate => ({ ...candidate,
      seeds: core.sharedSeeds(searchQuery, candidate.sequence, k),
      alignment: core.align(candidate.sequence, searchQuery, 'local') }));
    const passing = results.filter(result => result.seeds.length).length;
    byId('search-summary').textContent = `${passing} of ${database.length} candidates pass at k = ${k}. ${audit ? 'Audit shows exact local scores even for rejected candidates. Compare Interrupted with Short region.' : 'Rejected candidates are not reported as zero-score matches: their scores are hidden until you audit.'}`;
    const body = byId('search-results'); body.replaceChildren();
    results.forEach(result => {
      const row = document.createElement('tr');
      const inspected = audit || result.seeds.length > 0;
      [result.name + ': ' + result.sequence, result.seeds.length ? result.seeds.join(', ') : 'No seed',
        inspected ? result.alignment.score : 'Not examined', inspected ? pct(result.alignment.identity) : '—',
        inspected ? pct(result.alignment.queryCoverage) : '—'].forEach(value => {
        const cell = document.createElement('td'); cell.textContent = value; row.appendChild(cell);
      });
      const cell = document.createElement('td'), button = document.createElement('button');
      button.type = 'button'; button.className = 'button'; button.textContent = 'View';
      button.setAttribute('aria-label', `View ${result.name} alignment`); button.setAttribute('aria-controls', 'search-alignment'); button.disabled = !inspected;
      button.addEventListener('click', () => {
        byId('search-alignment').textContent = `${result.name}: subject / query\n${format(result.alignment)}\nScore ${result.alignment.score}; subject [${result.alignment.start[0]}, ${result.alignment.end[0]}), query [${result.alignment.start[1]}, ${result.alignment.end[1]}).`;
      });
      cell.appendChild(button); row.appendChild(cell); body.appendChild(row);
    });
    byId('search-alignment').textContent = 'Choose View to inspect an examined candidate. Coordinates use zero-based starts and exclude the end.';
  }
  ['seed-length', 'search-audit'].forEach(id => { byId(id).disabled = false; byId(id).addEventListener(id === 'seed-length' ? 'input' : 'change', search); });
  search();
})();
