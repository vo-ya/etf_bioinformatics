'use strict';
const assert = require('node:assert/strict');
const {overlap,join,spectrum,compareCandidates} = require('../assets/week3-interactions.js');
const strings=[];
for(let length=1;length<=4;length++) for(let bits=0;bits<2**length;bits++) strings.push(Array.from({length},(_,i)=>'AC'[(bits>>i)&1]).join(''));
let comparisons=0;
for(const a of strings) for(const b of strings){
  const candidates=Array.from({length:Math.min(a.length,b.length)},(_,i)=>i+1).filter(n=>a.substring(a.length-n)===b.substring(0,n));
  const expected=Math.max(0,...candidates);
  assert.equal(overlap(a,b),expected);
  if(expected){const result=join(a,b,1);assert.equal(result.size,expected);assert.ok(result.sequence.startsWith(a));assert.ok(result.sequence.endsWith(b));assert.equal(result.sequence.length,a.length+b.length-expected);}
  else assert.throws(()=>join(a,b,1));
  comparisons++;
}
assert.deepEqual(join('ATGAC','GACCT',3),{size:3,sequence:'ATGACCT'});
assert.equal(overlap('ATGA','TGAC'),3);assert.equal(overlap('ATGA','TGAT'),3);
assert.throws(()=>join('ATGAC','GACCT',4));assert.throws(()=>overlap('ATN','ATG'));assert.throws(()=>join('A','A',0));
assert.deepEqual(spectrum('AAAAA',3),{AAA:3});assert.throws(()=>spectrum('ACG',4));
assert.deepEqual(spectrum('ATGACCT',3),{ATG:1,TGA:1,GAC:1,ACC:1,CCT:1});
for(const k of [2,3]) assert.equal(compareCandidates(k).same,true);
assert.equal(compareCandidates(4).same,false);assert.deepEqual(compareCandidates(3,'GATC').supported,[true,false]);
assert.deepEqual(compareCandidates(3,'CATG').supported,[false,true]);assert.deepEqual(compareCandidates(3,'AAAA').supported,[false,false]);
console.log(`Week3 inline calculations pass: ${comparisons} exhaustive small overlap pairs, join validation, repeated words, and ambiguity evidence.`);
