# Compilador para a linguagem DOTH

Um compilador para a linguagem Doth, uma linguagem de programação baseada no idioma Dothraki, da série de TV e sequência de livros Game of Thrones.

## O que é a linguagem Doth?

A linguagem Doth é uma linguagem de programação inteiramente embasada no idioma Dothraki. Em homenagem à série que tomou o mundo e fez muito sucesso, a linguagem Doth foi criada.

Para isso, a linguagem busca incorporar alguns elementos do idioma e daqueles que a utilizavam, como por exemplo o tom alto e agressivo da fala, representado na linguagem pela necessidade de se escrever todos os comandos em caixa alta.

Do restante, a tipagem das variáveis e os comandos da linguagem são todos embasados na tradução dos comandos para o idioma dothraki, como exemplificado abaixo:

**Tipos de variáveis:**

- ASE -> String
- ATO -> Inteiro
- SOM -> Void
- TAWAK -> Booleano
- NAQIS -> Ponto Flutuante

**Comandos:**

- NAKHO -> End of statement/line
- FIN -> If
- ESHNA -> Else if
- NAKHAAN -> Else
- HAEI -> While
- EZAT -> Return
- FREDRIK -> Print

## Léxico:

**EBNF**: [Link](EBNF.md)


## Regras e limitações:

- Operações só são permitidas entre valores do mesmo tipo

## Funcionamento do Compilador

O compilador é operado através do código `main.py`, que reúne os arquivos `lexical.py`, `parser.py` e `codegen.py`, responsáveis por processar todo o código.

### Lexer

O arquivo de lexer faz uso do módulo `sly` para criar um analisador léxico de um arquivo. Nele definimos, com o uso de Regex Strings, qual o critério de cada um dos tokens que serão utilizados pelo parser.

### Parser

O arquivo do parser também faz uso do módulo `sly`. Nele definimos quais são as regras da linguagem, utilizando como base a EBNF. Cada regra definida é interpretada pelo parser no momento de análise do código. Ao ser interpretada, a função atrelada à regra é chamada.

As regras são definidas por misturas de Tokens e outras regras. Ao analisarmos, o encontro de um token retorna um token para a função, e o encontro de uma outra regra chama a função atrelada à essa segunda regra.

A maioria das funções gera um objeto do tipo `Node`. Esses nós são utilizados para gerar a AST, que futuramente será utilizada para a geração do código llvm.

### Codegen

A classe de codegen é utilizada para criar os objetos principais que serão utilizados na geração do código llvm. Além disso, também gera a função padrão de `printf`.

### Nodes

São os nós da AST. Ao serem avaliados, usam os objetos do Codegen para gerar o código da llvm.

## Como usar?

O compilador se utiliza de algumas bibliotecas que não são padrão do python. Por isso, será preciso instala-las para utilizá-lo.
Para isso, basta rodar o comando:

```bash
make config_env
```

Feito isso, você pode utilizar o programa rodando o seguinte comando:

```bash
make file=${path_to_file}
```

Atente-se ao fato de que a extensão de arquivos DothLang é .dt!

Você pode encontrar alguns exemplos de código dentro da pasta examples.
