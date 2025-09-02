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
        
        automato.estadosFinais.add(estadoAtual)
        AFNDs.append(automato)
    
    return AFNDs

##@todo
# tava pensando se a gramática vai ser só no formato simboloVariavel (sA)
# se tiver algo como simboloVariavelSimbolo (sAs) não sei como fazer
def usingGramaticas(gramaticas, AFNDs = []):
    automato = AFND({'q0'}, set(), {}, 'q0', set())     

    for gramatica in gramaticas:
        relacao_estado_letra = dict()
        for i, producao in enumerate(gramatica):
            estado, restante = producao.split('::=')
            producoes = restante.split('|')
            if estado not in relacao_estado_letra:
                relacao_estado_letra[estado] = 'q'+str(i)
                automato.adicionar_estado('q'+str(i))

            for p in producoes:
                for simbolo in p:
                    if(ord(simbolo)>=65 and ord(simbolo)<=90):
                        if simbolo not in relacao_estado_letra:
                            tam = len(relacao_estado_letra)
                            relacao_estado_letra[simbolo] = 'q'+str(tam)
                            automato.adicionar_estado('q'+str(tam))
                    else:
                        automato.alfabeto.add(simbolo)
    print(automato.estados, automato.alfabeto)
    

"""
    Junta dois ou mais automatos finitos não deterministicos em um único
    mantendo apenas os estados iniciais originais
    Atributos:
        AFNDs (Array): Conjunto de todas as palavra/tokens (ex: [se, enquanto]).
        estadoInicial (String): nome do estado inicial por padrão q0
    Retorno:
        retorna o objeto do novo Automato
"""
def unirAFNDs(AFNDs, estadoInicial = 'q0'):

    #Verificações se existe um autômato e se existe somente 1
    if not AFNDs:
        return AFND({estadoInicial}, set(), {}, estadoInicial, set())
    if len(AFNDs) == 1:
        return AFNDs[0]
    
    novosEstados = {estadoInicial}
    novoAlfabeto = set()
    novasTransicoes = {}
    novosEstadosFinais = set()

    for i, automato in enumerate(AFNDs):
        mapaRenomeacao = {automato.estadoInicial: estadoInicial}
        
        # Os outros estados recebem um prefixo para serem únicos
        outros_estados = automato.estados - {automato.estadoInicial}
        for estado in outros_estados:
            mapaRenomeacao[estado] = f"{i}.{estado}"
        
        # Adiciona os novos estados renomeados
        novosEstados.update(mapaRenomeacao.values())

        # Adiciona o alfabeto
        novoAlfabeto.update(automato.alfabeto)

        # Adiciona os estados finais renomeados
        for ef in automato.estadosFinais:
            novosEstadosFinais.add(mapaRenomeacao[ef])

        # 3. Copia e MESCLA as transições
        for (origem, simbolo), destinos in automato.transicoes.items():
            nova_origem = mapaRenomeacao[origem]
            novos_destinos = {mapaRenomeacao[d] for d in destinos}
            
            chave_transicao = (nova_origem, simbolo)
            
            # Se já existe uma transição para esta chave, une os destinos
            if chave_transicao in novasTransicoes:
                novasTransicoes[chave_transicao].update(novos_destinos)
            else:
                # Se não existe, apenas cria a nova transição
                novasTransicoes[chave_transicao] = novos_destinos

    return AFND(
        estados=novosEstados,
        alfabeto=novoAlfabeto,
        transicoes=novasTransicoes,
        estadoInicial=estadoInicial,
        estadosFinais=novosEstadosFinais
    )