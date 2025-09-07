from montaAutomato import *
from analisadorLexico import *

tokens = ['se', 'sai', 'foi']
gramaticas = [['S::=fA|aA|eA|iA', 'A::=fA|aA|eA|iA|']]
fita = []
ts = []

AFNDs = []
AFNDs = usingTokens(tokens)
AFNDs = usingGramaticas(gramaticas, AFNDs)
AFNDUnique = unirAFNDs(AFNDs)
AFDetrministico = AFNDUnique.determinizar()
analisadorLexico(AFDetrministico, fita, ts)

print(fita)
for l in ts:
    print(f"{l['linha']} | {l['estado']} | {l['label']}")