# game-ai-ladder

> Game AI from 1848 to 2017, one problem at a time, standard library only.

Learn AI by writing game AI, walking the textbook from the first chapter to the last.
Each rung of the ladder is one historical breakthrough, one textbook concept, one program with a verifiable answer.

Three constraints:

- **Pure Python standard library.** No numpy, no pytest, no torch. Every speedup must come from the algorithm or the data structure, never from someone else's C.
- **String output.** Every board renders to a `str`; `print` is the GUI.
- **Fast versions are guaranteed by slow ones.** Each rung starts with an obviously-correct implementation that serves as an oracle. The fast version must agree with it on random inputs.

---

## Contents

1. [The Ladder](#the-ladder)
   - [Historical timeline](#historical-timeline)
   - [Curriculum order](#curriculum-order)
   - [Where the two orders diverge](#where-the-two-orders-diverge)
2. [Repository layout](#repository-layout)
3. [Shared interface](#shared-interface)
4. [Progress](#progress)
5. [References](#references)

Acceptance criteria and engineering rules live in [`docs/engineering.md`](docs/engineering.md).

---

## The Ladder

Four technical threads run through the history of game AI: **search** (1848 → 1950 → 1975 → 2006), **learning** (1959 → 1992 → 2015 → 2017), **imperfect information** (2007 → 2017 → 2019), and **general agents** (2019 onward). They grew separately and converged in AlphaZero.

The curriculum below follows the concept-dependency order of Russell & Norvig and Sutton & Barto, which is deliberately *not* the historical order. Both orders are given; the third subsection explains where and why they disagree.

### Historical timeline

| Year | Milestone | Problem | What it introduced | Rung |
|---|---|---|---|---|
| 1848 | Bezzel poses the puzzle; Gauss finds 72 solutions by hand (1850) | Eight Queens | The prototype combinatorial search problem | 0 |
| 1912 | Torres Quevedo, *El Ajedrecista* | Chess endgame | First automatic chess-playing machine | — |
| 1948–50 | Turing's Turochamp; Shannon's chess paper | Chess | **Minimax**, evaluation functions | 5 |
| 1951–52 | Nimrod; Strachey's checkers; OXO | Nim, Checkers, Tic-tac-toe | First game programs on real computers | 5 |
| 1956–75 | Proposed by McCarthy; analysed by Knuth & Moore | — | **Alpha-beta pruning** | 5 |
| 1957 | Bellman | — | **Dynamic programming, MDPs** | 8 |
| 1959 | Samuel's Checkers | Checkers | **Self-play learning**; the term "machine learning" | 10 |
| 1961 | Michie's MENACE | Tic-tac-toe | Reinforcement learning in matchboxes | 9 |
| 1968 | Hart, Nilsson & Raphael | Pathfinding | **A\*** | 3 |
| 1970 | Conway's Game of Life | Life | Cellular automata, emergence | 1 |
| 1972 | Dijkstra, *Structured Programming* | Eight Queens | **Backtracking** as the textbook example | 0 |
| 1974 | Milton Bradley releases it | Connect Four | Commercial board game | 5 |
| 1979 | Berliner's BKG 9.8; Knuth's Algorithm X | Backgammon; exact cover | First program to beat a world champion in exhibition; **DLX** | 6, 4 |
| 1983 | Ballard | — | **star1 / star2 pruning** | 6 |
| 1985 | Korf | 15-puzzle | **IDA\*** | 3 |
| 1988 | Allen and Allis, independently | Connect Four | **First non-trivial game fully solved.** Allen by brute-force search, Allis by nine strategic rules | 5 |
| 1989 | Watkins | — | **Q-learning** | 9 |
| 1990 | Sosic & Gu | N-Queens | **Min-conflicts local search**, N = 1,000,000 | 0 |
| 1992 | Tesauro's TD-Gammon | Backgammon | **TD(λ) + neural network + self-play** | 10 |
| 1994 / 2007 | Schaeffer's Chinook | Checkers | Beats the champion → solves the game | 5 |
| 1995 | Tromp's Fhourstones | Connect Four | Alpha-beta + transposition table benchmark | 5 |
| 1996–97 | Culberson & Schaeffer | 15-puzzle | **Pattern databases** | 3 |
| 1997 | Deep Blue; Logistello | Chess; Othello | Deep search beats world champions | 5 |
| 2006 | Coulom; Kocsis & Szepesvári | Go | **MCTS / UCT** | 11 |
| 2007–08 | Zinkevich et al. | Poker | **CFR** | 7 |
| 2013–15 | DeepMind's DQN | Atari | **Deep reinforcement learning** | 12 |
| 2014 | Cirulli's 2048 | 2048 | The standard expectimax exercise | 6 |
| 2016–17 | AlphaGo → AlphaZero; Libratus | Go, chess, shogi; poker | **Pure self-play**; CFR beats professionals | 13, 7 |
| 2018–25 | OpenAI Five, Pluribus, MuZero, Cicero, LLM agents | Dota, poker, Atari, Diplomacy, Minecraft | Multi-agent, world models, language agents | future |

### Curriculum order

| Rung | Concept | Problem | History | Requires |
|---|---|---|---|---|
| 0 | Enumeration → backtracking → bitmasks → local search → constraint propagation | Eight Queens | 1848 → 1972 → 1990 | — |
| 1 | State, transitions, sparse vs. dense representation | Game of Life | 1970 | 0 |
| 2 | Uninformed search: BFS / DFS / IDDFS | Maze, 8-puzzle | 1950s | 0 |
| 3 | Heuristic search: A\* / IDA\* / pattern databases | 15-puzzle, Sokoban | 1968 / 1985 / 1997 | 2 |
| 4 | Constraint satisfaction | Sudoku (propagation → DLX), Minesweeper | 1979 | 0 (tier 5) |
| 5 | Adversarial search: minimax / alpha-beta / TT / bitboards | Tic-tac-toe → **Connect Four** → Othello | 1950 / 1975 / 1988 | 2 |
| 6 | Stochastic games: expectiminimax / star pruning | Pig → mini-backgammon → 2048 | 1979 / 1983 / 2014 | 5 |
| 7 | Imperfect information: CFR | Kuhn poker → Leduc poker | 2007 / 2017 | 6 |
| 8 | MDPs and dynamic programming | Gridworld, Blackjack | 1957 | 6 |
| 9 | Tabular RL: MC / TD / Q-learning / SARSA | Blackjack, Cliff Walking, small-grid Snake | 1961 / 1989 | 8 |
| 10 | Function approximation + TD(λ) + self-play | TD-Gammon replica | 1959 / 1992 | 9, 6 |
| 11 | MCTS / UCT | Gomoku, Hex, 9×9 Go | 2006 | 5, 9 |
| 12 | Deep RL (hand-written backprop) | CartPole → Snake | 2013–17 | 9, 10 |
| 13 | Self-play + MCTS + neural network | AlphaZero-lite on Connect Four | 2017 | 11, 12 |

Rungs 12 and 13 require hand-written matrix operations and backpropagation under the stdlib constraint. Whether to relax the constraint there is decided when we get there.

### Where the two orders diverge

| Observation | Reason |
|---|---|
| Eight Queens (1848) predates every computer, yet it is rung 0 | No opponent, no chance, no learning: the purest search problem there is |
| Q-learning (1989) predates Deep Blue (1997), yet the curriculum puts it later | RL needs the language of MDPs; MDPs need the "expectation over chance" idea from expectimax |
| MCTS (2006) is late historically, yet sits mid-curriculum | It depends only on adversarial search plus bandits, and it is the road to AlphaZero |
| Game of Life is not AI | But it is the cleanest exercise in sparse vs. dense state, and a prelude to the state spaces of rung 2 |
| CFR is skipped by most intro courses | Yet it is the root of poker, Stratego and Diplomacy, and is nearly independent of RL |
| 2048 is a 2014 casual game | Simpler than backgammon (no opponent), deeper than Pig (real engineering): exactly the expectimax slot |

---

## Repository layout

```
game-ai-ladder/
├── README.md
├── docs/
│   ├── engineering.md        acceptance criteria, engineering rules
│   ├── history.md            long-form timeline with papers
│   └── curriculum.md         concept map and reading list per rung
│
├── gameai/                   shared package, zero dependencies
│   ├── core.py               Game / Agent / Renderer protocols
│   ├── search/               uninformed, heuristic, minimax, expectimax, cfr, mcts
│   ├── rl/                   dp, tabular, nn (hand-written)
│   ├── eval/                 arena (round-robin), stats (bootstrap CI)
│   ├── render.py             string rendering: grids, ANSI clear-screen
│   └── testing.py            random-input generators (stands in for hypothesis)
│
├── stages/
│   ├── s00_nqueens/
│   │   ├── README.md         why this is rung 0, the five tiers, milestones
│   │   ├── nqueens.py        all five tiers, function names carry the tier
│   │   ├── bench.py
│   │   └── test_nqueens.py
│   ├── s01_life/
│   ├── s02_blind_search/
│   ├── s03_heuristic_search/
│   ├── s04_csp/
│   ├── s05_adversarial/
│   │   ├── tictactoe/
│   │   ├── connect4/         ← the core investment
│   │   └── othello/
│   ├── s06_stochastic/
│   │   ├── pig/
│   │   ├── nannon/
│   │   └── game2048/
│   ├── s07_imperfect_info/
│   ├── s08_mdp/
│   ├── s09_tabular_rl/
│   ├── s10_td_gammon/
│   ├── s11_mcts/
│   ├── s12_deep_rl/
│   └── s13_alphazero/
│
└── benchmarks/               nodes/sec per rung, JSON, compared across commits
```

Every rung (or sub-game) has the same internal shape:

```
<game>/
├── README.md        history, concepts, milestones, acceptance criteria
├── game.py          implements the Game protocol
├── agents.py        this rung's agents
├── play.py          human-vs-AI or spectator entry point, string output
├── bench.py
└── test_<game>.py   unittest: golden cases + fast/slow agreement
```

---

## Shared interface

```python
# gameai/core.py
from typing import Protocol, TypeVar, Sequence

S = TypeVar("S")   # state
M = TypeVar("M")   # move

class Game(Protocol[S, M]):
    def initial(self) -> S: ...
    def player(self, s: S) -> int: ...               # -1 at chance nodes
    def legal_moves(self, s: S) -> Sequence[M]: ...
    def apply(self, s: S, m: M) -> S: ...             # returns a new state, never mutates
    def is_terminal(self, s: S) -> bool: ...
    def utility(self, s: S, player: int) -> float: ...
    def chance_outcomes(self, s: S) -> Sequence[tuple[S, float]]: ...

class Agent(Protocol[S, M]):
    def select(self, s: S) -> M: ...
    def reset(self) -> None: ...

class Renderer(Protocol[S]):
    def draw(self, s: S) -> str: ...                  # returns a string; the caller prints
```

- `apply` returns a new state. Bitboards satisfy this for free; list-based states must copy.
- Engine, AI and rendering are strictly separated. `Renderer.draw` reads state and returns a string, nothing else.
- All randomness goes through an injectable `random.Random(seed)`.

---

## Progress

| Rung | Status |
|---|---|
| 0 Eight Queens | in progress — tier 1 |
| 1–13 | ☐ |

---

## References

- Russell & Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed. — Ch. 3–6, 17, 22
- Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed.
- Dijkstra, "Notes on Structured Programming" (1972) — Eight Queens by backtracking
- Sosic & Gu, "A polynomial time algorithm for the N-Queens problem" (1990)
- Allis, *A Knowledge-based Approach of Connect-Four* (1988)
- Tesauro, "Temporal Difference Learning and TD-Gammon" (1995)
- Browne et al., "A Survey of Monte Carlo Tree Search Methods" (2012)
- Zinkevich et al., "Regret Minimization in Games with Incomplete Information" (2008)
- Silver et al., "Mastering the game of Go without human knowledge" (2017)
- OEIS A000170 — number of N-Queens solutions
