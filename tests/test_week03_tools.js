'use strict';
const assert=require('node:assert/strict');
const core=require('../artifacts/week-03/assembly-core.js');
function near(a,b){assert(Math.abs(a-b)<1e-12,`${a} != ${b}`);}
// Independent depth examples: same measured total and mean, different observed breadth.
const spread=core.coverageFromStarts(12,4,[0,4,8]),cluster=core.coverageFromStarts(12,4,[0,0,0]);
assert.deepEqual(spread.depth,Array(12).fill(1));assert.deepEqual(cluster.depth,[3,3,3,3,0,0,0,0,0,0,0,0]);
near(spread.mean,1);near(cluster.mean,1);near(spread.breadth,1);near(cluster.breadth,1/3);
const seeded=core.simulateCoverage({genomeLength:80,readLength:20,readCount:12,seed:2027});
assert.deepEqual(seeded,core.simulateCoverage({genomeLength:80,readLength:20,readCount:12,seed:2027}));
assert.equal(seeded.depth.reduce((a,b)=>a+b,0),240);near(seeded.mean,3);
assert(seeded.starts.every(s=>s>=0&&s<=60));
// Exhaust all two-read draws in a tiny linear reference, independently counting uncovered bases.
let expected=0;for(let a=0;a<=2;a++)for(let b=0;b<=2;b++){const covered=new Set();for(const s of [a,b])for(let p=s;p<s+3;p++)covered.add(p);expected+=5-covered.size;}
near(core.simulateCoverage({genomeLength:5,readLength:3,readCount:2,seed:1}).expectedUncovered,expected/9);
assert.equal(core.simulateCoverage({genomeLength:5,readLength:5,readCount:1}).uncovered,0);
assert.equal(core.simulateCoverage({genomeLength:5,readLength:5,readCount:0}).expectedUncovered,5);
for(const bad of [()=>core.coverageFromStarts(12,4,[-1]),()=>core.coverageFromStarts(12,4,[9]),()=>core.simulateCoverage({genomeLength:12,readLength:13,readCount:3}),()=>core.simulateCoverage({readCount:1.5})])assert.throws(bad);
// Preserve read boundaries; repeated observations merge into support, not extra unique edges.
const graph=core.buildDeBruijn(['ATGAC','GACCT'],3);
assert.equal(graph.observationCount,6);assert.equal(graph.uniqueEdgeCount,5);assert.equal(graph.counts.GAC,2);
assert.deepEqual(graph.edges.map(e=>[e.kmer,e.from,e.to,e.support]),[['ATG','AT','TG',1],['TGA','TG','GA',1],['GAC','GA','AC',2],['ACC','AC','CC',1],['CCT','CC','CT',1]]);
let walk=core.startTraversal(graph,'AT');assert.throws(()=>core.stepTraversal(graph,walk,'GAC'));
for(const edge of ['ATG','TGA','GAC','ACC','CCT'])walk=core.stepTraversal(graph,walk,edge);
assert.equal(walk.spelled,'ATGACCT');assert(walk.complete);assert.throws(()=>core.stepTraversal(graph,walk,'ATG'));
const occurrence=core.buildDeBruijn(['ATGAC','GACCT'],3,{occurrenceEdges:true});
assert.equal(occurrence.edges.length,6);assert.equal(new Set(occurrence.edges.map(e=>e.id)).size,6);
assert.equal(occurrence.edges.filter(e=>e.kmer==='GAC').length,2);
const disconnected=core.buildDeBruijn(['ATGA','CCGT'],3);let dw=core.startTraversal(disconnected,'AT');dw=core.stepTraversal(disconnected,dw,'ATG');dw=core.stepTraversal(disconnected,dw,'TGA');assert.equal(core.availableEdges(disconnected,dw).length,0);assert(!dw.complete);
const a='ATGATCAT',b='ATCATGAT',ga=core.buildDeBruijn([a],3),gb=core.buildDeBruijn([b],3);
const sortedCounts=g=>Object.entries(g.counts).sort((a,b)=>a[0].localeCompare(b[0]));assert.deepEqual(sortedCounts(ga),sortedCounts(gb));assert.notDeepEqual(sortedCounts(core.buildDeBruijn([a],4)),sortedCounts(core.buildDeBruijn([b],4)));assert(a.includes('GATC'));assert(!b.includes('GATC'));
for(const edges of [['ATG','TGA','GAT','ATC','TCA','CAT'],['ATC','TCA','CAT','ATG','TGA','GAT']]){let w=core.startTraversal(ga,'AT');for(const edge of edges)w=core.stepTraversal(ga,w,edge);assert(w.complete);assert([a,b].includes(w.spelled));}
for(const bad of [()=>core.buildDeBruijn(['AT','GA'],3),()=>core.buildDeBruijn(['ATN'],3),()=>core.buildDeBruijn([' ATG'],3),()=>core.buildDeBruijn(['ATG'],1)])assert.throws(bad);
// N50 uses assembled bases, not a median over contig counts. Test against independent base weighting.
assert.deepEqual(core.assemblyStats([8,7,5]),{sorted:[8,7,5],total:20,count:3,n50:7,l50:2,cumulativeLengths:[8,15,20],threshold:10,largest:8});
assert.equal(core.assemblyStats([12,8]).n50,12);assert.equal(core.assemblyStats([12,8]).l50,1);
assert.equal(core.assemblyStats([]).n50,null);assert.equal(core.assemblyStats([]).l50,null);
for(let x=1;x<=4;x++)for(let y=1;y<=4;y++)for(let z=1;z<=4;z++){const lengths=[x,y,z],weighted=lengths.flatMap(length=>Array(length).fill(length)).sort((a,b)=>b-a),m=core.assemblyStats(lengths);assert.equal(m.n50,weighted[Math.ceil(weighted.length/2)-1]);assert(m.cumulativeLengths[m.l50-1]>=m.threshold);if(m.l50>1)assert(m.cumulativeLengths[m.l50-2]<m.threshold);}
assert.deepEqual(core.parseLengths('8, 7\n5'),[8,7,5]);
for(const bad of ['', '8, X, 5','8, 0, 5','8, -2','8, 1.5','1e3', '9007199254740992'])assert.throws(()=>core.parseLengths(bad));
console.log('Week 3 tools: coverage invariants and finite-boundary expectation, graph support/occurrences/valid walks/ambiguity, and base-weighted N50 checks passed.');
