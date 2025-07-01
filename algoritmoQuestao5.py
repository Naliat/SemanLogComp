import re
import os
import csv
from sympy.logic.boolalg import Implies, And, Or, Not, Equivalent
from sympy.abc import symbols
from itertools import product
from sympy import sympify

# Regex para átomos lógicos
_ATOM_PATTERN = r'[a-zA-Z_]+|True|False|\([^()]*?\)'

def _parse_and_evaluate_expression(formula_str_input, env):
    s = formula_str_input.strip()
    s = s.replace('<->', '==').replace('->', '>>')
    s = re.sub(r'~(' + _ATOM_PATTERN + r')', r'Not(\1)', s)
    s = re.sub(r'Nand\((.+?),\s*(.+?)\)', r'Not(And(\1,\2))', s)
    s = re.sub(r'Nor\((.+?),\s*(.+?)\)', r'Not(Or(\1,\2))', s)
    return sympify(s, locals=env)

def classify_formula(formula_str_input):
    try:
        all_syms_names = ['p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        present_syms_names = [name for name in all_syms_names if re.search(r'\b' + name + r'\b', formula_str_input)]
        variables = sorted([symbols(name) for name in present_syms_names], key=lambda x: x.name)

        env = {s.name: s for s in variables}
        env.update({
            'Implies': Implies, 'And': And, 'Or': Or, 'Not': Not, 'Equivalent': Equivalent,
            'True': True, 'False': False
        })

        formula_expr = _parse_and_evaluate_expression(formula_str_input, env)

        # --- Tabela Verdade ---
        table_string = "\n--- Tabela Verdade ---\n"
        header_parts = [str(v) for v in variables] + [formula_str_input]
        table_data_rows = []
        final_column_values = []

        if not variables:
            val = bool(formula_expr)
            table_data_rows = [[val]]
            final_column_values = [val]
        else:
            for values_tuple in product([False, True], repeat=len(variables)):
                assignment = dict(zip(variables, values_tuple))
                row_values = [assignment[v] for v in variables]
                result = formula_expr.subs(assignment)
                row_values.append(bool(result))
                table_data_rows.append(row_values)
                final_column_values.append(bool(result))

        # --- Formatação ---
        col_widths = [len(h) for h in header_parts]
        for row in table_data_rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len('V' if val else 'F'))

        header_line = " | ".join(h.ljust(w) for h, w in zip(header_parts, col_widths))
        table_string += header_line + "\n"
        table_string += "-+-".join("-" * w for w in col_widths) + "\n"

        for row in table_data_rows:
            table_string += " | ".join(('V' if val else 'F').ljust(col_widths[i]) for i, val in enumerate(row)) + "\n"
        table_string += "-" * (sum(col_widths) + 3 * (len(col_widths) - 1)) + "\n"

        # --- Classificação ---
        all_true = all(final_column_values)
        all_false = not any(final_column_values)

        if all_true:
            return "Válida", f"A fórmula '{formula_str_input}' é uma **tautologia** (sempre verdadeira).", table_string
        elif all_false:
            return "Insatisfazível", f"A fórmula '{formula_str_input}' é uma **contradição** (sempre falsa).", table_string
        else:
            return "Satisfazível, Inválida", f"A fórmula '{formula_str_input}' é **satisfazível** (pode ser verdadeira), mas **não é válida** (pode ser falsa).", table_string

    except Exception as e:
        return "Erro", f"Erro ao processar a fórmula: {e}", ""

def salvar_em_csv(formula, classificacao, justificativa, tabela_verdade):
    caminho_arquivo = "formulas_resultados.csv"
    criar_cabecalho = not os.path.exists(caminho_arquivo)

    with open(caminho_arquivo, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if criar_cabecalho:
            writer.writerow(['Fórmula', 'Classificação', 'Justificativa', 'Tabela Verdade'])

        writer.writerow([formula, classificacao, justificativa, tabela_verdade.strip()])

# --- Loop interativo ---
if __name__ == "__main__":
    print("Bem-vindo ao Classificador de Fórmulas Lógicas com Tabela Verdade!")
    print("\nOperadores suportados:")
    print("  ~A     → ¬A (negação)")
    print("  A & B  → A ∧ B (conjunção)")
    print("  A | B  → A ∨ B (disjunção)")
    print("  A -> B → A → B (implicação)")
    print("  A <-> B → A ↔ B (equivalência)")
    print("  Nand(A,B) e Nor(A,B) também funcionam.")
    print("Digite 'sair' para encerrar.\n")

    while True:
        formula_input = input("Digite a fórmula lógica: ").strip()
        if formula_input.lower() == 'sair':
            break

        classificacao, justificativa, tabela = classify_formula(formula_input)
        print(tabela)
        print(f"Classificação: {classificacao}")
        print(f"Justificativa: {justificativa}\n")

        salvar_em_csv(formula_input, classificacao, justificativa, tabela)
        print("Resultado salvo em 'formulas_resultados.csv'.\n")
