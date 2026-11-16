(() => {
  'use strict';
  const model=window.Week5;if(!model)return;
  const text=(el,value)=>{el.textContent=value;};
  const format=x=>x===null?'undefined (no retained observations)':x.toFixed(3);
  document.querySelectorAll('[data-w5-lab]').forEach(lab=>{
    const kind=lab.dataset.w5Lab;
    const control=name=>lab.querySelector(`[data-control="${name}"]`);
    const out=name=>lab.querySelector(`[data-output="${name}"]`);
    let evidenceShown=false;
    function update() {
      lab.querySelectorAll('[data-value]').forEach(el=>text(el,control(el.dataset.value).value));
      if(kind==='pileup') {
        const result=model.pileup(control('site').value,+control('base').value,+control('mapping').value);
        out('reads').replaceChildren(...result.reads.map(r=>{
          const el=document.createElement('div');el.className=`w5-read ${r.base==='G'?'alt':''} ${r.keep?'':'dropped'}`;
          const strong=document.createElement('strong');text(strong,r.base+r.strand);
          const detail=document.createElement('small');text(detail,`Q${r.baseQ} / M${r.mapQ}`);
          el.append(strong,detail);el.setAttribute('aria-label',`${r.base}, strand ${r.strand}, base Q ${r.baseQ}, mapping Q ${r.mapQ}, ${r.keep?'retained':'excluded'}`);return el;
        }));
        text(out('result'),`Retained: ${result.ref} A + ${result.alt} G = ${result.depth}. G fraction: ${format(result.fraction)}.`);
        text(out('detail'),`Retained G: ${result.forward} forward / ${result.reverse} reverse. Dashed, crossed-out tiles fail at least one threshold. A fraction alone is not a genotype.`);
      } else if(kind==='likelihood') {
        const ref=+control('ref').value,alt=+control('alt').value;
        const rows=model.likelihood(ref,alt,+control('error').value);
        out('bars').replaceChildren(...rows.map(r=>{
          const row=document.createElement('div'),label=document.createElement('span'),track=document.createElement('div'),bar=document.createElement('div'),value=document.createElement('small');
          text(label,r.gt);track.className='w5-bar-track';bar.className='w5-bar';bar.style.width=(r.relative*100)+'%';track.append(bar);
          text(value,`log₁₀ L ${r.score.toFixed(3)} · relative ${r.relative<.001?r.relative.toExponential(2):r.relative.toFixed(3)}`);
          row.append(label,track,value);return row;
        }));
        text(out('result'),ref+alt?`Best under this model: ${rows.filter(r=>r.best).map(r=>r.gt).join(' and ')}. Change depth to test the strength of the contrast.`:'No observations: all three likelihoods tie. Do not call a genotype.');
      } else if(kind==='structure') {
        const value=model.changes[control('change').value];
        out('blocks').replaceChildren(...[['Reference / chr 1','A→ B→ C→ D→ E→'],...value.rows].map(([label,sequence])=>{
          const row=document.createElement('div');row.className='w5-block-row';
          const title=document.createElement('span');title.className='w5-block-label';text(title,label);row.append(title);
          sequence.split(' ').forEach(symbol=>{const block=document.createElement('span');block.className='w5-block'+(symbol.includes('←')?' reverse':'');text(block,symbol);row.append(block);});return row;
        }));text(out('result'),value.note);
      } else if(kind==='coverage') {
        const r=model.coverage(control('profile').value);
        // All SVG strings below are constructed solely from fixed numeric teaching data.
        const bars=r.depth.map((d,i)=>`<rect x="${60+i*72}" y="${140-d*3}" width="68" height="${d*3}" fill="#0d7377"/>`).join('');
        const ticks=[0,400,800,1200].map(v=>`<text x="${60+v*.72}" y="165" text-anchor="middle">${v}</text>`).join('');
        out('plot').innerHTML=`<title>Mean depth: ${r.depth.join(', ')}; region to flank ratio ${r.ratio}</title><g font-family="Arial" font-size="18" fill="#14243b"><rect x="348" y="15" width="288" height="125" fill="#fbf1df"/>${bars}<path d="M60 80H924" stroke="#ad4936" stroke-width="2" stroke-dasharray="7 4"/><text x="8" y="84">20×</text>${ticks}<text x="60" y="184">0-based boundaries · shaded [400,800) · dashed: control 20×</text></g>`;
        text(out('result'),`Region mean ${r.inside} / flanks ${r.flanks} = ${r.ratio.toFixed(2)}. Depth alone does not establish the mechanism.`);
        text(out('evidence'),evidenceShown?r.evidence:'Junction evidence is hidden. What could explain this depth?');
        text(lab.querySelector('[data-action="reveal"]'),evidenceShown?'Hide junction evidence':'Reveal junction evidence');
      } else if(kind==='vcf') {
        const r=model.records[control('record').value];
        out('record').replaceChildren(...Object.entries({POS:r.pos,REF:r.ref,ALT:r.alt,GT:r.gt,AD:r.ad,DP:r.dp}).map(([key,value])=>{
          const el=document.createElement('span'),label=document.createElement('b'),val=document.createElement('span');text(label,key);text(val,value);el.append(label,val);return el;
        }));
        text(out('detail'),'GT is supplied, not calculated here. POS is 1-based. The record index and the deleted-base index can differ.');
      }
    }
    lab.addEventListener('input',event=>{
      if(!event.target.matches('[data-control]'))return;
      if(kind==='coverage')evidenceShown=false;
      if(kind==='vcf') {text(out('result'),'Enter the index, then check your answer.');if(event.target===control('record'))control('index').value='';}
      update();
    });
    lab.addEventListener('click',event=>{
      const action=event.target.closest('[data-action]')?.dataset.action;if(!action)return;
      if(kind==='pileup'){control('base').value=action==='raw'?0:20;control('mapping').value=action==='raw'?0:30;}
      if(kind==='likelihood'){const n=action==='empty'?0:action==='low'?1:6;control('ref').value=n;control('alt').value=n;control('error').value='.01';}
      if(kind==='structure')control('change').value='deletion';
      if(kind==='coverage'){if(action==='reset'){control('profile').value='loss';evidenceShown=false;}else evidenceShown=!evidenceShown;}
      if(kind==='vcf') {
        const r=model.records[control('record').value];
        if(action==='reset'){control('index').value='';text(out('result'),'Enter the index, then check your answer.');}
        else if(control('index').value.trim()===''||!Number.isInteger(+control('index').value)||+control('index').value<0)text(out('result'),'Enter a nonnegative whole-number index.');
        else text(out('result'),(+control('index').value===r.pos-1?'Correct. ':'Try POS − 1. ')+r.explanation);
      }
      update();
    });
    update();lab.querySelectorAll('input,select,button').forEach(el=>el.disabled=false);lab.classList.add('ready');
  });
})();
