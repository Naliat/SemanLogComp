import re
from sympy.logic.boolalg import Implies, And, Or, Not, Nand, Nor, Equivalent
from sympy.abc import symbols
from itertools import product

# Regex para identificar uma "unidade" de uma expressão lógica:
# Pode ser uma variável (p, q, r, etc.),
# um literal booleano (True, False),
# ou uma expressão entre parênteses.
_ATOM_PATTERN = r'[a-zA-Z_]+|True|False|\([^()]*?\)' 

def _parse_and_evaluate_expression(formula_str_input, env):
    """
    Parses a logical formula string with custom operators (->, &, |)
    and evaluates it into a SymPy expression.
    """
    s = formula_str_input.strip()

    # --- NOVO AJUSTE CRÍTICO AQUI ---
    # Substitui '->' por '>>' e '<->' por '==' ANTES de qualquer outra coisa.
    # Isso permite que eval() processe expressões aninhadas corretamente.
    s = s.replace('<->', '==').replace('->', '>>') 
    # --------------------------------

    # 1. Substituir Negação (`~`) por `Not()`
    s = re.sub(r'~(' + _ATOM_PATTERN + r')', r'Not(\1)', s) 
    
    # 2. Substituir NAND e NOR por suas definições (se forem usadas no formato de função)
    s = re.sub(r'Nand\((.+?),\s*(.+?)\)', r'Not(And(\1,\2))', s)
    s = re.sub(r'Nor\((.+?),\s*(.+?)\)', r'Not(Or(\1,\2))', s)

    # 3. Substituir Conjunção (`&`) e Disjunção (`|`) por And() e Or()
    # Garante que 'p & q' e 'p | q' sejam tratados como And(p,q) e Or(p,q) pelo SymPy
    # para consistência em expressões complexas.
    # Isso é feito para que a string de `eval` seja mais explícita com funções SymPy
    # para operadores que podem ser ambíguos ou ter precedência diferente.
    s = re.sub(r'(' + _ATOM_PATTERN + r')\s*&\s*(' + _ATOM_PATTERN + r')', r'And(\1,\2)', s)
    s = re.sub(r'(' + _ATOM_PATTERN + r')\s*\|\s*(' + _ATOM_PATTERN + r')', r'Or(\1,\2)', s)

    return eval(s, env)


def classify_formula(formula_str_input):
    """
    Classifica uma fórmula lógica e gera sua tabela verdade detalhada.

    Args:
        formula_str_input (str): A fórmula lógica em formato de string.
                           Usa 'p', 'q', 'r' para variáveis.
                           Operadores suportados:
                           '~' para negação (¬)
                           '&' para conjunção (∧)
                           '|' para disjunção (∨)
                           '->' para implicação (→)
                           '<->' para equivalência (↔)
                           Nand(A, B) e Nor(A, B) para NAND e NOR.

    Returns:
        tuple: Uma tupla contendo a classificação, a justificativa e a tabela verdade formatada.
    """
    try:
        # Cria um ambiente de execução para `eval` com os símbolos e funções do SymPy.
        all_syms_names = ['p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        
        present_syms_names = [name for name in all_syms_names if re.search(r'\b' + name + r'\b', formula_str_input)]
        variables = sorted([symbols(name) for name in present_syms_names], key=lambda x: x.name)
        
        env = {s.name: s for s in variables}
        env.update({
            'Implies': Implies, 'And': And, 'Or': Or, 'Not': Not,
            'Nand': Nand, 'Nor': Nor, 'Equivalent': Equivalent,
            'True': True, 'False': False 
        })

        # Processa a string de entrada para converter operadores para a sintaxe SymPy.
        formula_expr = _parse_and_evaluate_expression(formula_str_input, env)

        # --- Geração da Tabela Verdade ---
        table_string = "\n--- Tabela Verdade ---\n"
        
        # Define os cabeçalhos da tabela.
        # Usa a string original para o cabeçalho da fórmula completa.
        if not variables and formula_expr.is_Boolean:
            header_parts = [formula_str_input]
            table_data_rows = [[bool(formula_expr)]]
            final_column_values = [bool(formula_expr)]
        else:
            header_parts = [str(v) for v in variables]
            header_parts.append(formula_str_input) 
            
            table_data_rows = []
            final_column_values = [] 

            for values_tuple in product([False, True], repeat=len(variables)):
                assignment = dict(zip(variables, values_tuple))
                
                row_values = [assignment[v] for v in variables]
                evaluated_result = formula_expr.subs(assignment)
                row_values.append(bool(evaluated_result))
                
                table_data_rows.append(row_values)
                final_column_values.append(bool(evaluated_result))

        # --- Formatação da Tabela Verdade (Ajustes para Consistência) ---
        
        # Recalcula col_widths a CADA VEZ para garantir que se ajustem à fórmula atual
        col_widths = [len(h) for h in header_parts]
        for row in table_data_rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str('V' if val else 'F')))

        # Imprime o cabeçalho
        header_line = " | ".join(h.ljust(w) for h, w in zip(header_parts, col_widths))
        table_string += header_line + "\n"
        # Imprime a linha separadora
        table_string += "-+-".join("-" * w for w in col_widths) + "\n"

        # Imprime as linhas de dados
        for row in table_data_rows:
            formatted_row = []
            for i, val in enumerate(row):
                display_val = 'V' if val else 'F'
                formatted_row.append(display_val.ljust(col_widths[i]))
            table_string += " | ".join(formatted_row) + "\n"
        table_string += "----------------------\n" # Linha final para fechar a tabela

        # --- Classificação da Fórmula ---
        all_true = all(final_column_values)
        all_false = not any(final_column_values)

        classification = []
        justification = ""

        if all_true:
            classification.append("Válida")
            justification = f"A coluna da fórmula completa ('{formula_str_input}') contém apenas 'V' (Verdadeiro), indicando que é uma **tautologia** (sempre Verdadeira)."
        elif all_false:
            classification.append("Insatisfazível")
            justification = f"A coluna da fórmula completa ('{formula_str_input}') contém apenas 'F' (Falso), indicando que é uma **contradição** (sempre Falsa)."
        else:
            classification.append("Satisfazível")
            classification.append("Inválida")
            justification = f"A coluna da fórmula completa ('{formula_str_input}') contém tanto 'V' (Verdadeiro) quanto 'F' (Falso), indicando que é **satisfazível** (pode ser Verdadeira) mas **não é válida** (pode ser Falsa)."

        return ", ".join(classification), justification, table_string

    except Exception as e:
        return "Erro", f"Não foi possível processar a fórmula. Verifique a sintaxe. Certifique-se de usar parênteses para agrupar operações aninhadas. Erro: {e}", ""

# --- Loop para Interação via Terminal ---
if __name__ == "__main__":
    print("Bem-vindo ao Classificador de Fórmulas Lógicas com Tabela Verdade!")
    print("Use 'p', 'q', 'r', etc., para variáveis. O algoritmo detecta as variáveis usadas.")
    print("\nOperadores suportados (sintaxe comum):")
    print("  Negação (¬): **~A**")
    print("  Conjunção (∧): **A & B**")
    print("  Disjunção (∨): **A | B**")
    print("  Implicação (→): **A -> B**")
    print("  Equivalência (↔): **A <-> B**")
    print("  NAND (↑): **Nand(A, B)** (ainda requer a forma de função)")
    print("  NOR (↓): **Nor(A, B)** (ainda requer a forma de função)")
    print("\n**ATENÇÃO:** Use parênteses para agrupar operações aninhadas e garantir a precedência correta.")
    print("  Ex: `(p & q) -> r` é diferente de `p & (q -> r)`")

    print("\n**Exemplos:**")
    print("  `((p -> q) -> p) -> p`") # Lei de Peirce
    print("  `~p & q`")
    print("  `p | q`")
    print("  `p -> q`")
    print("  `p <-> q`")
    print("  `Nand(p, q)`") # Ainda requer a forma de função
    print("  `p | Nor(q, r)`") # Ainda requer a forma de função
    print("Digite 'sair' para encerrar.")

    while True:
        formula_input = input("\nDigite a fórmula lógica: ")
        if formula_input.lower() == 'sair':
            break

        classification, justification, truth_table_str = classify_formula(formula_input)
        
        if classification != "Erro":
            print(truth_table_str)
            print(f"Classificação: {classification}")
            print(f"Justificativa: {justification}")
        else:
            print(f"Erro: {justification}")