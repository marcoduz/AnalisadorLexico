from montaAutomato import *
from analisadorLexico import *
from GLC import *
from SLR_parser_generator import gerar_gramatica
from SLR import *

tokens = ["id", "if", "(", ")", "{", "}", "else", "while", "return", ";", "=", "+", "-", "*", "/", "&", ">", "<", ">=", "<=", "==", "!=", "and", "or", "true", "false"]
gramaticas = [["S::=$A", "A::=a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|w|y|z"], ["S::=1A|2A|3A|4A|5A|6A|7A|8A|9A|0A", "A::=1A|2A|3A|4A|5A|6A|7A|8A|9A|0A|"],]
fita = []
ts = []

AFNDs = []
AFNDs = usingTokens(tokens)
AFNDs = usingGramaticas(gramaticas, AFNDs)
AFNDUnique = unirAFNDs(AFNDs)
AFDetrministico = AFNDUnique.determinizar()

analisadorLexico(AFDetrministico, fita, ts)

AFDetrministico.exibir_automato()

#teste = GLC([], [])

#teste.criarRegrasPartirDoAFD(AFDetrministico)

#x = gerar_gramatica(teste)

# a = SLR(x, teste.naoTerminais)
# a.exibir()

# BLOCO_CODIGO ::= CODIGO | CODIGO BLOCO_CODIGO
# CODIGO_IF ::= if (BOOL) { BLOCO_CODIGO } FINAL_CODIGO_IF
# FINAL_CODIGO_IF ::= else { BLOCO_CODIGO } | if (BOOL) { BLOCO_CODIGO } FINAL_CODIGO_IF |
# BOOL ::= VAL_COMP OP_COMP VAL_COMP | true | false
# OP_COMP ::= > | < | >= | <= | == | != | or | and
# VAL_COMP ::= (BOOL) | VAL
# CODIGO ::= SALVAR_VAR | CODIGO_IF
# SALVAR_VAR ::= t_id = VAL EQ ;
# EQ ::= OP VAL EQ |
# OP ::= + | - | * | /
# VAL ::= t_num
