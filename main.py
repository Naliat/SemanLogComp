import sys
import ply.lex as lex
import ply.yacc as yacc
import graphviz

tokens = (
    'VARIAVEL',
    'AND',
    'OR',
    'IMPLIES',
    'IFF',
    'NOT',
    'LPAREN',
    'RPAREN',
    'NOR', 
    'NAND'
)

t_AND       = r'\^|\&'
t_OR        = r'\|'
t_IMPLIES   = r'->'
t_IFF       = r'<->'
t_NOT       = r'~|!'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_NOR       = r'v' # Usando 'v' minúsculo para NOR
t_NAND      = r'\^' # Usando '^' minúsculo para NAND (colidiria com AND, cuidado!)

# Para variáveis, permitimos letras minúsculas
def t_VARIAVEL(t):
    r'[a-z]'
    return t

# Ignorar espaços e tabs
t_ignore = ' \t'

# Tratamento de erros de caracteres inválidos
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na posição {t.lexpos}")
    t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex()

# --- Definição da Árvore Sintática Abstrata (AST) ---
class Node:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.value = value
        if children:
            self.children = children
        else:
            self.children = []

    def __repr__(self):
        if self.value:
            return f"Node({self.type}, value='{self.value}')"
        return f"Node({self.type})"

# --- Precedência dos Operadores (para o Parser) ---
# Da menor para a maior precedência
precedence = (
    ('left', 'IFF'),
    ('left', 'IMPLIES'),
    ('left', 'OR', 'NOR'),
    ('left', 'AND', 'NAND'), # NAND e AND têm a mesma precedência
    ('right', 'NOT'),
)

# Mapeamento para representação de string
OP_MAP = {
    'AND': '&',
    'OR': '|',
    'IMPLIES': '->',
    'IFF': '<->',
    'NOT': '~',
    'NOR': 'v', # Usando 'v' para NOR na saída
    'NAND': '^' # Usando '^' para NAND na saída
}

# Precedência numérica para a reconstrução de string (quanto maior, maior a precedência)
OP_PRECEDENCE = {
    'IFF': 1,
    'IMPLIES': 2,
    'OR': 3,
    'NOR': 3,
    'AND': 4,
    'NAND': 4,
    'NOT': 5,
    'VARIAVEL': 6 # Variáveis têm a maior "precedência" (não precisam de parênteses)
}

# --- Regras da Gramática (Análise Sintática) ---
def p_expression_binop(p):
    '''
    expression : expression AND expression
               | expression OR expression
               | expression IMPLIES expression
               | expression IFF expression
               | expression NOR expression
               | expression NAND expression
    '''
    # p[2] é o operador (string do token), ex: '&', '|', '->'
    # Convertemos para o nome do tipo de nó, ex: 'AND', 'OR'
    node_type = ''
    if p[2] == '&' or p[2] == '^': # Lida com ambos tokens para AND
        node_type = 'AND'
    elif p[2] == '|':
        node_type = 'OR'
    elif p[2] == '->':
        node_type = 'IMPLIES'
    elif p[2] == '<->':
        node_type = 'IFF'
    elif p[2] == 'v': # Nosso token para NOR
        node_type = 'NOR'
    elif p[2] == '^': # Nosso token para NAND
        node_type = 'NAND'

    p[0] = Node(node_type, [p[1], p[3]])

def p_expression_not(p):
    'expression : NOT expression'
    # p[1] é o token '!' ou '~'
    p[0] = Node('NOT', [p[2]])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2] # O nó é a expressão dentro dos parênteses

def p_expression_variable(p):
    'expression : VARIAVEL'
    p[0] = Node('VARIAVEL', value=p[1])

def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}' na posição {p.lexpos}")
    else:
        print("Erro de sintaxe no final da entrada")
    sys.exit(1) # Sai do programa em caso de erro

# Constrói o parser
parser = yacc.yacc()

# --- Geração da Imagem da Árvore (usando Graphviz) ---

# Função para reconstruir a string da subfórmula a partir de um nó da AST
def node_to_formula_string(node, parent_precedence=0):
    if node.type == 'VARIAVEL':
        return node.value
    elif node.type == 'NOT':
        # Negação tem alta precedência, geralmente não precisa de parênteses
        sub_formula = node_to_formula_string(node.children[0], OP_PRECEDENCE['NOT'])
        return f"{OP_MAP['NOT']}{sub_formula}"
    else: # Operadores binários
        op_symbol = OP_MAP[node.type]
        current_precedence = OP_PRECEDENCE[node.type]

        left_child = node.children[0]
        right_child = node.children[1]

        # Reconstrói a sub-fórmula esquerda
        left_str = node_to_formula_string(left_child, current_precedence)
        # Adiciona parênteses se a precedência do filho for menor ou igual à do operador atual
        # Exceto se o filho for uma variável, que não precisa de parênteses
        if OP_PRECEDENCE[left_child.type] < current_precedence and left_child.type != 'VARIAVEL':
             left_str = f"({left_str})"
        # Lida com associatividade à direita para IMPLIES e IFF
        elif (node.type == 'IMPLIES' or node.type == 'IFF') and left_child.type == node.type:
             left_str = f"({left_str})"


        # Reconstrói a sub-fórmula direita
        right_str = node_to_formula_string(right_child, current_precedence)
        # Adiciona parênteses se a precedência do filho for menor ou igual à do operador atual
        if OP_PRECEDENCE[right_child.type] < current_precedence and right_child.type != 'VARIAVEL':
             right_str = f"({right_str})"
        # Lida com associatividade à esquerda (padrão) para os outros operadores
        elif (node.type in ['AND', 'OR', 'NOR', 'NAND']) and right_child.type == node.type:
             right_str = f"({right_str})"

        # Adiciona parênteses se a precedência do operador atual for menor que a do pai
        # Isso é controlado pelo parent_precedence
        result = f"{left_str} {op_symbol} {right_str}"
        if current_precedence < parent_precedence:
            result = f"({result})"
        return result


def generate_ast_image(ast_root, filename="arvore_logica"):
    dot = graphviz.Digraph(comment='Árvore Sintática Lógica', format='png')
    dot.attr(rankdir='TB',  # Top-to-Bottom
             splines='polyline', # Estilo das linhas
             nodesep='0.6', # Espaçamento entre nós no mesmo nível
             ranksep='0.8' # Espaçamento entre níveis
            )

    node_counter = 0
    node_map = {} # Mapeia objetos Node para seus IDs no Graphviz
    subformulas = [] # Lista para armazenar as subfórmulas

    def add_nodes_edges(node, parent_precedence_for_string=0):
        nonlocal node_counter
        node_id = str(node_counter)
        node_counter += 1
        node_map[node] = node_id

        # Definir o label do nó para o Graphviz
        label = node.type
        if node.value:
            label = node.value # Para variáveis

        # Substituir símbolos para melhor visualização no Graphviz
        if label == 'AND': label = 'AND' # Já é AND
        elif label == 'OR': label = 'OR' # Já é OR
        elif label == 'IMPLIES': label = 'IMPLICA'
        elif label == 'IFF': label = 'BICONDICIONAL'
        elif label == 'NOT': label = 'NEG'
        elif label == 'NOR': label = 'NOR'
        elif label == 'NAND': label = 'NAND'

        dot.node(node_id, label=label, shape='box' if node.children else 'ellipse')

        # Adiciona a subfórmula à lista
        formula_str = node_to_formula_string(node, parent_precedence_for_string)
        subformulas.append(formula_str)

        for child in node.children:
            child_id = add_nodes_edges(child, OP_PRECEDENCE.get(node.type, 0)) # Passa a precedência do nó atual para o filho
            dot.edge(node_id, child_id)
        return node_id

    add_nodes_edges(ast_root)

    # --- Adicionar as subfórmulas no final da imagem ---
    # Ordenar e remover duplicatas para uma lista limpa
    unique_subformulas = sorted(list(set(subformulas)), key=len) # Ordena por tamanho para melhor visualização

    # Cria uma string formatada para o nó de texto
    subformulas_text = "Subfórmulas:\n" + "\n".join(unique_subformulas)

    # Adiciona um nó de texto invisível (ou visível como um retângulo) na parte inferior
    dot.node('subformulas_block', label=subformulas_text, shape='box',
             style='filled', fillcolor='lightgray', fontname='monospace',
             fontsize='10', peripheries='1') # Adiciona borda simples

    # Linka a raiz da árvore ao bloco de subfórmulas (opcional, pode ser só um nó flutuante)
    # Se quiser que o bloco flutue, remova esta linha
    # dot.edge(node_map[ast_root], 'subformulas_block', style='invis') # Aresta invisível

    dot.render(filename, view=True) # view=True abre a imagem após a geração
    print(f"Imagem da árvore gerada como '{filename}.png'")

# --- Função Principal ---
if __name__ == "__main__":
    print("Digite a fórmula lógica (ex: (s -> r v l) v (~q ^ r) -> (~(p -> s) -> r)):")
    formula_input = input(">> ")

    try:
        # Analisa a entrada
        ast = parser.parse(formula_input, lexer=lexer)

        if ast:
            # Gera a imagem da AST
            generate_ast_image(ast, "arvore_da_formula_logica_com_subformulas")
        else:
            print("Não foi possível construir a árvore sintática para a fórmula fornecida.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")