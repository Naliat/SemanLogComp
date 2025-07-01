# Tabelas Verdade de Fórmulas Lógicas

## Classificação da fórmula: ((p -> q) -> p) -> p

**Data:** 2025-06-30 22:36:46  
**Classificação:** Válida  
**Justificativa:** A fórmula '((p -> q) -> p) -> p' é uma **tautologia** (sempre verdadeira).
```
| p | q | ((p -> q) -> p) -> p |
|---|---|---|
| F | F | V |
| F | V | V |
| V | F | V |
| V | V | V |

---

## Classificação da fórmula: p | (~(q & (r -> q)))

**Data:** 2025-06-30 22:36:54  
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

## Classificação da fórmula: (p & q) -> (p | q)

**Data:** 2025-06-30 22:37:31  
**Classificação:** Válida  
**Justificativa:** A fórmula '(p & q) -> (p | q)' é uma **tautologia** (sempre verdadeira).

| p | q | (p & q) -> (p | q) |
|---|---|---|
| F | F | V |
| F | V | V |
| V | F | V |
| V | V | V |

---

## Classificação da fórmula: ((p -> ~q) -> ~p) -> q

**Data:** 2025-06-30 22:38:23  
**Classificação:** Satisfazível, Inválida  
**Justificativa:** A fórmula '((p -> ~q) -> ~p) -> q' é **satisfazível** (pode ser verdadeira), mas **não é válida** (pode ser falsa).

| p | q | ((p -> ~q) -> ~p) -> q |
|---|---|---|
| F | F | F |
| F | V | V |
| V | F | V |
| V | V | V |

---

## Classificação da fórmula: (p -> q) | (p -> ~q)

**Data:** 2025-06-30 22:38:53  
**Classificação:** Válida  
**Justificativa:** A fórmula '(p -> q) | (p -> ~q)' é uma **tautologia** (sempre verdadeira).

| p | q | (p -> q) | (p -> ~q) |
|---|---|---|
| F | F | V |
| F | V | V |
| V | F | V |
| V | V | V |

---

## Classificação da fórmula: ((p -> q) -> p) -> p

**Data:** 2025-06-30 22:39:18  
**Classificação:** Válida  
**Justificativa:** A fórmula '((p -> q) -> p) -> p' é uma **tautologia** (sempre verdadeira).

| p | q | ((p -> q) -> p) -> p |
|---|---|---|
| F | F | V |
| F | V | V |
| V | F | V |
| V | V | V |

---

## Classificação da fórmula: ((p | q) -> r) -> ((p -> r) | (q -> r))

**Data:** 2025-06-30 22:39:40  
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

## Classificação da fórmula: (p -> q) -> (~p -> ~q)

**Data:** 2025-06-30 22:41:06  
**Classificação:** Satisfazível, Inválida  
**Justificativa:** A fórmula '(p -> q) -> (~p -> ~q)' é **satisfazível** (pode ser verdadeira), mas **não é válida** (pode ser falsa).

| p | q | (p -> q) -> (~p -> ~q) |
|---|---|---|
| F | F | V |
| F | V | F |
| V | F | V |
| V | V | V |

---
```

