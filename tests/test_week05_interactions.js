'use strict';
const assert=require('node:assert/strict');
const core=require('../assets/week5-core.js');
assert.deepEqual(['A','B','C','D'].map(s=>core.pileup(s,20,30).depth),[12,8,12,6]);
assert.equal(core.pileup('B',0,0).fraction,6/14);
assert.equal(core.pileup('B',20,30).fraction,0);
assert.equal(core.pileup('D',30,30).fraction,null);
assert.equal(core.pileup('C',20,30).reverse,0);
assert.equal(core.pileup('A',20,30).reverse,3);
for(let r=0;r<=20;r++)for(let a=0;a<=20;a++)for(const e of [.01,.1,.25]){
 const rows=core.likelihood(r,a,e);
 const direct=[e,.5,1-e].map(p=>((1-p)**r)*(p**a));
 rows.forEach((v,i)=>{
  assert.ok(Math.abs(v.score-Math.log10(direct[i]))<1e-10);
  assert.ok(Math.abs(v.relative-direct[i]/Math.max(...direct))<1e-10);
 });
}
assert.ok(core.likelihood(0,0,.01).every(r=>r.relative===1&&!r.best));
assert.equal(core.likelihood(8,0,.01).find(r=>r.best).gt,'0/0');
assert.equal(core.coverage('loss').ratio,.5);
assert.deepEqual(core.coverage('loss').depth,core.coverage('ambiguous').depth);
assert.notEqual(core.coverage('loss').evidence,core.coverage('ambiguous').evidence);
assert.equal(core.coverage('gain').ratio,1.5);
assert.equal(core.coverage('inversion').ratio,1);
const inv=core.changes.inversion.rows[0][1];assert.equal(inv,'A→ B→ D← C← E→');
// Reciprocal translocation conserves each region exactly once across derivatives.
const derivatives=core.changes.translocation.rows.slice(1).map(r=>r[1]).join(' ').split(' ');
assert.deepEqual(derivatives.sort(),'A→ B→ C→ D→ E→ X→ Y→ Z→'.split(' ').sort());
assert.equal(core.records.deletion.pos-1,500);
assert.equal(core.records.deletion.ref.slice(1),'T');
assert.equal(core.records.insertion.alt.slice(core.records.insertion.ref.length),'GG');
// Keep the browser presets aligned with the embedded Python notebook helpers.
const {execFileSync}=require('node:child_process');
const py=execFileSync('python3',['-c',`import importlib.util,json
s=importlib.util.spec_from_file_location('v','practicals/week-05/variant_examples.py')
v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
print(json.dumps({k:v.summarize(v.retain_reads(r)) for k,r in v.pileups.items()}))`],{cwd:require('node:path').resolve(__dirname,'..'),encoding:'utf8'});
for(const [site,result]of Object.entries(JSON.parse(py))){
 const js=core.pileup(site,20,30);assert.equal(js.depth,result.depth);assert.equal(js.fraction,result.alt_fraction);assert.equal(js.forward,result.alt_forward);assert.equal(js.reverse,result.alt_reverse);
}
console.log('Week 5 interactive models: filter boundaries, 1323 likelihood cases, coverage ambiguity, block conservation, VCF coordinates, and notebook consistency passed.');
