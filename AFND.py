from collections import deque

class AFND:
    """
    Representa um Autômato Finito Não Determinístico (AFND).
    Atributos:
        estados (set): Conjunto de todos os estados (ex: {'q0', 'q1'}).
        alfabeto (set): Conjunto de  (ex: {'0símbolos do alfabeto', '1'}).
        transicoes (dict): Dicionário representando a função de transição.
                           A chave é uma tupla (estado, simbolo) e o valor é um conjunto de estados.
                           Para transições epsilon (ε), use '' como o símbolo.
                           Ex: {('q0', 'a'): {'q1'}, ('q1', ''): {'q2'}}
        estadoInicial (str): O estado inicial (ex: 'q0').
        estadosFinais (set): Conjunto dos estados de aceitação/finais (ex: {'q2'}).

        **SET: não permite elementos duplicados, Unordered, Mutável 
    """
    def __init__(self, estados, alfabeto, transicoes, estadoInicial, estadosFinais):
        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.transicoes = transicoes
        self.estadoInicial = estadoInicial
        self.estadosFinais = set(estadosFinais)
        
    def adicionar_estado(self, estado, eh_final=False):
        self.estados.add(estado)
        if eh_final:
            self.estadosFinais.add(estado)
    
    def adicionar_transicao(self, origem, simbolo, destino):
        if origem not in self.estados:
            raise ValueError(f"Estado de origem '{origem}' não existe.")
        if destino not in self.estados:
            raise ValueError(f"Estado de destino '{destino}' não existe.")
        if simbolo and simbolo not in self.alfabeto:
            raise ValueError(f"Símbolo '{simbolo}' não pertence ao alfabeto.")

        chave = (origem, simbolo)
        if chave in self.transicoes:
            self.transicoes[chave].add(destino)
        else:
            self.transicoes[chave] = {destino}

    """
    Converte este AFND em um AFD usando o algoritmo de construção de subconjuntos.
    Retorna um novo objeto AFND que é determinístico.
    peguei do Gemini
    """
    def determinizar(self):
        estado_inicial_afd_set = {self.estadoInicial}
        
        dfa_transicoes = {}
        dfa_estados_finais = set()

        mapa_estados = {frozenset(estado_inicial_afd_set): 'D0'}
        fila_trabalho = deque([estado_inicial_afd_set])
        contador_estados = 1

        while fila_trabalho:
            conjunto_atual_nfa = fila_trabalho.popleft()
            nome_estado_atual_dfa = mapa_estados[frozenset(conjunto_atual_nfa)]

            for simbolo in self.alfabeto:
                proximos_estados_nfa = set()
                for estado_nfa in conjunto_atual_nfa:
                    destinos = self.transicoes.get((estado_nfa, simbolo), set())
                    proximos_estados_nfa.update(destinos)
                
                if not proximos_estados_nfa:
                    continue
                
                proximo_conjunto_nfa = proximos_estados_nfa
                
                chave_proximo_conjunto = frozenset(proximo_conjunto_nfa)
                
                if chave_proximo_conjunto not in mapa_estados:
                    novo_nome_estado_dfa = f'D{contador_estados}'
                    mapa_estados[chave_proximo_conjunto] = novo_nome_estado_dfa
                    fila_trabalho.append(proximo_conjunto_nfa)
                    contador_estados += 1
                
                nome_proximo_estado_dfa = mapa_estados[chave_proximo_conjunto]
                dfa_transicoes[(nome_estado_atual_dfa, simbolo)] = {nome_proximo_estado_dfa}

        dfa_estados = set(mapa_estados.values())
        for conjunto_nfa, nome_dfa in mapa_estados.items():
            if not conjunto_nfa.isdisjoint(self.estadosFinais):
                dfa_estados_finais.add(nome_dfa)

        return AFND(
            estados=dfa_estados,
            alfabeto=self.alfabeto,
            transicoes=dfa_transicoes,
            estadoInicial='D0',
            estadosFinais=dfa_estados_finais
        )
    
    """
    Retorna o próximo estado para um AFD.

    Args:
        estadoAtual (str): O estado em que o autômato está.
        simbolo (str): O símbolo de entrada lido.

    Returns:
        str: O nome do próximo estado, se a transição existir.
        None: Se não houver transição definida.
    """
    def proximoEstado(self, estadoAtual, simbolo):
        # A chave que procuramos no dicionário de transições
        chave_transicao = (estadoAtual, simbolo)
        
        # Usamos .get() para buscar a chave de forma segura.
        # Se a chave não existir, ele retorna um conjunto vazio (definido por nós).
        conjunto_destino = self.transicoes.get(chave_transicao, set())
        
        # Se o conjunto não estiver vazio, uma transição foi encontrada.
        if conjunto_destino:
            # Como é um AFD, sabemos que o conjunto terá apenas UM elemento.
            # Podemos pegá-lo convertendo para lista ou usando next(iter(...))
            return list(conjunto_destino)[0]
        else:
            return None
    
    def exibir_automato(self):
        """
        Exibe a tabela de transições de um AFND no terminal de forma formatada.
        Gerado pelo gemini
        """
        estado_inicial = self.estadoInicial
        outros_estados = self.estados - {estado_inicial}
        outros_estados_ordenados = sorted(list(outros_estados))
        estados_ordenados = [estado_inicial] + outros_estados_ordenados
        
        has_epsilon = any(simbolo == '' for _, simbolo in self.transicoes.keys())
        
        alfabeto_ordenado = sorted(list(self.alfabeto))
        if has_epsilon:
            alfabeto_ordenado.append('')

        # 2. Calcular a largura máxima para cada coluna para o alinhamento
        largura_cols = {simbolo: len(simbolo) if simbolo != '' else 1 for simbolo in alfabeto_ordenado}
        
        largura_col_estados = 0
        for estado in estados_ordenados:
            prefixo = ""
            if estado == self.estadoInicial:
                prefixo += "->"
            if estado in self.estadosFinais:
                prefixo += "*"
            largura_col_estados = max(largura_col_estados, len(f"{prefixo}{estado}"))

        for estado in estados_ordenados:
            for simbolo in alfabeto_ordenado:
                destinos = self.transicoes.get((estado, simbolo), set())
                texto_celula = f"{{{', '.join(sorted(list(destinos)))}}}" if destinos else "-"
                largura_cols[simbolo] = max(largura_cols.get(simbolo, 0), len(texto_celula))

        # --- Impressão da Tabela ---

        print(f"{' ':<{largura_col_estados}} |", end="")
        for simbolo in alfabeto_ordenado:
            display_simbolo = 'ε' if simbolo == '' else simbolo
            print(f" {display_simbolo:^{largura_cols[simbolo]}} |", end="")
        print()

        print(f"{'-' * largura_col_estados}+", end="")
        for simbolo in alfabeto_ordenado:
            print(f"{'-' * (largura_cols[simbolo] + 2)}+", end="")
        print()

        for estado in estados_ordenados:
            prefixo = ""
            if estado == self.estadoInicial:
                prefixo += "->"
            if estado in self.estadosFinais:
                prefixo += "*"
            
            label_estado = f"{prefixo}{estado}"
            print(f"{label_estado:<{largura_col_estados}} |", end="")

            for simbolo in alfabeto_ordenado:
                destinos = self.transicoes.get((estado, simbolo), set())
                texto_celula = f"{{{', '.join(sorted(list(destinos)))}}}" if destinos else "-"
                print(f" {texto_celula:<{largura_cols[simbolo]}} |", end="")
            print() 