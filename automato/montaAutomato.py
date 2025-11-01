from automato.AFND import AFND

"""
    Monta um Automâto finito não deterministico de acordo com os tokens recebidos
    Percorre o token cada caracter se torna um símbolo do alfabeto e é gerado um novo estado
    saindo do estadoAtual para o novoEstado montado ao ler um símbolo
    Atributos:
        tokens (Array): Conjunto de todas as palavra/tokens (ex: [se, enquanto]).
        AFNDs (Array): Conjunto de automatos a qual será acrescentado os novos automatos gerados
    Retorno:
        retorna Array de automatos AFNDs modificado
    """


def usingTokens(tokens: list, AFNDs: list = []):
    for t in tokens:
        automato = AFND({"q0"}, set(), {}, "q0", {})
        i = 0
        estadoAtual = "q0"
        for c in t:
            i += 1
            novoEstado = "q" + str(i)
            automato.alfabeto.add(c)
            automato.adicionar_estado(novoEstado)
            automato.adicionar_transicao(estadoAtual, c, novoEstado)
            estadoAtual = novoEstado

        automato.estadosFinais[estadoAtual] = t
        AFNDs.append(automato)

    return AFNDs


"""
Recebe uma lista de gramáticas e cria um AFND independente para cada uma.

Args:
    gramaticas (list): Uma lista onde cada item é uma gramática.
                        Ex: [['S::=aA'], ['B::=bB']]
    AFNDs (list): Lista inicial para popular (opcional).

Returns:
    list: Uma lista contendo todos os objetos AFND criados.
"""


def usingGramaticas(gramaticas: dict[str, list[str]], AFNDs: list[AFND] = []):
    for token_name, gramatica in gramaticas.items():
        relacaoNaoTerminalEstado = {}
        estadosFinais_locais = set()
        estadosAutomato = set()
        naoTerminais = set()

        ##Este for percorre a gramaticapara encontrar todos os símbolos não terminais ou seja letras maiusculas
        ##Também define os estados finais que são aqueles que possuem uma produção vazia
        for producao in gramatica:
            estado, restante = producao.split("::=")
            naoTerminais.add(estado)
            for producao in restante.split("|"):
                if producao == "":
                    estadosFinais_locais.add(estado.strip())
                for char in producao.strip():
                    if "A" <= char <= "Z":
                        naoTerminais.add(char)

        ##Deixar o S no inicio da lista para ele sempre ser o estado inicial
        outros = naoTerminais - {"S"}
        outros = sorted(list(outros))
        naoTerminais = ["S"] + outros

        # Mapeia cada não-terminal a um nome de estado único para este autômato
        for i, nt in enumerate(list(naoTerminais)):
            novoNome = f"q{i}"
            relacaoNaoTerminalEstado[nt] = novoNome
            estadosAutomato.add(novoNome)

        # Assume que o primeiro não-terminal encontrado é o inicial
        simbolo_inicial = gramatica[0].split("::=")[0].strip()
        estadoInicial = relacaoNaoTerminalEstado[simbolo_inicial]

        # --- Monta o objeto do automato ainda sem as transições ---
        automato = AFND(
            estados=estadosAutomato,
            alfabeto=set(),
            transicoes={},
            estadoInicial=estadoInicial,
            estadosFinais={},
        )

        # Constrói as transições para o autômato novo
        for producao in gramatica:
            estado, restante = producao.split("::=")
            estadoOrigem = relacaoNaoTerminalEstado[estado.strip()]

            for producao in restante.split("|"):
                producao = producao.strip()
                proximoEstado = ""
                terminal = ""
                for char in producao:
                    if "A" <= char <= "Z":
                        proximoEstado = char
                    else:
                        terminal += char

                if terminal:
                    automato.alfabeto.add(terminal)
                else:
                    automato.estadosFinais[estadoOrigem] = token_name

                if not proximoEstado:
                    continue

                proximoEstado = relacaoNaoTerminalEstado.get(proximoEstado)
                automato.adicionar_transicao(estadoOrigem, terminal, proximoEstado)

        # Adiciona o autômato recém-criado à lista de automatos
        AFNDs.append(automato)

    return AFNDs


"""
    Junta dois ou mais automatos finitos não deterministicos em um único
    mantendo apenas os estados iniciais originais
    Atributos:
        AFNDs (Array): Conjunto de todas as palavra/tokens (ex: [se, enquanto]).
        estadoInicial (String): nome do estado inicial por padrão q0
    Retorno:
        retorna o objeto do novo Automato
"""


def unirAFNDs(AFNDs: list[AFND], estadoInicial="q0"):

    # Verificações se existe um autômato e se existe somente 1
    if not AFNDs:
        return AFND({estadoInicial}, set(), {}, estadoInicial, {})
    if len(AFNDs) == 1:
        return AFNDs[0]

    novosEstados = {estadoInicial}
    novoAlfabeto = set()
    novasTransicoes = {}
    novosEstadosFinais = {}

    for i, automato in enumerate(AFNDs):
        mapaRenomeacao = {automato.estadoInicial: estadoInicial}

        ##mapaRenomeacao é um dicionario que relaciona o estado do automato ao seu novo nome no novo automato
        # Os outros estados recebem um prefixo para serem únicos
        outros_estados = automato.estados - {automato.estadoInicial}
        for estado in outros_estados:
            mapaRenomeacao[estado] = f"{i}.{estado}"

        # Adiciona os novos estados renomeados aos estados do novo automato
        # e adiciona o alfabeto deste automato ao alfabet do novo automato
        # por ser set não corre o risco de duplicatas
        novosEstados.update(mapaRenomeacao.values())
        novoAlfabeto.update(automato.alfabeto)

        # Adiciona os estados finais renomeados
        for ef_estado, ef_token in automato.estadosFinais.items():
            novosEstadosFinais[mapaRenomeacao[ef_estado]] = ef_token

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
        estadosFinais=novosEstadosFinais,
    )
