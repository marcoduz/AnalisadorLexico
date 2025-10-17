class SLR:
    """ """

    def __init__(self, dados_completos: dict, nao_terminais_gramatica: list[str]):
        self.producoes = []
        self.first_follow = {}
        self.tabela_action = {}
        self.tabela_transicao = {}
        self.nao_terminais_referencia = nao_terminais_gramatica

        if dados_completos:
            self.processar_dados(dados_completos)

    def processar_dados(self, dados: dict[str, list[str]]):
        self.producoes = dados.get("producoes", [])

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

    def exibir(self):
        """
        Imprime todas as tabelas salvas
        """
        print("\n" + "=" * 40)
        print(" DADOS DE PARSING SALVOS NA CLASSE")
        print("=" * 40 + "\n")

        print("--- Produções Numeradas ---\n")
        if self.producoes:
            for prod in self.producoes:
                print(prod)
        else:
            print("Nenhuma produção encontrada.")

        print("\n--- Tabela de FIRST e FOLLOW ---\n")
        if self.first_follow:
            print(f"{'Nonterminal':<15} | {'FIRST':<20} | {'FOLLOW':<20}")
            print("-" * 60)
            for nt, sets in self.first_follow.items():
                print(f"{nt:<15} | {sets['FIRST']:<20} | {sets['FOLLOW']:<20}")
        else:
            print("Nenhuma tabela de FIRST/FOLLOW encontrada.")
