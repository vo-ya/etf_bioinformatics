"""Draw original, explicitly synthetic Week 5 teaching figures as SVG."""
from pathlib import Path
from html import escape
HERE = Path(__file__).resolve().parent
INK, TEAL, RED, GOLD = '#14243b', '#0d7377', '#ad4936', '#946018'

def text(x, y, label, size=24, fill=INK, anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}">{escape(str(label))}</text>'

def rect(x, y, w, h, fill):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}"/>'

def line(x1,y1,x2,y2,color=INK,dash=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="3" stroke-dasharray="{dash}"/>'

def save(name, title, desc, parts, height=400):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc><g font-family="Arial,sans-serif">{''.join(parts)}</g></svg>'''
    (HERE / name).write_text(svg + '\n')

def blocks(label, symbols, y):
    parts = [text(10,y+31,label,22)]
    for i, symbol in enumerate(symbols):
        x=225+i*115
        color = GOLD if symbol.startswith('X') else RED if '←' in symbol else TEAL
        parts += [rect(x,y,100,45,color),text(x+50,y+31,symbol,25,'white','middle')]
    return parts

parts=[]
for label, seq, y in [('Reference',['A→','B→','C→','D→','E→'],10),
                       ('Deletion',['A→','B→','D→','E→'],75),
                       ('Duplication',['A→','B→','C→','C→','D→','E→'],140),
                       ('Insertion',['A→','B→','X→','C→','D→','E→'],205)]:
    parts += blocks(label,seq,y)
parts += [text(10,300,'Blocks represent oriented regions, not individual bases.',22),text(10,335,'Loss, gain, and a new junction can provide different kinds of evidence.',22)]
save('sequence-changes.svg','Sequence loss and gain','Reference A B C D E; deletion removes C; duplication repeats C; insertion adds X.',parts,360)
parts=blocks('Reference',['A→','B→','C→','D→','E→'],25)+blocks('Inversion',['A→','B→','D←','C←','E→'],115)
parts += [text(20,230,'The C–D segment is reverse-complemented; both orientations flip.',25),text(20,280,'A balanced inversion can preserve copy number and ordinary depth.',25),text(20,330,'Look for new junctions and changed alignment orientations.',25)]
save('inversion.svg','An inversion reverses order and orientation','A B C D E becomes A B reverse D reverse C E. Copy number can remain unchanged.',parts,365)
parts=blocks('Chr 1 reference',['A→','B→','C→'],10)+blocks('Chr 2 reference',['X→','Y→','Z→'],75)+blocks('Derivative 1',['A→','B→','Z→'],175)+blocks('Derivative 2',['X→','Y→','C→'],240)
parts += [text(15,345,'Reciprocal exchange: new B–Z and Y–C joins; no net loss in this toy.',24)]
save('translocation.svg','A reciprocal translocation','Two chromosomes exchange terminal regions C and Z without net sequence loss in this simplified example.',parts,375)
parts=[text(15,28,'Site A: one invented fragment per row',24),text(670,28,'Reference position',22)]
for j,pos in enumerate(range(99,104)):
    parts += [text(280+j*60,64,pos,20,INK,'middle')]
for i,seq in enumerate(['TCAAT']+['TCAAT']*6+['TCGAT']*6):
    y=92+i*22
    parts += [text(20,y,'Reference' if i==0 else f'Fragment {i:02}',18)]
    for j,b in enumerate(seq):
        if j==2:
            parts += [rect(258+j*60,y-18,44,21,'#f7e6df' if b=='G' else '#e3f0ef')]
        parts += [text(280+j*60,y,b,19,RED if b=='G' else INK,'middle')]
parts += [text(670,130,'REF = A',30),text(670,180,'ALT candidate = G',30,RED),text(670,240,'6 A + 6 G = 12',30),text(670,290,'G fraction = 6/12',30),text(670,340,'= 0.5',36,TEAL)]
save('pileup.svg','A pileup of twelve synthetic fragments','At reference position 101 six fragments report A and six report G; alternate fraction is 0.5.',parts,395)
parts=[text(15,30,'Mean depth in equal 100-base windows',24)]
depths=[20,22,18,20,10,9,11,10,20,18,22,20]
x0,y0,scale=100,290,8
parts += [rect(x0+4*65,70,4*65,220,'#fbf1df'),line(x0,y0,900,y0),line(x0,60,x0,y0)]
for d in [0,10,20]:
    parts += [text(85,y0-d*scale+7,d,20,INK,'end')]
for i,d in enumerate(depths):
    parts += [rect(x0+i*65+2,y0-d*scale,61,d*scale,TEAL)]
parts += [line(x0,y0-20*scale,x0+780,y0-20*scale,RED,'8 5')]
for pos in [0,400,800,1200]:
    parts += [text(x0+pos/100*65,322,pos,22,INK,'middle')]
parts += [text(500,360,'Reference position (0-based boundaries)',24,INK,'middle'),text(500,395,'Region 10 / flanks 20 = 0.5; dashed control depth = 20.',24,INK,'middle')]
save('coverage.svg','Half-depth region in a synthetic sample','The four windows in [400,800) average depth 10; eight flanking windows average 20. Control depth is 20.',parts,425)
parts=[text(15,30,'A 400-base deletion on one sample chromosome',26)]
# Reference scale x=100 + 0.65*position.
parts += [rect(100,80,260,35,TEAL),rect(360,80,260,35,'#ead3c9'),rect(620,80,260,35,TEAL)]
for pos in [0,400,800,1200]:
    parts += [text(100+.65*pos,65,pos,22,INK,'middle')]
parts += [text(490,105,'deleted region',21,INK,'middle')]
parts += [text(10,160,'Pair',22),line(262.5,160,717.5,160,INK,'7 5'),rect(262.5,145,32.5,25,TEAL),rect(685,145,32.5,25,TEAL),text(278,165,'→',24,'white','middle'),text(701,165,'←',24,'white','middle')]
parts += [text(100,210,'Reference outer span: 950 − 250 = 700 bp',25),text(100,247,'Sample fragment span: 700 − 400 = 300 bp (typical library span)',25)]
parts += [text(10,302,'Split read',22),rect(347,280,13,28,RED),rect(620,280,13,28,RED),line(360,294,620,294,RED,'6 5')]
parts += [text(100,355,'One 40-base read: [380,400) joined to [800,820)',25),text(100,393,'Independent reads spanning this join help locate the breakends.',23)]
save('deletion-evidence.svg','Pair and split-read evidence for a deletion','A typical 300-base fragment spans 700 reference bases across a 400-base deletion. A split read joins the flanks at boundaries 400 and 800.',parts,420)
print('Wrote six original Week 5 SVG diagrams')
