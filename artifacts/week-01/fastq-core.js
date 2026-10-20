/* Week 1 adaptation of bioinformatis-web's lecture-01/06-fastq-inspector.html.
 * Modified: strict modern four-line parser, multi-record support and expected errors.
 * Apache-2.0; see ../../third_party/bioinformatis-web-LICENSE. */
(function (root) {
  'use strict';
  function pError(q) { return Math.pow(10, -q / 10); }
  function parseFastq(text) {
    const lines = text.replace(/\r\n/g, '\n').split('\n');
    if (lines[lines.length - 1] === '') lines.pop();
    if (!lines.length || (lines.length === 1 && !lines[0])) throw new Error('Paste at least one four-line FASTQ record.');
    if (lines.length % 4 !== 0) {
      throw new Error(`Expected a multiple of 4 lines; found ${lines.length}. Record ${Math.floor(lines.length / 4) + 1} is incomplete. Check for missing lines or blank lines. This inspector does not accept wrapped records.`);
    }
    const records = [];
    for (let i = 0; i < lines.length; i += 4) {
      const [header, rawSequence, separator, quality] = lines.slice(i, i + 4);
      const prefix = `Record ${i / 4 + 1}, lines ${i + 1}–${i + 4}: `;
      if (!header.startsWith('@') || !header.slice(1).trim()) throw new Error(prefix + 'the first line must start with @ and contain a read identifier.');
      if (!separator.startsWith('+')) throw new Error(prefix + 'the third line must start with +.');
      // The optional + line repeats the original identifier and description exactly.
      if (separator.length > 1 && separator.slice(1) !== header.slice(1)) throw new Error(prefix + 'text after + must match the header text after @, or use a bare +.');
      if (!/^[ACGTN]+$/i.test(rawSequence)) throw new Error(prefix + 'sequence must contain A, C, G, T or N without spaces. Other IUPAC symbols are outside this teaching inspector’s scope.');
      if (rawSequence.length !== quality.length) throw new Error(prefix + `sequence has ${rawSequence.length} bases but quality has ${quality.length} characters; they must match.`);
      if (!/^[!-~]+$/.test(quality)) throw new Error(prefix + 'quality must use printable ASCII characters ! through ~ (Phred+33, Q0–93); spaces and tabs are invalid.');
      const qs = Array.from(quality, c => c.charCodeAt(0) - 33);
      const probabilities = qs.map(pError);
      records.push({ header: header.slice(1), seq: rawSequence.toUpperCase(), quality, qs, probabilities,
        expectedErrors: probabilities.reduce((sum, p) => sum + p, 0) });
    }
    return records;
  }
  function trimRecord(record, threshold = 20, minLength = 6) {
    if (!Number.isInteger(threshold) || threshold < 0 || threshold > 41) throw new Error('Threshold must be a whole number from 0 to 41.');
    if (!Number.isInteger(minLength) || minLength < 1 || minLength > 1000) throw new Error('Minimum length must be a whole number from 1 to 1000.');
    let end = record.qs.length;
    while (end > 0 && record.qs[end - 1] < threshold) end--;
    if (end < minLength) return null;
    const probabilities = record.probabilities.slice(0, end);
    return { ...record, seq: record.seq.slice(0, end), quality: record.quality.slice(0, end),
      qs: record.qs.slice(0, end), probabilities,
      expectedErrors: probabilities.reduce((sum, p) => sum + p, 0) };
  }
  function summarize(records) {
    const bases = records.reduce((sum, r) => sum + r.seq.length, 0);
    const expectedErrors = records.reduce((sum, r) => sum + r.expectedErrors, 0);
    return { reads: records.length, bases, expectedErrors,
      expectedErrorsPer1000: bases ? 1000 * expectedErrors / bases : null };
  }
  const api = { parseFastq, pError, trimRecord, summarize };
  root.Week1Fastq = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
