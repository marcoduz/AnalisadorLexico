class GLC:
    def __init__(
        self,
        naoTerminais: list[str],
        terminais: list[str],
        simbolo_inicial: str,
        regras: list[str] = None,
        gramatica: dict[str, list[str]] = None,
    ):
        self.naoTerminais = naoTerminais
        self.terminais = terminais
        self.regras = regras if regras is not None else []
        self.gramatica = gramatica if gramatica is not None else {}
        self.simbolo_inicial = simbolo_inicial

    def criarGramatica(self):
        """
        Processa a lista de strings self.regras e a transforma
        em um dicionário self.gramatica.
        """
        self.gramatica.clear()
        for regra in self.regras:
            partes = regra.split("::=")
            if len(partes) == 2:
                estado = partes[0].strip()
                producao = partes[1].strip()

                if estado not in self.gramatica:
                    self.gramatica[estado] = []

                self.gramatica[estado].append(producao)

        self.naoTerminais = list(self.gramatica.keys())
