# Tabelas Verdade de Fórmulas Lógicas

## Classificação da fórmula: ((p -> q) -> p) -> p

**Data:** 2025-06-30 22:26:26  
**Classificação:** Válida  
**Justificativa:** A fórmula '((p -> q) -> p) -> p' é uma **tautologia** (sempre verdadeira).

| p | q | ((p -> q) -> p) -> p |
|---|---|---|
| F | F | V |
| F | V | V |
| V | F | V |
| V | V | V |

---

## Classificação da fórmula: p | (~(q & (r -> q)))

**Data:** 2025-06-30 22:27:35  
**Classificação:** Satisfazível, Inválida  
**Justificativa:** A fórmula 'p | (~(q & (r -> q)))' é **satisfazível** (pode ser verdadeira), mas **não é válida** (pode ser falsa).

| p | q | r | p | (~(q & (r -> q))) |
|---|---|---|---|
| F | F | F | V |
| F | F | V | V |
| F | V | F | F |
| F | V | V | F |
| V | F | F | V |
| V | F | V | V |
| V | V | F | V |
| V | V | V | V |

---

## Classificação da fórmula: ((p | q) -> r) -> ((p -> r) | (q -> r))

**Data:** 2025-06-30 22:27:45  
**Classificação:** Válida  
**Justificativa:** A fórmula '((p | q) -> r) -> ((p -> r) | (q -> r))' é uma **tautologia** (sempre verdadeira).

| p | q | r | ((p | q) -> r) -> ((p -> r) | (q -> r)) |
|---|---|---|---|
| F | F | F | V |
| F | F | V | V |
| F | V | F | V |
| F | V | V | V |
| V | F | F | V |
| V | F | V | V |
| V | V | F | V |
| V | V | V | V |

---

## Classificação da fórmula: (p -> q) & (~r -> (q | (~p & r)))

**Data:** 2025-06-30 22:27:55  
**Classificação:** Satisfazível, Inválida  
**Justificativa:** A fórmula '(p -> q) & (~r -> (q | (~p & r)))' é **satisfazível** (pode ser verdadeira), mas **não é válida** (pode ser falsa).

| p | q | r | (p -> q) & (~r -> (q | (~p & r))) |
|---|---|---|---|
| F | F | F | F |
| F | F | V | V |
| F | V | F | V |
| F | V | V | V |
| V | F | F | F |
| V | F | V | F |
| V | V | F | V |
| V | V | V | V |

---

