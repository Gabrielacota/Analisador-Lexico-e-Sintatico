# ficheiro: errors.py
# Integrante 5: Recuperação de Erros Léxicos e Sintáticos (Washington)
#
# Este módulo centraliza toda a lógica de tratamento de erros do compilador AraLang.
# Ele fornece:
#   1. t_error_handler  → para ser usado no lex.py (erros léxicos)
#   2. sintatico_error_handler  → para ser usado no parser.py (erros sintáticos, Panic Mode)
#   3. CompilerErrorLog → classe que acumula todos os erros encontrados durante a análise


# ==========================================
# 1. Classe de Registro de Erros
# ==========================================
class CompilerErrorLog:
    """
    Acumula todos os erros léxicos e sintáticos encontrados durante a compilação.
    Permite que o compilador continue após o primeiro erro (não aborta na primeira falha).
    """

    def __init__(self):
        self.errors = []       # Lista de dicionários com detalhes de cada erro
        self.warnings = []     # Lista de avisos (não fatais)

    def add_error(self, kind: str, message: str, line: int, value: str = ""):
        """Registra um erro com tipo, mensagem, linha e valor problemático."""
        entry = {
            "kind": kind,
            "message": message,
            "line": line,
            "value": value,
        }
        self.errors.append(entry)
        # Imprime imediatamente para dar feedback ao programador durante a análise
        print(f"[ERRO {kind}] Linha {line}: {message}" + (f" → '{value}'" if value else ""))

    def add_warning(self, message: str, line: int):
        """Registra um aviso (não impede a geração da AST)."""
        self.warnings.append({"message": message, "line": line})
        print(f"[AVISO] Linha {line}: {message}")

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def summary(self):
        """Imprime o resumo final após a análise completa."""
        print("\n" + "=" * 55)
        print("          RELATÓRIO FINAL DO COMPILADOR")
        print("=" * 55)
        if not self.errors and not self.warnings:
            print("  ✔  Nenhum erro encontrado. Compilação bem-sucedida.")
        else:
            print(f"  Erros encontrados   : {len(self.errors)}")
            print(f"  Avisos encontrados  : {len(self.warnings)}")
            print()
            if self.errors:
                print("  Detalhes dos erros:")
                for i, e in enumerate(self.errors, start=1):
                    valor = f" (valor: '{e['value']}')" if e["value"] else ""
                    print(f"    {i}. [{e['kind']}] Linha {e['line']}: {e['message']}{valor}")
        print("=" * 55 + "\n")


# ==========================================
# 2. Instância Global do Log
# ==========================================
# Importada pelos outros módulos para centralizar o registro de erros.
error_log = CompilerErrorLog()


# ==========================================
# 3. Handler de Erro Léxico  (t_error)
# ==========================================
# Cole esta função no lex.py (substituindo a implementação mínima atual),
# ou chame-a de dentro do t_error existente.
#
#   from errors import t_error_handler
#   def t_error(t):
#       t_error_handler(t)
#
def t_error_handler(t):
    """
    Chamado pelo PLY sempre que o lexer encontra um caractere que não
    corresponde a nenhuma regra definida.

    Estratégia de recuperação:
      - Registra o erro com número de linha.
      - Pula o caractere inválido (t.lexer.skip(1)) e continua a análise.
    """
    char = t.value[0]
    error_log.add_error(
        kind="LÉXICO",
        message=f"Caractere não reconhecido '{char}'",
        line=t.lineno,
        value=char,
    )
    t.lexer.skip(1)   # Descarta o caractere inválido e tenta continuar


# ==========================================
# 4. Handler de Erro Sintático  (p_error)
# ==========================================
# Cole esta função no parser.py como a regra p_error.
#
#   from errors import sintatico_error_handler
#   def p_error(p):
#       sintatico_error_handler(p)
#
def sintatico_error_handler(p):
    """
    Chamado pelo PLY (yacc) quando a sequência de tokens não obedece
    à gramática definida nas regras de produção.

    Estratégia: Panic Mode
      - Se 'p' for None → fim de arquivo inesperado.
      - Caso contrário → descarta tokens até encontrar um ';' ou '}' (âncoras de
        recuperação), depois retoma a análise. Isso permite que o compilador
        reporte múltiplos erros sintáticos em uma única execução.
    """
    if p is None:
        # O parser chegou ao fim do arquivo sem completar uma regra
        error_log.add_error(
            kind="SINTÁTICO",
            message="Fim de arquivo inesperado (estrutura incompleta)",
            line=0,
        )
        return

    error_log.add_error(
        kind="SINTÁTICO",
        message=f"Token inesperado '{p.value}'",
        line=p.lineno,
        value=str(p.value),
    )

    # --- Panic Mode: descarta tokens até uma âncora de sincronização ---
    # As âncoras ';' e '}' marcam o fim de instruções/blocos,
    # pontos seguros a partir dos quais a análise pode ser retomada.
    ANCHORS = {'PONTOVIRGULA', 'RCHAVE'}
    while True:
        tok = p.parser.token()       # Consome o próximo token do lexer
        if tok is None:              # Fim do arquivo
            break
        if tok.type in ANCHORS:
            break

    p.parser.restart()               # Reinicia o parser no estado inicial


# ==========================================
# 5. Exportações Públicas
# ==========================================
__all__ = [
    "CompilerErrorLog",
    "error_log",
    "t_error_handler",
    "sintatico_error_handler",
]