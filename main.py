from montaAutomato import *
from analisadorLexico import *
from GLC import *

tokens = ["se", "foi"]
gramaticas = [["S::=fA|aA|eA|iA", "A::=fA|aA|eA|iA|"]]
fita = []
ts = []

AFNDs = []
AFNDs = usingTokens(tokens)
AFNDs = usingGramaticas(gramaticas, AFNDs)
AFNDUnique = unirAFNDs(AFNDs)
AFDetrministico = AFNDUnique.determinizar()

analisadorLexico(AFDetrministico, fita, ts)

AFDetrministico.exibir_automato()

# print("\n-------Fita-------\n")
# print(fita)

# print("\n-------Tablea de Símbolos-------\n")
# for l in ts:
#     print(f"{l['linha']} | {l['estado']} | {l['label']}")

teste = GLC([], [], [])

teste.criarRegrasPartirDoAFD(AFDetrministico)
teste.criarGramatica()

print("\n-------GLC-------\n")
print(teste.naoTerminais)
print(teste.terminais)
for regra in teste.regras:
    print(regra)
for gramatica in teste.gramatica.items():
    print(gramatica)
