from montaAutomato import *
from analisadorLexico import *

tokens = ['sei', 'nem', 'sai']
gramaticas = [['S::=oA|qA|tA', 'A::=oA|qA|tA']]
fita = []
ts = []

AFNDs = []
AFNDs = usingTokens(tokens)
AFNDUnique = unirAFNDs(AFNDs)
AFDetrministico = AFNDUnique.determinizar()
# AFDetrministico.exibir_automato()
analisadorLexico(AFDetrministico, fita, ts)

print(fita)
for l in ts:
    print(f"{l['linha']} | {l['estado']} | {l['label']}")
