# ficheiro: parser.py
import ply.yacc as yacc
from ast_nodes import *

# Importamos os tokens gerados pelo Gabriel no módulo lex.py
# Isso é essencial para que o yacc reconheça a mesma linguagem
from lex import tokens
from errors import sintatico_error_handler, error_log

# ==========================================
# 1. Precedência de Operadores
# ==========================================
# Resolve ambiguidades da matemática (ex: multiplicação ocorre antes da soma)
precedence = (
    ('left', 'IGUAL', 'DIFERENTE', 'MENOR', 'MAIOR', 'MENOR_IGUAL', 'MAIOR_IGUAL'),
    ('left', 'SOMA', 'SUB'),
    ('left', 'MULT', 'DIV'),
)

# ==========================================
# 2. Regras de Produção da Gramática (BNF)
# ==========================================
# A regra principal (o axioma) - Um programa é uma lista de comandos
def p_programa(p):
    '''programa : lista_comandos'''
    p[0] = ProgramaNode(p[1])

# Permite que o programa tenha vários comandos em sequência
def p_lista_comandos_multiplos(p):
    '''lista_comandos : lista_comandos comando'''
    p[0] = p[1] + [p[2]]

# Caso base: o programa tem pelo menos um comando
def p_lista_comandos_simples(p):
    '''lista_comandos : comando'''
    p[0] = [p[1]]

# ==========================================
# 3. Definição dos Comandos Possíveis
# ==========================================
def p_comando(p):
    '''comando : atribuicao
               | condicional
               | repeticao
               | impressao'''
    p[0] = p[1]

# Regra de Atribuição (ex: x = 10;)
def p_atribuicao(p):
    '''atribuicao : ID ATRIBUICAO expressao PONTOVIRGULA'''
    p[0] = AtribuicaoNode(p[1], p[3])

# Regra de Impressão (ex: imprima(x);)
def p_impressao(p):
    '''impressao : IMPRIMA LPAREN expressao RPAREN PONTOVIRGULA'''
    p[0] = Print(p[3])

# ==========================================
# 4. Estruturas de Repetição e Condição
# ==========================================
# Regra do Loop "enquanto"
def p_repeticao(p):
    '''repeticao : ENQUANTO LPAREN condicao RPAREN LCHAVE lista_comandos RCHAVE'''
    p[0] = While(p[3], p[6])

# Regra do "se" simples
def p_condicional_simples(p):
    '''condicional : SE LPAREN condicao RPAREN LCHAVE lista_comandos RCHAVE'''
    p[0] = If(p[3], p[6])

# Regra do "se / senao"
def p_condicional_composta(p):
    '''condicional : SE LPAREN condicao RPAREN LCHAVE lista_comandos RCHAVE SENAO LCHAVE lista_comandos RCHAVE'''
    p[0] = IfElse(p[3], p[6], p[10])

# ==========================================
# 5. Condições Lógicas e Operadores Relacionais
# ==========================================
def p_condicao(p):
    '''condicao : expressao IGUAL expressao
                | expressao DIFERENTE expressao
                | expressao MENOR expressao
                | expressao MAIOR expressao
                | expressao MENOR_IGUAL expressao
                | expressao MAIOR_IGUAL expressao'''
    p[0] = CondicaoNode(p[2], p[1], p[3])

# ==========================================
# 6. Expressões Matemáticas
# ==========================================
def p_expressao_binaria(p):
    '''expressao : expressao SOMA expressao
                 | expressao SUB expressao
                 | expressao MULT expressao
                 | expressao DIV expressao'''
    p[0] = BinOpNode(p[2], p[1], p[3])

# Expressão agrupada por parênteses
def p_expressao_agrupada(p):
    '''expressao : LPAREN expressao RPAREN'''
    p[0] = p[2]

# Tipos de dados básicos suportados nas expressões
def p_expressao_numero(p):
    '''expressao : NUMERO'''
    p[0] = NumeroNode(p[1])

def p_expressao_id(p):
    '''expressao : ID'''
    p[0] = IdNode(p[1])

# ==========================================
# 7. Tratamento de Erros (Integrante 5 - Washington)
# ==========================================
# Delega ao módulo errors.py que implementa o Panic Mode:
# descarta tokens até encontrar ';' ou '}' e retoma a análise.
def p_error(p):
    sintatico_error_handler(p)

# Inicializa o parser
parser = yacc.yacc()

# ==========================================
# TESTE ISOLADO DO MÓDULO (Para você testar)
# ==========================================
if __name__ == '__main__':
    from lex import lexer

    codigo_teste = """
    x = 0;
    y = 10;
    enquanto (x < y) {
        se (x == 5) {
            imprima(x);
        } senao {
            x = x + 1;
        }
    }
    """

    print("Iniciando a Análise Sintática...")
    resultado = parser.parse(codigo_teste, lexer=lexer)

    print("\n--- ÁRVORE SINTÁTICA EM FORMATO HIERÁRQUICO ---")
    print(resultado.exibir())

    error_log.summary()
