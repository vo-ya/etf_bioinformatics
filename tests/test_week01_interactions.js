'use strict';
const assert = require('node:assert/strict');
const { signalAt, retainedEvidence } = require('../assets/week1-interactions.js');
const near = (actual, expected) => assert.ok(Math.abs(actual - expected) < 1e-10, `${actual} != ${expected}`);
// A tied observation must not silently become a confident single-base call.
assert.equal(signalAt(0).call, 'A');
assert.equal(signalAt(59).call, 'A');
assert.equal(signalAt(60).call, null);
near(signalAt(60).gap, 0);
assert.equal(signalAt(61).call, 'C');
assert.equal(signalAt(100).call, 'C');
for (let value = 0; value <= 100; value++) {
  assert.ok(signalAt(value).intensities.every(n => n >= 0 && n <= 100));
}
// Average probabilities, not Q scores; removing all data has no mean quality.
near(retainedEvidence(8).meanError, .02755);
near(retainedEvidence(6).meanError, .0034);
near(retainedEvidence(4).meanError, .0001);
assert.equal(retainedEvidence(6).retainedPercent, 75);
assert.equal(retainedEvidence(0).meanError, null);
assert.equal(retainedEvidence(0).retainedPercent, 0);
for (const invalid of [-1, 9, 2.5, NaN]) assert.throws(() => retainedEvidence(invalid), RangeError);
assert.throws(() => signalAt(NaN), RangeError);
console.log('OK: signal ambiguity and call changes; retained-data tradeoff and empty-data handling.');
