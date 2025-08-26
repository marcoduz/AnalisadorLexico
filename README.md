# Gerador de Autômato Finito Determinístico (AFD)

## Descrição

Este projeto é uma ferramenta desenvolvida em Python para a área de compiladores e teoria da computação. O programa recebe como entrada um conjunto de **tokens** e **gramáticas não regulares** e, a partir deles, gera um **Autômato Finito Determinístico (AFD)**.

O autômato gerado é projetado para ser utilizado na construção de analisadores léxicos (scanners), que são a primeira fase de um compilador, responsáveis por reconhecer os padrões da linguagem de entrada.

## Funcionalidades

-   **Entrada**: Aceita definições de tokens e gramáticas não regulares como entrada.
-   **Processamento**: Converte as regras gramaticais em um Autômato Finito Determinístico, aplicando os algoritmos necessários para a conversão.
-   **Saída**: Gera uma representação clara do AFD, incluindo seus estados, alfabeto, função de transição, estado inicial e estados de aceitação.

## Tecnologias Utilizadas

-   **Linguagem**: Python 3.13.4

## Pré-requisitos

Para executar o projeto, você precisará ter o Python 3.13.4 (ou uma versão compatível) instalado em sua máquina.

-   [Download do Python](https://www.python.org/downloads/)

## Como Usar

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/GERADORDOAFD.git](https://github.com/seu-usuario/GERADORDOAFD.git)
    ```

2.  **Navegue até o diretório do projeto:**
    ```bash
    cd GERADORDOAFD
    ```

3.  **Execute o programa:**
    *(Adapte esta seção para a forma como seu programa é executado. Abaixo está um exemplo)*
    ```bash
    python main.py < arquivo_de_entrada.txt
    ```
    Certifique-se de fornecer os arquivos de entrada necessários (com os tokens e a gramática), conforme a implementação do seu programa.

## Exemplo de Uso

*(Opcional: Se você tiver um exemplo claro de entrada e saída, pode adicioná-lo aqui para facilitar o entendimento.)*

**Entrada (exemplo de arquivo `gramatica.txt`):**
```
DIGITO=[0-9]
LETRA=[a-zA-Z]
ID={LETRA}({LETRA}|{DIGITO})*
```

**Saída (exemplo):**
```
Autômato Finito Determinístico gerado:
Estados: {q0, q1, q2}
Alfabeto: {letra, digito}
Estado Inicial: q0
Estados Finais: {q2}
Transições:
  - (q0, letra) -> q1
  - (q1, letra) -> q2
  - (q1, digito) -> q2
  ...
```

## Autor

-   **Marco Antonio Duz**
-   **GitHub**: `https://github.com/marcoduz`
