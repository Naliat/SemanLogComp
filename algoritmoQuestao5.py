import re
from sympy.logic.boolalg import Implies, And, Or, Not, Equivalent
from sympy.abc import symbols
from itertools import product
from sympy import sympify
from datetime import datetime
import os

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

        filename = "tabelas_verdade.md"
        write_header = not os.path.isfile(filename)

        with open(filename, "a", encoding="utf-8") as f:
            if write_header:
                f.write("# Tabelas Verdade de Fórmulas Lógicas\n\n")
                print(f"[DEBUG] Criado novo arquivo '{filename}' com header")

            f.write(f"## Classificação da fórmula: {formula_str_input}\n\n")
            f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
            f.write(f"**Classificação:** {classification}  \n")
            f.write(f"**Justificativa:** {justification}\n\n")

            # Header Markdown da tabela
            f.write("| " + " | ".join(header_parts) + " |\n")
            f.write("|" + "|".join("---" for _ in header_parts) + "|\n")

            # Linhas da tabela
            for row in table_data_rows:
                f.write("| " + " | ".join('V' if val else 'F' for val in row) + " |\n")

            f.write("\n---\n\n")  # Separador entre fórmulas

        print(f"[DEBUG] Salvo no arquivo '{filename}' com sucesso.")

        return classification, justification, None

    except Exception as e:
        print(f"[ERRO] {e}")
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

        classification, justification, _ = classify_formula(formula_input)
        print(f"\nClassificação: {classification}")
        print(f"Justificativa: {justification}")
        print(f"Tabela verdade salva no arquivo 'tabelas_verdade.md'\n")
