# ficheiro: lex.py
import ply.lex as lex

# ==========================================
# 1. Mapeamento de Palavras Reservadas
# ==========================================
# Utilizamos um dicionário para garantir que palavras como "senao" 
# não sejam confundidas com identificadores comuns de variáveis.
reservadas = {
    'se': 'SE',
    'senao': 'SENAO',
    'enquanto': 'ENQUANTO',
    'imprima': 'IMPRIMA'
}

# ==========================================
# 2. Definição Oficial dos Tokens
# ==========================================
tokens = [
    'ID', 'NUMERO',
    # Operadores Matemáticos
    'SOMA', 'SUB', 'MULT', 'DIV',
    # Operadores Relacionais e de Atribuição
    'ATRIBUICAO', 'IGUAL', 'MENOR', 'MAIOR', 
    'MENOR_IGUAL', 'MAIOR_IGUAL', 'DIFERENTE',
    # Delimitadores de Escopo e Fim de Instrução
    'LPAREN', 'RPAREN', 'LCHAVE', 'RCHAVE', 'PONTOVIRGULA'
] + list(reservadas.values())

# ==========================================
# 3. Expressões Regulares (Regex) Simples
# ==========================================
t_SOMA          = r'\+'
t_SUB           = r'-'
t_MULT          = r'\*'
t_DIV           = r'/'
t_IGUAL         = r'=='
t_ATRIBUICAO    = r'='
t_MENOR_IGUAL   = r'<='
t_MAIOR_IGUAL   = r'>='
t_MENOR         = r'<'
t_MAIOR         = r'>'
t_DIFERENTE     = r'!='
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LCHAVE        = r'\{'
t_RCHAVE        = r'\}'
t_PONTOVIRGULA  = r';'

# ==========================================
# 4. Regras e Ignorados
# ==========================================
# Ignorar espaços em branco e tabulações
t_ignore = ' \t'

# Acompanhar a contagem de linhas (crucial para o Integrante 5 reportar erros depois)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar comentários (ex: // este é um comentário)
def t_ignore_COMENTARIO(t):
    r'//.*'
    pass

# ==========================================
# 5. Expressões Regulares Complexas (Funções)
# ==========================================
# Identificadores e verificação de palavras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value, 'ID')  # Verifica no dicionário
    return t

# Números (Suporta inteiros e decimais)
def t_NUMERO(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# ==========================================
# 6. Tratamento de Erros (Fallback)
# ==========================================
# Implementação mínima para garantir que o lexer roda isoladamente.
# O Integrante 5 irá expandir esta lógica no ficheiro errors.py.
def t_error(t):
    print(f"[Aviso Léxico] Caractere não reconhecido '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Inicialização do motor léxico
lexer = lex.lex()

# ==========================================
# TESTE ISOLADO DO MÓDULO (Para o Integrante 1)
# ==========================================
if __name__ == '__main__':
    codigo_teste = """
    x = 0;
    y = 10;
    // Iniciando o loop de teste
    enquanto (x < y) {
        se (x == 5) {
            imprima(x);
        } senao {
            x = x + 1;
        }
    }
    """
    print("A testar a tokenização...\n")
    lexer.input(codigo_teste)
    
    for tok in lexer:
        print(f"Tipo: {tok.type:<12} | Valor: {tok.value:<10} | Linha: {tok.lineno}")