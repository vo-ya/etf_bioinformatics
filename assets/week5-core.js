/* Synthetic teaching models shared by the Week 5 browser activities. */
(function (root) {
  'use strict';
  const make = (bases, baseQ=35, mapQ=60, allForward=false) => [...bases].map((base,i)=>({base,baseQ,mapQ,strand:allForward||i%2===0?'+':'-'}));
  const sites = {A:make('AAAAAAGGGGGG'),B:[...make('AAAAAAAA'),...make('GGGG',10),...make('GG',35,5)],C:[...make('AAAAAA'),...make('GGGGGG',35,60,true)],D:make('AAAGGG',20,30)};
  function pileup(site, baseQ, mapQ) {
    if(!sites[site] || !Number.isFinite(baseQ)||!Number.isFinite(mapQ)||baseQ<0||mapQ<0)throw Error('Invalid pileup settings');
    const reads=sites[site].map(r=>({...r,keep:r.baseQ>=baseQ&&r.mapQ>=mapQ}));
    const kept=reads.filter(r=>r.keep), alt=kept.filter(r=>r.base==='G');
    return {reads,depth:kept.length,ref:kept.length-alt.length,alt:alt.length,fraction:kept.length?alt.length/kept.length:null,forward:alt.filter(r=>r.strand==='+').length,reverse:alt.filter(r=>r.strand==='-').length};
  }
  function likelihood(ref,alt,error) {
    if(!Number.isInteger(ref)||!Number.isInteger(alt)||ref<0||alt<0||!(error>0&&error<.5))throw Error('Invalid likelihood settings');
    const scores=[error,.5,1-error].map(p=>ref*Math.log10(1-p)+alt*Math.log10(p));
    const best=Math.max(...scores);
    return scores.map((score,i)=>({gt:['0/0','0/1','1/1'][i],score,relative:10**(score-best),best:ref+alt>0&&Math.abs(score-best)<1e-10}));
  }
  const changes={
    deletion:{rows:[['Sample','A→ B→ D→ E→']],note:'C is absent. A loss of one diploid copy can reduce depth; look for the new B–D join.'},
    duplication:{rows:[['Sample','A→ B→ C→ C→ D→ E→']],note:'A tandem extra C creates a C–C join. Copy gain can raise depth under comparable sampling.'},
    insertion:{rows:[['Sample','A→ B→ X→ C→ D→ E→']],note:'X is new relative to the reference. Reads at its boundaries may split or contain unmapped sequence.'},
    inversion:{rows:[['Sample','A→ B→ D← C← E→']],note:'C–D is reverse-complemented: both order and orientation change. A balanced inversion can leave depth unchanged.'},
    translocation:{rows:[['Chr 2 reference','X→ Y→ Z→'],['Derivative 1','A→ B→ Z→'],['Derivative 2','X→ Y→ C→ D→ E→']],note:'A reciprocal exchange creates B–Z and Y–C joins. This toy preserves total sequence content across both derivatives.'}
  };
  const profiles={
    loss:{depth:[20,22,18,20,10,9,11,10,20,18,22,20],evidence:'Independent split reads join boundaries 400 and 800; pairs span about 700 reference bases rather than the usual 300. Together these support a candidate 400-base deletion.'},
    ambiguous:{depth:[20,22,18,20,10,9,11,10,20,18,22,20],evidence:'No junction observations have been supplied. Both deletion and mapping loss remain possible. Inspect mappability and seek independent junction-spanning sequence.'},
    gain:{depth:[20,22,18,20,30,29,31,30,20,18,22,20],evidence:'Invented reads span a tandem repeat junction. The 1.5 depth ratio is compatible with three copies against a diploid baseline; inspect placement and independence.'},
    inversion:{depth:[20,22,18,20,20,20,20,20,20,18,22,20],evidence:'Invented split alignments show reversed orientation at the two region boundaries. Ordinary depth does not rule out a balanced inversion.'}
  };
  function coverage(key) {
    const p=profiles[key];if(!p)throw Error('Unknown profile');
    const inside=p.depth.slice(4,8),flanks=[...p.depth.slice(0,4),...p.depth.slice(8)];
    const avg=a=>a.reduce((s,x)=>s+x,0)/a.length;
    return {...p,inside:avg(inside),flanks:avg(flanks),ratio:avg(inside)/avg(flanks)};
  }
  const records={snv:{pos:101,ref:'A',alt:'G',gt:'0/1',ad:'6,6',dp:12,explanation:'A→G at 1-based position 101. Python index 100. GT is supplied; the read fraction is 6/12.'},deletion:{pos:501,ref:'AT',alt:'A',gt:'0/1',ad:'7,5',dp:12,explanation:'A at 501 is the anchor. T at 502 is deleted (Python index 501); the record starts at Python index 500.'},insertion:{pos:601,ref:'A',alt:'AGG',gt:'0/1',ad:'8,4',dp:12,explanation:'A at 601 is the anchor (Python index 600). GG is inserted after it; the two new bases have no separate positions on this reference.'}};
  const api={sites,pileup,likelihood,changes,coverage,records};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.Week5=api;
})(typeof globalThis!=='undefined'?globalThis:this);
