class AnalisadorSemantico:
    """
    Esta classe (Etapa 2) recebe a Árvore Sintática Abstrata (AST)
    gerada pelo parser (Etapa 1).

    Ela "visita" cada nó da árvore para:
    1. Realizar a análise semântica (verificação de tipos, etc).
    2. Gerenciar a Tabela de Símbolos Global.
    3. Executar/Interpretar a lógica do código.
    """

    def __init__(self):
        self.tabela_simbolos_global = {}

    def analisar_linhas(self, lista_asts: list[dict]):
        """
        Ponto de entrada principal. Itera sobre a lista de ASTs
        (cada AST representa uma linha de código) e as analisa.
        """

        for ast_raiz in lista_asts:
            linha = self._get_linha(ast_raiz)
            try:
                self.visitar_no(ast_raiz)

                print(f"Codigo {linha}: Análise Semântica Aceita.")

            except Exception as e:
                print(f"\nCodigo {linha}: Rejeitada (Semântica)")
                print(f"  --> {e}")
                
                return False

            print("\n" + "---" * 10)

        return True

    def _get_linha(self, no: dict):
        """Função utilitária para extrair o número da linha de um nó."""
        if not isinstance(no, dict):
            return "?"
        return no.get("linha", "?")

    def visitar_no(self, no: dict):
        """
        O "Visitante" da AST. Esta é a função recursiva central.
        Ela determina o tipo do nó e decide o que fazer.
        Retorna um dicionário com {'valor': ..., 'tipo_dado': ...}
        """
        
        if not isinstance(no, dict):
            return None

        tipo_no = no.get("tipo_no")

        # --- NÓS DE ESTRUTURA DE BLOCO ---
        if tipo_no == "BLOCO_CODIGO":
            # Visita todas as instruções na ordem
            for instrucao in no.get("instrucoes", []):
                self.visitar_no(instrucao)
            return None  # Blocos não retornam valor

        # --- NÓS DE ATRIBUIÇÃO ---
        elif tipo_no == "SALVAR_VAR":
            var_nome = no["variavel"]["label"]
            linha = self._get_linha(no)

            # 1. Avalia o primeiro valor (Lado esquerdo da expressão aritmética)
            val_node = self.visitar_no(no["expressao_val"])
            
            if val_node.get("tipo_dado") != "int":
                raise Exception(f"Erro Semântico (Linha {linha}): Tipo incompatível na inicialização de '{var_nome}'. Esperado 'int'.")

            valor_acumulado = val_node["valor"]

            # 2. Itera sobre a cadeia EQ (Lado direito: OP VAL EQ ...)
            # Transforma a recursão à direita em um loop iterativo (Esquerda -> Direita)
            curr_eq = no["expressao_eq"]
            
            while curr_eq and curr_eq.get("tipo_no") == "EQ_RECURSIVO":
                # Visita o operador e o próximo valor
                op_node = self.visitar_no(curr_eq["operador"])
                rhs_node = self.visitar_no(curr_eq["valor"])
                
                if rhs_node.get("tipo_dado") != "int":
                    raise Exception(f"Erro Semântico (Linha {linha}): Operação aritmética com tipo não inteiro.")

                operador = op_node["valor"]
                rhs_valor = rhs_node["valor"]

                # Executa a operação acumulando no valor total
                if operador == "+":
                    valor_acumulado += rhs_valor
                elif operador == "-":
                    valor_acumulado -= rhs_valor
                elif operador == "*":
                    valor_acumulado *= rhs_valor
                elif operador == "/":
                    if rhs_valor == 0:
                        raise Exception(
                            f"Erro Semântico (Linha {linha}): Divisão por zero na atribuição de '{var_nome}'."
                        )
                    valor_acumulado = int(valor_acumulado / rhs_valor)

                # Avança para o próximo nó da cadeia EQ
                curr_eq = curr_eq["resto"]

            # 3. Salva o resultado final na Tabela de Símbolos
            var_tipo = "int"
            self.tabela_simbolos_global[var_nome] = {
                "valor": valor_acumulado,
                "tipo_dado": var_tipo,
            }
            # print(
            #     f"[AÇÃO SEMÂNTICA (Linha {linha})]: Variável '{var_nome}' definida como {valor_acumulado} (Tipo: {var_tipo})"
            # )
            return None

        # --- NÓS DE EXPRESSÃO ARITMÉTICA (EQ) ---
        # Nota: Com a lógica iterativa no SALVAR_VAR, esses nós são processados manualmente lá.
        # Mantemos aqui apenas caso seja necessário visitar individualmente (ex: debug),
        # mas a lógica principal de cálculo foi movida para o loop acima.
        elif tipo_no == "EQ_RECURSIVO":
             return None 
        elif tipo_no == "EQ_EPSILON":
             return None

        # --- NÓS DE ESTRUTURA DE CONTROLE (IF) ---
        elif tipo_no == "CODIGO_IF":
            linha = self._get_linha(no)

            # 1. Avalia a condição
            condicao_node = self.visitar_no(no["condicao"])

            # 2. Análise Semântica: A condição é booleana?
            if condicao_node.get("tipo_dado") != "bool":
                raise Exception(
                    f"Erro Semântico (Linha {linha}): A condição do 'if' deve resultar em um booleano (recebeu '{condicao_node.get('tipo_dado')}'')."
                )

            # 3. Execução (Interpretação)
            if condicao_node.get("valor") == True:
                # Visita o bloco 'then'
                self.visitar_no(no["bloco_then"])
            else:
                # Visita o bloco 'else' (que pode ser um else-if, um bloco, ou nada)
                self.visitar_no(no["bloco_else"])
            return None

        elif tipo_no == "ELSE_BLOCO":
            self.visitar_no(no["bloco"])
            return None

        elif tipo_no == "ELSE_IF":
            self.visitar_no(no["if_node"])  # Visita o 'CODIGO_IF' aninhado
            return None

        elif tipo_no == "ELSE_EPSILON":
            return None  # Não faz nada

        # --- NÓS DE EXPRESSÃO BOOLEANA ---
        elif tipo_no == "BOOL_REL_COMP":  # VAL OP_COMP VAL
            val1_node = self.visitar_no(no["val1"])
            op_node = self.visitar_no(no["op"])
            val2_node = self.visitar_no(no["val2"])
            linha = self._get_linha(no)

            tipo1 = val1_node.get("tipo_dado")
            tipo2 = val2_node.get("tipo_dado")

            if tipo1 != tipo2:
                raise Exception(
                    f"Erro Semântico (Linha {linha}): Comparação entre tipos incompatíveis ({tipo1} e {tipo2})."
                )

            op = op_node["valor"]
            v1 = val1_node["valor"]
            v2 = val2_node["valor"]
            resultado = False

            if op == ">":
                resultado = v1 > v2
            elif op == "<":
                resultado = v1 < v2
            elif op == ">=":
                resultado = v1 >= v2
            elif op == "<=":
                resultado = v1 <= v2
            elif op == "==":
                resultado = v1 == v2
            elif op == "!=":
                resultado = v1 != v2

            return {"valor": resultado, "tipo_dado": "bool"}

        elif tipo_no == "BOOL_AND":
            lhs_node = self.visitar_no(no["lhs"])
            rhs_node = self.visitar_no(no["rhs"])

            if (
                lhs_node.get("tipo_dado") != "bool"
                or rhs_node.get("tipo_dado") != "bool"
            ):
                raise Exception(
                    f"Erro Semântico (Linha {self._get_linha(no)}): Operador 'and' requer operandos booleanos."
                )

            return {
                "valor": lhs_node.get("valor") and rhs_node.get("valor"),
                "tipo_dado": "bool",
            }

        elif tipo_no == "BOOL_OR":
            lhs_node = self.visitar_no(no["lhs"])
            rhs_node = self.visitar_no(no["rhs"])

            if (
                lhs_node.get("tipo_dado") != "bool"
                or rhs_node.get("tipo_dado") != "bool"
            ):
                raise Exception(
                    f"Erro Semântico (Linha {self._get_linha(no)}): Operador 'or' requer operandos booleanos."
                )

            return {
                "valor": lhs_node.get("valor") or rhs_node.get("valor"),
                "tipo_dado": "bool",
            }

        # --- NÓS FOLHA (Tokens) ---
        elif no.get("token") == "t_num":
            return {"valor": int(no["label"]), "tipo_dado": "int"}

        elif no.get("token") == "t_id":
            var_nome = no["label"]
            linha = self._get_linha(no)

            # Análise Semântica: Variável foi definida?
            if var_nome not in self.tabela_simbolos_global:
                raise Exception(
                    f"Erro Semântico (Linha {linha}): Variável '{var_nome}' usada antes de ser definida."
                )

            # Busca o valor e tipo da TDS
            return self.tabela_simbolos_global[var_nome]

        elif no.get("token") == "true":
            return {"valor": True, "tipo_dado": "bool"}

        elif no.get("token") == "false":
            return {"valor": False, "tipo_dado": "bool"}

        elif no.get("token") in [
            "+",
            "-",
            "*",
            "/",
            ">",
            "<",
            ">=",
            "<=",
            "==",
            "!=",
            "and",
            "or",
        ]:
            # Retorna o próprio operador para o nó pai usar
            return {"valor": no["label"], "tipo_dado": "operador"}

        # Se nenhum tipo de nó for reconhecido
        # print(f"Nó desconhecido encontrado: {no}")
        return None