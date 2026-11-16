"""Refresh shared activities in place within the Week 5 text lesson."""
from pathlib import Path
from labs_markup import lab
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'weeks/week-05.html'
s=p.read_text()
items=[
 ('pileup','Filter the same reads','At Q20/MQ30, B retains eight A and no G. A and C both retain six A and six G, but only A has G on both strands. D has no retained observations at base Q30.'),
 ('likelihood','Compare genotype predictions','With six A and six G, log₁₀ likelihoods in the binary e=0.01 model are −12.026, −3.612, and −12.026. No observations make all candidates tie.'),
 ('structure','Change the sequence arrangement','Reference A→ B→ C→ D→ E→. Deletion removes C; duplication repeats it; inversion gives A→ B→ D← C← E→. A balanced inversion need not change depth.'),
 ('coverage','Ask what evidence distinguishes the cases','Cases 1 and 2 have the same 0.5 depth ratio; only case 1 supplies junction support for a deletion. Case 3 has a 1.5 ratio and tandem-junction support. Case 4 has a 1.0 ratio and inversion-junction evidence. All observations are invented.'),
 ('vcf','Check a VCF coordinate','POS=501, REF=AT, ALT=A starts at Python index 500. The T at 1-based 502 (Python index 501) is deleted; A anchors the record.')]
for kind,title,fallback in items:
 start=f'<!-- WEEK05 LAB {kind} START -->'
 stop=f'<!-- WEEK05 LAB {kind} END -->'
 if s.count(start) != 1 or s.count(stop) != 1:
  raise ValueError(f'Expected one marker pair for {kind} in {p}')
 a=s.index(start);b=s.index(stop,a)+len(stop)
 content=(start+f'\n<article id="lab-{kind}" class="interactive-lab lesson-activity">'
          f'<p class="activity-label">Predict → change a setting → explain</p><h3>{title}</h3>'
          +lab(kind,'<p>'+fallback+'</p>')+'</article>\n'+stop)
 s=s[:a]+content+s[b:]
if 'week5-interactions.css' not in s:
 s=s.replace('</head>','<link rel="stylesheet" href="../assets/week5-interactions.css"><script src="../assets/week5-core.js" defer></script><script src="../assets/week5-interactions.js" defer></script></head>')
p.write_text(s)
print('Updated five activities in the Week 5 guide')
