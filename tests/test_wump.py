import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'game')))
from wumpus import Game


class TestWumpusGame(unittest.TestCase):
    
    def test_adjacent_wumpus_triggers_smell(self):
        game = Game()
        game.player_pos = (2, 2)
        game.wumpus_pos = (2, 3)
        cues = game.get_cues()
        self.assertIn("You smell a Wumpus.", cues)

    def test_arrow_hits_wumpus(self):
        game = Game()
        game.player_pos = (2, 2)
        game.wumpus_pos = (2, 0)
        game.grid[0][2] = 'W'
        game.shoot_arrow('W')
        self.assertTrue(game.game_over)

if __name__ == '__main__':
    unittest.main()
