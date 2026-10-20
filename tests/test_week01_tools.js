/* Verify the shipped browser calculation module against the practical dataset. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { parseFastq, trimRecord, summarize, pError } = require('../artifacts/week-01/fastq-core.js');
const close = (actual, expected) => assert.ok(Math.abs(actual - expected) < 1e-8, `${actual} != ${expected}`);

const toy = parseFastq('@toy_read_01\nACGTACGT\n+\nIIII55++\n')[0];
close(toy.expectedErrors, .2204);
const trimmed = trimRecord(toy, 20, 6);
assert.equal(trimmed.seq, 'ACGTAC');
assert.equal(trimmed.quality, 'IIII55');
close(trimmed.expectedErrors, .0204);
assert.equal(trimRecord(toy, 20, 7), null);
assert.equal(trimRecord(toy, 10, 8).seq.length, 8); // Q equal to threshold stays.
assert.equal(trimRecord(parseFastq('@internal\nACG\n+\nI!I')[0], 20, 1).seq, 'ACG');
assert.equal(trimRecord(parseFastq('@low\nAC\n+\n!!')[0], 20, 1), null);
assert.equal(summarize([]).expectedErrorsPer1000, null);
assert.deepEqual(parseFastq('@toy\r\nAC\r\n+\r\n@+\r\n')[0].qs, [31, 10]);
close(pError(30), .001);
assert.throws(() => parseFastq('@incomplete\nAC\n+\n'));
assert.throws(() => parseFastq('@bad\nAC\n+\nI\n'));

const source = path.join(__dirname, '../practicals/week-01/synthetic_reads.fastq');
const records = parseFastq(fs.readFileSync(source, 'utf8'));
const before = summarize(records);
const after = summarize(records.map(record => trimRecord(record, 20, 50)).filter(Boolean));
assert.equal(before.reads, 200);
assert.equal(before.bases, 16000);
assert.equal(after.reads, 160);
assert.equal(after.bases, 10599);
close(before.expectedErrors, 810.356334784294);
close(after.expectedErrors, 12.078297440835);
console.log('OK: toy, parser boundaries, trimming decisions, and browser/practical dataset agreement.');
