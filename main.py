from src.analisador.lexico.builder import *
from src.analisador.sintatico.slr import SLR
from src.analisador.sintatico.parser import AnalisadorSemantico
from src.analisador.sintatico.gramatica import *
from src.analisador.lexico.analisador import *
from src.constantes import *
from src.analisador.sintatico.slr_generator import gerar_gramatica

def etapa_0(fita: list , ts : list):

    print("--- Iniciando Análise Léxica (Etapa 0) ---")

    AFNDs = []
    AFNDs = usingTokens(TOKENS)
    AFNDs = usingGramaticas(GRAMATICAS, AFNDs)

    AFNDUnique = unirAFNDs(AFNDs)
    AFDetrministico = AFNDUnique.determinizar()

    analisadorLexico(AFDetrministico, fita, ts, "./input/codigo.txt")

    tem_erro = any(
            t["token"] == "ERRO_LEXICO" or t["estado_final"] == "X"
            for t in ts
        )

    if tem_erro:
        for token in ts:
            if token["token"] == "ERRO_LEXICO":
                print(f"Erro Lexico - Token: {token['label']}, Linha: {token['linha']}")
        return False
    else:
        print("\n--- Análise Léxica Concluida ---")

    return True

def etapa_1( fita: list, linhas : list):

    print("\n--- Iniciando Análise Sintática (Etapa 1) ---")
    
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

    resultado = slr.resolver(fita)

    linhas.clear()
    linhas.extend(resultado)

    if not linhas:
        print("\nNenhuma linha foi sintaticamente correta. Encerrando.")
        return False

    return True

def etapa_2( linhas : list):
    
    print("\n--- Iniciando Análise Semântica (Etapa 2) ---")

    analisador_sem = AnalisadorSemantico()

    sucesso = analisador_sem.analisar_linhas(linhas)

    if not sucesso:
        return False

    print("\n--- Análise Semântica Concluída (Etapa 2) ---")
    print("\n Tabela de Símbolos Final ")
    if analisador_sem.tabela_simbolos_global:
        for var, data in analisador_sem.tabela_simbolos_global.items():
            print(f"  {var:<10} = {data['valor']} (Tipo: {data['tipo_dado']})")
    else:
        return False

    return True


def executar():

    fita, ts, linhas = [], [], []

    if not etapa_0(fita, ts):
        return

    if not etapa_1(fita, linhas):
        return
    
    # print(linhas)

    #linhas = [{'tipo_no': 'BLOCO_CODIGO', 'instrucoes': [{'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 1, 'token': 't_id', 'label': '$var', 'estado_final': 'D31'}, 'expressao_val': {'linha': 1, 'token': 't_num', 'label': '1', 'estado_final': 'D6'}, 'expressao_eq': {'tipo_no': 'EQ_EPSILON'}, 'linha': 1}, {'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 1, 'token': 't_id', 'label': '$var1', 'estado_final': 'D31'}, 'expressao_val': {'linha': 1, 'token': 't_num', 'label': '1', 'estado_final': 'D6'}, 'expressao_eq': {'tipo_no': 'EQ_EPSILON'}, 'linha': 1}, {'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 1, 'token': 't_id', 'label': '$x', 'estado_final': 'D31'}, 'expressao_val': {'linha': 1, 'token': 't_num', 'label': '1', 'estado_final': 'D6'}, 'expressao_eq': {'tipo_no': 'EQ_EPSILON'}, 'linha': 1}, {'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 1, 'token': 't_id', 'label': '$y', 'estado_final': 'D31'}, 'expressao_val': {'linha': 1, 'token': 't_num', 'label': '1', 'estado_final': 'D6'}, 'expressao_eq': {'tipo_no': 'EQ_EPSILON'}, 'linha': 1}, {'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 1, 'token': 't_id', 'label': '$z', 'estado_final': 'D31'}, 'expressao_val': {'linha': 1, 'token': 't_num', 'label': '1', 'estado_final': 'D6'}, 'expressao_eq': {'tipo_no': 'EQ_EPSILON'}, 'linha': 1}, {'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 1, 'token': 't_id', 'label': '$a', 'estado_final': 'D31'}, 'expressao_val': {'linha': 1, 'token': 't_num', 'label': '1', 'estado_final': 'D6'}, 'expressao_eq': {'tipo_no': 'EQ_EPSILON'}, 'linha': 1}, {'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 1, 'token': 't_id', 'label': '$outra', 'estado_final': 'D31'}, 'expressao_val': {'linha': 1, 'token': 't_num', 'label': '1', 'estado_final': 'D6'}, 'expressao_eq': {'tipo_no': 'EQ_EPSILON'}, 'linha': 1}, {'tipo_no': 'CODIGO_IF', 'condicao': {'linha': 2, 'token': 'true', 'label': 'true', 'estado_final': 'D38'}, 'bloco_then': {'tipo_no': 'BLOCO_CODIGO', 'instrucoes': [{'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 2, 'token': 't_id', 'label': '$var', 'estado_final': 'D31'}, 'expressao_val': {'linha': 2, 'token': 't_num', 'label': '1', 'estado_final': 'D6'}, 'expressao_eq': {'tipo_no': 'EQ_RECURSIVO', 'operador': {'linha': 2, 'token': '+', 'label': '+', 'estado_final': 'D18'}, 'valor': {'linha': 2, 'token': 't_num', 'label': '2', 'estado_final': 'D6'}, 'resto': {'tipo_no': 'EQ_EPSILON'}, 'linha': 2}, 'linha': 2}, {'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 2, 'token': 't_id', 'label': '$var', 'estado_final': 'D31'}, 'expressao_val': {'linha': 2, 'token': 't_id', 'label': '$var1', 'estado_final': 'D31'}, 'expressao_eq': {'tipo_no': 'EQ_RECURSIVO', 'operador': {'linha': 2, 'token': '+', 'label': '+', 'estado_final': 'D18'}, 'valor': {'linha': 2, 'token': 't_id', 'label': '$var', 'estado_final': 'D31'}, 'resto': {'tipo_no': 'EQ_EPSILON'}, 'linha': 2}, 'linha': 2}, {'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 2, 'token': 't_id', 'label': '$var2', 'estado_final': 'D31'}, 'expressao_val': {'linha': 2, 'token': 't_id', 'label': '$var1', 'estado_final': 'D31'}, 'expressao_eq': {'tipo_no': 'EQ_EPSILON'}, 'linha': 2}], 'linha': 2}, 'bloco_else': {'tipo_no': 'ELSE_IF', 'if_node': {'tipo_no': 'CODIGO_IF', 'condicao': {'linha': 2, 'token': 'false', 'label': 'false', 'estado_final': 'D40'}, 'bloco_then': {'tipo_no': 'BLOCO_CODIGO', 'instrucoes': [{'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 2, 'token': 't_id', 'label': '$var3', 'estado_final': 'D31'}, 'expressao_val': {'linha': 2, 'token': 't_num', 'label': '1', 'estado_final': 'D6'}, 'expressao_eq': {'tipo_no': 'EQ_EPSILON'}, 'linha': 2}], 'linha': 2}, 'bloco_else': {'tipo_no': 'ELSE_EPSILON'}, 'linha': 2}, 'linha': 2}, 'linha': 2}, {'tipo_no': 'CODIGO_IF', 'condicao': {'tipo_no': 'BOOL_OR', 'lhs': {'tipo_no': 'BOOL_REL_COMP', 'val1': {'linha': 3, 'token': 't_id', 'label': '$x', 'estado_final': 'D31'}, 'op': {'linha': 3, 'token': '==', 'label': '==', 'estado_final': 'D32'}, 'val2': {'linha': 3, 'token': 't_num', 'label': '1', 'estado_final': 'D6'}, 'linha': 3}, 'rhs': {'tipo_no': 'BOOL_REL_COMP', 'val1': {'linha': 3, 'token': 't_id', 'label': '$y', 'estado_final': 'D31'}, 'op': {'linha': 3, 'token': '<', 'label': '<', 'estado_final': 'D11'}, 'val2': {'linha': 3, 'token': 't_id', 'label': '$z', 'estado_final': 'D31'}, 'linha': 3}, 'linha': 3}, 'bloco_then': {'tipo_no': 'BLOCO_CODIGO', 'instrucoes': [{'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 3, 'token': 't_id', 'label': '$a', 'estado_final': 'D31'}, 'expressao_val': {'linha': 3, 'token': 't_num', 'label': '1', 'estado_final': 'D6'}, 'expressao_eq': {'tipo_no': 'EQ_EPSILON'}, 'linha': 3}], 'linha': 3}, 'bloco_else': {'tipo_no': 'ELSE_EPSILON'}, 'linha': 3}, {'tipo_no': 'CODIGO_IF', 'condicao': {'tipo_no': 'BOOL_REL_COMP', 'val1': {'linha': 4, 'token': 't_id', 'label': '$var', 'estado_final': 'D31'}, 'op': {'linha': 4, 'token': '>', 'label': '>', 'estado_final': 'D2'}, 'val2': {'linha': 4, 'token': 't_num', 'label': '0', 'estado_final': 'D6'}, 'linha': 4}, 'bloco_then': {'tipo_no': 'BLOCO_CODIGO', 'instrucoes': [{'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 4, 'token': 't_id', 'label': '$var', 'estado_final': 'D31'}, 'expressao_val': {'linha': 4, 'token': 't_num', 'label': '1', 'estado_final': 'D6'}, 'expressao_eq': {'tipo_no': 'EQ_EPSILON'}, 'linha': 4}], 'linha': 4}, 'bloco_else': {'tipo_no': 'ELSE_EPSILON'}, 'linha': 4}, {'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 5, 'token': 't_id', 'label': '$a', 'estado_final': 'D31'}, 'expressao_val': {'linha': 5, 'token': 't_num', 'label': '1', 'estado_final': 'D6'}, 'expressao_eq': {'tipo_no': 'EQ_EPSILON'}, 'linha': 5}, {'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 5, 'token': 't_id', 'label': '$b', 'estado_final': 'D31'}, 'expressao_val': {'linha': 5, 'token': 't_id', 'label': '$a', 'estado_final': 'D31'}, 'expressao_eq': {'tipo_no': 'EQ_EPSILON'}, 'linha': 5}, {'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 6, 'token': 't_id', 'label': '$total', 'estado_final': 'D31'}, 'expressao_val': {'linha': 6, 'token': 't_id', 'label': '$var1', 'estado_final': 'D31'}, 'expressao_eq': {'tipo_no': 'EQ_RECURSIVO', 'operador': {'linha': 6, 'token': '*', 'label': '*', 'estado_final': 'D20'}, 'valor': {'linha': 6, 'token': 't_num', 'label': '100', 'estado_final': 'D6'}, 'resto': {'tipo_no': 'EQ_RECURSIVO', 'operador': {'linha': 6, 'token': '+', 'label': '+', 'estado_final': 'D18'}, 'valor': {'linha': 6, 'token': 't_id', 'label': '$outra', 'estado_final': 'D31'}, 'resto': {'tipo_no': 'EQ_RECURSIVO', 'operador': {'linha': 6, 'token': '/', 'label': '/', 'estado_final': 'D3'}, 'valor': {'linha': 6, 'token': 't_num', 'label': '2', 'estado_final': 'D6'}, 'resto': {'tipo_no': 'EQ_EPSILON'}, 'linha': 6}, 'linha': 6}, 'linha': 6}, 'linha': 6}, {'tipo_no': 'SALVAR_VAR', 'variavel': {'linha': 7, 'token': 't_id', 'label': '$x', 'estado_final': 'D31'}, 'expressao_val': {'linha': 7, 'token': 't_num', 'label': '10', 'estado_final': 'D6'}, 'expressao_eq': {'tipo_no': 'EQ_EPSILON'}, 'linha': 7}], 'linha': 1}]

    if not  etapa_2(linhas):
        return

executar()