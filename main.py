# ficheiro: main.py

import sys
from lex import lexer
from parser import parser
from errors import error_log


def imprimir_ast(ast):
    """
    Faz o pretty print da AST.
    Como todos os nós já possuem o método exibir(),
    basta chamar esse método.
    """
    print("\n" + "=" * 60)
    print("ÁRVORE SINTÁTICA ABSTRATA (AST)")
    print("=" * 60)
    print(ast.exibir())


def compilar(arquivo):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"Erro: arquivo '{arquivo}' não encontrado.")
        return

    print(f"\nCompilando: {arquivo}")

    ast = parser.parse(codigo, lexer=lexer)

    if ast:
        imprimir_ast(ast)

    error_log.summary()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso:")
        print("python main.py exemplo1.ara")
        sys.exit(1)

    compilar(sys.argv[1])