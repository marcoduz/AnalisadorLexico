from analisador_sintatico.analisador_sintatico import AnalisadorSemantico
from gramatica_livre_contexto.GLC import *
from automato.montaAutomato import *
from reconhecedor_lexico.analisadorLexico import *
from analisador_sintatico.SLR_parser_generator import *
from analisador_sintatico.SLR import *
from arquivos.constantes import *


fita = []
ts = []
AFNDs = []

print("--- Iniciando Análise Léxica (Etapa 0) ---")

AFNDs = usingTokens(TOKENS)
AFNDs = usingGramaticas(GRAMATICAS, AFNDs)

AFNDUnique = unirAFNDs(AFNDs)
AFDetrministico = AFNDUnique.determinizar()

analisadorLexico(AFDetrministico, fita, ts)

print(f"--- Análise Léxica Concluída: {len(fita)} linhas válidas encontradas ---")

glc = GLC(
    naoTerminais=NAO_TERMINAIS,
    terminais=TERMINAIS,
    simbolo_inicial=SIMBOLO_INICIAL,
    regras=REGRAS_ESTATICAS,
)

glc.criarGramatica()

gramatica_gerada = gerar_gramatica(glc)

slr = SLR(gramatica_gerada, NAO_TERMINAIS)

print("\n--- Iniciando Análise Sintática (Etapa 1) ---")

lista_asts_linhas = slr.resolver(fita)

if not lista_asts_linhas:
    print("\nNenhuma linha foi sintaticamente correta. Encerrando.")
else:
    print(
        f"\n--- Análise Sintática Concluída. {len(lista_asts_linhas)} linhas prontas para a próxima etapa ---"
    )

    analisador_sem = AnalisadorSemantico()

    analisador_sem.analisar_linhas(lista_asts_linhas)

    print("\n--- Análise Semântica Concluída (Etapa 2) ---")
    print("\n=== Tabela de Símbolos Final ===")
    if analisador_sem.tabela_simbolos_global:
        for var, data in analisador_sem.tabela_simbolos_global.items():
            print(f"  {var:<10} = {data['valor']} (Tipo: {data['tipo_dado']})")
    else:
        print("  (Vazia)")
