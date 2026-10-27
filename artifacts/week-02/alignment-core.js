/* Small exact teaching algorithms. DNA only; linear gap scores; no external services. */
(function (root) {
  'use strict';
  function dna(value, allowEmpty = false) {
    const sequence = value.trim().toUpperCase();
    if ((!sequence && !allowEmpty) || !/^[ACGT]*$/.test(sequence)) throw new Error('Use only A, C, G, and T; do not include spaces inside the sequence.');
    if (sequence.length > 60) throw new Error('Keep teaching sequences to 60 bases or fewer.');
    return sequence;
  }
  function exactMatches(reference, query) {
    const hits = [];
    if (!query.length) throw new Error('An empty query does not define a read to locate.');
    for (let i = 0; i <= reference.length - query.length; i++) if (reference.slice(i, i + query.length) === query) hits.push(i);
    return hits;
  }
  function reverseComplement(sequence) {
    const complement = { A: 'T', C: 'G', G: 'C', T: 'A' };
    return [...sequence].reverse().map(base => complement[base]).join('');
  }
  function scoreAlignment(a, b, match = 2, mismatch = -1, gap = -2) {
    if (a.length !== b.length || !/^[ACGT-]*$/.test(a + b)) throw new Error('Aligned rows must use A/C/G/T/-, and have equal length.');
    let score = 0;
    const columns = [];
    for (let i = 0; i < a.length; i++) {
      if (a[i] === '-' && b[i] === '-') throw new Error('A column cannot contain two gaps.');
      const value = a[i] === '-' || b[i] === '-' ? gap : a[i] === b[i] ? match : mismatch;
      columns.push(value); score += value;
    }
    return { score, columns };
  }
  function align(reference, query, mode = 'global', gap = -2) {
    if (!['global', 'local'].includes(mode) || !Number.isFinite(gap) || gap >= 0) throw new Error('Choose global or local alignment and a negative gap score.');
    const m = reference.length, n = query.length;
    const table = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
    if (mode === 'global') {
      for (let i = 1; i <= m; i++) table[i][0] = i * gap;
      for (let j = 1; j <= n; j++) table[0][j] = j * gap;
    }
    let best = 0, bestI = 0, bestJ = 0;
    for (let i = 1; i <= m; i++) for (let j = 1; j <= n; j++) {
      table[i][j] = Math.max(table[i - 1][j - 1] + (reference[i - 1] === query[j - 1] ? 2 : -1),
        table[i - 1][j] + gap, table[i][j - 1] + gap, mode === 'local' ? 0 : -Infinity);
      if (table[i][j] > best) { best = table[i][j]; bestI = i; bestJ = j; }
    }
    let i = mode === 'local' ? bestI : m, j = mode === 'local' ? bestJ : n;
    const end = [i, j], path = [[i, j]];
    let a = '', b = '';
    while (i > 0 || j > 0) {
      if (mode === 'local' && table[i][j] === 0) break;
      if (i > 0 && j > 0 && table[i][j] === table[i - 1][j - 1] + (reference[i - 1] === query[j - 1] ? 2 : -1)) {
        a = reference[--i] + a; b = query[--j] + b;
      } else if (i > 0 && table[i][j] === table[i - 1][j] + gap) {
        a = reference[--i] + a; b = '-' + b;
      } else { a = '-' + a; b = query[--j] + b; }
      path.push([i, j]);
    }
    const matches = [...a].filter((base, k) => base === b[k]).length;
    return { reference: a, query: b, score: mode === 'local' ? best : table[m][n], table, path,
      start: [i, j], end, identity: a.length ? 100 * matches / a.length : null,
      queryCoverage: n ? 100 * (end[1] - j) / n : 0 };
  }
  function sharedSeeds(query, subject, k) {
    if (!Number.isInteger(k) || k < 1) throw new Error('Seed length must be a positive whole number.');
    const seeds = new Set();
    for (let i = 0; i <= query.length - k; i++) {
      const seed = query.slice(i, i + k);
      if (subject.includes(seed)) seeds.add(seed);
    }
    return [...seeds];
  }
  const api = { dna, exactMatches, reverseComplement, scoreAlignment, align, sharedSeeds };
  root.Week2Alignment = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
