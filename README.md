# Analisador-Lexico-e-Sintatico - AraLang

## Detalhamento do Projeto

### Analisador Sintático com AST O.O.

Este projeto consiste na implementação dos analisadores léxico e sintático para a **AraLang**, uma linguagem procedural didática estruturada em blocos com chaves `{}`. 

O compilador utiliza a biblioteca `PLY (Python Lex-Yacc)` para realizar a tokenização e a construção de uma Árvore Sintática Abstrata (AST) totalmente representada por estruturas puras de `Orientação a Objetos`, gerando saídas hierárquicas ramificadas no terminal.

## Propósito

Este projeto tem como objetivo aplicar, na prática, os conhecimentos adquiridos na disciplina de **Compiladores**, por meio da utilização de ferramentas de análise léxica (Regex), gramáticas livres de contexto (BNF) e mapeamento de árvores sintáticas baseadas em nós operacionais.

## Estrutura do Projeto

- `lex.py`: Motor léxico desenvolvido para ler o código-fonte da AraLang, realizar o casamento de padrões via expressões regulares, descartar elementos invisíveis (espaços e comentários) e emitir o fluxo estruturado de tokens.
- `ast_nodes.py`: Declaração das classes que moldam a Árvore Sintática Abstrata (AST). Implementa a lógica recursiva e o gerenciamento de prefixos para a renderização dos galhos no console.
- `parser.py`: Ponto de entrada e coração do analisador sintático (Yacc). Valida as regras de produção gramaticais, consome os delimitadores e instancia os objetos da AST. Contém também o script de execução e testes automatizados.

## Como Usar

### Pré-requisitos

- **Python 3.x** instalado na máquina.
- Biblioteca **PLY** (`pip install ply`).

### Execução

1. Clone o repositório:
```bash
git clone [https://github.com/Gabrielacota/Analisador-Lexico-e-Sintatico.git](https://github.com/Gabrielacota/Analisador-Lexico-e-Sintatico.git)
```

2. Acesse o diretório:
```bash
cd Analisador-Lexico-e-Sintatico
```

3. Instale as dependências:
```bash
pip install ply
```

4. Execute o analisador sintático:
```bash
python parser.py
```

## Funcionamento

O interpretador recebe uma string de código escrito em AraLang contendo estruturas de repetição (`enquanto`), condicionais (`se`/`senao`), blocos de comandos delimitados e expressões aritméticas.

Durante o processamento, caracteres puramente estruturais e delimitadores como `;`, `{`, `}`, `(` e `)` são completamente consumidos e descartados pelo parser, de modo que apenas a verdadeira semântica operacional e as dependências lógicas sejam acopladas e exibidas na árvore de destino.

## Exemplo de Código e Saída da AST

O bloco de testes integrado simula um script em AraLang focado em controle de fluxo, contendo um laço de repetição (`enquanto`) com uma condicional aninhada (`se`/`senao`), além de operações matemáticas básicas:

### Código-Fonte Simulado:
```plaintext
x = 0;
y = 10;
enquanto (x < y) {
    se (x == 5) {
        imprima(x);
    } senao {
        x = x + 1;
    }
}
```

### Saída Gerada no Terminal (AST):
```plaintext
Iniciando a Análise Sintática...

--- ÁRVORE SINTÁTICA DA ARALANG ---
ProgramaNode
├── Assign (=)
│   ├── Identifier: x
│   └── LiteralInt: 0
├── Assign (=)
│   ├── Identifier: y
│   └── LiteralInt: 10
└── While
    ├── [Condition]
    │   └── Op(<)
    │       ├── Identifier: x
    │       └── Identifier: y
    └── [Body Bloco]
        └── IfElse
            ├── [Condition]
            │   └── Op(==)
            │       ├── Identifier: x
            │       └── LiteralInt: 5
            ├── [Then Bloco]
            │   └── Print
            │       └── Identifier: x
            └── [Else Bloco]
                └── Assign (=)
                    ├── Identifier: x
                    └── Op(+)
                        ├── Identifier: x
                        └── LiteralInt: 1
```

## Infraestrutura

O projeto segue princípios de:

- Configuração e execução direta via script principal (`parser.py`).
- Modularização desacoplada entre Léxico, Sintático e Nós da Árvore.
- Visualização hierárquica legível por meio de ramificações estruturadas (`├──` e `└──`).

## Tecnologias Utilizadas

`Python`, `PLY (Python Lex-Yacc)`, `Expressões Regulares (Regex)`, `Gramática BNF` e `Orientação a Objetos`.

## Equipe

- **Gabriela Cota**
- **Rian Carlos**
- **Mayara Barbosa**
- **Washington Medeiros**
- **Gabriel Ferreira Lima**
```

```
