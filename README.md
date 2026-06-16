# Analisador Léxico e Sintático - AraLang 🔤

Um compilador didático implementando análise léxica e sintática para **AraLang**, uma linguagem procedural estruturada com foco educacional na disciplina de Compiladores.

## 📋 Sobre o Projeto

### O que é?

Este projeto implementa um **analisador léxico e sintático** completo para a **AraLang**, uma linguagem procedural didática estruturada em blocos com chaves `{}`. 

O compilador utiliza a biblioteca **PLY (Python Lex-Yacc)** para realizar:
- **Tokenização** através de expressões regulares
- **Construção de AST (Árvore Sintática Abstrata)** em puro Orientação a Objetos
- **Renderização hierárquica** da árvore no terminal

### Propósito

Aplicar na prática conhecimentos adquiridos na disciplina de **Compiladores**, explorando:
- Análise léxica com Regex
- Gramáticas livres de contexto (BNF)
- Mapeamento de árvores sintáticas com nós operacionais
- Recuperação de erros em análise léxica e sintática

## 📂 Estrutura do Projeto

| Arquivo | Descrição |
|---------|-----------|
| `lex.py` | **Motor Léxico**: Lê o código-fonte, realiza casamento de padrões via regex, descarta espaços e comentários, emite fluxo de tokens |
| `ast_nodes.py` | **Nós da AST**: Classes que moldam a Árvore Sintática Abstrata com lógica recursiva e renderização em console |
| `parser.py` | **Analisador Sintático (Yacc)**: Valida regras gramaticais, consome delimitadores, instancia objetos da AST |
| `errors.py` | **Gerenciador de Erros**: Registra e exibe erros léxicos e sintáticos com recuperação inteligente |
| `main.py` | **Interface Principal**: Script CLI que aceita arquivo `.ara` como entrada e exibe a AST |
| `teste_erros.py` | **Suite de Testes**: Testes automatizados para validar recuperação de erros |
| `exemplo1.ara` | **Exemplo Válido**: Implementação da sequência de Fibonacci |
| `exemplo2.ara` | **Exemplo com Erros**: Demonstração de recuperação de erros léxicos e sintáticos |

## 🚀 Como Usar

### Pré-requisitos

- **Python 3.8+** instalado na máquina
- Biblioteca **PLY** 

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Gabrielacota/Analisador-Lexico-e-Sintatico.git
cd Analisador-Lexico-e-Sintatico
```

2. Instale as dependências:
```bash
pip install ply
```

### Uso

#### Compilar um arquivo AraLang:
```bash
python main.py exemplo1.ara
```

#### Executar os testes automatizados:
```bash
python teste_erros.py
```

## 🔍 Linguagem AraLang

### Recursos Suportados

A linguagem AraLang suporta:

| Recurso | Descrição | Exemplo |
|---------|-----------|---------|
| **Variáveis** | Identificadores de nomes livres | `x = 10;` |
| **Tipos** | Inteiros e floats | `a = 5; b = 3.14;` |
| **Operadores Aritméticos** | `+`, `-`, `*`, `/` | `resultado = x + y;` |
| **Operadores Relacionais** | `<`, `>`, `==`, `!=`, `<=`, `>=` | `se (x > y) {...}` |
| **Condicionais** | `se` / `senao` | `se (cond) {...} senao {...}` |
| **Laços** | `enquanto` | `enquanto (cond) {...}` |
| **Funções Nativas** | `imprima()` | `imprima(x);` |
| **Blocos** | Delimitados por `{}` | `{ cmd1; cmd2; }` |
| **Comentários** | `//` para linha | `// comentário` |

## 📊 Funcionamento

### Processo de Compilação

1. **Análise Léxica** (`lex.py`)
   - Lê o código-fonte caractere por caractere
   - Agrupa em tokens usando expressões regulares
   - Descarta espaços em branco e comentários
   - Valida caracteres permitidos

2. **Análise Sintática** (`parser.py`)
   - Valida a sequência de tokens contra a gramática BNF
   - Consome delimitadores estruturais (`;`, `{}`, `()`)
   - Instancia objetos da AST representando a semântica do código
   - Recupera de erros quando possível

3. **Geração da AST** (`ast_nodes.py`)
   - Cada construção sintática é um nó (classe) especializado
   - Nós contêm referências a sub-nós (hierarquia)
   - Método `exibir()` renderiza a árvore no console com indentação

### Recuperação de Erros

O compilador implementa **recuperação inteligente de erros**:
- Reporta erros léxicos com linha e caractere problemático
- Continua tokenização ignorando caracteres inválidos
- Implementa **Panic Mode** para erros sintáticos
- Tenta recuperar o parsing após encontrar erro
- Gera AST parcial do código válido

## 📋 Exemplos

### Exemplo 1: Sequência de Fibonacci

**Arquivo**: `exemplo1.ara`
```ara
a = 0;
b = 1;
contador = 0;
limite = 10;

enquanto (contador < limite) {
    se (contador == 0) {
        imprima(a);
    } senao {
        se (contador == 1) {
            imprima(b);
        } senao {
            proximo = a + b;
            imprima(proximo);
            a = b;
            b = proximo;
        }
    }
    contador = contador + 1;
}
```

**Execução**:
```bash
python main.py exemplo1.ara
```

### Exemplo 2: Teste de Recuperação de Erros

**Arquivo**: `exemplo2.ara`
Contém erros intencionais para demonstrar recuperação:
- Erros léxicos: caracteres inválidos (`@`, `#`, `$`)
- Erros sintáticos: parêntese não fechado
- Expressões incompletas

**Execução**:
```bash
python main.py exemplo2.ara
```

### Saída da AST (Exemplo)

```
============================================================
ÁRVORE SINTÁTICA ABSTRATA (AST)
============================================================
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

## 🧪 Testes

O projeto inclui uma suite de testes automatizados:

```bash
python teste_erros.py
```

Os testes validam:
- Recuperação de erros léxicos
- Recuperação de erros sintáticos
- Geração correta de AST
- Casos limítrofes (edge cases)

## 🏗️ Arquitetura

### Padrões de Design

- **Modularização**: Separação clara entre léxica, sintática e representação da AST
- **Orientação a Objetos**: Cada nó da AST é uma classe especializada
- **Visitante Implícito**: Método `exibir()` em cada nó para renderização
- **Gerenciamento de Erro Centralizado**: Módulo `errors.py` para tratamento unificado

### Fluxo de Dados

```
Código-Fonte (.ara)
    ↓
Análise Léxica (lex.py)
    ↓
Fluxo de Tokens
    ↓
Análise Sintática (parser.py)
    ↓
Árvore Sintática Abstrata (ast_nodes.py)
    ↓
Renderização no Console
```

## 📚 Tecnologias

- **Python** 3.8+
- **PLY (Python Lex-Yacc)** - Gerador de analisadores léxicos e sintáticos
- **Expressões Regulares (Regex)** - Tokenização
- **Gramática Livre de Contexto (BNF)** - Especificação sintática
- **Orientação a Objetos (OO)** - Arquitetura da AST

## 👥 Autores

- **Gabriela Cota** — Coordenação
- **Rian Carlos** — Desenvolvimento
- **Mayara Barbosa** — Testes
- **Washington Medeiros** — Análise
- **Gabriel Ferreira Lima** — Documentação


**Desenvolvido como trabalho prático da disciplina de Compiladores** 🎓
