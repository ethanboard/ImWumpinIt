from game.wumpus import Game

def test_wumpus_not_in_same_room():
    game = Game()
    assert game.player != game.wumpus
