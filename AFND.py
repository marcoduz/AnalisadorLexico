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
        estado_inicial (str): O estado inicial (ex: 'q0').
        estados_finais (set): Conjunto dos estados de aceitação/finais (ex: {'q2'}).

        **SET: não permite elementos duplicados, Unordered, Mutável 
    """
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = set(estados_finais)
        
    def adicionar_estado(self, estado, eh_final=False):
        self.estados.add(estado)
        if eh_final:
            self.estados_finais.add(estado)
    
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

    def exibir_automato(self):
        """
        Exibe a tabela de transições de um AFND no terminal de forma formatada.
        Pedi pro Gemini gerar esta função
        """
        estados_ordenados = sorted(list(self.estados))
        
        has_epsilon = any(simbolo == '' for _, simbolo in self.transicoes.keys())
        
        alfabeto_ordenado = sorted(list(self.alfabeto))
        if has_epsilon:
            alfabeto_ordenado.append('')

        # 2. Calcular a largura máxima para cada coluna para o alinhamento
        largura_cols = {simbolo: len(simbolo) if simbolo != '' else 1 for simbolo in alfabeto_ordenado}
        
        largura_col_estados = 0
        for estado in estados_ordenados:
            prefixo = ""
            if estado == self.estado_inicial:
                prefixo += "->"
            if estado in self.estados_finais:
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

        print(f"{'-' * largura_col_estados}-+", end="")
        for simbolo in alfabeto_ordenado:
            print(f"{'-' * (largura_cols[simbolo] + 2)}-+", end="")
        print()

        for estado in estados_ordenados:
            prefixo = ""
            if estado == self.estado_inicial:
                prefixo += "->"
            if estado in self.estados_finais:
                prefixo += "*"
            
            label_estado = f"{prefixo}{estado}"
            print(f"{label_estado:<{largura_col_estados}} |", end="")

            for simbolo in alfabeto_ordenado:
                destinos = self.transicoes.get((estado, simbolo), set())
                texto_celula = f"{{{', '.join(sorted(list(destinos)))}}}" if destinos else "-"
                print(f" {texto_celula:<{largura_cols[simbolo]}} |", end="")
            print() 