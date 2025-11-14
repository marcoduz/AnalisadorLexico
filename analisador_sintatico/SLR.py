class SLR:
    """ """

    def __init__(self, dados_completos: dict, nao_terminais_gramatica: list[str]):
        self.producoes = []
        self.first_follow = {0: {}}
        self.tabela_action = {0: {}}
        self.tabela_transicao = {0: {}}
        self.nao_terminais_referencia = nao_terminais_gramatica

        self.mapa_producoes = {0: (0, 0)}

        if dados_completos:
            self.processar_dados(dados_completos)

    def processar_dados(self, dados: dict[str, list[str]]):
        self.producoes = dados.get("producoes", [])

        for prod_info in self.producoes:
            num_prod = prod_info[0]
            regra_str = prod_info[1]

            lhs, rhs_str = regra_str.split(" -> ")
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

    def parse(self, fita_tokens: list[str]):
        """
        Executa o algoritmo de parsing SLR para UMA linha de tokens.
        """

        pilha = [0]
        ponteiro = 0

        while True:
            estado_atual = pilha[-1]

            simbolo_atual_dict = fita_tokens[ponteiro]

            if isinstance(simbolo_atual_dict, dict):
                simbolo_token = simbolo_atual_dict.get("token", "$")
            else:
                simbolo_token = simbolo_atual_dict

            acao = self.tabela_action.get(estado_atual, {}).get(simbolo_token, "")

            if acao.startswith("s"):
                novo_estado_str = acao[1:]
                if not novo_estado_str.isdigit():
                    return False

                novo_estado = int(novo_estado_str)
                pilha.append(simbolo_atual_dict)
                pilha.append(novo_estado)
                ponteiro += 1

            elif acao.startswith("r"):
                num_producao_str = acao[1:]
                if not num_producao_str.isdigit():
                    raise SyntaxError(f"Erro: Redução inválida '{acao}'")
                num_producao = int(num_producao_str)

                if num_producao not in self.mapa_producoes:
                    raise SyntaxError(
                        f"Erro: Regra de produção {num_producao} não mapeada."
                    )

                lhs, len_rhs = self.mapa_producoes[num_producao]

                simbolos_reduzidos = []
                if len_rhs > 0:
                    simbolos_reduzidos = pilha[-(len_rhs * 2) :: 2]
                    pilha = pilha[: -(len_rhs * 2)]

                estado_anterior = pilha[-1]

                novo_no_semantico = self.construir_no_ast(lhs, simbolos_reduzidos)

                pilha.append(novo_no_semantico)

                novo_estado_str = self.tabela_transicao.get(estado_anterior, {}).get(
                    lhs
                )

                if not novo_estado_str or not novo_estado_str.isdigit():
                    token_atual = fita_tokens[ponteiro]
                    linha = token_atual.get("linha", "desconhecida")
                    label = token_atual.get("label", "desconhecido")
                    raise SyntaxError(
                        f"Erro Sintático/Semântico na Linha {linha}: Transição GOTO inválida para '{lhs}' após redução. Token: '{label}'"
                    )

                pilha.append(int(novo_estado_str))

            elif acao == "acc":
                return pilha[1]

            else:
                linha = simbolo_atual_dict.get("linha", "Desconhecida")
                label = simbolo_atual_dict.get("label", simbolo_token)

                acoes_do_estado = self.tabela_action.get(estado_atual, {})

                esperados = []
                for terminal, acao_tabela in acoes_do_estado.items():
                    if acao_tabela and acao_tabela.strip() != "-":
                        esperados.append(terminal)

                esperados.sort()

                msg_erro = f"Erro Sintático na Linha {linha}: Encontrado '{label}'. "

                if esperados:
                    msg_erro += f"Esperado: {', '.join(esperados)}"
                else:
                    msg_erro += "Nenhum token era esperado neste ponto."

                raise SyntaxError(msg_erro)

    def construir_no_ast(self, regra_lhs: str, simbolos_reduzidos: list):
        """
        Cria o novo nó da AST que será empilhado.
        NÃO faz mais cálculos nem verificações de tipo. Apenas monta a estrutura.
        """

        # O nó base é o próprio token (um dicionário)
        if not simbolos_reduzidos and regra_lhs not in ["EQ", "ELSE_PART"]:
            # Isso geralmente não deve acontecer para regras de construção
            return None
        
        # VAL ::= t_num
        # VAL ::= t_id
        if regra_lhs == "VAL":
            return simbolos_reduzidos[0]

        # OP ::= + | - | * | /
        elif regra_lhs == "OP":
            return simbolos_reduzidos[0]

        # OP_COMP ::= > | < | >= | <= | == | !=
        elif regra_lhs == "OP_COMP":
            return simbolos_reduzidos[0]

        # --- REGRAS DE CÁLCULO DE EXPRESSÃO (Nós Ramo) ---

        # EQ ::= OP VAL EQ
        elif regra_lhs == "EQ" and simbolos_reduzidos:
            op_node = simbolos_reduzidos[0]
            val_node = simbolos_reduzidos[1]
            eq_node = simbolos_reduzidos[2]
            return {
                "tipo_no": "EQ_RECURSIVO",
                "operador": op_node,
                "valor": val_node,
                "resto": eq_node,
                "linha": op_node.get("linha"),
            }

        # EQ ::= ε
        elif regra_lhs == "EQ" and not simbolos_reduzidos:
            return {"tipo_no": "EQ_EPSILON"}

        # SALVAR_VAR ::= t_id = VAL EQ ;
        elif regra_lhs == "SALVAR_VAR":
            return {
                "tipo_no": "SALVAR_VAR",
                "variavel": simbolos_reduzidos[0],
                "expressao_val": simbolos_reduzidos[2],
                "expressao_eq": simbolos_reduzidos[3],
                "linha": simbolos_reduzidos[0].get("linha"),
            }

        # --- REGRAS DE LÓGICA BOOLEANA (Nós Ramo) ---

        # BOOL_ATOM ::= true | false | VAL
        elif regra_lhs == "BOOL_ATOM" and len(simbolos_reduzidos) == 1:
            # Apenas passa o nó filho (true, false, ou VAL) para cima
            return simbolos_reduzidos[0]

        # BOOL_ATOM ::= ( BOOL_OR )
        elif regra_lhs == "BOOL_ATOM" and len(simbolos_reduzidos) == 3:
            # Retorna o nó do meio (o resultado de BOOL_OR)
            return simbolos_reduzidos[1]

        # BOOL_REL ::= BOOL_ATOM
        elif regra_lhs == "BOOL_REL" and len(simbolos_reduzidos) == 1:
            return simbolos_reduzidos[0]  # Passa o nó BOOL_ATOM para cima

        # BOOL_REL ::= VAL OP_COMP VAL
        elif regra_lhs == "BOOL_REL" and len(simbolos_reduzidos) == 3:
            return {
                "tipo_no": "BOOL_REL_COMP",
                "val1": simbolos_reduzidos[0],
                "op": simbolos_reduzidos[1],
                "val2": simbolos_reduzidos[2],
                "linha": simbolos_reduzidos[1].get("linha"),
            }

        # BOOL_AND ::= BOOL_AND and BOOL_REL
        elif regra_lhs == "BOOL_AND" and len(simbolos_reduzidos) == 3:
            return {
                "tipo_no": "BOOL_AND",
                "lhs": simbolos_reduzidos[0],  # Nó BOOL_AND
                "rhs": simbolos_reduzidos[2],  # Nó BOOL_REL
                "linha": simbolos_reduzidos[1].get("linha"),  # Linha do 'and'
            }

        # BOOL_AND ::= BOOL_REL
        elif regra_lhs == "BOOL_AND" and len(simbolos_reduzidos) == 1:
            return simbolos_reduzidos[0]  # Passa o nó BOOL_REL para cima

        # BOOL_OR ::= BOOL_OR or BOOL_AND
        elif regra_lhs == "BOOL_OR" and len(simbolos_reduzidos) == 3:
            return {
                "tipo_no": "BOOL_OR",
                "lhs": simbolos_reduzidos[0],  # Nó BOOL_OR
                "rhs": simbolos_reduzidos[2],  # Nó BOOL_AND
                "linha": simbolos_reduzidos[1].get("linha"),  # Linha do 'or'
            }

        # BOOL_OR ::= BOOL_AND
        elif regra_lhs == "BOOL_OR" and len(simbolos_reduzidos) == 1:
            return simbolos_reduzidos[0]  # Passa o nó BOOL_AND para cima

        # --- REGRAS ESTRUTURAIS (IF, BLOCOS) ---

        # CODIGO_IF ::= if ( BOOL_OR ) { BLOCO_CODIGO } ELSE_PART
        elif regra_lhs == "CODIGO_IF":
            return {
                "tipo_no": "CODIGO_IF",
                "condicao": simbolos_reduzidos[2],
                "bloco_then": simbolos_reduzidos[5],
                "bloco_else": simbolos_reduzidos[7],
                "linha": simbolos_reduzidos[0].get("linha"),  # Linha do 'if'
            }

        # ELSE_PART ::= else { BLOCO_CODIGO }
        elif regra_lhs == "ELSE_PART" and len(simbolos_reduzidos) == 3:
            return {
                "tipo_no": "ELSE_BLOCO",
                "bloco": simbolos_reduzidos[2],
                "linha": simbolos_reduzidos[0].get("linha"),
            }

        # ELSE_PART ::= else CODIGO_IF
        elif regra_lhs == "ELSE_PART" and len(simbolos_reduzidos) == 2:
            return {
                "tipo_no": "ELSE_IF",
                "if_node": simbolos_reduzidos[1],  # O nó 'CODIGO_IF'
                "linha": simbolos_reduzidos[0].get("linha"),
            }

        # ELSE_PART ::= ε
        elif regra_lhs == "ELSE_PART" and not simbolos_reduzidos:
            return {"tipo_no": "ELSE_EPSILON"}

        # CODIGO ::= SALVAR_VAR | CODIGO_IF
        elif regra_lhs == "CODIGO":
            return simbolos_reduzidos[0]  # Apenas passa o nó filho para cima

        # BLOCO_CODIGO ::= CODIGO
        elif regra_lhs == "BLOCO_CODIGO" and len(simbolos_reduzidos) == 1:
            return {
                "tipo_no": "BLOCO_CODIGO",
                "instrucoes": [simbolos_reduzidos[0]],  # Lista de instruções
                "linha": simbolos_reduzidos[0].get("linha", "?"),
            }

        # BLOCO_CODIGO ::= CODIGO BLOCO_CODIGO
        elif regra_lhs == "BLOCO_CODIGO" and len(simbolos_reduzidos) == 2:
            # Pega a lista de instruções do nó BLOCO_CODIGO filho
            instrucoes_filhas = simbolos_reduzidos[1].get("instrucoes", [])
            # Adiciona a nova instrução no início
            return {
                "tipo_no": "BLOCO_CODIGO",
                "instrucoes": [simbolos_reduzidos[0]] + instrucoes_filhas,
                "linha": simbolos_reduzidos[0].get("linha", "?"),
            }

        # Se nenhuma regra bateu, retorna um nó genérico para depuração
        return {"tipo": regra_lhs, "filhos": simbolos_reduzidos}

    def resolver(self, fita: list[list[dict]]):
        """
        Itera sobre a fita (uma lista de listas de tokens)
        e chama o parser para cada linha.
        """

        arvores_sintaticas = []

        for tokens_linha in fita:

            linha_num = tokens_linha[-1]["linha"]
            fita_com_marcador = tokens_linha + [
                {"token": "$", "label": "$", "linha": linha_num}
            ]

            try:
                ast_raiz = self.parse(fita_com_marcador)

                if ast_raiz:
                    print(f"\nLinha {linha_num}: Sintaxe Aceita.")
                    arvores_sintaticas.append(ast_raiz)
                else:
                    print(
                        f"\nLinha {linha_num}: Rejeitada (Erro de parser desconhecido)."
                    )

            except (Exception, SyntaxError) as e:
                print(f"\nLinha {linha_num}: Rejeita (Sintaxe)")
                print(f"  --> {e}")

                print("  ", " ".join([t.get("label", "") for t in tokens_linha]))

            print("\n" + "---" * 10)

        return arvores_sintaticas

    def exibir(self):
        """
        Imprime todas as tabelas salvas em um formato de grade legível.
        """
        print("\n" + "=" * 50)
        print(" DADOS DE PARSING SALVOS NA CLASSE (SLR.py)")
        print("=" * 50 + "\n")

        # --- 1. IMPRIMIR PRODUÇÕES ---
        print("--- Produções Numeradas ---\n")
        if self.producoes:
            for num in sorted(self.mapa_producoes.keys()):
                try:
                    regra_str = self.producoes[num][1]
                    print(f"  ({num}) {regra_str}")
                except IndexError:
                    pass
        else:
            print("Nenhuma produção encontrada.")

        # --- 2. IMPRIMIR FIRST E FOLLOW ---
        print("\n--- Tabela de FIRST e FOLLOW ---\n")
        if self.first_follow:
            print(f"{'Nonterminal':<20} | {'FIRST':<30} | {'FOLLOW':<30}")
            print("-" * 80)
            for nt, sets in self.first_follow.items():
                first_str = " ".join(sorted(list(sets.get("FIRST", set()))))
                follow_str = " ".join(sorted(list(sets.get("FOLLOW", set()))))
                print(f"{nt:<20} | {first_str:<30} | {follow_str:<30}")
        else:
            print("Nenhuma tabela de FIRST/FOLLOW encontrada.")

        # --- 3. IMPRIMIR TABELA DE ACTION ---
        print("\n--- Tabela de ACTION ---\n")
        if self.tabela_action:
            # 1. Obter todos os estados e cabeçalhos de terminais
            estados = sorted(self.tabela_action.keys())
            terminais = set()
            for acoes in self.tabela_action.values():
                terminais.update(acoes.keys())

            # Ordena os terminais (coloca '$' no final)
            terminais_ordenados = sorted([t for t in terminais if t != "$"])
            if "$" in terminais:
                terminais_ordenados.append("$")

            # 2. Calcular a largura de cada coluna
            col_larguras = {t: len(t) for t in terminais_ordenados}
            for estado in estados:
                for t in terminais_ordenados:
                    acao = self.tabela_action[estado].get(t, "-")
                    col_larguras[t] = max(col_larguras[t], len(acao))

            # 3. Imprimir o Cabeçalho da Tabela
            print(f"{'Estado':<6} |", end="")
            for t in terminais_ordenados:
                print(f" {t:^{col_larguras[t]}} |", end="")
            print()

            print(
                f"{'-'*6:->}+{'-' * (sum(col_larguras.values()) + len(col_larguras) * 3 - 1):->}"
            )

            # 4. Imprimir as linhas de dados
            for estado in estados:
                print(f"{estado:<6} |", end="")
                for t in terminais_ordenados:
                    acao = self.tabela_action[estado].get(t, "")
                    if acao == "":
                        acao = "-"
                    print(f" {acao:^{col_larguras[t]}} |", end="")
                print()
        else:
            print("Nenhuma tabela de ACTION encontrada.")

        # --- 4. IMPRIMIR TABELA DE GOTO ---
        print("\n--- Tabela de GOTO ---\n")
        if self.tabela_transicao:
            # 1. Obter todos os estados e cabeçalhos de não-terminais
            estados = sorted(self.tabela_transicao.keys())
            nao_terminais = set()
            for transicoes in self.tabela_transicao.values():
                nao_terminais.update(transicoes.keys())

            nao_terminais_ordenados = sorted(
                [nt for nt in nao_terminais if "'" not in nt]
            )
            if "S'" in nao_terminais:
                nao_terminais_ordenados.insert(0, "S'")

            # 2. Calcular a largura de cada coluna
            col_larguras_goto = {nt: len(nt) for nt in nao_terminais_ordenados}
            for estado in estados:
                for nt in nao_terminais_ordenados:
                    goto = self.tabela_transicao[estado].get(nt, "-")
                    if goto == "":
                        goto = "-"
                    col_larguras_goto[nt] = max(col_larguras_goto[nt], len(str(goto)))

            # 3. Imprimir o Cabeçalho
            print(f"{'Estado':<6} |", end="")
            for nt in nao_terminais_ordenados:
                print(f" {nt:^{col_larguras_goto[nt]}} |", end="")
            print()

            print(
                f"{'-'*6:->}+{'-' * (sum(col_larguras_goto.values()) + len(col_larguras_goto) * 3 - 1):->}"
            )

            # 4. Imprimir as linhas de dados
            for estado in estados:
                print(f"{estado:<6} |", end="")
                for nt in nao_terminais_ordenados:
                    goto = self.tabela_transicao[estado].get(nt, "")
                    if goto == "":
                        goto = "-"
                    print(f" {str(goto):^{col_larguras_goto[nt]}} |", end="")
                print()
        else:
            print("Nenhuma tabela de GOTO encontrada.")
