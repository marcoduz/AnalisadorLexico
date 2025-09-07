# Gerador de Autômato Finito Determinístico (AFD)

## Descrição

Este projeto é uma ferramenta desenvolvida em Python para a matéria de construção de compiladoreso, do curso de Ciêncida da computação - UFFS. O programa recebe como entrada um conjunto de **tokens** e **gramáticas não regulares** e, a partir deles, gera um **Autômato Finito Determinístico (AFD)**. 

Este então é utilizado para efetuar a análise léxica de um **código**, também inserido como entrada em um arquivo.

## Funcionalidades

- **Entradas**: 
 - Arquivo contendo o código a ser analisado pelo analisador lexico caminho ./arquivos/tokens.txt
 - No próprio códico inserir um array com os tokens, ['if', 'else'] e outro com as gramáticas, [['S::=aS|bS|']], para o épson finalizar com | as produções 
- **Processamento**: Converte as regras gramaticais em um Autômato Finito Determinístico, aplicando a seguinte sequência:
  - Montar Autômatos Finitos Não Determinísticos (AFND), um para cada token e gramática.
  - Unir todos os AFNDs gerados anteriormente em um único.
  - Determinizar o AFND resultante para gerar o AFD final.
Após efetua a leitura do codigo.txt simulando a leitura de um código e gera a fita e tabela de símbolos da análise léxica do arquivo considerando os tokens e gramáticas inseirdas anteriormente
- **Saída**: Fita e tabela de símbolos.

## Tecnologias Utilizadas

- **Linguagem**: Python 3.13.4

## Pré-requisitos

Para executar o projeto, você precisará ter o Python 3.13.4 (ou uma versão compatível) instalado em sua máquina.

- [Download do Python](https://www.python.org/downloads/)

## Como Usar

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/marcoduz/AnalisadorLexico.git
    ```

2.  **Navegue até o diretório do projeto:**

    ```bash
    cd AnalisadorLexico
    ```

3.  **Execute o programa:**
   Insira o código a ser análisado dentro da pasta arquivos com o nome codigo.txt em seguida rode o comando abaixo:

    ```bash
    python main.py
    ```
    Certifique-se de iniciar as variáveis no arquivo main.py com seus tokens e gramáticas como no exemplo abaixo

    ```bash
    tokens = ['se', 'sai', 'foi']
    gramaticas = [['S::=fA|aA|eA|iA', 'A::=fA|aA|eA|iA|']]
    ```
    
## Autores

- **Marco Antonio Duz**
- **Mátriculo**: 2311100006

- **Carlos Giovane Neu Nogueira**
- **Mátriculo**: 2311100010
