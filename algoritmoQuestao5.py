import re
import csv
import os
from sympy.logic.boolalg import Implies, And, Or, Not, Equivalent
from sympy.abc import symbols
from itertools import product
from sympy import sympify
from datetime import datetime

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

        # Formatação da tabela em Markdown
        table_lines = []
        table_lines.append("| " + " | ".join(header_parts) + " |")
        table_lines.append("| " + " | ".join(["---"] * len(header_parts)) + " |")
        for row in table_data_rows:
            table_lines.append("| " + " | ".join('V' if val else 'F' for val in row) + " |")
        table_markdown = "\n".join(table_lines)

        # Classificação
        all_true = all(final_column_values)
        all_false = not any(final_column_values)

        if all_true:
            classification = "Válida"
            justification = f"A fórmula '{formula_str_input}' é uma **tautologia** (sempre verdadeira)."
        elif all_false:
            classification = "Insatisfazível"
            justification = f"A fórmula '{formula_str_input}' é uma **contradição** (sempre falsa)."
        else:
            classification = "Satisfazível, Inválida"
            justification = f"A fórmula '{formula_str_input}' é **satisfazível** (pode ser verdadeira), mas **não é válida** (pode ser falsa)."

        # Verifica se o arquivo existe e se está vazio para escrever cabeçalho
        filename = "tabelas_verdade.csv"
        file_exists = os.path.isfile(filename)
        write_header = not file_exists or os.path.getsize(filename) == 0

        with open(filename, mode="a", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["Data/Hora", "Fórmula", "Classificação", "Justificativa", "Tabela Verdade Markdown"])
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), formula_str_input, classification, justification, table_markdown])

        return classification, justification, table_markdown

    except Exception as e:
        return "Erro", f"Erro ao processar a fórmula: {e}", ""

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

        classification, justification, truth_table_str = classify_formula(formula_input)
        print("\n" + truth_table_str)
        print(f"\nClassificação: {classification}")
        print(f"Justificativa: {justification}")
