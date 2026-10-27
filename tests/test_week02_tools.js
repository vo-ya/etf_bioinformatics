'use strict';
const assert = require('node:assert/strict');
const key = require('../practicals/week-02/expected_results.json');
const core = require('../artifacts/week-02/alignment-core.js');
assert.deepEqual(core.exactMatches(key.reference, 'ATGCCA'), key.exact_matches.repeated);
assert.deepEqual(core.exactMatches(key.reference, 'CCATGA'), key.exact_matches.unique);
assert.deepEqual(core.exactMatches('AAAAA', 'AAA'), [0,1,2]);
assert.deepEqual(core.exactMatches(key.reference, 'ATG'), [0,5,12]);
assert.throws(() => core.exactMatches('AAA', ''), /empty/);
assert.equal(core.reverseComplement('ATGCCA'), 'TGGCAT');
assert.equal(core.reverseComplement('ACGT'), 'ACGT');
assert.throws(() => core.dna('AC GT'), /only/);
for (const example of key.alignments) {
  const result = core.align(example.reference, example.read);
  assert.equal(result.score, example.score);
  assert.equal(result.reference, example.aligned_reference);
  assert.equal(result.query, example.aligned_read);
}
assert.deepEqual(core.align('AC', 'AG').table, key.score_table_AC_AG);
assert.equal(core.align('AA','A').query, '-A');
// Enumerate every legal alignment for tiny pairs without using a score table.
function exhaustive(a, b) {
  if (!a.length) return b.length ? -2*b.length : 0;
  if (!b.length) return -2*a.length;
  return Math.max((a[0] === b[0] ? 2 : -1) + exhaustive(a.slice(1), b.slice(1)),
    -2 + exhaustive(a.slice(1), b), -2 + exhaustive(a, b.slice(1)));
}
function words(max) {
  const result = ['']; let layer = [''];
  for (let n=1;n<=max;n++) {layer=layer.flatMap(s=>['A','C'].map(c=>s+c));result.push(...layer);}
  return result;
}
for (const a of words(3)) for (const b of words(3)) {
  const result=core.align(a,b);
  assert.equal(result.score,exhaustive(a,b));
  assert.equal(result.reference.replaceAll('-',''),a);
  assert.equal(result.query.replaceAll('-',''),b);
  assert.equal(core.scoreAlignment(result.reference,result.query).score,result.score);
}
for (const a of words(2)) for (const b of words(2)) {
  let best=0;
  for(let i=0;i<=a.length;i++) for(let j=i;j<=a.length;j++)
    for(let k=0;k<=b.length;k++) for(let l=k;l<=b.length;l++) best=Math.max(best,exhaustive(a.slice(i,j),b.slice(k,l)));
  const result=core.align(a,b,'local');
  assert.equal(result.score,best);
  assert.equal(core.scoreAlignment(result.reference,result.query).score,best);
  assert.equal(result.reference.replaceAll('-',''),a.slice(result.start[0],result.end[0]));
  assert.equal(result.query.replaceAll('-',''),b.slice(result.start[1],result.end[1]));
}
const global=core.align('TTACGTAA','GGACGTCC'), local=core.align('TTACGTAA','GGACGTCC','local');
assert.deepEqual([global.score,global.identity,global.queryCoverage],[4,50,100]);
assert.deepEqual([local.score,local.identity,local.queryCoverage],[8,100,50]);
assert.equal(core.align('AAA','CCC','local').identity,null);
assert.equal(core.scoreAlignment('ACGT','A-GT').score,4);
assert.equal(core.scoreAlignment('ACGT','AGT-').score,-2);
assert.throws(()=>core.scoreAlignment('A-','--'),/two gaps/);
assert.deepEqual(core.sharedSeeds('ACGTTGCA','ACATTACA',4),[]);
assert.ok(core.sharedSeeds('ACGTTGCA','ACATTACA',2).length);
const missed=core.align('ACATTACA','ACGTTGCA','local');
assert.deepEqual([missed.score,missed.identity,missed.queryCoverage],[10,75,100]);
const partial=core.align('GGGACGTTTT','ACGTTGCA','local');
assert.deepEqual([partial.score,partial.identity,partial.queryCoverage],[10,100,62.5]);
console.log('OK: browser/homework agreement, 225 global and 49 local oracle cases, coordinates, seed misses and coverage.');
