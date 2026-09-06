# Rung 0 — Eight Queens

> 1848 → 1972 → 1990. One problem, five tiers of technique.

| | |
|---|---|
| Problem | Place N queens on an N×N board so that no two attack each other |
| History | Bezzel 1848 · Gauss 1850 · Dijkstra 1972 · Sosic & Gu 1990 |
| Concepts | Enumeration, backtracking, bitmasks, local search, constraint propagation |
| Requires | nothing |
| Leads to | rung 2 (state-space search), rung 4 (CSP) |

---

## Why this is rung 0

The same problem can be solved at five levels of sophistication, and each level is a real historical step:

```
Tier 1  Brute-force enumeration   Check the diagonals of all N! permutations       Gauss 1850
Tier 2  Backtracking              Place one row at a time, retreat on conflict      Dijkstra 1972
Tier 3  Bitmask backtracking      Three ints track columns and both diagonals       1990s; how N=27 was counted
Tier 4  Min-conflicts             Random start, repair the worst queen              Sosic & Gu 1990, N = 1,000,000
Tier 5  Constraint propagation    Forward checking, arc consistency                 Road to Sudoku (rung 4)
```

Tiers 1–3 find **all** solutions. Tier 4 finds **one**. That split is the textbook's split between systematic search and local search, and it appears here before any opponent, chance, or learning gets in the way.

Every tier has the previous one as its oracle, and every speedup is measurable. This rung is the engineering rules of the whole repository in miniature.

---

## Interface

```python
Placement = tuple[int, ...]     # placement[row] = col

def is_valid(p: Placement) -> bool
def render(p: Placement) -> str            # 'Q' for a queen, '.' otherwise, rows joined by '\n'

def solve_brute(n: int) -> list[Placement]         # tier 1
def solve_backtrack(n: int) -> list[Placement]     # tier 2
def solve_bitmask(n: int) -> list[Placement]       # tier 3
def solve_min_conflicts(n: int, rng: random.Random) -> Placement   # tier 4
def solve_propagate(n: int) -> list[Placement]     # tier 5
```

A placement is a permutation: row `r` holds a queen at column `p[r]`. Row and column conflicts are impossible by construction, so only diagonals need checking. This single observation cuts 8⁸ ≈ 16.7 million candidates to 8! = 40,320.

---

## Golden values

OEIS A000170:

| N | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| solutions | 1 | 0 | 0 | 2 | 10 | 4 | 40 | 92 | 352 | 724 | 2680 | 14200 |

---

## Milestones

- [ ] **Tier 1** — `solve_brute`, `is_valid`, `render`. Passes counts for N ≤ 8. Record the time for N=8 and N=10.
- [ ] **Tier 2** — `solve_backtrack`. Agrees with tier 1 for N ≤ 8. Passes N=9, 10. Record the speedup.
- [ ] **Tier 3** — `solve_bitmask`. Agrees with tier 2 for N ≤ 10. Passes N=12. Record nodes/sec.
- [ ] **Tier 4** — `solve_min_conflicts`. Returns a valid placement for N=1000 in under a second. Note that it cannot be validated against tier 3 by count, only by `is_valid`.
- [ ] **Tier 5** — `solve_propagate`. Agrees with tier 3. Record how many fewer nodes it visits than tier 2.
- [ ] `bench.py` writes all timings to `benchmarks/s00_nqueens.json`.

---

## Acceptance

- All counts match the golden table for N ≤ 12.
- Tier 3 on N=12 runs faster than tier 1 on N=10.
- Tier 4 solves N=1000 in under one second.
- Every fast tier agrees with the tier before it on every N where both finish.

---

## Reading

- Dijkstra, "Notes on Structured Programming" (1972), §"The problem of eight queens"
- Sosic & Gu, "A polynomial time algorithm for the N-Queens problem", *SIGART Bulletin* (1990)
- Russell & Norvig, *AIMA* 4e, §4.1 (local search), §6.1–6.3 (CSPs)
- OEIS A000170
