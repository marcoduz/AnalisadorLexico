class GeradorCodigoIntermediario:
    def __init__(self):
        self.temp_contador = 0
        self.codigo_intermediario = []

    def novo_temp(self):
        """Gera um nome de variável temporária (t0, t1, t2...)"""
        temp = f"t{self.temp_contador}"
        self.temp_contador += 1
        return temp

    def emitir(self, codigo):
        """Adiciona uma linha de código à lista"""
        self.codigo_intermediario.append(codigo)

    def gerar(self, lista_asts: list):
        print("\n--- Gerando Código Intermediário (Etapa 3) ---")
        self.codigo_intermediario = []
        self.temp_contador = 0

        for ast in lista_asts:
            self.visitar_no(ast)
        
        # Imprime o resultado final
        print("Código Intermediário Gerado:")
        for linha in self.codigo_intermediario:
            print(linha)
        
        return self.codigo_intermediario

    def visitar_no(self, no: dict):
        if not isinstance(no, dict):
            return str(no)

        tipo_no = no.get("tipo_no")

        # --- ESTRUTURA DE BLOCO ---
        if tipo_no == "BLOCO_CODIGO":
            for instrucao in no.get("instrucoes", []):
                self.visitar_no(instrucao)
            return

        # --- ESTRUTURA DE CONTROLE (IF) - Opcional para o exemplo, mas útil ---
        elif tipo_no == "CODIGO_IF":
            # Exemplo simplificado apenas para não quebrar se tiver IF
            self.emitir("\n# Inicio IF")
            cond = self.visitar_no(no.get("condicao"))
            self.emitir(f"if {cond} goto L_THEN")
            self.visitar_no(no.get("bloco_then"))
            self.visitar_no(no.get("bloco_else"))
            return

        # --- GERAÇÃO PARA ATRIBUIÇÃO (SALVAR_VAR) ---
        # Regra: t_id = VAL EQ ;
        elif tipo_no == "SALVAR_VAR":
            var_destino = no["variavel"]["label"]
            
            # 1. Obter o primeiro operando (ex: '1' ou '$x')
            # 'expressao_val' é um nó VAL (t_num ou t_id)
            addr_esquerda = self.visitar_no(no["expressao_val"])
            
            # O resultado atual começa sendo o primeiro valor
            ultimo_temp = addr_esquerda

            # 2. Processar a cadeia de operações (EQ)
            # A estrutura é: EQ -> OP VAL EQ
            curr_eq = no["expressao_eq"]
            
            while curr_eq and curr_eq.get("tipo_no") == "EQ_RECURSIVO":
                # Pega o operador (+, -, *, /)
                op_node = curr_eq["operador"]
                operador = op_node["label"] # ou op_node["valor"] dependendo da construção

                # Pega o próximo operando (lado direito)
                addr_direita = self.visitar_no(curr_eq["valor"])

                # Gera um novo temporário para guardar o resultado parcial
                temp_result = self.novo_temp()

                # Emite a quádrupla: t_novo = t_anterior op operando
                # Ex: t0 = 1 + 2
                self.emitir(f"{temp_result} = {ultimo_temp} {operador} {addr_direita}")

                # O último temporário passa a ser o resultado atual
                ultimo_temp = temp_result

                # Avança para a próxima parte da expressão
                curr_eq = curr_eq["resto"]

            # 3. Atribuição final à variável do usuário
            # Ex: $var = t0
            self.emitir(f"{var_destino} = {ultimo_temp}")
            return

        # --- NÓS FOLHA / VALORES ---
        # Retornam seu rótulo para serem usados nas expressões
        elif no.get("token") == "t_num":
            return no["label"]

        elif no.get("token") == "t_id":
            return no["label"]
        
        # Caso genérico para bools ou outros
        elif "label" in no:
            return no["label"]

        return ""