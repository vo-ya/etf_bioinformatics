"""Insert the shared Week 5 activities in the existing student guide."""
from pathlib import Path
from labs_markup import lab
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'weeks/week-05.html'
s=p.read_text()
start='<!-- WEEK05 ACTIVITIES START -->'
stop='<!-- WEEK05 ACTIVITIES END -->'
items=[
 ('pileup','Filter the same reads','At Q20/MQ30, B retains eight A and no G. A and C both retain six A and six G, but only A has G on both strands. D has no retained observations at base Q30.'),
 ('likelihood','Compare genotype predictions','With six A and six G, log₁₀ likelihoods in the binary e=0.01 model are −12.026, −3.612, and −12.026. No observations make all candidates tie.'),
 ('structure','Change the sequence arrangement','Reference A→ B→ C→ D→ E→. Deletion removes C; duplication repeats it; inversion gives A→ B→ D← C← E→. A balanced inversion need not change depth.'),
 ('coverage','Ask what evidence distinguishes the cases','Cases 1 and 2 have the same 0.5 depth ratio; only case 1 supplies junction support for a deletion. Case 3 has a 1.5 ratio and tandem-junction support. Case 4 has a 1.0 ratio and inversion-junction evidence. All observations are invented.'),
 ('vcf','Check a VCF coordinate','POS=501, REF=AT, ALT=A starts at Python index 500. The T at 1-based 502 (Python index 501) is deleted; A anchors the record.')]
content=start+'\n<section id="activities"><h2>Try the examples</h2><p>Predict a result, change one setting, then explain what the output does and does not establish. All observations below are synthetic; changes stay in this page and reset when it reloads.</p>'
for kind,title,fallback in items:
 content+=f'<article id="lab-{kind}"><h3>{title}</h3>'+lab(kind,'<p>'+fallback+'</p>')+'</article>'
content+='</section>\n'+stop
if start in s:
 a=s.index(start);b=s.index(stop,a)+len(stop);s=s[:a]+content+s[b:]
else:
 s=s.replace('<section id="pileups">',content+'\n<section id="pileups">')
if 'week5-interactions.css' not in s:
 s=s.replace('</head>','<link rel="stylesheet" href="../assets/week5-interactions.css"><script src="../assets/week5-core.js" defer></script><script src="../assets/week5-interactions.js" defer></script></head>')
s=s.replace('<a href="../presentations/week-05/index.html">Slides</a>','<a href="../presentations/week-05/index.html">Slides</a><a href="#activities">Try the examples</a>') if '<a href="#activities">' not in s else s
p.write_text(s)
print('Updated five activities in the Week 5 guide')
