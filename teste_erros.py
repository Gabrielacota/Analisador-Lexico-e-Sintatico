# ficheiro: tratamento_erros_exemplo2.py
# Roda: python tratamento_erros_exemplo2.py

from lex import lexer
from parser import parser
from errors import error_log

with open('exemplo2.ara', 'r', encoding='utf-8') as f:
    codigo = f.read()

print("=" * 55)
print("     ANÁLISE LÉXICA + SINTÁTICA DO EXEMPLO 2")
print("=" * 55 + "\n")

parser.parse(codigo, lexer=lexer)

error_log.summary()