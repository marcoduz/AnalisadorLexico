from AFND import AFND

"""
    Monta um Automâto finito não deterministico de acordo com os tokens recebidos
    Atributos:
        tokens (Array): Conjunto de todas as palavra/tokens (ex: [se, enquanto]).
        AFNDs (Array): Conjunto de automatos a qual será acrescentado os novos automatos gerados
    Retorno:
        retorna Array de automatos AFNDs modificado
    """
def usingTokens(tokens, AFNDs = []): 
    for t in tokens:
        automato = AFND({'q0'}, set(), {}, 'q0', set())
        i=0
        estadoAtual='q0'
        for c in t:
            i+=1
            novoEstado = 'q'+ str(i)
            automato.alfabeto.add(c)
            automato.adicionar_estado(novoEstado)
            automato.adicionar_transicao(estadoAtual, c, novoEstado)
            estadoAtual = novoEstado
        
        automato.estados_finais.add(estadoAtual)
        AFNDs.append(automato)
    
    return AFNDs

def usingGramaticas(gramaticas, AFNDs = []):
    ##@todo
    print('a fazer')