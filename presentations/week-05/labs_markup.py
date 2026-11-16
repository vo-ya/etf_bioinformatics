"""Shared accessible activity markup for the deck and student guide."""

def select(name, label, choices):
    return f'<label>{label}<select data-control="{name}" disabled>'+''.join(f'<option value="{key}">{title}</option>' for key,title in choices)+'</select></label>'

def slider(name,label,value,maximum):
    return f'<label>{label} <output data-value="{name}">{value}</output><input data-control="{name}" type="range" min="0" max="{maximum}" step="1" value="{value}" disabled></label>'

def button(label,action):
    return f'<button type="button" data-action="{action}" disabled>{label}</button>'

LABS = {
'pileup': ('Predict which G observations survive, then change one threshold.',
    select('site','Candidate site',[('B','B: suspect G'),('A','A: balanced'),('C','C: one-strand G'),('D','D: threshold boundary')])+slider('base','Minimum base Q',20,40)+slider('mapping','Minimum mapping Q',30,60),
    '<div class="w5-read-grid" data-output="reads" aria-label="Read observations"></div><p class="w5-result" data-output="result" role="status"></p><p class="w5-detail" data-output="detail"></p>',
    button('Show all reads','raw')+button('Restore Q20 / MQ30','defaults')),
'likelihood': ('Predict the best-fitting genotype. Compare 1 A + 1 G with 6 A + 6 G.',
    slider('ref','A observations',6,20)+slider('alt','G observations',6,20)+select('error','Binary error probability',[('.01','0.01'),('.1','0.10'),('.25','0.25')]),
    '<div data-output="bars" class="w5-likelihood"></div><p class="w5-result" data-output="result" role="status"></p><p class="w5-detail">Bars: likelihood / best likelihood, not posterior probabilities. Independent binary A↔G errors; correct mappings; no priors.</p>',
    button('1 A + 1 G','low')+button('No observations','empty')+button('Reset 6 + 6','reset')),
'structure': ('Choose a change. Predict whether total copy number must change.',
    select('change','Sequence change',[('deletion','Deletion'),('duplication','Tandem duplication'),('insertion','Insertion'),('inversion','Balanced inversion'),('translocation','Reciprocal translocation')]),
    '<div data-output="blocks" class="w5-blocks"></div><p class="w5-result" data-output="result" role="status"></p>',button('Reset to deletion','reset')),
'coverage': ('Use depth first. Then reveal the junction evidence and revise your explanation.',
    select('profile','Synthetic case',[('loss','Case 1'),('ambiguous','Case 2'),('gain','Case 3'),('inversion','Case 4')]),
    '<svg class="w5-depth" data-output="plot" viewBox="0 0 1000 185" role="img" aria-label="Synthetic window depth"></svg><p class="w5-result" data-output="result" role="status"></p><p class="w5-detail" data-output="evidence" aria-live="polite">Junction evidence is hidden. What could explain this depth?</p>',button('Reveal junction evidence','reveal')+button('Reset case 1','reset')),
'vcf': ('Read the allele replacement. Convert the record’s POS to a Python index.',
    select('record','Record',[('deletion','One-base deletion'),('snv','A→G SNV'),('insertion','Two-base insertion')]),
    '<div class="w5-vcf" data-output="record"></div><div class="w5-controls"><label>Python index of POS<input data-control="index" type="number" min="0" step="1" placeholder="Your answer" disabled></label>'+button('Check index','check')+'</div><p class="w5-result" data-output="result" role="status">Enter the index, then check your answer.</p><p class="w5-detail" data-output="detail"></p>',button('Reset answer','reset'))
}

def lab(kind, fallback):
    prompt, controls, outputs, actions=LABS[kind]
    return f'''<div class="w5-lab" data-w5-lab="{kind}"><div class="w5-live"><p class="w5-prompt">{prompt}</p><div class="w5-controls">{controls}</div>{outputs}<div class="w5-actions">{actions}</div></div><div class="w5-fallback">{fallback}</div></div>'''
