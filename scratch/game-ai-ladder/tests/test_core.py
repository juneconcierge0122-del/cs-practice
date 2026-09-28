# tests/test_core.py


import unittest
from genai.core import Problem, Game, StochasticGame, Agent, Renderer

class CountTo3:
    """Problem: start at 0, +1, or +2 per step, goal at 3."""
    def initial(self):
        return 0
    def actions(self, s):
        return (1, 2)
    def results(self, s, a):
        return s+a
    def is_goal(self, s):
        return s ==3
    def step_cost(self, s, a, s2):
        return 1.0

class Nim3:
    """Game: 3 sticks, taker of the last stick wins."""
    def initial(self): return (3, 0) #(sticks, player_to_move)
    def player(self, s): return s[1]
    def legal_moves(self, s): return tuple(k for k in (1, 2) if k<=s[0])
    def apply(self, s, a): return (s[0] - a, 1-s[1])
    def is_terminal(self, s): return s[0] == 0
    def utility(self, s, player):
        return 1.0 if s[1] != player else -1.0 #whoever is NOT to move took the last stick

class TestProtocols(unitest.TestCase):
    def test_problem_conformance(self):
        self.assertIsInstance(CountTo3(), Problem)
        self.assertNotIsInstance(CountTo3(), Game)

    def test_game_conformance(self):
        self.assertIsInstance(Nim3(), Game)
        self.assertNotIsInstance(Nim3(), StochasticGame)
        self.assertNotIsInstance(Nim3(), Problem)

    def test_apply_does_not_mutate(self):
        g, s = Nim3(), Nim3().initial()
        g.apply(s, 1)
        self.assertEqual(s, (3, 0))

    def test_nim3_first_player_wins_by_taking_two(self):
        g = Nim3()
        s = g.apply(g.initial(), 2)
        s = g.apply(s, 1)
        self.assertTrue(g.is_terminal(s))
        self.assertEqual(g.utility(s, 0), 1.0)

if __name__ == "__main__":
    unittest.main()
