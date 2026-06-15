class ASTNode:
    def exibir(self, prefixo="", ultimo=True):
        """Método base que gera os galhos da árvore automaticamente."""
        raise NotImplementedError()

# ==========================================
# 1. Nó Raiz do Programa
# ==========================================
class ProgramaNode(ASTNode):
    # Nó raiz que armazena a lista completa de comandos
    def __init__(self, comandos):
        self.comandos = comandos  

    def exibir(self, prefixo="", ultimo=True):
        resultado = "ProgramaNode\n"
        total = len(self.comandos)
        for i, cmd in enumerate(self.comandos):
            eh_ultimo = (i == total - 1)
            resultado += cmd.exibir(prefixo, eh_ultimo)
        return resultado

# ==========================================
# 2. Definição dos Comandos Básicos
# ==========================================
class AtribuicaoNode(ASTNode):
    # Armazena o identificador da variável e seu respectivo valor
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor

    def exibir(self, prefixo="", ultimo=True):
        marcador = "└── " if ultimo else "├── "
        resultado = f"{prefixo}{marcador}Assign (=)\n"
        
        # Prepara o prefixo para os filhos do nó de atribuição
        proximo_prefixo = prefixo + ("    " if ultimo else "│   ")
        
        resultado += f"{proximo_prefixo}├── Identifier: {self.nome}\n"
        resultado += self.valor.exibir(proximo_prefixo, ultimo=True)
        return resultado

class Print(ASTNode):
    # Representa a instrução de saída de dados (imprima)
    def __init__(self, expressao):
        self.expressao = expressao

    def exibir(self, prefixo="", ultimo=True):
        marcador = "└── " if ultimo else "├── "
        resultado = f"{prefixo}{marcador}Print\n"
        
        proximo_prefixo = prefixo + ("    " if ultimo else "│   ")
        resultado += self.expressao.exibir(proximo_prefixo, ultimo=True)
        return resultado

# ==========================================
# 3. Estruturas de Repetição e Condição
# ==========================================
class If(ASTNode):
    # Estrutura condicional simples (se)
    def __init__(self, condicao, bloco):
        self.condicao = condicao
        self.bloco = bloco

    def exibir(self, prefixo="", ultimo=True):
        marcador = "└── " if ultimo else "├── "
        resultado = f"{prefixo}{marcador}If\n"
        
        proximo_prefixo = prefixo + ("    " if ultimo else "│   ")
        resultado += f"{proximo_prefixo}├── [Condition]\n"
        resultado += self.condicao.exibir(proximo_prefixo + "│   ", ultimo=True)
        
        resultado += f"{proximo_prefixo}└── [Then Bloco]\n"
        total = len(self.bloco)
        for i, cmd in enumerate(self.bloco):
            resultado += cmd.exibir(proximo_prefixo + "    ", i == total - 1)
        return resultado

class IfElse(ASTNode):
    # Estrutura condicional composta (se / senao)
    def __init__(self, condicao, bloco_if, bloco_else):
        self.condicao = condicao
        self.bloco_if = bloco_if
        self.bloco_else = bloco_else

    def exibir(self, prefixo="", ultimo=True):
        marcador = "└── " if ultimo else "├── "
        resultado = f"{prefixo}{marcador}IfElse\n"
        
        proximo_prefixo = prefixo + ("    " if ultimo else "│   ")
        resultado += f"{proximo_prefixo}├── [Condition]\n"
        resultado += self.condicao.exibir(proximo_prefixo + "│   ", ultimo=True)
        
        resultado += f"{proximo_prefixo}├── [Then Bloco]\n"
        for i, cmd in enumerate(self.bloco_if):
            resultado += cmd.exibir(proximo_prefixo + "│   ", i == len(self.bloco_if) - 1)
            
        resultado += f"{proximo_prefixo}└── [Else Bloco]\n"
        for i, cmd in enumerate(self.bloco_else):
            resultado += cmd.exibir(proximo_prefixo + "    ", i == len(self.bloco_else) - 1)
        return resultado

class While(ASTNode):
    # Estrutura de repetição baseada em uma condição (enquanto)
    def __init__(self, condicao, bloco):
        self.condicao = condicao
        self.bloco = bloco

    def exibir(self, prefixo="", ultimo=True):
        marcador = "└── " if ultimo else "├── "
        resultado = f"{prefixo}{marcador}While\n"
        
        proximo_prefixo = prefixo + ("    " if ultimo else "│   ")
        resultado += f"{proximo_prefixo}├── [Condition]\n"
        resultado += self.condicao.exibir(proximo_prefixo + "│   ", ultimo=True)
        
        resultado += f"{proximo_prefixo}└── [Body Bloco]\n"
        total = len(self.bloco)
        for i, cmd in enumerate(self.bloco):
            resultado += cmd.exibir(proximo_prefixo + "    ", i == total - 1)
        return resultado

# ==========================================
# 4. Condições Lógicas e Operadores Relacionais
# ==========================================
class CondicaoNode(ASTNode):
    # Operações relacionais de comparação (==, !=, <, >, <=, >=)
    def __init__(self, operador, esq, dir):
        self.operador = operador  
        self.esq = esq            
        self.dir = dir            

    def exibir(self, prefixo="", ultimo=True):
        marcador = "└── " if ultimo else "├── "
        resultado = f"{prefixo}{marcador}Op({self.operador})\n"
        
        proximo_prefixo = prefixo + ("    " if ultimo else "│   ")
        resultado += self.esq.exibir(proximo_prefixo, ultimo=False)
        resultado += self.dir.exibir(proximo_prefixo, ultimo=True)
        return resultado

# ==========================================
# 5. Expressões Matemáticas e Nós Terminais
# ==========================================
class BinOpNode(ASTNode):
    # Operações matemáticas binárias (+, -, *, /)
    def __init__(self, operador, esq, dir):
        self.operador = operador  
        self.esq = esq
        self.dir = dir

    def exibir(self, prefixo="", ultimo=True):
        marcador = "└── " if ultimo else "├── "
        resultado = f"{prefixo}{marcador}Op({self.operador})\n"
        
        proximo_prefixo = prefixo + ("    " if ultimo else "│   ")
        resultado += self.esq.exibir(proximo_prefixo, ultimo=False)
        resultado += self.dir.exibir(proximo_prefixo, ultimo=True)
        return resultado

class NumeroNode(ASTNode):
    # Nó terminal para valores numéricos (int ou float)
    def __init__(self, valor):
        self.valor = valor  

    def exibir(self, prefixo="", ultimo=True):
        marcador = "└── " if ultimo else "├── "
        return f"{prefixo}{marcador}LiteralInt: {self.valor}\n"

class IdNode(ASTNode):
    # Nó terminal que armazena strings de identificadores
    def __init__(self, nome):
        self.nome = nome  

    def __repr__(self):
         return f"IdNode('{self.nome}')"

    def exibir(self, prefixo="", ultimo=True):
        marcador = "└── " if ultimo else "├── "
        return f"{prefixo}{marcador}Identifier: {self.nome}\n"