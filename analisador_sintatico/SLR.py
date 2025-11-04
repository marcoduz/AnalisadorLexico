class SLR:
    """ """

    def __init__(self, dados_completos: dict, nao_terminais_gramatica: list[str]):
        self.producoes = []
        self.first_follow = {}
        self.tabela_action = {}
        self.tabela_transicao = {}
        self.nao_terminais_referencia = nao_terminais_gramatica

        self.mapa_producoes = {}

        if dados_completos:
            self.processar_dados(dados_completos)

    def processar_dados(self, dados: dict[str, list[str]]):
        self.producoes = dados.get("producoes", [])

        for prod_info in self.producoes:
            num_prod = prod_info[0]
            regra_str = prod_info[1]
            
            lhs, rhs_str = regra_str.split(' -> ')
            rhs_simbolos = rhs_str.split() if rhs_str != "''" else []
            
            self.mapa_producoes[num_prod] = (lhs, len(rhs_simbolos))

        ff_data = dados.get("first_follow", [])
        if len(ff_data) > 1:

            for linha in ff_data[2:]:
                nao_terminal = linha[0]
                self.first_follow[nao_terminal] = {
                    "FIRST": linha[1],
                    "FOLLOW": linha[2],
                }

        data = dados.get("tabela_slr", [])
        if len(data) > 2:
            header_completo = data[1]

            split_index = -1
            for i, simbolo in enumerate(header_completo):
                if simbolo in self.nao_terminais_referencia:
                    split_index = i
                    break

            if split_index == -1:
                print(
                    "Erro: Não foi possível dividir o cabeçalho da tabela SLR em ACTION e GOTO."
                )
                return

            teminais = header_completo[:split_index]
            nao_terminais = header_completo[split_index:]

            for linha in data[2:]:
                estado_str = linha[0]
                if not estado_str.isdigit():
                    continue
                estado = int(estado_str)

                self.tabela_action[estado] = {}
                self.tabela_transicao[estado] = {}

                for i, simbolo in enumerate(teminais):
                    self.tabela_action[estado][simbolo] = linha[i + 1]

                for i, simbolo in enumerate(nao_terminais):
                    self.tabela_transicao[estado][simbolo] = linha[i + split_index + 1]

    # RETIRADO DO CHAT GPT
    def exibir(self):
        """
        Imprime todas as tabelas salvas em um formato de grade legível.
        """
        print("\n" + "=" * 50)
        print(" DADOS DE PARSING SALVOS NA CLASSE (SLR.py)")
        print("=" * 50 + "\n")

        # --- 1. IMPRIMIR PRODUÇÕES (Igual ao seu) ---
        print("--- Produções Numeradas ---\n")
        if self.producoes:
            # Pega o 'mapa_producoes' que já processamos
            # (Assumindo que você usou o 'enumerate(..., 0)' corrigido)
            for num in sorted(self.mapa_producoes.keys()):
                # O mapa_producoes que criamos não guarda a string inteira,
                # então vamos pegar da lista original 'self.producoes'
                # Assumindo que self.producoes[num] é [0, "S' -> ..."]
                try:
                    regra_str = self.producoes[num][1]
                    print(f"  ({num}) {regra_str}")
                except IndexError:
                    pass # Ignora se houver dessincronia
        else:
            print("Nenhuma produção encontrada.")

        # --- 2. IMPRIMIR FIRST E FOLLOW (Igual ao seu) ---
        print("\n--- Tabela de FIRST e FOLLOW ---\n")
        if self.first_follow:
            print(f"{'Nonterminal':<20} | {'FIRST':<30} | {'FOLLOW':<30}")
            print("-" * 80)
            for nt, sets in self.first_follow.items():
                # Transforma o set em uma string legível
                first_str = " ".join(sorted(list(sets.get("FIRST", set()))))
                follow_str = " ".join(sorted(list(sets.get("FOLLOW", set()))))
                print(f"{nt:<20} | {first_str:<30} | {follow_str:<30}")
        else:
            print("Nenhuma tabela de FIRST/FOLLOW encontrada.")

        # --- 3. IMPRIMIR TABELA DE ACTION (Formato de Grade) ---
        print("\n--- Tabela de ACTION ---\n")
        if self.tabela_action:
            # 1. Obter todos os estados e cabeçalhos de terminais
            estados = sorted(self.tabela_action.keys())
            terminais = set()
            for acoes in self.tabela_action.values():
                terminais.update(acoes.keys())
            
            # Ordena os terminais (coloca '$' no final)
            terminais_ordenados = sorted([t for t in terminais if t != '$'])
            if '$' in terminais:
                terminais_ordenados.append('$')

            # 2. Calcular a largura de cada coluna
            col_larguras = {t: len(t) for t in terminais_ordenados}
            for estado in estados:
                for t in terminais_ordenados:
                    acao = self.tabela_action[estado].get(t, '-')
                    col_larguras[t] = max(col_larguras[t], len(acao))

            # 3. Imprimir o Cabeçalho da Tabela
            print(f"{'Estado':<6} |", end="")
            for t in terminais_ordenados:
                print(f" {t:^{col_larguras[t]}} |", end="")
            print()
            
            # Imprimir linha separadora
            print(f"{'-'*6:->}+{'-' * (sum(col_larguras.values()) + len(col_larguras) * 3 - 1):->}")

            # 4. Imprimir as linhas de dados
            for estado in estados:
                print(f"{estado:<6} |", end="")
                for t in terminais_ordenados:
                    acao = self.tabela_action[estado].get(t, "")
                    if acao == "": acao = "-" # Substitui vazio por '-'
                    print(f" {acao:^{col_larguras[t]}} |", end="")
                print()
        else:
            print("Nenhuma tabela de ACTION encontrada.")

        # --- 4. IMPRIMIR TABELA DE GOTO (Formato de Grade) ---
        print("\n--- Tabela de GOTO ---\n")
        if self.tabela_transicao:
            # 1. Obter todos os estados e cabeçalhos de não-terminais
            estados = sorted(self.tabela_transicao.keys())
            nao_terminais = set()
            for transicoes in self.tabela_transicao.values():
                nao_terminais.update(transicoes.keys())
            
            # Ordena (coloca S' no início, se existir)
            nao_terminais_ordenados = sorted([nt for nt in nao_terminais if "'" not in nt])
            if "S'" in nao_terminais:
                nao_terminais_ordenados.insert(0, "S'")

            # 2. Calcular a largura de cada coluna
            col_larguras_goto = {nt: len(nt) for nt in nao_terminais_ordenados}
            for estado in estados:
                for nt in nao_terminais_ordenados:
                    goto = self.tabela_transicao[estado].get(nt, '-')
                    if goto == "": goto = "-"
                    col_larguras_goto[nt] = max(col_larguras_goto[nt], len(str(goto)))
            
            # 3. Imprimir o Cabeçalho
            print(f"{'Estado':<6} |", end="")
            for nt in nao_terminais_ordenados:
                print(f" {nt:^{col_larguras_goto[nt]}} |", end="")
            print()
            
            # Imprimir linha separadora
            print(f"{'-'*6:->}+{'-' * (sum(col_larguras_goto.values()) + len(col_larguras_goto) * 3 - 1):->}")

            # 4. Imprimir as linhas de dados
            for estado in estados:
                print(f"{estado:<6} |", end="")
                for nt in nao_terminais_ordenados:
                    goto = self.tabela_transicao[estado].get(nt, "")
                    if goto == "": goto = "-"
                    print(f" {str(goto):^{col_larguras_goto[nt]}} |", end="")
                print()
        else:
            print("Nenhuma tabela de GOTO encontrada.")

    def parse(self, fita_tokens: list[str]):
        """
        Executa o algoritmo de parsing SLR para UMA linha de tokens.
        """
        
        pilha = [0]
        ponteiro = 0 

        while True:
            estado_atual = pilha[-1]
            simbolo_atual = fita_tokens[ponteiro]

            acao = self.tabela_action.get(estado_atual, {}).get(simbolo_atual, "")

            if acao[0] == 's':
                novo_estado_str = acao[1:]
                if not novo_estado_str.isdigit():
                    return False
                
                novo_estado = int(novo_estado_str)
                pilha.append(simbolo_atual)
                pilha.append(novo_estado)
                ponteiro += 1

            elif acao[0] == 'r':
                num_producao_str = acao[1:]
                if not num_producao_str.isdigit():
                    return False
                num_producao = int(num_producao_str)
                
                if num_producao not in self.mapa_producoes:
                    return False
                
                lhs, len_rhs = self.mapa_producoes[num_producao]    
                
                if len_rhs > 0:
                    pilha = pilha[: - (len_rhs * 2)]
                
                estado_anterior = pilha[-1]
                pilha.append(lhs)
                
                novo_estado_str = self.tabela_transicao.get(estado_anterior, {}).get(lhs)

                if not novo_estado_str or not novo_estado_str.isdigit():
                    return False
                    
                pilha.append(int(novo_estado_str))
                
            elif acao == 'acc':
                return True

            else:
                return False
                
            
    def resolver(self, fita: list[list[str]]):
        """
        Itera sobre a fita (uma lista de listas de tokens)
        e chama o parser para cada linha.
        """
        
        for i, tokens_linha in enumerate(fita, 1):
            fita_com_marcador = tokens_linha + ['$']
            
            try:
                
                resultado = self.parse(fita_com_marcador)
                    
                
                print(f"Linha {i}: {'Aceita' if resultado else 'Rejeita'}")

            except Exception as e:
                print(f"Linha {i}: Rejeita")
                
        
        print("Análise Sintática Concluída.")

        

