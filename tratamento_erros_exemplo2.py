# ficheiro: teste_integrante5.py
from lex import lexer
from errors import error_log

with open('exemplo2.ara', 'r', encoding='utf-8') as f:
    codigo = f.read()

lexer.input(codigo)

print("=" * 55)
print("         TOKENS RECONHECIDOS")
print("=" * 55)

for tok in lexer:
    print(f"Tipo: {tok.type:<15} | Valor: {str(tok.value):<10} | Linha: {tok.lineno}")

error_log.summary()