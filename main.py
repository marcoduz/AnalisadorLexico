from montaAutomato import *
from analisadorLexico import *

tokens = ['se', 'foi']
gramaticas = [['S::=fA|aA|eA|iA', 'A::=fA|aA|eA|iA|']]
fita = []
ts = []

AFNDs = []
AFNDs = usingTokens(tokens)
AFNDs = usingGramaticas(gramaticas, AFNDs)
AFNDUnique = unirAFNDs(AFNDs)
AFDetrministico = AFNDUnique.determinizar()
analisadorLexico(AFDetrministico, fita, ts)

print("\n-------Fita-------\n")
print(fita)
print("\n-------Tablea de Símbolos-------\n")
for l in ts:
    print(f"{l['linha']} | {l['estado']} | {l['label']}")