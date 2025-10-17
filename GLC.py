# No seu arquivo GLC.py

from AFND import AFND


class GLC:
    def __init__(
        self,
        naoTerminais: list[str],
        terminais: list[str],
        regras: list[str] = None,
        gramatica: dict[str, list[str]] = None,
    ):
        self.naoTerminais = naoTerminais
        self.terminais = terminais
        self.regras = regras if regras is not None else []
        self.gramatica = gramatica if gramatica is not None else {}
        self.simbolo_inicial = None

    def criarRegrasPartirDoAFD(self, afd: AFND):
        self.regras.clear()
        self.naoTerminais = list(afd.estados)
        self.terminais = list(afd.alfabeto)
        self.simbolo_inicial = f"{afd.estadoInicial}"

        for (estado, simbolo), destinos in afd.transicoes.items():
            if destinos:
                proximoEstado = list(destinos)[0]
                nova_regra = f"{estado} ::= '{simbolo}' {proximoEstado}"
                self.regras.append(nova_regra)

        for estado_final in afd.estadosFinais:
            nova_regra = f"{estado_final} ::= "
            self.regras.append(nova_regra)

        self.criarGramatica()

    def criarGramatica(self):
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
