from montaAutomato import *
from analisadorLexico import *
from GLC import *
from SLR_parser_generator import gerar_gramatica
from SLR import *

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

teste = GLC([], [])

teste.criarRegrasPartirDoAFD(AFDetrministico)

x = gerar_gramatica(teste)

a = SLR(x, teste.naoTerminais)
a.exibir()
