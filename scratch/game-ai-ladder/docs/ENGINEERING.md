# Engineering

Rules that apply to every rung, and the acceptance criteria that define "done".

---

## Rules

**Performance.** Search code reports **nodes per second**, never wall-clock time — wall-clock is not comparable across machines. Each rung's `bench.py` writes JSON to `benchmarks/` so numbers can be compared across commits.

**Correctness.**
- Slow first, then fast. The obviously-correct implementation is the oracle; the fast one must agree with it on random inputs. `gameai/testing.py` provides generators such as `random_boards(seed, n)` in place of `hypothesis`.
- A pruned search must return **exactly** the same value as the unpruned one. Only the node count may differ.
- Solved problems (Eight Queens counts, tic-tac-toe, Connect Four) use their theoretical values as golden tests.

**Profiling.** `cProfile` → read with `pstats` → change the algorithm. No C extensions.

**Statistics.** Any claim that agent A is stronger than agent B comes with a sample size and a bootstrap confidence interval. Write the bootstrap yourself; `random.choices` is all you need. Use paired comparisons on a fixed seed sequence to cut variance.

**Tests.** `unittest` only:

```
python -m unittest discover -s stages -p "test_*.py"
```

**Randomness.** Always through an injectable `random.Random(seed)`. Tests fix the seed.

**Rendering.** `Renderer.draw(state) -> str`. Never `print` inside the engine or the agents.

---

## Acceptance criteria

A rung is done when it passes its criteria, not when it looks like it works.

| Rung | Criteria |
|---|---|
| 0 | Solution counts match OEIS A000170 (N=8 → 92, N=10 → 724). Tier 3 on N=12 is faster than tier 1 on N=10. Tier 4 solves N=1000 in under a second. |
| 1 | Loop version and sparse version agree on 1000 random boards evolved 100 generations. A glider translates by (1, 1) every 4 generations. |
| 2 | BFS and IDDFS return the same solution length on 8-puzzle. |
| 3 | A\* and IDA\* return the same solution length on 100 random 15-puzzles. The pattern-database version expands ≥100× fewer nodes. |
| 4 | Propagation-based solver finishes the "world's hardest" Sudoku in under 1 s. DLX version enumerates all solutions of a multi-solution grid. |
| 5 | Tic-tac-toe: first player draws. Connect Four: agrees with the Pons / Tromp theoretical values on 1000 random positions; bitboard version ≥ 200k nodes/sec in pure Python. |
| 6 | Pig: expectimax converges toward value iteration as depth grows. star1/star2 return exactly the unpruned values. 2048: fast and slow engines agree on 100k random boards in all four directions; ≥300 games with the 2048-tile rate reported with a CI. |
| 7 | Kuhn poker converges to the known Nash equilibrium; exploitability < 0.001. |
| 8 | Value iteration and policy iteration converge to the same policy. |
| 9 | Cliff Walking: SARSA takes the safe path, Q-learning hugs the cliff (Sutton & Barto Fig. 6.4). |
| 10 | Self-play agent beats random > 95% and a pubeval-class heuristic > 50%. |
| 11 | Gomoku MCTS has a measurable win rate against rung 5's alpha-beta agent, with nodes/sec benchmarked. |
| 12 | CartPole reaches 500 steps. Snake median score rises monotonically with training. |
| 13 | Learned policy agrees with rung 5's solver on > 90% of positions, and beats depth-4 alpha-beta without search. |
