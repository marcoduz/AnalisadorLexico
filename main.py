from montaAFND import *

tokens = ['se', 'foi', 'sai']
AFNDs = []
AFNDs = usingTokens(tokens)
AFNDUnique = unirAFNDs(AFNDs)

# AFNDs[0].exibir_automato()
# print()
# AFNDs[1].exibir_automato()
# print()
# AFNDs[2].exibir_automato()
# print()
AFNDUnique.exibir_automato()

