from gramatica_livre_contexto.GLC import *
from automato.montaAutomato import *
from reconhecedor_lexico.analisadorLexico import *
from analisador_sintatico.SLR_parser_generator import *
from analisador_sintatico.SLR import *
from arquivos.constantes import *


fita = []
ts = []
AFNDs = []

AFNDs = usingTokens(TOKENS)
AFNDs = usingGramaticas(GRAMATICAS, AFNDs)
AFNDUnique = unirAFNDs(AFNDs)
AFDetrministico = AFNDUnique.determinizar()

analisadorLexico(AFDetrministico, fita, ts)

glc = GLC(
    naoTerminais=NAO_TERMINAIS,
    terminais=TERMINAIS,
    simbolo_inicial=SIMBOLO_INICIAL,
    regras=REGRAS_ESTATICAS,
)

glc.criarGramatica()

gramatica_gerada = gerar_gramatica(glc)

slr = SLR(gramatica_gerada, glc.naoTerminais)
slr.exibir()
