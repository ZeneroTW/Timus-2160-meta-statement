# 🌳 Counting Equivalent Permutation Patterns — Cartesian Tree + Combinatorics

> 🇷🇺 [Читать на русском](README.ru.md)

A solution to **Timus 2160 "Meta-problem"**: given a permutation, count how many other permutations are *equivalent* to it under a recursive "split by minimum" pattern definition. The naive approach is O(N · N!); this solution reduces the problem to **Cartesian tree isomorphism** and solves it in **O(N)**.

Accepted on Timus with **1.14 s** runtime and **39 MB** memory at N up to 10⁵.

---

## Problem

The jury arranges N problems in a contest by difficulty (1 = hardest) using a *pattern* — a permutation of 1…N. The pattern is interpreted recursively: find the minimum, split the array into the left and right parts, repeat for each part.

Two patterns are **equivalent** if both are empty, or if the position of the minimum coincides and their left and right sub-patterns are equivalent.

| Property   | Value                    |
| ---------- | ------------------------ |
| Input      | N, then p₁ … pₙ          |
| Constraint | 1 ≤ N ≤ 10⁵              |
| Output     | Answer modulo 10⁹ + 7    |
| Time limit | 2 s                      |
| Memory     | 256 MB                   |

### Examples

| Input        | Output |
| ------------ | ------ |
| `3` `2 1 3`  | 2      |
| `5` `3 1 4 2 5` | 8   |

Brute force is hopeless: enumerating all N! permutations and checking each one gives O(N · N!) — already ≈ 2.4 · 10¹⁸ operations at N = 20.

---

## Idea

A pattern **is** a Cartesian tree. The root is the minimum of the array; the left and right subtrees are built recursively from the elements to the left and right of it.

```
(3, 1, 4, 2, 5)          1
                        / \
                       3   2
                          / \
                         4   5
```

A Cartesian tree combines two properties at once — a BST by positions (left to right = the original array) and a min-heap by values (top to bottom = increasing, root is the global minimum). For an array with distinct values it is built uniquely.

**Equivalence ⟺ tree isomorphism.** Two patterns are equivalent if and only if their Cartesian trees have the same shape, values ignored.

```
(2, 1, 3) and (3, 1, 2)  →  same shape     →  equivalent
(1, 2, 3)                →  different shape →  not equivalent
```

---

## Solution

The number of permutations producing a given tree shape is a product over all nodes:

```
answer = Π C(L + R, L)  mod 10⁹ + 7
```

where for each node **L** and **R** are the sizes of its left and right subtrees. The intuition: the L + R values below a node have to be distributed between the two subtrees, and choosing which L of them go left fully determines the arrangement.

Worked example for (3, 1, 4, 2, 5):

| Node | L, R  | C(L+R, L) |
| ---- | ----- | --------- |
| 1    | 1, 3  | C(4,1) = 4 |
| 3    | 0, 0  | 1          |
| 2    | 1, 1  | C(2,1) = 2 |
| 4    | 0, 0  | 1          |
| 5    | 0, 0  | 1          |

Product = 4 · 1 · 2 · 1 · 1 = **8**.

---

## Implementation

### Building the tree in O(N) — monotonic stack

Walk the array left to right, keeping nodes in the stack in increasing order of value from bottom to top. For each new `x`:

1. while the stack top is greater than `x` — pop; the last popped node becomes the left child of `x`
2. if the stack is non-empty — `x` becomes the right child of the new top
3. push `x`

Every element enters and leaves the stack exactly once → O(N). The root is the bottom of the stack.

### Binomial coefficients modulo a prime

There is no division modulo p — a modular inverse is needed. Since p = 10⁹ + 7 is prime, Fermat's little theorem gives `a⁻¹ ≡ a^(p−2) (mod p)`, computed in O(log p) by fast exponentiation.

Factorials and inverse factorials are precomputed once:

- `fac[i] = i! mod p`
- `invfac[i]` via the recurrence `(k−1)!⁻¹ = k!⁻¹ · k` — a single `pow` at the start, everything else in O(N)

After that any `C(n, k) = fac[n] · invfac[k] · invfac[n−k]` costs **O(1)**.

---

## Architecture

Four classes:

| Class            | Responsibility                                                        |
| ---------------- | --------------------------------------------------------------------- |
| `Node`           | Cartesian tree node — `value`, `left`, `right`, `size_val` (subtree size) |
| `Stack`          | Stack over a list — `push` / `pop` / `top` / `is_empty`                |
| `Combinatorics`  | Precomputed `fac[]` / `invfac[]`, `C(n, k)` in O(1)                   |
| `CartesianTree`  | Algorithm orchestrator — `build()` in O(N), `count()` = Π C(L+R, L)   |

### Pitfall: recursion on the tree

On sorted input the Cartesian tree degenerates into a linear chain of depth N. At N = 10⁵ a recursive traversal overflows the call stack and crashes.

All tree traversals are therefore **iterative**, over an explicit list-based stack. Depth is now bounded by heap size instead of the system stack.

---

## Complexity

| Stage                     | Complexity |
| ------------------------- | ---------- |
| Building the tree         | O(N) — monotonic stack |
| One binomial coefficient  | O(1) — after precomputation |
| **Total**                 | **O(N)** — a single linear pass |

Verdict on Timus: **Accepted**, Python 3.12 x64, 1.14 s, 39 364 KB.

---

## Tech Stack

- **Python 3.12** — standard library only, no external dependencies
- **Monotonic stack** — linear Cartesian tree construction
- **Modular arithmetic** — Fermat's little theorem, `pow(a, p-2, p)`

---

## Project Structure

```
├── solution.py         # Solution (reads from stdin, writes to stdout)
├── presentation.pdf    # Coursework defence slides
├── README.md           # This file (English)
└── README.ru.md        # Russian version
```

---

## Getting Started

```
# No dependencies required
python solution.py

# Or with input from a file
echo "5
3 1 4 2 5" | python solution.py
```

Problem statement: [Timus 2160 — Meta-problem](https://acm.timus.ru/problem.aspx?space=1&num=2160)

---

*Coursework — RTU MIREA, Institute of Artificial Intelligence. Group KRBO-12-24.*
