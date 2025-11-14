# AnalisadorLexico/analisador_sintatico/analisador_semantico.py
# NOVO ARQUIVO


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

        print("\n" + "=" * 50)
        print(" INICIANDO ANÁLISE SEMÂNTICA (Etapa 2)")
        print("=" * 50 + "\n")

        for ast_raiz in lista_asts:
            linha = self._get_linha(ast_raiz)
            try:
                self.visitar_no(ast_raiz)

                print(f"Linha {linha}: Análise Semântica Aceita.")

            except Exception as e:
                print(f"\nLinha {linha}: Rejeitada (Semântica)")
                print(f"  --> {e}")

            print("\n" + "---" * 10)

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

            # Visita os filhos para obter seus valores e tipos
            val_node = self.visitar_no(no["expressao_val"])
            eq_node = self.visitar_no(no["expressao_eq"])

            # --- Início da Análise Semântica (Lógica do 'executar_acao_semantica' original) ---
            if val_node.get("tipo_dado") != "int" or eq_node.get("tipo_dado") != "int":
                raise Exception(
                    f"Erro Semântico (Linha {linha}): Tipos incompatíveis na atribuição da variável '{var_nome}'."
                )

            var_valor = val_node["valor"] + eq_node["valor"]
            var_tipo = "int"  # Assumindo que todas as atribuições são int

            # Atualiza ou insere na Tabela de Símbolos Global
            self.tabela_simbolos_global[var_nome] = {
                "valor": var_valor,
                "tipo_dado": var_tipo,
            }
            print(
                f"[AÇÃO SEMÂNTICA (Linha {linha})]: Variável '{var_nome}' definida como {var_valor} (Tipo: {var_tipo})"
            )
            return None  # Atribuição não retorna valor

        # --- NÓS DE EXPRESSÃO ARITMÉTICA ---
        elif tipo_no == "EQ_RECURSIVO":
            # Visita os filhos
            op_node = self.visitar_no(no["operador"])
            val_node = self.visitar_no(no["valor"])
            eq_node = self.visitar_no(no["resto"])  # O resultado do resto da expressão
            linha = self._get_linha(no)

            if val_node.get("tipo_dado") != "int" or eq_node.get("tipo_dado") != "int":
                raise Exception(
                    f"Erro Semântico (Linha {linha}): Operação aritmética com tipos incompatíveis (esperado 'int')."
                )

            operador = op_node["valor"]  # O 'valor' de um nó OP é seu label
            v_val = val_node["valor"]
            v_eq = eq_node["valor"]

            resultado = 0
            if operador == "+":
                resultado = v_val + v_eq
            elif operador == "-":
                resultado = v_val - v_eq
            elif operador == "*":
                resultado = v_val * v_eq
            elif operador == "/":
                if v_eq == 0:
                    raise Exception(
                        f"Erro Semântico (Linha {linha}): Divisão por zero."
                    )
                resultado = int(v_val / v_eq)

            return {"valor": resultado, "tipo_dado": "int"}

        elif tipo_no == "EQ_EPSILON":
            # Caso base da recursão de expressão: ε (identidade)
            return {"valor": 0, "tipo_dado": "int"}

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
